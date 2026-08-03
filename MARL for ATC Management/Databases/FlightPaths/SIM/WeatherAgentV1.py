# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 18:50:13 2025

@author: Leslie, Santiago, & Sandra
    ECE 508
"""

"""
Note: I added Tornado Warning to diverte all traffic, we can update this as needed
Note: Can add more WX cells or keep it generic
    How would an Multi-Agent affect the rest of our code
    - Sandra 
"""
import random
class WeatherAgent:
    """Controls weather conditions that impact runway operation"""
    
    def __init__(self):
        self.runway_weather = {1: "clear", 2: "clear", 3: "clear", 4: "clear"}  # Initial WX is clear
        self.tornado_active = False 

    def update_weather(self):
        """Randomly changes weather conditions per runway, including tornadoes."""
        self.tornado_active = random.random() < 0.05  # 5% chance of a tornado

        if self.tornado_active:
            print("🌪️ **TORNADO WARNING!** !! All runways closed !!! Diverting all traffic !!")
            for rwy in self.runway_weather:
                self.runway_weather[rwy] = "tornado"
        else:
            for rwy in self.runway_weather:
                weather_chance = random.random()
                if weather_chance < 0.3:  # 30% chance of bad weather
                    self.runway_weather[rwy] = random.choice(["fog", "storm", "high winds"])
                    print(f"🌩️ WEATHER ALERT: Runway {rwy} affected by {self.runway_weather[rwy].upper()}!")
                else:
                    self.runway_weather[rwy] = "clear"

    def is_runway_closed(self, runway):
        """Checks if a runway is affected by bad weather or a tornado."""
        return self.runway_weather[runway] in ["fog", "storm", "high winds", "tornado"]