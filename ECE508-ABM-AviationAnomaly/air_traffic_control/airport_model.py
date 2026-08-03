from mesa import Model
from mesa.space import ContinuousSpace
from datetime import datetime, date, time, timezone, timedelta
import time
import threading
import random
from typing import Tuple
from air_traffic_control.agents.aircraft import Aircraft, Waypoint
from air_traffic_control.agents.weather import Weather
from air_traffic_control.agents.control_tower import ControlTower
from air_traffic_control.data.data_loader import get_flights, get_aircraft_track_path
from air_traffic_control.monitor.anomaly_monitor import AnomalyMonitor
import matplotlib.pyplot as plt

class Airport(Model):
    def __init__(
        self,
        date: date,
        time: time,
        duration: int,
        airport_id: str,
        gps: Tuple[float, float],
    ):
        super().__init__()
        self.running = False
        from mesa.time import RandomActivation
        self.schedule = RandomActivation(self)
        self.airport_id = airport_id
        self.latitude, self.longitude = gps
        self.control_radius_km = 100
        self.space = self._create_airport_ctrl_space()
        self.num_runways = 2
        self.num_gates = 10
        
        start = datetime.combine(date, time)
        if start.tzinfo is None:
            start = start.replace(tzinfo=timezone.utc)
        end = start + timedelta(minutes=duration)
        
        self.start = start
        self.end = end
        self.current_time = start
        
        self.atc_agent = ControlTower(model=self, control_radius_km=self.control_radius_km)
        self.weather_agent = Weather(model=self)
        self.flights_loaded = False 
        self.anomaly_log = [] #added this to log aircrafts
        self.anoamlies = []
        self.epsilon_values = []
        self.rewards_over_time = []
        self.anomaly_monitor = AnomalyMonitor()
        threading.Thread(target=self._load_flights, args=(start, end), daemon=True).start()
        
    def _create_airport_ctrl_space(self):
        space = ContinuousSpace(x_max=-116, y_max=36, x_min=-122, y_min=32, torus=True)
        return space
    
    def _inject_dummy_arrivals(self):
        now = self.current_time
        for i in range(3):  # Add 3 dummy aircraft
            waypoints = [
                Waypoint(
                    time=now + timedelta(seconds=j),
                    latitude=33.94 + 0.01 * j,
                    longitude=-118.4 + 0.005 * j,
                    altitude=10000 - j * 100,
                    true_track=90,
                    on_ground=False
                ) for j in range(10)
            ]

            ac = Aircraft(
                model=self,
                uid=f"SIM{i}",
                callsign=f"TEST{i}",
                departure_airport="KLAX",
                arrival_airport=self.airport_id,
                departure_time=now,
                arrival_time=now + timedelta(minutes=2),
                track_start=now,
                track_end=now + timedelta(minutes=2),
                waypoints=waypoints
            )
            self.schedule.add(ac)
            print(f"✅ Simulated aircraft injected: {ac.callsign}")

    
    def _load_flights(self, start: datetime, end: datetime):
        try:
            print(f"Loading flights for airport {self.airport_id} from {start} to {end}")
            
            # Query arrivals for the airport in the time window
            arrivals = get_flights(f"{self.airport_id}", start, end, type="arrival")
            if not arrivals:
                print("⚠️ No arrivals found — injecting simulated aircraft.")
                self._inject_dummy_arrivals()
            else:
                print(f"✅ Found {len(arrivals)} arrivals")
            # if arrivals and len(arrivals) > 0:
            #     print(f"✅ Found {len(arrivals)} arrivals.")
            # else:
            #     print("⚠️ No arrivals found.")
            for flight in arrivals:
                uid = flight.icao24
                arrival_airport = flight.estArrivalAirport
                departure_airport = flight.estDepartureAirport
                arrival_time = flight.lastSeen
                departure_time = flight.firstSeen

                print(f"Querying track for flight {uid}")
                track = get_aircraft_track_path(uid, timestamp=departure_time)

                # Build waypoint list from track
                waypoints = [
                    Waypoint(
                        time=w[0],
                        latitude=w[1],
                        longitude=w[2],
                        altitude=w[3],
                        true_track=w[4],
                        on_ground=w[5]
                    )
                    for w in track.path
                ]

                # Create aircraft agent
                ac = Aircraft(
                    model=self,
                    uid=uid,
                    callsign=flight.callsign,
                    departure_airport=departure_airport,
                    arrival_airport=arrival_airport,
                    departure_time=departure_time,
                    arrival_time=arrival_time,
                    track_start=track.startTime,
                    track_end=track.endTime,
                    waypoints=waypoints
                )
                self.schedule.add(ac)

        except Exception as e:
            print(f"Error loading flights: {e}")

        finally:
            self.flights_loaded = True
            self.running = True
            print("Flights loaded successfully. Starting simulation.")
    def step(self):
        print(f"✈️ Airport step called at {self.current_time}")
        
        # Advance time
        self.current_time += timedelta(seconds=1)

        # Trigger all agent steps (Aircraft, Weather, ATC, etc.)
        self.agents.do("step")

        # Log aircraft statuses, reward trends, and anomaly triggers
        aircraft = [a for a in self.schedule.agents if isinstance(a, Aircraft)]

        for agent in aircraft:
            # Track and decay epsilon
            agent.epsilon = max(agent.epsilon * 0.995, 0.01)
            agent.epsilon_values.append(agent.epsilon)

            # Store current reward
            reward = agent.compute_reward()
            agent.rewards_over_time.append(reward)

            # Random vs Q-learning reward logging
            if random.random() < agent.epsilon:
                agent.random_rewards.append(reward)
            else:
                agent.q_rewards.append(reward)

            # Q-delta tracking
            if hasattr(agent, "last_q_value"):
                delta = abs(agent.Q.get((agent.get_state(), agent.current_action), 0) - agent.last_q_value)
                agent.q_deltas.append(delta)

            # Q-matrix snapshot for visualization
            state = agent.get_state()
            agent.q_matrix[state] = {
                a: agent.Q.get((state, a), 0) for a in agent.available_actions
            }

        # Log collision risks
        for i in range(len(aircraft)):
            for j in range(i + 1, len(aircraft)):
                a1, a2 = aircraft[i], aircraft[j]
                if a1.pos[0] is not None and a2.pos[0] is not None:
                    dx = a1.pos[0] - a2.pos[0]
                    dy = a1.pos[1] - a2.pos[1]
                    dist = (dx**2 + dy**2) ** 0.5
                    if dist < 0.01:  # Adjust as needed
                        anomaly = {
                            "type": "Collision Risk",
                            "time": self.current_time,
                            "aircraft_1": a1.callsign,
                            "aircraft_2": a2.callsign,
                            "distance": round(dist, 5)
                        }
                        self.anomaly_log.append(anomaly)
                        print(f"💥 Collision Risk between {a1.callsign} and {a2.callsign} – Distance: {dist:.5f}")
  
    def run_model(self):
        while not self.flights_loaded:
            time.sleep(1)
           
        while self.running:
            if self.current_time >= self.end:
                print("Simulation has reached the end time.")
                self.running = False  # Stop the simulation
                return
            
            self.step()
            time.sleep(1)  # Simulate a delay for each step

