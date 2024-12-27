import streamlit as st
import pandas as pd
import plotly.express as px
import os

def visualize_yearly_top_songs(year, data_dir):
    """
    Visualizes the top songs for a given month and year.

    Args:
        year (int): Year.
        data_dir (str): Path to the directory containing monthly top songs data.

    Returns:
        None
    """

    filename = f"top_89_songs_{year}.csv"  # Pad month with zero
    filepath = os.path.join(data_dir, filename)

    try:
        df = pd.read_csv(filepath)
        df = df.sort_values(by=['count'], ascending=False)

        fig = px.bar(df.head(20), x="count", y="song", 
                    orientation='h', 
                    labels={"song": "Song", "count": "Play Count"}, 
                    title=f"Top Songs Played in {year}")
        
        # Update layout
        fig.update_layout(
            width=800, height=600,
            yaxis={'autorange': "reversed"}  # Reverse the y-axis 
        )

        return fig

    except FileNotFoundError:
        st.error(f"Data for {year} not found.")
