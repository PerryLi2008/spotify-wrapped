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
st.title("2022 Spotify Wrapped")


# Create sample data for the bar charts
df = pd.read_json('StreamingHistory0_NEW.json')

# Get Top artists
num_artists_listened = df['artistName'].value_counts()
num_artists_listened = pd.DataFrame(num_artists_listened)
num_artists_listened.reset_index(names='Artist', inplace=True)
# num_artists_listened = num_artists_listened.rename(columns={'artistName': 'Count'}).head(10)
num_artists_listened = num_artists_listened.head(10)

# Get Top songs
num_songs_listened = df['trackName'].value_counts()
# num_songs_listened = df['trackName'].value_counts().reset_index().rename(columns={'index': 'Track', 'trackName': 'Count'}).head(25)
num_songs_listened = pd.DataFrame(num_songs_listened)
num_songs_listened.reset_index(names='Track', inplace=True)
num_songs_listened = num_songs_listened.head(20)
# num_songs_listened = num_songs_listened.rename(columns={'index': 'Track', 'trackName': 'Count'}).head(25)


col1, col2 = st.columns(2)

# Create the first bar chart
with col1: 
    st.header("Top Artist")
    top_artist = num_artists_listened.loc[0, 'Artist']
    artist_count = num_artists_listened.loc[0, 'count']
   
    # # num_artists_listened.rename(columns={'index': 'Artist', 'artistName': 'Count'}, inplace=True)
    # top_artist = num_artists_listened.loc[0, ['index']].iloc[0]
    # artist_count = num_artists_listened.loc[0, ['artistName']].iloc[0]
    # # artist_col1 = top_artist.iloc[0]
    st.subheader(top_artist)
    st.image("./images/" + top_artist + ' new.jpg')
    st.text("Your top artist was " + top_artist)
    st.text("You listened " + str(artist_count) + " times of his song this year.")
    
   
# Create the second bar chart
with col2: 
    st.header("Top Song")
    top_song = num_songs_listened.loc[0, 'Track']
    song_count = num_songs_listened.loc[0, 'count']

    # top_song = num_songs_listened.loc[0,['index']].iloc[0]
    # song_counts = num_songs_listened.loc[0,['trackName']].iloc[0]
    st.subheader(top_song)
    st.image("./images/" + top_song + 'new.jpg')
    st.text("Your top song was " + top_song + " by " + top_artist)
    st.text("You played it " + str(song_count) + " times.")

# st.title("Lower section")

col3, col4  = st.columns(2)

# Create the first bar chart
with col3: 
    st.header("Top Artists")
    # num_artists_listened = df['artistName'].value_counts().reset_index()
    fig1, ax1 = plt.subplots()
    ax1.barh(num_artists_listened['Artist'], num_artists_listened['count'])
    plt.xlabel('# of Times Played')
    plt.ylabel('Artists')
    plt.title('Top Artists')
    st.pyplot(fig1)


# Create the second bar chart
with col4: 
    st.header("Top Songs")

    fig2, ax2 = plt.subplots()
    ax2.barh(num_songs_listened['Track'], num_songs_listened['count'])
    plt.xlabel('# of Times Played')
    plt.ylabel('Songs')
    plt.title('Top Songs')
    st.pyplot(fig2)