#Added this for initializing the enviornment        
if __name__ == "__main__":
    print("✅ Airport model loaded successfully.")
    model = Airport(
        date=datetime(2025, 4, 1).date(),
        time=datetime(2025, 4, 1, 18, 15).time(),
        duration=1,
        airport_id="KLAX",
        gps=(33.942791, -118.410042)
    )
    model.run_model()
    model.anomaly_monitor.save_to_file("anomaly_log.json")
    model.anomaly_monitor.plot_summary()
    model.anomaly_monitor.plot_route_deviation_heatmap()
    #model.anomaly_monitor.plot_deviation_heatmap()
    for agent in model.schedule.agents:
        if isinstance(agent, Aircraft):
            monitor = model.anomaly_monitor
            monitor.plot_epsilon_vs_reward(agent.epsilon_values, agent.rewards_over_time)
            monitor.plot_q_deltas(agent.q_deltas)
            monitor.compare_q_vs_random(agent.q_rewards, agent.random_rewards)
            monitor.plot_q_evolution(agent.q_matrix)
    model.anomaly_monitor.show_all_figures()

    # for agent in model.schedule.agents:
    #     if hasattr(agent, 'epsilon_values') and hasattr(agent, 'rewards_over_time'):
    #         model.anomaly_monitor.plot_epsilon_vs_reward(agent.epsilon_values, agent.rewards_over_time)
    #     if hasattr(agent, 'q_deltas'):
    #         model.anomaly_monitor.plot_q_deltas(agent.q_deltas)
    #     if hasattr(agent, 'q_rewards') and hasattr(agent, 'random_rewards'):
    #         model.anomaly_monitor.compare_q_vs_random(agent.q_rewards, agent.random_rewards)
    #     if hasattr(agent, 'q_matrix'):
    #         model.anomaly_monitor.plot_q_evolution(agent.q_matrix)



"""
DO NOT DELETE THE BELOW CODE UNTIL ALL GRAPHS ARE VERIFIED AND VALIDATED
"""
    # model.anomaly_monitor.save_to_file("anomaly_log.json")
    # model.anomaly_monitor.plot_summary()

    # aircraft = next(
    #     (a for a in model.schedule.agents if a.__class__.__name__ == "Aircraft"),
    #     None)

    # if aircraft is not None:
    #     plt.plot(aircraft.epsilon_values, aircraft.rewards_over_time)
    #     plt.title("Epsilon vs. Reward")
    #     plt.grid(True)
    #     plt.tight_layout()
    #     plt.show()

    #     plt.plot(range(len(aircraft.q_deltas)), aircraft.q_deltas)
    #     plt.title("Q-value Change Over Time")
    #     plt.grid(True)
    #     plt.tight_layout()
    #     plt.show()
    # else:
    #     print("⚠️ No aircraft agents found in schedule — skipping learning plots.")
