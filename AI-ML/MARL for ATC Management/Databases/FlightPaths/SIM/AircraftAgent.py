# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 18:50:13 2025

@author: Leslie, Santiago, & Sandra
    ECE 508
"""
import random

'''
Need Leslie Script
'''
class AircraftAgent:
    """aircraft in the airspace"""
    def __init__(self, id):
        self.id = id
        self.altitude = random.randint(3000, 40000)  # Feet
        self.speed = random.randint(200, 600)  # Knots
        self.fuel = random.uniform(20, 100)  # Percentage
        self.status = random.choice(["ready_for_takeoff", "approaching", "normal", "emergency"])  # Flight status
        self.runway = None  # Assigned runway
