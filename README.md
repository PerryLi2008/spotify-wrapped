# **Spotify Wrapped for 2022**
## Background
Every year, Spotify sends a personalized report to each user called “Spotify Wrapped.” It’s called “Wrapped” since it’s a little holiday gift to you. It’s a fun, well-designed summary of what the user listens to throughout the year. It’s really fun & interesting which leads to people sharing with family & friends.  
This is great marketing for Spotify. Thousands of people saying the word “Spotify” & honestly, those that don’t have Spotify feel a little left out. Hence, this analytics report is worth a lot of Spotify!  
[Here's an example on youtube.](https://youtu.be/KknMSXE3a-c?t=58).  
## Project scope
This project is to create my own version of Spotify Wrapped.  
The project is implemented in several steps:  
1. [Request a download dump from Spotify.](https://www.spotify.com/us/account/privacy/) It takes a few days to get dump from Spotify in json format.
2. Create an interactive dashboard / web application using Streamlit in Python.
3. Link streamlit app with [Spotify API](https://developer.spotify.com/documentation/web-api) data to obtain genres and audio features endpoint using [Python parckage Spotipy](https://spotipy.readthedocs.io/en/2.22.1/).  
## Streamlit Web app
[2022 Spotify Wrapped for Perry report can be accessed through this link.](https://spotify-wrapped.streamlit.app/)
Web page consists of 4 sections:
### Section 1: Show favorite Artist & Song user listened most during 2022.
### Section 2: Top 10 Artists listened and artists streamed most in bar charts.
### Section 3: Top 10 Songs listened and songs streamed most in bar charts.
### Section 4: Two interactive charts.  
First one is radar chart, displays how many time user listened to Spotify during time of day.  
If you hover over any point of brown line, exact time and how many times listened will be displayed.  
Another histogram shows distribution of length of time spend on Spotify. Again, hover over will display details.
### Section 4: Top Genres listened and Songs with most Danceability in bar charts.
Through Spotify API calls, Genres info and Danceability audio features were obtained and added back to json file. Seperate python program was used since it takes quite long time to complete thousands of api queries. 
### Section 5: Top 10 Genres and songs with most danceability.
Note: Charts use similar color series as Spotify wrapped. More details will show when hover mouse over charts.