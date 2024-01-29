import pandas as pd

# Load the "stairs" and "lift" CSV files
stairs_df = pd.read_csv("rate_of_change_data_stairs_filtered.csv")
lift_df = pd.read_csv("rate_of_change_data_lift_filtered.csv")

# Concatenate the two DataFrames
combined_df = pd.concat([stairs_df, lift_df], ignore_index=True)

# Save the combined DataFrame to a new CSV file
combined_df.to_csv("combined_data.csv", index=False)
