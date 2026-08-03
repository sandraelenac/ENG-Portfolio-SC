# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 18:50:13 2025

@author: Leslie, Santiago, & Sandra
    ECE 508
"""

"""
Note: will update once Aircraft Agent is finalized 
     Should we also include an Agent for Current Ground Traffic ?
     should probbaly add delay of ATC 
     Any visulations? 
    -Sandra
"""
import logging 
import random

class ATCAgent:
    """Manages ATC operations, including collision avoidance """
    
    def __init__(self, weather_agent, reward_agent):
        self.runways = {1: "free", 2: "free", 3: "free", 4: "free"}  # Four available runways at LAX
        self.weather_agent = weather_agent  # Connect to WeatherAgent
        self.reward_agent = reward_agent  # Delegating rewards to RewardAgent
        self.waiting_queue = []  # Standard queue for non-emergency aircraft
        self.emergency_queue = []  # Priority queue for emergency aircraft
        self.holding_patterns = []  # Aircraft in holding due to collision risk
        self.aircraft_positions = {rwy: None for rwy in self.runways}  # Track aircraft on runways
        self.runway_timers = {}  # Store active timers for runway clearance
        logging.basicConfig(filename="ATC_simulation.log", level=logging.INFO, format="%(asctime)s - %(message)s")
    
    def check_aircraft_proximity(self, aircraft):
        """Prevents aircraft from landing if another is too close in altitude."""
        for other in self.aircraft_positions.values():
            if other is not None and hasattr(other, "altitude"):
                if abs(aircraft.altitude - other.altitude) < 500:  # If within 500 ft, hold pattern
                    print(f"⚠️ Collision Risk! Aircraft {aircraft.id} must enter holding pattern! Potential collision with Aircraft {other.id}.")
                    self.holding_patterns.append(aircraft)  # Store aircraft in holding
                    self.reward_agent.assign_reward(aircraft.id, "collision_avoidance")  # Reward for avoiding collision
                    return True
        return False
    
    def assign_runway(self, aircraft, priority=False):
        """Assigns a runway while checking weather and collision risks, with ATC delays."""
        if self.weather_agent.tornado_active:
            self.reward_agent.assign_reward(aircraft.id, "weather_reroute")
            self.reroute_aircraft(aircraft)
            return

        available_runways = [rwy for rwy, status in self.runways.items() if status == "free" and not self.weather_agent.is_runway_closed(rwy)]
        
        if available_runways:
            assigned_runway = available_runways.pop(0)  # Assign the first available runway
            self.runways[assigned_runway] = "occupied"
            self.aircraft_positions[assigned_runway] = aircraft  # Store aircraft
            aircraft.runway = assigned_runway  # Store assigned runway
            
            action = "emergency_landing" if priority else "landing"
            self.reward_agent.assign_reward(aircraft.id, action)
            self.reward_agent.assign_reward(aircraft.id, "efficient_runway_utilization")  # Reward for efficient runway use
            
            logging.info(f"Aircraft {aircraft.id} assigned to Runway {assigned_runway}")
            print(f"✅ Aircraft {aircraft.id} assigned to Runway {assigned_runway}")
            
            self.display_runway_assignments()
            return

        self.waiting_queue.append(aircraft) if not priority else self.emergency_queue.append(aircraft)
    
    def display_runway_assignments(self):
        """Displays the current aircraft assignments for each runway."""
        print("\n📌 Current Runway Assignments:")
        for rwy, aircraft in self.aircraft_positions.items():
            if aircraft is not None:
                print(f"Runway {rwy}: Aircraft {aircraft.id}")
            else:
                print(f"Runway {rwy}: Free")
                
    def reroute_aircraft(self, aircraft):
        """Simulates rerouting due to congestion or weather issues."""
        alternate_airports = ["Nearby Airport A", "Nearby Airport B"]
        chosen_airport = min(alternate_airports, key=lambda x: random.randint(50, 200))  # Simulate distance-based selection
        logging.info(f"Aircraft {aircraft.id} rerouted to {chosen_airport}")
        print(f"🚨 Aircraft {aircraft.id} rerouted to {chosen_airport}!")
        self.reward_agent.assign_reward(aircraft.id, "reroute")
    
    
    def process_waiting_queue(self):
        """Assigns waiting aircraft and those in holding patterns to free runways, minimizing wait times."""
        available_runways = [rwy for rwy, status in self.runways.items() if status == "free"]
        while available_runways and (self.emergency_queue or self.waiting_queue or self.holding_patterns):
            if self.emergency_queue:
                next_aircraft = self.emergency_queue.pop(0)  # Prioritize emergency aircraft
            elif self.holding_patterns:
                next_aircraft = self.holding_patterns.pop(0)  # Prioritize holding aircraft
            else:
                next_aircraft = self.waiting_queue.pop(0)  # Otherwise, take the next in line
            assigned_runway = available_runways.pop(0)
            self.assign_runway(next_aircraft, priority=False)