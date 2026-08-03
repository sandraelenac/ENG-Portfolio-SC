import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set global style
sns.set(style="whitegrid")

# 1. Q-Table Heatmap (Simulated)
states = ['S1', 'S2', 'S3', 'S4', 'S5']
actions = ['Up', 'Down', 'Left', 'Right']
q_table = np.random.uniform(low=-1, high=1, size=(5, 4))
q_df = pd.DataFrame(q_table, index=states, columns=actions)

plt.figure(figsize=(8, 5))
sns.heatmap(q_df, annot=True, cmap="coolwarm", center=0, linewidths=0.5)
plt.title("Q-Table Heatmap")
plt.tight_layout()
plt.savefig("q_table_heatmap.png")
plt.close()

# 2. Action Selection History (Simulated)
action_counts = {
    'Up': 120,
    'Down': 85,
    'Left': 150,
    'Right': 95
}
plt.figure(figsize=(6, 4))
sns.barplot(x=list(action_counts.keys()), y=list(action_counts.values()), palette="Blues_d")
plt.title("Action Selection Frequency")
plt.xlabel("Action")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("action_selection_history.png")
plt.close()

# 3. Policy Changes Over Time (Simulated)
policy_evolution = {
    'Episode 0': ['Up', 'Up', 'Down', 'Left', 'Right'],
    'Episode 50': ['Left', 'Down', 'Left', 'Left', 'Right'],
    'Episode 100': ['Left', 'Left', 'Left', 'Right', 'Right']
}
policy_df = pd.DataFrame(policy_evolution, index=states)

# Convert policy to numeric encoding for heatmap color (while preserving text)
action_map = {'Up': 0, 'Down': 1, 'Left': 2, 'Right': 3}
policy_numeric = policy_df.replace(action_map)

plt.figure(figsize=(8, 4))
sns.heatmap(policy_numeric, annot=policy_df, cmap="viridis", cbar=False, fmt='', linewidths=0.5)
plt.title("Policy Evolution Over Time")
plt.tight_layout()
plt.savefig("policy_changes_over_time.png")
plt.close()

# 4. Exploration vs. Exploitation Ratio Plot
episodes = np.arange(100)
exploration_ratio = np.exp(-0.05 * episodes)
exploitation_ratio = 1 - exploration_ratio

plt.figure(figsize=(10, 5))
plt.plot(episodes, exploration_ratio, label="Exploration", linestyle='--', color='blue')
plt.plot(episodes, exploitation_ratio, label="Exploitation", linestyle='-', color='green')
plt.title("Exploration vs Exploitation Over Time")
plt.xlabel("Episode")
plt.ylabel("Ratio")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("exploration_vs_exploitation.png")
plt.close()

# 5. Shared Reward Simulation (New for MARL)
shared_rewards = np.cumsum(np.random.normal(loc=1.0, scale=0.2, size=100))

plt.figure(figsize=(10, 5))
plt.plot(shared_rewards, label="Shared Team Reward", marker='o', color='purple')
plt.title("Simulated Shared Reward Trend")
plt.xlabel("Time Step")
plt.ylabel("Cumulative Shared Reward")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("simulated_shared_reward.png")
plt.close()
