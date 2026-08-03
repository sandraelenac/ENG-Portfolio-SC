from mesa import Agent, Model
from datetime import datetime, timezone
import random
import matplotlib.pyplot as plt
import numpy as np

class Waypoint:
    def __init__(self, time: int, latitude: float, longitude: float, altitude: float, true_track: float, on_ground: bool):
        self.time = datetime.fromtimestamp(time, tz=timezone.utc)
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.true_track = true_track
        self.on_ground = on_ground

class Aircraft(Agent):
    def __init__(self,
                 model: Model,
                 uid: str,
                 callsign: str, 
                 departure_airport: str, 
                 arrival_airport: str, 
                 departure_time: int, 
                 arrival_time: int, 
                 track_start: int, 
                 track_end: int, 
                 waypoints):
        super().__init__(model=model)
        self.unique_id = uid
        self.callsign = callsign
        self.departure_airport = departure_airport
        self.arrival_airport = arrival_airport
        self.departure_time = datetime.fromtimestamp(departure_time, tz=timezone.utc)
        self.arrival_time = datetime.fromtimestamp(arrival_time, tz=timezone.utc)
        self.track_start = datetime.fromtimestamp(track_start, tz=timezone.utc)
        self.track_end = datetime.fromtimestamp(track_end, tz=timezone.utc)
        self.waypoints = waypoints
        self.status = "Scheduled"
        self.curr_waypoint_idx = 0
        self.pos = (None, None)
        self.altitude = None
        self.has_requested_takeoff = False
        self.has_requested_landing = False

        self.actions = {
            "follow_track": self.follow_track,
            "accelerate": self.accelerate,
            "decelerate": self.decelerate,
            "takeoff": self._request_to_takeoff,
            "land": self._request_to_land,
            "hold": self._hold,
            "adjust_track": self._adjust_track
        }
        self.available_actions = list(self.actions.keys())

        self.Q = {}
        self.epsilon = 0.1
        self.alpha = 0.1
        self.gamma = 0.99

        self.current_action = None
        self.epsilon_values = []
        self.rewards_over_time = []
        self.q_rewards = []
        self.random_rewards = []
        self.q_deltas = []
        self.last_q_value = 0

    def choose_action(self):
        state = self.get_state()
        if random.random() < self.epsilon:
            action = random.choice(self.available_actions)
        else:
            q_values = [self.Q.get((state, a), 0) for a in self.available_actions]
            max_q = max(q_values)
            best_actions = [a for a, q in zip(self.available_actions, q_values) if q == max_q]
            action = random.choice(best_actions)
        return action

    
    def step(self, shared_reward=None):
        current_time = self.model.current_time
        print(f"Aircraft: {self.callsign} | Status: {self.status} | Time: {current_time} | Pos: {self.pos} | Alt: {self.altitude}")

        if current_time < self.track_start:
            self.status = "Scheduled"
            return

        old_state = self.get_state()
        #chosen_action = self.choose_action()
        state = self.get_state()

        # Check if using exploration (random) or exploitation
        if random.random() < self.epsilon:
            chosen_action = random.choice(self.available_actions)
            from_exploration = True
        else:
            q_values = [self.Q.get((state, a), 0) for a in self.available_actions]
            max_q = max(q_values)
            best_actions = [a for a, q in zip(self.available_actions, q_values) if q == max_q]
            chosen_action = random.choice(best_actions)
            from_exploration = False

        self.actions[chosen_action]()
        new_state = self.get_state()
        reward = shared_reward if shared_reward is not None else self.compute_reward()
        if from_exploration:
            self.random_rewards.append(reward)
        else:
            self.q_rewards.append(reward)

        self._update_q(old_state, chosen_action, reward, new_state)
        self._check_route_deviation()

        if self.curr_waypoint_idx >= len(self.waypoints):
            self.status = "Landed"
        else:
            self.status = "In Flight"

        self.epsilon_values.append(self.epsilon)
        self.rewards_over_time.append(reward)
        self.epsilon = max(self.epsilon * 0.995, 0.01)

        old_q = self.Q.get((old_state, chosen_action), 0)
        max_q = max([self.Q.get((new_state, a), 0) for a in self.available_actions])
        new_q = old_q + self.alpha * (reward + self.gamma * max_q - old_q)
        self.q_deltas.append(abs(new_q - old_q))

    def get_state(self):
        if self.pos[0] is None or self.pos[1] is None:
            pos_x, pos_y = 0, 0
        else:
            pos_x, pos_y = self.pos
        alt = self.altitude if self.altitude is not None else 0
        return (self.curr_waypoint_idx, int(pos_x), int(pos_y), int(alt))

    def compute_reward(self):
        return 10 if self.status == "Landed" else 1

    def _update_q(self, state, action, reward, next_state):
        next_best = max([self.Q.get((next_state, a), 0) for a in self.available_actions])
        old_value = self.Q.get((state, action), 0)
        self.Q[(state, action)] = old_value + self.alpha * (reward + self.gamma * next_best - old_value)

    def follow_track(self):
        self.advance_waypoints(steps=1)

    def accelerate(self):
        self.advance_waypoints(steps=2)

    def decelerate(self):
        print(f"{self.callsign}: Decelerating.")

    def _request_to_land(self):
        print(f"{self.callsign}: Requesting permission to land.")

    def _request_to_takeoff(self):
        print(f"{self.callsign}: Requesting takeoff clearance.")

    def _adjust_track(self):
        if self.curr_waypoint_idx < len(self.waypoints):
            next_wp = self.waypoints[self.curr_waypoint_idx]
            if self.pos[0] is None or self.pos[1] is None:
                self.pos = (next_wp.longitude, next_wp.latitude)
                self.altitude = next_wp.altitude
            else:
                new_long = (self.pos[0] + next_wp.longitude) / 2
                new_lat = (self.pos[1] + next_wp.latitude) / 2
                self.pos = (new_long, new_lat)
                self.altitude = (self.altitude + next_wp.altitude) / 2 if self.altitude is not None else next_wp.altitude
            print(f"{self.callsign}: Adjusted track. New position: {self.pos}, Altitude: {self.altitude}.")
        else:
            print(f"{self.callsign}: Adjust track not applicable; no remaining waypoints.")

    def _hold(self):
        print(f"{self.callsign}: Executing hold; maintaining current position {self.pos} and altitude {self.altitude}.")

    def advance_waypoints(self, steps=1):
        current_time = self.model.current_time
        for _ in range(steps):
            if self.curr_waypoint_idx < len(self.waypoints) and self.waypoints[self.curr_waypoint_idx].time <= current_time:
                wp = self.waypoints[self.curr_waypoint_idx]
                self.pos = (wp.longitude, wp.latitude)
                self.altitude = wp.altitude
                self.curr_waypoint_idx += 1
            else:
                break

    def _check_route_deviation(self):
        pass

    def get_q_matrix(self):
        state_keys = sorted(set([s for (s, _) in self.Q.keys()]))
        action_keys = sorted(set([a for (_, a) in self.Q.keys()]))

        state_index = {s: i for i, s in enumerate(state_keys)}
        action_index = {a: i for i, a in enumerate(action_keys)}

        matrix = np.zeros((len(state_keys), len(action_keys)))
        for (s, a), val in self.Q.items():
            matrix[state_index[s]][action_index[a]] = val

        return matrix

