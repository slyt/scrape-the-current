# process_top_songs_all_time.py
# This script will process the playlist data to find the top 89 songs played across all playlists. It will combine the data from all CSV files, calculate the song counts, and save the top 89 songs to a new CSV file in the processed directory.

import pandas as pd
from glob import glob
import os
import logging

# Configure logging
logging.basicConfig(filename='process_playlist.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Path to the directory containing the CSV files
csv_dir = "output"

# Path to the directory where the processed data will be saved
processed_dir = "processed"

# Create the 'processed' directory if it doesn't exist
os.makedirs(processed_dir, exist_ok=True)

# Get a list of all CSV files in the directory
csv_files = glob(os.path.join(csv_dir, "playlist_*.csv"))

# Log the number of CSV files found
logging.info(f"Found {len(csv_files)} CSV files in '{csv_dir}'.")

# Define a list to store the DataFrames from each CSV file
all_data = []

# Loop through all CSV files
for filename in csv_files:
  logging.info(f"Processing file: {filename}")
  # Read the CSV data into a DataFrame
  df = pd.read_csv(filename)
  
  # Add the DataFrame to the list
  all_data.append(df)

logging.info("Combining DataFrames...")
# Combine all DataFrames into a single DataFrame
df = pd.concat(all_data, ignore_index=True)

logging.info("Creating 'song' column...")
# Create a new 'song' column combining artist and title
df['song'] = df['artists'] + " - " + df['title']

logging.info("Calculating song counts...")
# Get the song counts
song_counts = df['song'].value_counts()

logging.info("Creating DataFrame of top 89 songs...")
# Create a DataFrame of the top 89 songs
top_89_songs_df = pd.DataFrame({'song': song_counts.index, 'count': song_counts.values})[:89]

logging.info("Saving top 89 songs to CSV...")
# Save the top 89 songs DataFrame to a CSV file in the 'processed' directory
top_89_songs_df.to_csv(os.path.join(processed_dir, "top_89_songs.csv"), index=False)

logging.info(f"Top 89 songs saved to {os.path.join(processed_dir, 'top_89_songs.csv')}")