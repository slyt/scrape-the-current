import pandas as pd
import os
import glob

# Directory containing output files
OUTPUT_DIR = 'output'

# Function to load all CSV files into a single DataFrame
def load_all_csv_files(output_dir):
    """Load all CSV files in the specified directory into a single DataFrame."""
    csv_files = glob.glob(os.path.join(output_dir, "playlist_*.csv"))
    dataframes = [pd.read_csv(f) for f in csv_files]
    if dataframes:
        return pd.concat(dataframes, ignore_index=True)
    else:
        return pd.DataFrame()

# Load the data
df = load_all_csv_files(OUTPUT_DIR)

# Preprocess data
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['year_month'] = df['timestamp'].dt.to_period('M').astype(str)
df['title_artist'] = df['title'] + " - " + df['artists']

# Aggregate data by month
monthly_counts = (
    df.groupby(['year_month', 'title_artist'])
    .size()
    .reset_index(name='play_count')
)

# Calculate top 10 songs for each month
top_10_per_month = (
    monthly_counts.sort_values(['year_month', 'play_count'], ascending=[True, False])
    .groupby('year_month')
    .head(10)
    .reset_index(drop=True)
)

# Save to a CSV file
preprocessed_file = os.path.join(OUTPUT_DIR, 'top_10_per_month.csv')
top_10_per_month.to_csv(preprocessed_file, index=False)
print(f"Preprocessed top 10 lists saved to {preprocessed_file}")
