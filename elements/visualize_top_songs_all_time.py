import pandas as pd
import plotly.express as px
import streamlit as st

def visualize_top_songs_all_time(data_path):
  """
  This function reads the top songs data and creates a visualization.

  Args:
      data_path (str): Path to the CSV file containing the top songs data.

  Returns:
      plotly.graph_objects.Figure: The Plotly figure object for the visualization.
  """

  # Read the data from the CSV file
  df = pd.read_csv(data_path)

  # Sort by count in descending order
  df = df.sort_values(by=['count'], ascending=False)

  # Create the visualization (horizontal bar chart)
  fig = px.bar(df.head(20), x="count", y="song", 
                orientation='h', 
                labels={"song": "Song", "count": "Play Count"}, 
                title="Top Songs Played (All Time)")

  # Update layout
  fig.update_layout(
      width=800, height=600,
      yaxis={'autorange': "reversed"}  # Reverse the y-axis 
  )

  return fig