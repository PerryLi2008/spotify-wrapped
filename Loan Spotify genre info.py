import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Create sample data for the bar charts
df = pd.read_json('./data/StreamingHistory0_NEW.json')

# Connect to Spotify API
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

# Add new "genre" column
df['genre'] = [[] for _ in range(len(df))]

# Since Spotify API doesn't like too many request at once,
# Slice df into 3 chunks and process one at a time
n = 2700  #chunk row size
list_df = [df[i:i+n] for i in range(0, len(df), n)]

# Request genre info from API through artistName
for work_df in list_df:
    for index, row in work_df.iterrows():
        artist_name = row['artistName']
        results = spotify.search(q=artist_name, type='artist')
        
        if results['artists']['items']:
            genres = results['artists']['items'][0]['genres']
            work_df.at[index, 'genre'] = genres
        else:
            work_df.at[index, 'genre'] = ['Not found']

# Put chunks back together
df = pd.concat(list_df)

# Data cleaning for genre data
def fill_null(x):
    if len(x) == 0: 
        return ['Not found']
    else: 
        return x
    
df['genre'] = df['genre'].apply(fill_null).apply(lambda x: x[0])

# %%
# Export data to json file
df.to_json('./data/StreamingHistory0_final.json', orient='records')
