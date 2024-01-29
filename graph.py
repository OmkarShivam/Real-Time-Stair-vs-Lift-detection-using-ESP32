import pandas as pd
import matplotlib.pyplot as plt

def plot_graphs(data_df, activity):
    plt.figure(figsize=(14, 10))

    # Line plot for altitude rate of change
    plt.subplot(2, 2, 1)
    plt.plot(data_df['timestamp'], data_df['altitude_rate_of_change'], color='orange', label='Altitude Rate of Change')
    plt.xlabel('Timestamp')
    plt.ylabel('Altitude Rate of Change')
    plt.title(f'Line Plot for Altitude Rate of Change ({activity})')
    plt.legend()

    # Line plot for gyroX rate of change
    plt.subplot(2, 2, 2)
    plt.plot(data_df['timestamp'], data_df['gyroX_rate_of_change'], color='blue', label='gyroX Rate of Change')
    plt.xlabel('Timestamp')
    plt.ylabel('gyroX Rate of Change')
    plt.title(f'Line Plot for gyroX Rate of Change ({activity})')
    plt.legend()

    # Line plot for gyroY rate of change
    plt.subplot(2, 2, 3)
    plt.plot(data_df['timestamp'], data_df['gyroY_rate_of_change'], color='red', label='gyroY Rate of Change')
    plt.xlabel('Timestamp')
    plt.ylabel('gyroY Rate of Change')
    plt.title(f'Line Plot for gyroY Rate of Change ({activity})')
    plt.legend()

    # Line plot for gyroZ rate of change
    plt.subplot(2, 2, 4)
    plt.plot(data_df['timestamp'], data_df['gyroZ_rate_of_change'], color='green', label='gyroZ Rate of Change')
    plt.xlabel('Timestamp')
    plt.ylabel('gyroZ Rate of Change')
    plt.title(f'Line Plot for gyroZ Rate of Change ({activity})')
    plt.legend()

    plt.tight_layout()
    plt.show()

# Load data for stairs
stairs_df = pd.read_csv("rate_of_change_data_stairs_filtered.csv")
plot_graphs(stairs_df, "Stairs")

# Load data for lift
lift_df = pd.read_csv("rate_of_change_data_lift_filtered.csv")
plot_graphs(lift_df, "Lift")
