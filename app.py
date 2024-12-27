import streamlit as st
import pandas as pd
from elements import visualize_top_songs_all_time
  # Import from visualize_top_songs.py

# Path to the CSV file containing top songs data (replace with your actual path)
data_path = "processed/top_89_songs.csv"

# Available data views
view_options = ["Top 89 Songs for All Time", "Top 89 Songs Over Time"] 

# Sidebar selection
selected_view = st.sidebar.selectbox("Select Data View", view_options)

if selected_view == "Top 89 Songs for All Time":
  st.markdown("# Top 89 Songs for All Time")
  fig = visualize_top_songs_all_time.visualize_top_songs_all_time(data_path)
  st.plotly_chart(fig)  # Display the figure using Streamlit
elif selected_view == "Top 89 Songs Over Time":
  st.markdown("# Top 89 Songs Over Time")
  # ... (placeholder for future implementation)