import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

class AnomalyMonitor:
    def __init__(self):
        self.records = []

    def record(self, entry):
        self.records.append(entry)

    def save_to_file(self, filename="anomaly_log.json"):
        with open(filename, "w") as f:
            json.dump(self.records, f, indent=4, default=str)
        print(f"📁 Anomaly log saved to {filename}")

    def plot_summary(self):
        if not self.records:
            print("⚠️ No anomalies to plot.")
            return

        df = pd.DataFrame(self.records)
        df["time"] = pd.to_datetime(df["time"])
        df = df.dropna(subset=["time", "type"])

        counts = df.groupby([pd.Grouper(key="time", freq="1s"), "type"]).size().unstack(fill_value=0)

        counts.plot(marker="o")
        plt.title("Aircrafts Anomaly Counts Over Time")
        plt.xlabel("Simulation Time")
        plt.ylabel("Count")
        plt.legend(title="Anomaly Type")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("AircraftAnomalyCountsOverTime.png")
        print("✅ Saved AircraftAnomalyCountsOverTime.png")
        plt.show(block=False)
        plt.close()

    def plot_route_deviation_heatmap(self, airport_coords):
        deviation_coords = [
            (record["position"][0], record["position"][1])
            for record in self.records
            if record.get("type") in ["Route Deviation", "Collision Risk"] and "position" in record
        ]

        if not deviation_coords:
            print("⚠️ No route deviations to plot.")
            return

        df = pd.DataFrame(deviation_coords, columns=["longitude", "latitude"])

        plt.figure(figsize=(10, 6))
        sns.kdeplot(
            data=df,
            x="longitude",
            y="latitude",
            cmap="Reds",
            fill=True,
            bw_adjust=0.5,
        )

        for name, coords in airport_coords.items():
            plt.text(coords[0], coords[1], f" {name}", verticalalignment='bottom', fontsize=9)

        plt.title("Route Deviation Heatmap")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("AircraftRerouteHeatmap.png")
        print("✅ AircraftRerouteHeatmap.png")
        plt.show(block=False)
        plt.close()

    def plot_epsilon_vs_reward(self, epsilons, rewards, agent_id = "agent"):
        if len(epsilons) < 2 or len(epsilons) != len(rewards):
            print("⚠️ Not enough data to plot Epsilon vs Reward.")
            return

        plt.figure(figsize=(10, 5))
        plt.plot(epsilons, rewards, marker='o', label="Individual Agent")
        plt.xlabel("Epsilon")
        plt.ylabel("Reward")
        plt.title("Epsilon vs. Reward")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"EpsilonVSreward_{agent_id}.png")
        print(f"✅ EpsilonVSreward.png for {agent_id}")
        plt.show(block=False)
        plt.close()

    def plot_q_deltas(self, q_deltas, agent_id="agent"):
        if not q_deltas:
            print("⚠️ No Q-deltas to plot.")
            return

        plt.figure(figsize=(10, 5))
        plt.plot(range(len(q_deltas)), q_deltas, color='tab:green')
        plt.xlabel("Step")
        plt.ylabel("ΔQ")
        plt.title("Q-value Change Over Time")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"Q-valueOverTime_{agent_id}.png")
        print(f"✅ Q-valueOverTime.png for {agent_id}")
        plt.show(block=False)
        plt.close()

    def compare_q_vs_random(self, q_rewards, random_rewards, agent_id="agent"):
        plt.figure(figsize=(10, 5))
        plt.plot(q_rewards, label="Q-learning", color='tab:blue')
        plt.plot(random_rewards, label="Random Actions", color='tab:orange')
        plt.xlabel("Step")
        plt.ylabel("Reward")
        plt.title("Q-learning vs Random Action Rewards")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"QL-VS-Actions_{agent_id}.png")
        print(f"✅ QL-VS-Actions.png for {agent_id}")
        plt.show(block=False)
        plt.close()

    def plot_q_evolution(self, q_evolution_matrix, agent_id="agent"):
        if q_evolution_matrix is None or len(q_evolution_matrix) == 0:
            print("⚠️ Q-matrix is empty or None.")
            return

        q_array = np.array(q_evolution_matrix)

        if q_array.ndim != 2 or q_array.size == 0:
            print(f"⚠️ Invalid Q-matrix shape: {q_array.shape}. Skipping plot.")
            return

        plt.figure(figsize=(10, 6))
        sns.heatmap(q_evolution_matrix, cmap="Blues", cbar=True)
        plt.title("Q-value Evolution Over Time")
        plt.xlabel("Action")
        plt.ylabel("State")
        plt.tight_layout()
        plt.savefig(f"Q-ValueOverTime_{agent_id}.png")
        print(f"✅ Q-ValueOverTime for {agent_id}.png")
        plt.show(block=False)
        plt.close()

    def plot_atc_interventions(self, timestamps):
        if not timestamps:
            print("⚠️ No ATC interventions recorded.")
            return
        counts = pd.Series(timestamps).value_counts().sort_index()
        plt.figure(figsize=(10, 4))
        counts.plot(marker="o")
        plt.title("ATC Interventions Over Time")
        plt.xlabel("Time Step")
        plt.ylabel("Interventions")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("ATC-Interventions.png")
        print("✅ ATC-Interventions.png")
        plt.show(block=False)
        plt.close()

    def plot_shared_rewards(self, shared_rewards):
        if not shared_rewards:
            print("⚠️ No shared rewards to plot.")
            return

        plt.figure(figsize=(10, 5))
        plt.plot(shared_rewards, marker='o', label="Shared Reward")
        plt.xlabel("Step")
        plt.ylabel("Shared Reward")
        plt.title("Shared Reward Over Time")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig("SharedRewardOverTime.png")
        print("✅ SharedRewardOverTime.png")
        plt.show(block=False)
        plt.close()

    def plot_all_metrics(self, epsilons, rewards, q_deltas, q_rewards, random_rewards, q_matrices=[]):
        if epsilons and rewards:
            filename = "EpsilonVSreward_ALL.png"
            plt.figure(figsize=(10, 5))
            plt.plot(epsilons, rewards, marker='o', label="Combined")
            plt.xlabel("Epsilon")
            plt.ylabel("Reward")
            plt.title("Epsilon vs. Reward (ALL)")
            plt.grid(True)
            plt.legend()
            plt.tight_layout()
            plt.savefig(filename)
            print(f"✅ {filename}")
            plt.close()

        if q_deltas:
            filename = "Q-valueOverTime_ALL.png"
            plt.figure(figsize=(10, 5))
            plt.plot(range(len(q_deltas)), q_deltas, color='tab:green')
            plt.xlabel("Step")
            plt.ylabel("ΔQ")
            plt.title("Q-value Change Over Time (ALL)")
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(filename)
            print(f"✅ {filename}")
            plt.close()

        if q_rewards and random_rewards:
            filename = "QL-VS-Actions_ALL.png"
            plt.figure(figsize=(10, 5))
            plt.plot(q_rewards, label="Q-learning", color='tab:blue')
            plt.plot(random_rewards, label="Random Actions", color='tab:orange')
            plt.xlabel("Step")
            plt.ylabel("Reward")
            plt.title("Q-learning vs Random Actions (ALL)")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(filename)
            print(f"✅ {filename}")
            plt.close()

        if q_matrices:
            # Note to self, look into add an GEO map in the background
            filename = "Q-ValueHeatmap_ALL.png"
            avg_matrix = np.mean(np.array(q_matrices), axis=0)
            plt.figure(figsize=(10, 6))
            sns.heatmap(avg_matrix, cmap="Blues", cbar=True)
            plt.title("Average Q-Value Heatmap (ALL)")
            plt.xlabel("Action")
            plt.ylabel("State")
            plt.tight_layout()
            plt.savefig(filename)
            print(f"✅ {filename}")
            plt.close()

