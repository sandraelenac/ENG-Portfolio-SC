import json
import matplotlib.pyplot as plt
import pandas as pd
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

        # Count anomalies over time
        counts = df.groupby([pd.Grouper(key="time", freq="1S"), "type"]).size().unstack(fill_value=0)

        counts.plot(marker="o")
        plt.title("Aircrafts Anomaly Counts Over Time")
        plt.xlabel("Simulation Time")
        plt.ylabel("Count")
        plt.legend(title="Anomaly Type")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

def plot_route_deviation_heatmap(self):
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd

    route_data = [a for a in self.anomalies if a["type"] == "Route Deviation"]
    if not route_data:
        print("No route deviations found for heatmap.")
        return

    df = pd.DataFrame([a["position"] for a in route_data], columns=["longitude", "latitude"])
    plt.figure(figsize=(10, 8))
    sns.kdeplot(
        data=df, x="longitude", y="latitude", fill=True, cmap="Reds", bw_adjust=0.5, levels=100, thresh=0.05
    )
    plt.title("📍 Route Deviation Heatmap")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.tight_layout()
    plt.show()


    # def plot_deviation_heatmap(self):
    #     df = pd.DataFrame(self.records)
    #     if "position" not in df.columns:
    #         print("⚠️ No position data available.")
    #         return

    #     df = df[df["type"] == "Route Deviation"]
    #     df = df.dropna(subset=["position"])
    #     df["longitude"] = df["position"].apply(lambda x: x[0] if x and len(x) > 0 else None)
    #     df["latitude"] = df["position"].apply(lambda x: x[1] if x and len(x) > 1 else None)

    #     # Filter invalid points
    #     df = df.dropna(subset=["longitude", "latitude"])
    #     df = df[(df["longitude"] > -180) & (df["longitude"] < 180)]
    #     df = df[(df["latitude"] > -90) & (df["latitude"] < 90)]

    #     if df.empty:
    #         print("⚠️ No valid deviation positions to plot.")
    #         return

    #     plt.figure(figsize=(10, 6))
    #     sns.kdeplot(
    #         x=df["longitude"],
    #         y=df["latitude"],
    #         cmap="Reds",
    #         fill=True,
    #         bw_adjust=0.5
    #     )
    #     plt.title("Aircraft Route Deviation Heatmap")
    #     plt.xlabel("Longitude")
    #     plt.ylabel("Latitude")
    #     plt.tight_layout()
    #     plt.grid(True)
    #     plt.show()

    def plot_epsilon_vs_reward(epsilons, rewards):
        if len(epsilons) != len(rewards) or len(epsilons) < 2:
            print("Not enough data to plot.")
            return

        plt.figure(figsize=(12, 6))
        plt.plot(epsilons, rewards, marker='o')
        plt.xlabel("Epsilon")
        plt.ylabel("Reward")
        plt.title("Epsilon vs. Reward")
        plt.grid(True)
        plt.show()

    # def plot_epsilon_vs_reward(self, epsilons, rewards):
    #     if not epsilons or not rewards:
    #         print("⚠️ Missing epsilon or reward data.")
    #         return

    #     plt.figure(figsize=(10, 5))
    #     plt.plot(epsilons, rewards, marker='o', linestyle='-', color='tab:blue')
    #     plt.xlabel("Epsilon")
    #     plt.ylabel("Reward")
    #     plt.title("Epsilon vs. Reward")
    #     plt.grid(True)
    #     plt.tight_layout()
    #     plt.show()

    def plot_q_deltas(self, q_deltas):
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
        plt.show()

    def compare_q_vs_random(self, q_rewards, random_rewards):
        plt.figure(figsize=(10, 5))
        plt.plot(q_rewards, label="Q-learning", color='tab:blue')
        plt.plot(random_rewards, label="Random Actions", color='tab:orange')
        plt.xlabel("Step")
        plt.ylabel("Reward")
        plt.title("Q-learning vs Random Action Rewards")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_q_evolution(self, q_evolution_matrix):
        plt.figure(figsize=(12, 6))
        sns.heatmap(q_evolution_matrix, cmap="Blues", cbar=True)
        plt.title("Q-value Evolution Over Time")
        plt.xlabel("Action")
        plt.ylabel("State")
        plt.tight_layout()
        plt.show()

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
        plt.show()

"""
DO NOT DELETE THE BELOW CODE UNTIL ALL GRAPHS ARE VERIFIED AND VALIDATED
"""
# """
# Visuals & Metrics
# """

# import json
# import matplotlib.pyplot as plt
# import pandas as pd
# import seaborn as sns

# class AnomalyMonitor:
#     def __init__(self):
#         self.log = []

#     def record(self, entry: dict):
#         self.log.append(entry)
#         print(f"📍 Anomaly recorded: {entry['type']}")

#     def save_to_file(self, path="anomaly_log.json"):
#         with open(path, "w") as f:
#             json.dump(self.log, f, indent=2, default=str)
#         print(f"📁 Anomaly log saved to {path}")

#     def plot_summary(self):
#         if not self.log:
#             print("No anomalies to plot.")
#             return

#         df = pd.DataFrame(self.log)
#         df["time"] = pd.to_datetime(df["time"])
#         counts = df.groupby([pd.Grouper(key='time', freq='1S'), 'type']).size().unstack(fill_value=0)

#         counts.plot(kind='line', marker='o', figsize=(10, 5), title="📊 Anomaly Counts Over Time")
#         plt.xlabel("Simulation Time")
#         plt.ylabel("Count")
#         plt.grid(True)
#         plt.legend(title="Anomaly Type")
#         plt.tight_layout()
#         plt.show()

#         # Heatmap (route deviation only)
#         if "position" in df.columns:
#             pos_df = df[df["type"] == "Route Deviation"]
#             if not pos_df.empty:
#                 pos_coords = pd.DataFrame(pos_df["position"].tolist(), columns=["lon", "lat"])
#                 if pos_coords.shape[0] > 1 and pos_coords.nunique().min() > 1:
#                     plt.figure(figsize=(6, 6))
#                     sns.kdeplot(data=pos_coords, x="lon", y="lat", fill=True, cmap="Reds", thresh=0.05)
#                     plt.title("🔥 Heatmap of Route Deviations")
#                     plt.tight_layout()
#                     plt.show()
#                 else:
#                     print("⚠️ Not enough data for heatmap.")
