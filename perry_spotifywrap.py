# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 17:03:16 2023

@author: avery
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# Set the title of the app
st.title("Bar Chart Visualization")


# Create sample data for the bar charts

df = pd.read_json('StreamingHistory0_NEW.json')


col1, col2  = st.columns(2)

# Create the first bar chart
with col1: 
    st.subheader("Top Artists")
    # num_artists_listened = df['artistName'].value_counts().reset_index()
    # num_artists_listened = num_artists_listened.rename(columns={'index': 'Artist', 'artistName': 'Count'}).head(10)
    fig1, ax1 = plt.subplots()
    # ax1.barh( num_artists_listened['Artist'], num_artists_listened['Count'])
    plt.xlabel('# of Times Played')
    plt.ylabel('Artists')
    plt.title('Top Artists')
    st.pyplot(fig1)

# Create the second bar chart
with col2: 
    st.subheader("Top Songs")
    # num_songs_listened = df['trackName'].value_counts().reset_index().rename(columns={'index': 'Track', 'trackName': 'Count'}).head(25)
    fig2, ax2 = plt.subplots()
    # ax2.barh(num_songs_listened['Track'], num_songs_listened['Count'])
    plt.xlabel('# of Times Played')
    plt.ylabel('Songs')
    plt.title('Top Songs')
    st.pyplot(fig2)