from mesa import Agent, Model
from datetime import datetime, timezone
import random
import matplotlib.pyplot as plt

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
        # Store departure and arrival times as datetime objects
        self.departure_time = datetime.fromtimestamp(departure_time, tz=timezone.utc)
        self.arrival_time = datetime.fromtimestamp(arrival_time, tz=timezone.utc)
        self.track_start = datetime.fromtimestamp(track_start, tz=timezone.utc)
        self.track_end = datetime.fromtimestamp(track_end, tz=timezone.utc)
        self.waypoints = waypoints
        self.status = "Scheduled"
        self.curr_waypoint_idx = 0
        self.pos = (None, None)
        self.altitude = None
        
        # Need to add the phase of flight (takeoff, climb, cruise, decsent, landing, taxiing)
        
        # Flags to ensure requests (takeoff/landing) are sent only once
        self.has_requested_takeoff = False
        self.has_requested_landing = False
        
        # ------ Action Functions Dictionary ------
        # Each action is mapped to a function.
        self.actions = {
            "follow_track": self.follow_track,
            "accelerate": self.accelerate,
            "decelerate": self.decelerate,
            "takeoff": self._request_to_takeoff,
            "land": self._request_to_land,
            "hold": self._hold,
            "adjust_track": self._adjust_track
        }
        # The available actions (keys) for Q-table lookups.
        self.available_actions = list(self.actions.keys())
        
        # Q-table: keys are (state, action) pairs; value is estimated Q-value.
        self.Q = {}
        self.epsilon = 0.1   # Exploration rate.
        self.alpha = 0.1     # Learning rate.
        self.gamma = 0.99    # Discount factor.
        
        # Will store the current state and chosen action (for training updates).
        self.current_action = None

        self.epsilon_values = []
        self.rewards_over_time = []
        self.q_rewards = []           # Stores rewards when Q-learning action is taken
        self.random_rewards = []      # Stores rewards when random action is taken
        self.q_deltas = []            # Tracks changes in Q-values after updates
        self.q_matrix = {}            # Stores Q-table snapshots by state
        self.last_q_value = 0         # Temporary storage for comparing Q deltas
                
    def advance_waypoints(self, steps=1):
        """
        Advances the aircraft along its waypoints based on current model time.
        'steps' indicates how many waypoints to attempt to advance.
        """
        current_time = self.model.current_time
        for _ in range(steps):
            if self.curr_waypoint_idx < len(self.waypoints) and self.waypoints[self.curr_waypoint_idx].time <= current_time:
                wp = self.waypoints[self.curr_waypoint_idx]
                self.pos = (wp.longitude, wp.latitude)
                self.altitude = wp.altitude
                self.curr_waypoint_idx += 1
            else:
                break  # Either no more waypoints or the next waypoint time has not been reached.
    
    def execute_action(self, action):
        """
        Executes the chosen action:
          - 0: Follow the track normally (advance one waypoint)
          - 1: Hold position (do nothing)
          - 2: Accelerate (advance two waypoints if possible)
          - 3: Decelerate (simulate deceleration by holding)
        """
        if action == 0:
            self.advance_waypoints(steps=1)
        elif action == 1:
            # Hold position: do nothing.
            pass
        elif action == 2:
            self.advance_waypoints(steps=2)
        elif action == 3:
            # Decelerate: for this simple implementation, we treat deceleration as a hold.
            pass
    
    def compute_reward(self):
        """
        Computes the reward for the aircraft. For demonstration,
        reward is defined as:
          +1 for each waypoint advancement,
          and a bonus +10 when the aircraft has landed.
        """
        if self.status == "Landed":
            return 10
        else:
            return 1

    def step(self):
        """
        Each step:
          - Updates the flight status based on current_time.
          - Uses Q-learning to decide which action to execute.
          - Calls the corresponding function (via self.actions).
          - Observes the new state and updates the Q-table.
          - Updates the flight status (e.g., "In Flight" or "Landed").
        """
        current_time = self.model.current_time
        print(f"Aircraft: {self.callsign} | Status: {self.status} | Time: {current_time} | Pos: {self.pos} | Alt: {self.altitude}")
        
        # If before the track starts, remain scheduled.
        if current_time < self.track_start:
            self.status = "Scheduled"
            return
        
        # Record the old state.
        old_state = self.get_state()
        # Choose an action from the available set.
        chosen_action = self.choose_action()
        
        # Execute the action by calling its corresponding function.
        # This abstracts the control decisions as function calls.
        self.actions[chosen_action]()
        
        # Get the new state after executing the chosen action.
        new_state = self.get_state()
        
        # Compute reward based on progress.
        reward = self.compute_reward()
        
        # Update the Q-table with the observed transition.
        self._update_q(old_state, chosen_action, reward, new_state)
        self._check_route_deviation() #for logging purposes 

        # Update flight status.
        if self.curr_waypoint_idx >= len(self.waypoints):
            self.status = "Landed"
        else:
            self.status = "In Flight"

        self.epsilon_values.append(self.epsilon)
        self.rewards_over_time.append(reward)
        self.epsilon = max(self.epsilon * 0.995, 0.01)

        # Track Q-delta for convergence
        old_q = self.Q.get((old_state, chosen_action), 0)
        max_q = max([self.Q.get((new_state, a), 0) for a in self.available_actions])
        new_q = old_q + self.alpha * (reward + self.gamma * max_q - old_q)
        self.q_deltas.append(abs(new_q - old_q))

                
    def choose_action(self):
        state = self.get_state()
        # ε-greedy: choose a random action with probability epsilon.
        if random.random() < self.epsilon:
            action = random.choice(self.available_actions)
        else:
            # Retrieve Q-values for all available actions (default to 0 if unseen).
            q_values = [self.Q.get((state, a), 0) for a in self.available_actions]
            max_q = max(q_values)
            # Break ties at random.
            best_actions = [a for a, q in zip(self.available_actions, q_values) if q == max_q]
            action = random.choice(best_actions)
        return action
    
    def get_state(self):
        """
        Returns a discretized state that represents the aircraft's progress.
        For this example, the state is a tuple:
          (current waypoint index, pos_x, pos_y, altitude)
        If pos or altitude is not yet set, defaults to 0.
        """
        # If pos was not yet defined, use default 0,0.
        if self.pos[0] is None or self.pos[1] is None:
            pos_x, pos_y = 0, 0
        else:
            pos_x, pos_y = self.pos
        alt = self.altitude if self.altitude is not None else 0
        return (self.curr_waypoint_idx, int(pos_x), int(pos_y), int(alt))
    
    def follow_track(self):
        """Normal progression along the track (advance one waypoint)."""
        self.advance_waypoints(steps=1)
        
    def accelerate(self):
        """Accelerate: attempt to advance two waypoints."""
        self.advance_waypoints(steps=2)
    
    def decelerate(self):
        '''Decelerate to reduce speed.'''
        print(f"{self.callsign}: Decelerating.") 
    
    def _request_to_land(self):
        '''Send message to Control Tower when approaching destination or seeking permission to land.'''
        print(f"{self.callsign}: Requesting permission to land.")

    def _request_to_takeoff(self):
        '''Send message to Control Tower when departing from the gate/runway.'''
        print(f"{self.callsign}: Requesting takeoff clearance.")
        
    def _adjust_track(self):
        """
        Adjust track: simulate correcting the course.
        For example, move the aircraft's current position toward the next waypoint
        by taking the average of the current position and the next waypoint's position.
        """
        if self.curr_waypoint_idx < len(self.waypoints):
            next_wp = self.waypoints[self.curr_waypoint_idx]
            # If current position is undefined, initialize with next waypoint.
            if self.pos[0] is None or self.pos[1] is None:
                self.pos = (next_wp.longitude, next_wp.latitude)
                self.altitude = next_wp.altitude
            else:
                new_long = (self.pos[0] + next_wp.longitude) / 2
                new_lat = (self.pos[1] + next_wp.latitude) / 2
                self.pos = (new_long, new_lat)
                # Similarly adjust altitude.
                self.altitude = (self.altitude + next_wp.altitude) / 2 if self.altitude is not None else next_wp.altitude
            print(f"{self.callsign}: Adjusted track. New position: {self.pos}, Altitude: {self.altitude}.")
        else:
            print(f"{self.callsign}: Adjust track not applicable; no remaining waypoints.")

    def _hold(self):
        """
        Hold: simulate a holding pattern by not advancing the waypoint index.
        The aircraft stays at its current location until next instructions.
        """
        print(f"{self.callsign}: Executing hold; maintaining current position {self.pos} and altitude {self.altitude}.")
    
    def _update_q(self, state, action, reward, next_state):
        """
        Performs the Q-learning update:
          Q(s, a) ← Q(s, a) + α [reward + γ · max Q(next_state, ⋅) − Q(s, a)]
        """
        next_best = max([self.Q.get((next_state, a), 0) for a in self.available_actions])
        old_value = self.Q.get((state, action), 0)
        self.Q[(state, action)] = old_value + self.alpha * (reward + self.gamma * next_best - old_value)
    
    #added this by Sandra
    def _check_route_deviation(self):
        if self.curr_waypoint_idx < len(self.waypoints):
            wp = self.waypoints[self.curr_waypoint_idx]
            if self.pos[0] is not None and self.pos[1] is not None:
                lon_diff = abs(self.pos[0] - wp.longitude)
                lat_diff = abs(self.pos[1] - wp.latitude)
                if lon_diff > 0.05 or lat_diff > 0.05:
                    self.model.anomaly_monitor.record({
                        "type": "Route Deviation",
                        "time": self.model.current_time,
                        "aircraft": self.callsign,
                        "position": self.pos
                    })
                    print(f"🚨 Route Deviation: {self.callsign} deviated at {self.pos}")
