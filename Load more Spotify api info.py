import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Create sample data for the bar charts
df = pd.read_json('./data/StreamingHistory0_NEW final - genre only.json')

# Connect to Spotify API
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

# Add new "genre" column
# df['genre'] = [[] for _ in range(len(df))]
# df['genre'] = ''
df['danceability'] = 0.0

# Since Spotify API doesn't like too many request at once,
# Slice df into 3 chunks and process one at a time
n = 2700  #chunk row size
list_df = [df[i:i+n] for i in range(0, len(df), n)]
# list_df = [df[0:10], df[10:20], df[20:30]]

# Request genre/danceability info from API through artistName
for work_df in list_df:
    # Request genre info
    # for index, row in work_df.iterrows():
    #     artist_name = row['artistName']
    #     results = spotify.search(q=artist_name, type='artist')
        
    #     if results['artists']['items']:
    #         if results['artists']['items'][0]['genres']:
    #             genres = results['artists']['items'][0]['genres'][0]
    #             work_df.at[index, 'genre'] = genres
    #         else:
    #             work_df.at[index, 'genre'] = 'Not found'
    #     else:
    #         work_df.at[index, 'genre'] = 'Not found'

    # Request danceability info
    for index, row in work_df.iterrows():
        track_name = row['trackName']
        results = spotify.search(track_name, type='track')
        
        if results['tracks']['items']:
            track_id = results['tracks']['items'][0]['id']
            audio_features = spotify.audio_features(track_id)
            if audio_features[0]:
                work_df.at[index, 'danceability'] = audio_features[0]['danceability']

# Put chunks back together
df_final = pd.concat(list_df)

# Data cleaning for genre data
# def fill_null(x):
#     if len(x) == 0: 
#         return 'Not found'
#     else: 
#         return x[0]
# df['genre'] = df['genre'].apply(fill_null)

# Export data to json file
df_final.to_json('./data/StreamingHistory0_NEW final.json', orient='records')

# Request danceability info from API through trackName
# track_name = 'Cold As You'
# results = spotify.search(track_name, type='track')
# track_id = results['tracks']['items'][0]['id']

# audio_features = spotify.audio_features(track_id)
# test = audio_features[0]['danceability']


# work_df = df[0:20]
# list_df = [df[0:20], df[20:40], df[40:60]]

# for work_df in list_df:
#     for index, row in work_df.iterrows():
#         track_name = row['trackName']
#         results = spotify.search(track_name, type='track')
        
#         if results['tracks']['items']:
#             track_id = results['tracks']['items'][0]['id']
#             audio_features = spotify.audio_features(track_id)
#             work_df.at[index, 'danceability'] = audio_features[0]['danceability']

# Request genre info
# for index, row in work_df.iterrows():
#     artist_name = row['artistName']
#     results = spotify.search(q=artist_name, type='artist')
    
#     if results['artists']['items'][0]['genres']:
#         genres = results['artists']['items'][0]['genres'][0]
#         work_df.at[index, 'genre'] = genres
#     else:
#         work_df.at[index, 'genre'] = 'Not found'

# artist_name = 'The Joe Rogan Experience'
# results = spotify.search(artist_name, type='artist')
# genres = results['artists']['items'][0]['genres'][0]