# process_top_songs_per_year.py
import pandas as pd
from glob import glob
import os
import logging

# Configure logging
logging.basicConfig(filename='process_playlist_yearly.log', level=logging.INFO,
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

# Create 'year' column
df['year'] = df['timestamp'].dt.year

# Create 'song' column (optional, can be removed if not needed)
df['song'] = df['artists'] + " - " + df['title']

# Group by year, count songs, and get top 89
yearly_top_songs = df.groupby('year')['song'].value_counts() \
                   .groupby(level=0).head(89).reset_index(name='count')

# Include title and artist columns (if the 'song' column was created, remove this block)
if 'song' in df.columns:
  # Group by year, get unique songs with title and artist
  yearly_unique_songs = df.groupby('year')[['title', 'artists']].nunique().reset_index()

  # Merge yearly_top_songs with yearly_unique_songs to include title and artist
  yearly_top_songs = yearly_top_songs.merge(yearly_unique_songs, how='left', on='year')

# Save yearly top songs to CSV files
for year, group_df in yearly_top_songs.groupby('year'):
  filename = f"top_89_songs_{year}.csv"  # No month padding needed for year
  filepath = os.path.join(processed_dir, filename)
  group_df.to_csv(filepath, index=False)
  logging.info(f"Saved yearly top songs for {year} to {filepath}")