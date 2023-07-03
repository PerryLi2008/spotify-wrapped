import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
from PIL import Image
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import timedelta, datetime

st.set_page_config(layout="wide")

# Set the title of the app
st.title("Spotify Wrapped for Perry")
st.write("October 2022 - June 2023")
# color_purple = st.color_picker('purple', '#6806bf', label_visibility='hidden')
# color_orange = st.color_picker('orange', '#f78b00')
# color_yellow = st.color_picker('yellow', '#f2ff2b')
# color_pink = st.color_picker('pink', '#ee74c5')

# st.header(""":pink[ Spotify ] :orange[Wrapped] :yellow[for] :purple[Perry]""")

# Create sample data for the bar charts
df = pd.read_json('./data/StreamingHistory0 final.json')

# Connect to Spotify API
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

# Get Top artists
num_artists_listened = df['artistName'].value_counts().to_frame()
num_artists_listened = num_artists_listened.reset_index(names='Artist').head(10)

# Get Top songs
num_songs_listened = df['trackName'].value_counts().to_frame()
num_songs_listened = num_songs_listened.reset_index(names='Track').head(15)

# Get Top genres
num_genres_listened = df['genre'].value_counts().to_frame()
num_genres_listened = num_genres_listened.reset_index(names='Genre').iloc[1:11]

# Get Most Dancibility list
unique_trackName = df['trackName'].unique()
danceability_scores = pd.DataFrame(unique_trackName, columns=['trackName'])
danceability_scores['danceability'] = 0.0

for index, row in danceability_scores.iterrows():
    track_name = row['trackName']
    danceability_num = df['danceability'][df['trackName'] == track_name].values[0]
    danceability_scores.at[index, 'danceability'] = danceability_num

# Get hour. Since Spotify uses UTC time to generate dump file
# There're 4 hours difference between UTC and EDT, has to convert for hour
df['datetime'] = pd.to_datetime(df['endTime']).apply(lambda dt: dt - timedelta(hours=4))
df['Hour'] = df['datetime'].dt.hour

# Plot Top artist and Top Song
col1, col2 = st.columns(2)

# Create the first bar chart
with col1: 
    st.subheader("Top Artist")
    top_artist = num_artists_listened.loc[0, 'Artist']
    artist_count = num_artists_listened.loc[0, 'count']
   
    # st.subheader(top_artist)
    
    # Get url of artist's image
    image1 = Image.open(f"./images/{top_artist}.jpg")
    # results = spotify.search(top_artist, type='artist')
    # url = results['artists']['items'][0]['images'][0]['url']
    # image1 = Image.open(urlopen(url))
    image1 = image1.resize((300, 300))
    st.image(image1, use_column_width=False)
    st.text(f"Your top artist was \n{top_artist}.")
    st.text(f"You listened {str(artist_count)} times of his song.")
    
# Create the second bar chart
with col2: 
    st.subheader("Top Song")
    top_song = num_songs_listened.loc[0, 'Track']
    song_count = num_songs_listened.loc[0, 'count']

    # st.subheader(top_song)

    # Get url of album's image
    image2 = Image.open(f"./images/{top_song}.jpg")
    # results = spotify.search(top_song, type='track')
    # url = results['tracks']['items'][0]['album']['images'][0]['url']
    # image2 = Image.open(urlopen(url))
    image2 = image2.resize((300, 300))
    st.image(image2, use_column_width=False)
    st.text(f"Your top song was {top_song}.\n")
    st.text(f"You played it {str(song_count)} times this year.")

# Plot Top artists list and Top songs list
col3, col4  = st.columns(2)

# Create the first bar chart
with col3: 
    st.subheader("Top Artists")
    num_artists_listened = num_artists_listened.sort_values('count')

    # fig1, ax1 = plt.subplots()
    # ax1.barh(num_artists_listened['Artist'], num_artists_listened['count'])
    # plt.xlabel('# of Times Played')
    # plt.ylabel('Artists')
    # plt.title('Top Artists')
    # st.pyplot(fig1)

    # Create a color gradient based on the size of x-axis values
    colorscale = [[0, '#8b08fd'], [1, '#6806bd']]
    hover_template = "User played %{y}'s songs %{x} times"

    fig_bar1 = go.Figure()    
    fig_bar1.add_trace(go.Bar(
        x=num_artists_listened['count'],
        y=num_artists_listened['Artist'],
        orientation='h',
        marker=dict(
        color=num_artists_listened['count'],
        colorscale=colorscale,
        showscale=False
        ),
        hovertemplate=hover_template
    ))

    fig_bar1.update_layout(
        xaxis_title='# of Times Played',
        yaxis_title='Artists'
    )

    st.plotly_chart(fig_bar1, use_container_width=True)

# Create the second bar chart
with col4: 
    st.subheader("Top Songs")
    num_songs_listened = num_songs_listened.sort_values(by='count')
    num_songs_listened['Track'] = num_songs_listened['Track'].str.slice(0,30)

    # fig2, ax2 = plt.subplots()
    # ax2.barh(num_songs_listened['Track'], num_songs_listened['count'])
    # plt.xlabel('# of Times Played')
    # plt.ylabel('Songs')
    # plt.title('Top Songs')
    # st.pyplot(fig2)

    # Create a color gradient based on the size of x-axis values
    colorscale = [[0, '#fc9b39'], [1, '#bc732b']]
    hover_template = "User played %{y} %{x} times"

    fig_bar2 = go.Figure()    
    fig_bar2.add_trace(go.Bar(
        x=num_songs_listened['count'],
        y=num_songs_listened['Track'],
        orientation='h',
        marker=dict(
        color=num_songs_listened['count'],
        colorscale=colorscale,
        showscale=False
        ),
        hovertemplate=hover_template
    ))

    fig_bar2.update_layout(
        xaxis_title='# of Times Played',
        yaxis_title='Songs'
    )

    st.plotly_chart(fig_bar2, use_container_width=True)

