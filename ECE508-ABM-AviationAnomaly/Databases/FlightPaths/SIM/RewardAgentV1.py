# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 18:50:13 2025

@author: Leslie, Santiago, & Sandra
    ECE 508
"""
import logging

class RewardAgent:
    """Manages and tracks rewards and penalties for aircraft and ATC actions."""
    # Need to integrate Aircraft 
    
    def __init__(self):
        self.total_reward = 0
        self.aircraft_rewards = {}  # Track rewards per aircraft
        self.reward_breakdown = {"landing": 0, "reroute": 0, "waiting_penalty": 0,
                                 "collision_avoidance": 0, "weather_reroute": 0, 
                                 "emergency_landing": 0, "efficient_runway_utilization": 0}
        logging.basicConfig(filename="./penalty_log.log", filemode='w', level=logging.INFO, format="%(asctime)s - %(message)s")

    def assign_reward(self, aircraft_id, action):
        """Assigns rewards or penalties based on the aircraft's action commanded from the ATC
        Note: Need to assign new rewards once other agents are integrated           """
        reward_values = {
            "landing": 10,
            "emergency_landing": 20,
            "reroute": -15,
            "waiting_penalty": -5,
            "collision_avoidance": -20,
            "weather_reroute": -8,
            "inefficient_landing": -6
        }
        reward = reward_values.get(action, 0)
        self.total_reward += reward
        self.aircraft_rewards[aircraft_id] = self.aircraft_rewards.get(aircraft_id, 0) + reward
        if action in self.reward_breakdown:
            self.reward_breakdown[action] += reward
        else:
            self.reward_breakdown[action] = reward
        logging.info(f"Aircraft {aircraft_id} received penalty for {action}: {reward} points")
        return reward
    
    def display_summary(self):
        """Displays simulation reward summary"""
        print("\n🔹🔹🔹🔹🔹🔹 SIMULATION REWARD SUMMARY 🔹🔹🔹🔹🔹🔹")
        for key, value in self.reward_breakdown.items():
            print(f"✅ {key.replace('_', ' ').title()}: {value}")
        print(f"🏆 Total Reward: {self.total_reward}")
        print("🔹🔹🔹🔹🔹🔹 SIMULATION COMPLETED 🔹🔹🔹🔹🔹🔹")
        logging.info("Simulation Completed - Reward Summary Logged")
