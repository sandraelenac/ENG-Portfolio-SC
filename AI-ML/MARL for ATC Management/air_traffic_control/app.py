import threading
from datetime import datetime, date, time, timedelta
import solara
import time

from mesa.visualization import (
    SolaraViz,
    make_plot_component,
    make_space_component
)

from air_traffic_control.airport_model import Airport
from agents.aircraft import Aircraft

def aircraft_portrayal(agent):
    if agent is None:
        return

    portrayal = {
        "Shape": "circle",
        "r": 0.5,
        "Layer": 0,
        "Color": "#1f77b4",
        "Filled": "true",
        "x": agent.pos[0],
        "y": agent.pos[1],
        "text": f"{agent.callsign} ({agent.status})",
        "text_color": "black",
        "text_position": "bottom"
    }

    # Add trail lines for track history
    if hasattr(agent, "waypoints") and agent.curr_waypoint_idx > 1:
        trail = [(wp.longitude, wp.latitude) for wp in agent.waypoints[:agent.curr_waypoint_idx]]
        portrayal["trail"] = trail  # Supported by Solara's make_space_component
        portrayal["trail_color"] = "gray"

    return portrayal

"""
Code section below and above will be determined once, the visuals are fixed
"""
# def aircraft_portrayal(agent):
#     if agent is None:
#         return
    
#     portrayal = {}
#     if isinstance(agent, Aircraft):
#         portrayal["Shape"] = "circle"
#         portrayal["r"] = 0.5
#         portrayal["Layer"] = 0
#         portrayal["Color"] = "#1f77b4"
#         portrayal["Filled"] = "true"
#         portrayal["x"] = agent.pos[0]
#         portrayal["y"] = agent.pos[1]        
#     return portrayal

default = datetime(2025, 3, 1, 14, 0)
reactive_date = solara.reactive(default.date())
reactive_time = solara.reactive(default.time())
airport_id = "LAX"
gps = (33.942791, -118.410042)

model_params = {
    "airport_id": {
        "value": airport_id,
        "description": "ICAO code of the airport",
    },
    "gps": {
        "value": gps,
        "description": "GPS coordinates of the airport",
    },
    "date": {
        "value": reactive_date.value,
        "description": "Date of the simulation",
    },
    "time": {
        "value": reactive_time.value,
        "description": "Time of the simulation",
    },
    "duration": {
        "value": 10, 
        "description": "Duration of the simulation in minutes",
    }
}

airport = Airport(
    date=default.date(),
    time=default.time(),
    duration=10,
    airport_id=airport_id,
    gps=gps
)

space_component = make_space_component(portrayal_method=aircraft_portrayal, canvas_height=1000, canvas_width=1000, x_max=-116, y_max=36, x_min=-122, y_min=32)
page = SolaraViz(
    airport,
    components=[
        space_component
    ],
    play_interval=1000,
    model_params=model_params,
    name="Airport Simulation"
)

page