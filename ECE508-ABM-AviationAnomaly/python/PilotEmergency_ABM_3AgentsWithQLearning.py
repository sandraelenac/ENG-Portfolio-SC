import random
import numpy as np
import matplotlib.pyplot as plt

# Q-learning Parameters
alpha = 0.1   # Learning rate
gamma = 0.9   # Discount factor
epsilon = 0.1 # Exploration rate (ε-greedy)

# Q-table
Q_table = {}

# Actions
ACTIONS = ["continue_flight", "request_ATC_help"]

# Initialize simulation
def initialize_simulation(num_pilots=2):
    return {
        "pilots": [
            {"successful_decisions": 0, "fatigue_factor": 1.0, "training": 1.0}
            for _ in range(num_pilots)
        ],
        "atc": {"interventions": 0, "penalty": 1.0},
        "engine": {"failure_rate": 0.1, "failed": False},
        "sensor": {"detections": 0}
    }

# Decision-making with Q-learning or Random Action
def pilot_decision(pilot, atc, engine, use_q_learning=True):
    state = (engine["failed"], round(pilot["fatigue_factor"], 1), round(pilot["training"], 1))

    if state not in Q_table:
        Q_table[state] = {action: 0.0 for action in ACTIONS}

    if use_q_learning:
        if random.random() < epsilon:
            action = random.choice(ACTIONS)  # Exploration
        else:
            action = max(Q_table[state], key=Q_table[state].get)  # Exploitation
    else:
        action = random.choice(ACTIONS)  # No learning (Baseline)

    # Execute action
    if action == "continue_flight":
        success_prob = (0.6 * pilot["training"]) / pilot["fatigue_factor"]
        success = random.random() < success_prob
        if success:
            reward = 1
            pilot["successful_decisions"] += 1
        else:
            reward = -0.5
            pilot["fatigue_factor"] += 0.002
    else:
        atc["interventions"] += 1
        pilot["training"] += 0.01
        reward = -1

    new_state = (engine["failed"], round(pilot["fatigue_factor"], 1), round(pilot["training"], 1))

    if new_state not in Q_table:
        Q_table[new_state] = {action: 0.0 for action in ACTIONS}

    if use_q_learning:
        best_future_q = max(Q_table[new_state].values())
        Q_table[state][action] += alpha * (reward + gamma * best_future_q - Q_table[state][action])

# Run Simulation (Returns Data)
def run_simulation(steps=1000, num_pilots=3, use_q_learning=True):
    sim = initialize_simulation(num_pilots)
    success_over_time, interventions_over_time, detections_over_time, step_range = [], [], [], []
    
    for step in range(steps):
        sim["engine"]["failed"] = random.random() < sim["engine"]["failure_rate"]
        if sim["engine"]["failed"]:
            sim["sensor"]["detections"] += 1

        for pilot in sim["pilots"]:
            pilot_decision(pilot, sim["atc"], sim["engine"], use_q_learning)

        if step % 100 == 0:
            total_success = sum(p["successful_decisions"] for p in sim["pilots"])
            print(f"Step {step}: Success {total_success}, ATC Interventions {sim['atc']['interventions']}, Sensor {sim['sensor']['detections']}")
            success_over_time.append(total_success)
            interventions_over_time.append(sim["atc"]["interventions"])
            detections_over_time.append(sim["sensor"]["detections"])
            step_range.append(step)

    return success_over_time, interventions_over_time, detections_over_time, step_range

# Run Simulations
success_q, atc_q, detect_q, steps = run_simulation(use_q_learning=True)   # Q-learning
success_no_q, atc_no_q, detect_no_q, _ = run_simulation(use_q_learning=False)  # Random actions

# Plot Results
plt.figure(figsize=(12, 6))
plt.plot(steps, success_q, label="Q-learning: Successful Decisions", marker='o')
plt.plot(steps, success_no_q, label="Random: Successful Decisions", linestyle="dashed", marker='o')
plt.plot(steps, atc_q, label="Q-learning: ATC Interventions", marker='x')
plt.plot(steps, atc_no_q, label="Random: ATC Interventions", linestyle="dashed", marker='x')
plt.xlabel("Steps")
plt.ylabel("Count")
plt.legend()
plt.title("Q-learning vs Random: Pilot Success and ATC Interventions Over Time")
plt.show()
