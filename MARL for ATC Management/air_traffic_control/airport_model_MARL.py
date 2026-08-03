from mesa import Model
from mesa.space import ContinuousSpace
from datetime import datetime, date, time, timezone, timedelta
import time
import threading
import random
from random import uniform
from typing import Tuple
from air_traffic_control.agents.aircraft_MARL import Aircraft, Waypoint
from air_traffic_control.agents.weather import Weather
from air_traffic_control.agents.control_tower import ControlTower
from air_traffic_control.data.data_loader import get_flights, get_aircraft_track_path
from air_traffic_control.monitor.anomaly_monitor_MARL import AnomalyMonitor
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
        self.anomaly_log = []
        self.epsilon_values = []
        self.rewards_over_time = []
        self.anomaly_monitor_MARL = AnomalyMonitor()
        threading.Thread(target=self._load_flights, args=(start, end), daemon=True).start()

    def _create_airport_ctrl_space(self):
        space = ContinuousSpace(x_max=-116, y_max=36, x_min=-122, y_min=32, torus=True)
        return space

    def _inject_dummy_arrivals(self):
        print("🛠 Injecting 3 dummy aircrafts into simulation...")

        for i in range(3):
            track_start = self.start + timedelta(seconds=i * 60)
            track_end = track_start + timedelta(seconds=120)

            waypoints = [
                Waypoint(
                    time=track_start + timedelta(seconds=j * 10),
                    latitude=33.94 + uniform(-0.01, 0.01),
                    longitude=-118.41 + uniform(-0.01, 0.01),
                    altitude=5000 - j * 100,
                    true_track=90 + uniform(-5, 5),
                    on_ground=False
                ) for j in range(12)
            ]

            ac = Aircraft(
                model=self,
                uid=f"DUMMY{i}",
                callsign=f"DUMMY{i}",
                departure_airport="TEST",
                arrival_airport=self.airport_id,
                departure_time=track_start,
                arrival_time=track_end,
                track_start=track_start,
                track_end=track_end,
                waypoints=waypoints
            )

            self.schedule.add(ac)

    def _load_flights(self, start: datetime, end: datetime):
        try:
            print(f"Loading flights for airport {self.airport_id} from {start} to {end}")
            arrivals = get_flights(f"{self.airport_id}", start, end, type="arrival")
            if not arrivals:
                print("⚠️ No arrivals found — injecting simulated aircraft.")
                self._inject_dummy_arrivals()
            else:
                print(f"✅ Found {len(arrivals)} arrivals")

            for flight in arrivals:
                uid = flight.icao24
                arrival_airport = flight.estArrivalAirport
                departure_airport = flight.estDepartureAirport
                arrival_time = flight.lastSeen
                departure_time = flight.firstSeen

                print(f"Querying track for flight {uid}")
                track = get_aircraft_track_path(uid, timestamp=departure_time)

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

    def compute_shared_reward(self):
        aircraft_agents = [a for a in self.schedule.agents if isinstance(a, Aircraft)]
        reward_total = 0
        penalty = 0

        for ac in aircraft_agents:
            reward_total += ac.compute_reward()

        for i in range(len(aircraft_agents)):
            for j in range(i + 1, len(aircraft_agents)):
                a1, a2 = aircraft_agents[i], aircraft_agents[j]
                if a1.pos[0] is not None and a2.pos[0] is not None:
                    dx = a1.pos[0] - a2.pos[0]
                    dy = a1.pos[1] - a2.pos[1]
                    dist = (dx**2 + dy**2) ** 0.5
                    if dist < 0.01:
                        penalty += 5

        return (reward_total - penalty) / len(aircraft_agents) if aircraft_agents else 0

    def step(self):
        print(f"✈️ Airport step called at {self.current_time}")
        self.current_time += timedelta(seconds=1)

        aircraft = [a for a in self.schedule.agents if isinstance(a, Aircraft)]
        shared_reward = self.compute_shared_reward()

        for agent in aircraft:
            agent.step(shared_reward=shared_reward)

        self.rewards_over_time.append(shared_reward)

        for i in range(len(aircraft)):
            for j in range(i + 1, len(aircraft)):
                a1, a2 = aircraft[i], aircraft[j]
                if a1.pos[0] is not None and a2.pos[0] is not None:
                    dx = a1.pos[0] - a2.pos[0]
                    dy = a1.pos[1] - a2.pos[1]
                    dist = (dx**2 + dy**2) ** 0.5
                    if dist < 0.01:
                        anomaly = {
                            "type": "Collision Risk",
                            "time": self.current_time,
                            "aircraft_1": a1.callsign,
                            "aircraft_2": a2.callsign,
                            "distance": round(dist, 5), 
                            "position": [
                                round((a1.pos[0] + a2.pos[0]) / 2, 6),
                                round((a1.pos[1] + a2.pos[1]) / 2, 6)
                            ]
                        }
                        # self.anomaly_log.append(anomaly)  # Optional legacy backup
                        self.anomaly_monitor_MARL.record(anomaly)  # ✅ Proper logging
                        print(f"💥 Collision Risk between {a1.callsign} and {a2.callsign} – Distance: {dist:.5f}")

    def run_model(self):
        while not self.flights_loaded:
            time.sleep(1)

        while self.running:
            if self.current_time >= self.end:
                print("Simulation has reached the end time.")
                self.running = False
                return

            self.step()
            time.sleep(1)

