import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
from PIL import Image
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

st.set_page_config(layout="wide")

# Set the title of the app
st.title("2022 Spotify Wrapped for Perry")

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
most_danceability = pd.DataFrame(unique_trackName, columns=['trackName'])
most_danceability['danceability'] = 0.0

for index, row in most_danceability.iterrows():
    track_name = row['trackName']
    danceability_num = df['danceability'][df['trackName'] == track_name].values[0]
    most_danceability.at[index, 'danceability'] = danceability_num

# Get hour
df['datetime'] = pd.to_datetime(df['endTime'])
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
    st.text("Your top artist was \n" + top_artist)
    st.text(f"You listened {str(artist_count)} times of his song this year.")
    
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
    st.text(f"Your top song was {top_song} by \n{top_artist}")
    st.text(f"You played it {str(song_count)} times.")

# Plot Top artists list and Top songs list
col3, col4  = st.columns(2)

# Create the first bar chart
with col3: 
    st.subheader("Top Artists")
    num_artists_listened = num_artists_listened.sort_values(by='count')

    fig1, ax1 = plt.subplots()
    ax1.barh(num_artists_listened['Artist'], num_artists_listened['count'])
    plt.xlabel('# of Times Played')
    plt.ylabel('Artists')
    plt.title('Top Artists')
    st.pyplot(fig1)


# Create the second bar chart
with col4: 
    st.subheader("Top Songs")
    num_songs_listened = num_songs_listened.sort_values(by='count')
    num_songs_listened['Track'] = num_songs_listened['Track'].str.slice(0,30)

    fig2, ax2 = plt.subplots()
    ax2.barh(num_songs_listened['Track'], num_songs_listened['count'])
    plt.xlabel('# of Times Played')
    plt.ylabel('Songs')
    plt.title('Top Songs')
    st.pyplot(fig2)

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
    data = [
        go.Scatterpolar(
            r = num_listens_by_hour['count'],
            theta = thetas,
            mode = 'lines',
            marker = dict(
                color = 'peru'
            )
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

    fig_histogram = px.histogram(df, x='minutesPlayed')
    st.plotly_chart(fig_histogram)

# Plot Top Genres and Most Danceability
col7, col8  = st.columns(2)

# # Create Top Genres list
with col7:
    st.subheader("Top Genres")
    num_genres_listened = num_genres_listened.sort_values(by='count')

    fig3, ax3 = plt.subplots()
    ax3.barh(num_genres_listened['Genre'], num_genres_listened['count'])
    plt.xlabel('# of Times Played')
    plt.ylabel('Genres')
    st.pyplot(fig3)

# # Create Most Danceability list
with col8:
    st.subheader("Most Danceability list")
    most_danceability = most_danceability.sort_values(by='danceability', ascending=False)
    most_danceability = most_danceability.head(10).reset_index(drop=True)
    
    fig4, ax4 = plt.subplots()
    ax4.barh(most_danceability['trackName'], most_danceability['danceability'])
    ax4.invert_yaxis()
    plt.xlabel('Danceability score')
    plt.ylabel('Songs')
    st.pyplot(fig4, use_container_width=True)