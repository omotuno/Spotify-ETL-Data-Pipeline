# Importing the libraries
import json
import os
import spotipy
import boto3
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime
# import pandas as pd

def lambda_handler(event, context):
    # spotify client ID and secret client ID
    client_id= os.environ.get('client_id')
    client_secret= os.environ.get('client_secret')
    
    
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    # authentication and authorization for spotify
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    
    
    playlist_link = "https://open.spotify.com/playlist/6nvDix6ABiGTqZghg4qaHs"
    # Extracting the playlist ID from the playlist uri 
    playlist_URI= playlist_link.split("/")[-1]
    
    
    # extracting the json data and saving it in data variable
    data = sp.playlist_tracks(playlist_URI)
    
    filename= "spotify_raw_" + str(datetime.now()) + ".json"
    
    client=boto3.client('s3')
    client.put_object(
       Bucket="spotify-etl-project-olusegun",
       Key="raw_data/to_processed/" + filename,
       Body=json.dumps(data)
       )