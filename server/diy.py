import requests
import spotipy
import re
from download import Download
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from dotenv import load_dotenv
import os

load_dotenv('../client/.env')
client_id = os.getenv('REACT_APP_CLIENT_ID')
client_secret = os.getenv('REACT_APP_CLIENT_SECRET')
redirect_uri = os.getenv('REACT_APP_REDIRECT_URI')

scope = ['playlist-read-private', 'playlist-read-collaborative','user-read-private','user-library-read']
username = 'ed582'

token = util.prompt_for_user_token(username, scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
sp = spotipy.Spotify(auth=token)

playlist_location = 'downloads/spotifyDownloadedSongs'
downloader = Download()

def get_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def get_playlist_name(playlist_id):
    playlist = sp.playlist(playlist_id)
    return playlist['name']

def download_playlist(playlist_id):
    tracks = get_playlist_tracks(playlist_id)
    playlist_name = get_playlist_name(playlist_id)
    for track in tracks:
        track_name = re.sub('[^a-zA-Z0-9 ]', '', track['track']['name'])
        track_id = track['track']['id']
        artist_details = track['track']['artists']
        artist_names = []

        for artist in artist_details:
            artist_names.append(artist['name'])

        photo_url = track['track']['album']['images'][0]['url']
        track_location = f'{playlist_location}/{playlist_name}'

        downloader.download_track(track_name, artist_names, photo_url, track_location)

if __name__ == '__main__':
    download_playlist('1TrAc56xVfca83PV7UDWTE')