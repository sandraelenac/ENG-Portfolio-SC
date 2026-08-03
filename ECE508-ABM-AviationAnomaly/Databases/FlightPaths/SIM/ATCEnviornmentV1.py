# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 18:50:13 2025

@author: Leslie, Santiago, & Sandra
    ECE 508
"""

import random
import threading
import time
import logging
import matplotlib.pyplot as plt
from WeatherAgentV1 import WeatherAgent
from AircraftAgent import AircraftAgent
from RewardAgentV1 import RewardAgent
from ATCAgentV1 import ATCAgent

class ATCEnvironment:
    """Simulates ATC interactions with Aircraft, Weather, & Reward AGENTS"""
    
    def __init__(self):
        self.weather_agent = WeatherAgent()
        self.reward_agent = RewardAgent() 
        self.aircraft_agents = [AircraftAgent(i) for i in range(num_aircrafts_in_sim)]
        self.atc_agent = ATCAgent(self.weather_agent, self.reward_agent)

    def step(self):
        """Runs one iteration of the sim & track rewards"""
        print("\n🌦️ Checking weather conditions...")
        self.weather_agent.update_weather()
        
        threads = []  # Multi-threaded processing for faster simulation
        for aircraft in self.aircraft_agents:
            t = threading.Thread(target=self.process_aircraft, args=(aircraft,))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()  # Ensure all aircraft actions complete before proceeding
        
        self.atc_agent.process_waiting_queue()
    
    def process_aircraft(self, aircraft):
        """individual aircraft actions"""
        if aircraft.status == "emergency":
            self.reward_agent.assign_reward(aircraft.id, "emergency_landing")
            self.atc_agent.assign_runway(aircraft, priority=True)
        elif aircraft.status == "approaching":
            self.reward_agent.assign_reward(aircraft.id, "landing")
            self.atc_agent.assign_runway(aircraft, priority=False)
        elif aircraft.status == "ready_for_takeoff":
            self.reward_agent.assign_reward(aircraft.id, "landing")
            self.atc_agent.assign_runway(aircraft, priority=False)
    
    def run_simulation(self, sim=5):
        """Runs the simulation"""
        for step in range(sim):
            print(f"\n🔄 RUNNING SIMULATION {step + 1} 🔄")
            self.step()
            
        self.reward_agent.display_summary()

# Run Simulation
"""
Note: the num of aircrafts incoming & outbounding can be another Agent
"""
num_aircrafts_in_sim  = 20 ## of aircafts ATC has incoming
num_times_running_sim = 6 #num times to running the simulation 
env = ATCEnvironment()
env.run_simulation(num_times_running_sim)