# Plot Listening by Time of Day and Track Length Distribution
col5, col6  = st.columns(2)

# Create radar chart for Listening by Time of Day
with col5:
    # Plot count by hour
    num_listens_by_hour = df['Hour'].value_counts().to_frame().reset_index()
    num_listens_by_hour = num_listens_by_hour.sort_values(by='Hour')
    fig_line = px.area(num_listens_by_hour, x='Hour', y='count')

    def angle2hr(angle):
        return (((angle - 15) % 360) + 15) / 15

    def hr2angle(hr):
        return (hr * 15) % 360

    def hr_str(hr):
        # Normalize hr to be between 1 and 12
        hr_str = str(((hr-1) % 12) + 1)
        suffix = ' AM' if (hr % 24) < 12 else ' PM'
        return hr_str + suffix

    thetas = [hr2angle(i) for i in num_listens_by_hour['Hour']]
    hover_template = "Play songs %{r} times at %{theta}"
    
    data = [
        go.Scatterpolar(
            r = num_listens_by_hour['count'],
            theta = thetas,
            mode = 'lines',
            marker = dict(
                color = 'peru'
            ),
            hovertemplate=hover_template
        )
    ]

    layout = go.Layout(
        showlegend = False,
        polar_radialaxis_gridcolor="#ffffff", 
        polar_angularaxis_gridcolor="#ffffff"
    )

    layout.polar.angularaxis.direction = 'clockwise'
    layout.polar.angularaxis.tickvals = [hr2angle(hr) for hr in range(24)]
    layout.polar.angularaxis.ticktext = [hr_str(hr) for hr in range(24)]
    fig_radar = go.FigureWidget(data=data, layout=layout)

    st.subheader("Time of Day Listened")
    st.plotly_chart(fig_radar, use_container_width=True)

# Create bar chart for minutes played
with col6:
    st.subheader("Track Length Distribution")
    df['minutesPlayed'] = df['msPlayed']/1000/60

    # Example of create new column based on calculation on another column
    # df['podcast'] = 0
    # df['podcast'][df['minutesPlayed'] > 6] = 1

    # fig_histogram = px.histogram(df, x='minutesPlayed')
    colorscale = [[0, '#54ff68'], [1, '#36a342']]
    hover_template = "Songs with %{x} minutes length were played %{y} times"
    # Compute the total counts for each bin
    counts, bins = np.histogram(df['minutesPlayed'], bins=np.arange(0.0, 20.0, 0.1))

    fig_histogram = go.Figure()
    fig_histogram.add_trace(go.Bar(
        x=bins,
        y=counts,
        marker=dict(
        color=counts,
        colorscale=colorscale,
        showscale=False
        ),
        hovertemplate=hover_template
    ))

    fig_histogram.update_layout(
        xaxis_title='Track Minutes Played',
        yaxis_title='Counts'
    )

    st.plotly_chart(fig_histogram)

# Plot Top Genres and Most Danceability
col7, col8  = st.columns(2)

# # Create Top Genres list
with col7:
    st.subheader("Top Genres")
    num_genres_listened = num_genres_listened.sort_values(by='count')

    # fig3, ax3 = plt.subplots()
    # ax3.barh(num_genres_listened['Genre'], num_genres_listened['count'])
    # plt.xlabel('# of Times Played')
    # plt.ylabel('Genres')
    # st.pyplot(fig3)

        # Create a color gradient based on the size of x-axis values
    colorscale = [[0, '#fe7bd2'], [1, '#c35ea1']]
    hover_template = "User played %{y} songs %{x} times"

    fig_bar3 = go.Figure()    
    fig_bar3.add_trace(go.Bar(
        x=num_genres_listened['count'],
        y=num_genres_listened['Genre'],
        orientation='h',
        marker=dict(
        color=num_genres_listened['count'],
        colorscale=colorscale,
        showscale=False
        ),
        hovertemplate=hover_template
    ))

    fig_bar3.update_layout(
        xaxis_title='# of Times Played',
        yaxis_title='Genres'
    )

    st.plotly_chart(fig_bar3, use_container_width=True)

# # Create Most Danceability list
with col8:
    st.subheader("Songs with Most Danceability")
    danceability_scores = danceability_scores.sort_values('danceability', ascending=False).head(15)
    # danceability_scores = danceability_scores.reset_index(drop=True)
    
    # blank_row = pd.DataFrame({}, columns=most_danceability.columns)
    # most_danceability.loc[len(most_danceability)] = ['', np.nan]
    # danceability_scores = pd.concat([most_danceability, least_danceability], ignore_index=True)

    # fig4, ax4 = plt.subplots()
    # ax4.barh(most_danceability['trackName'], most_danceability['danceability'])
    # ax4.invert_yaxis()
    # plt.xlabel('Danceability score')
    # plt.ylabel('Songs')
    # st.pyplot(fig4, use_container_width=True)

    colorscale = [[0, '#f2ff2e'], [1, '#dee82a']]
    hover_template = "%{y}'s danceability score is %{x}"

    fig_bar4 = go.Figure()    
    fig_bar4.add_trace(go.Bar(
        x=danceability_scores['danceability'],
        y=danceability_scores['trackName'],
        orientation='h',
        marker=dict(
        color=danceability_scores['danceability'],
        colorscale=colorscale,
        showscale=False
        ),
        hovertemplate=hover_template
    ))

    fig_bar4.update_layout(
        yaxis=dict(autorange="reversed"),
        xaxis_title='Danceability score',
        yaxis_title='Songs'
    )

    st.plotly_chart(fig_bar4, use_container_width=True)