if __name__ == "__main__":
    print("✅ Airport model loaded successfully.")
    model = Airport(
        date=datetime(2025, 4, 1).date(),
        time=datetime(2025, 4, 1, 18, 15).time(),
        duration=10,
        airport_id="KLAX",
        gps=(33.942791, -118.410042)
    )
    model.run_model()
    model.anomaly_monitor_MARL.save_to_file("anomaly_log.json")
    model.anomaly_monitor_MARL.plot_summary()
    model.anomaly_monitor_MARL.plot_route_deviation_heatmap(airport_coords={"KLAX":(33.9428, -118.4100)})

    for agent in model.schedule.agents:
        if isinstance(agent, Aircraft):
            monitor = model.anomaly_monitor_MARL

            if agent.epsilon_values and agent.rewards_over_time:
                monitor.plot_epsilon_vs_reward(agent.epsilon_values, agent.rewards_over_time, agent.callsign.strip())
            else:
                print(f"⚠️ Skipping ε vs reward for {agent.callsign} — missing data.")

            if agent.q_deltas:
                monitor.plot_q_deltas(agent.q_deltas, agent.callsign.strip())
            else:
                print(f"⚠️ Skipping Q-deltas for {agent.callsign} — missing data.")

            if agent.q_rewards and agent.random_rewards:
                monitor.compare_q_vs_random(agent.q_rewards, agent.random_rewards, agent.callsign.strip())
            else:
                print(f"⚠️ Skipping Q vs Random for {agent.callsign} — missing reward history.")

            q_matrix = agent.get_q_matrix()
            if q_matrix is not None and q_matrix.shape != (1, 1):
                monitor.plot_q_evolution(q_matrix, agent.callsign.strip())
            else:
                print(f"⚠️ Skipping Q evolution for {agent.callsign} — insufficient Q-table shape.")
        all_epsilons = []
        all_rewards = []
        all_q_deltas = []
        all_q_rewards = []
        all_random_rewards = []
        all_q_matrices = []
        q_matrix = agent.get_q_matrix()
        if q_matrix is not None and q_matrix.shape != (1, 1):
            monitor.plot_q_evolution(q_matrix, agent.callsign.strip())
            all_q_matrices.append(q_matrix)
        else:
            print(f"⚠️ Skipping Q evolution for {agent.callsign} — insufficient Q-table shape.")
        
        monitor.plot_all_metrics(all_epsilons,
                                  all_rewards, 
                                  all_q_deltas, 
                                  all_q_rewards,
                                  all_random_rewards,
                                  q_matrices=all_q_matrices)
