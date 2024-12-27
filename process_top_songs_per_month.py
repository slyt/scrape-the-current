import pandas as pd
from glob import glob
import os
import logging

# Configure logging
logging.basicConfig(filename='process_playlist_monthly.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Paths
csv_dir = "output"
processed_dir = "processed"

# Create the 'processed' directory if it doesn't exist
os.makedirs(processed_dir, exist_ok=True)

# Get a list of all CSV files in the directory
csv_files = glob(os.path.join(csv_dir, "playlist_*.csv"))
logging.info(f"Found {len(csv_files)} CSV files in '{csv_dir}'.")

# Combine all DataFrames into a single DataFrame
all_data = []
for filename in csv_files:
  logging.info(f"Processing file: {filename}")
  df = pd.read_csv(filename)
  all_data.append(df)
df = pd.concat(all_data, ignore_index=True)

# Convert 'timestamp' to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Create 'month' and 'year' columns
df['month'] = df['timestamp'].dt.month
df['year'] = df['timestamp'].dt.year

# Create 'song' column
df['song'] = df['artists'] + " - " + df['title']

# Group by month and year, count songs, and get top 89
monthly_top_songs = df.groupby(['year', 'month'])['song'].value_counts() \
                     .groupby(level=[0, 1]).head(89).reset_index(name='count')

# Save monthly top songs to CSV files
for (year, month), group_df in monthly_top_songs.groupby(['year', 'month']):
  filename = f"top_89_songs_{year}_{month:02d}.csv"  # Pad month with zero
  filepath = os.path.join(processed_dir, filename)
  group_df.to_csv(filepath, index=False)
  logging.info(f"Saved monthly top songs for {year}-{month:02d} to {filepath}")