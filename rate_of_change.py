import pandas as pd
from scipy.stats import zscore

# Read the collected data from CSV file
df = pd.read_csv('Stairs_data.csv')

# Step 1: Sort the data based on timestamps
df.sort_values(by='timestamp', inplace=True)

# Step 2: Calculate delta time (time difference between consecutive timestamps)
df['delta_time'] = df['timestamp'].diff()

# Step 3: Compute the rate of change for each sensor reading
sensor_columns = ['accelX', 'accelY', 'accelZ', 'gyroX', 'gyroY', 'gyroZ', 'altitude']
for sensor in sensor_columns:
    # Compute rate of change by dividing sensor value difference by delta time
    df[f'{sensor}_rate_of_change'] = df[sensor].diff() / df['delta_time']

# Drop rows with NaN values (due to first row differences being NaN)
df.dropna(inplace=True)

# Step 4: Remove outliers using z-score
z_scores = zscore(df[['accelX_rate_of_change', 'accelY_rate_of_change', 'accelZ_rate_of_change',
                      'gyroX_rate_of_change', 'gyroY_rate_of_change', 'gyroZ_rate_of_change',
                      'altitude_rate_of_change']])
abs_z_scores = abs(z_scores)
filtered_entries = (abs_z_scores < 3).all(axis=1)
df = df[filtered_entries]

# Save the updated DataFrame to a new CSV file
df.to_csv('rate_of_change_data_stairs_filtered.csv', index=False)
