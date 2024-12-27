import streamlit as st
import pandas as pd
from elements import visualize_top_songs_all_time, visualize_monthly_top_songs  # Import both functions

# Path to the directory containing monthly top songs data (replace with your actual path)
data_dir = "processed"

# Path to the CSV file containing all-time top songs data (replace with your actual path)
data_path = "processed/top_89_songs.csv"

# Available data views
view_options = ["Top 89 Songs for All Time", "Top 89 Songs Monthly"]

# Sidebar selection
selected_view = st.sidebar.selectbox("Select Data View", view_options)

if selected_view == "Top 89 Songs for All Time":
  st.markdown("# Top 89 Songs for All Time")
  fig = visualize_top_songs_all_time.visualize_top_songs_all_time(data_path)
  st.plotly_chart(fig)  # Display the figure using Streamlit
elif selected_view == "Top 89 Songs Monthly":
  st.markdown("# Top 89 Songs Monthly")
  # Month and year selection widgets
  months = [
      "January", "February", "March", "April", "May", "June",
      "July", "August", "September", "October", "November", "December"
  ]
  selected_month = st.selectbox("Select Month", months)
  selected_month_index = months.index(selected_month)  # Get month index (0-based)

  years = [2023, 2024]  # Adjust based on your data
  selected_year = st.selectbox("Select Year", years)

  # Call visualization function with selections
  fig = visualize_monthly_top_songs.visualize_monthly_top_songs(selected_month_index + 1, selected_year, data_dir)
  st.plotly_chart(fig)  # Display the figure using Streamlit
else:
  st.error("Invalid view selection.")