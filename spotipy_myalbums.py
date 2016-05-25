# Script for getting playlists, which are stupidly inaccessible from the webapp.

import os

os.environ['SPOTIPY_CLIENT_ID'] = 'Get this value from https://developer.spotify.com/my-applications/#!/applications'
os.environ['SPOTIPY_CLIENT_SECRET'] = 'https://developer.spotify.com/my-applications/#!/applications'
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:888/callback'

from spotipy.oauth2 import SpotifyClientCredentials
import sys

import spotipy
import spotipy.util as util
import json

username = 'username (should be a long number in decimal)'

scope = 'user-top-read'
token = util.prompt_for_user_token(username)

def show_tracks(tracks):
    curalbum = ''
    for i, item in enumerate(tracks['items']):
        track = item['track']
        if track['album']['name'] != curalbum:
            curalbum = track['album']['name']
            print("   %d %40.40s %s" % (i, track['artists'][0]['name'],
                                        curalbum))

if token:
    sp = spotipy.Spotify(auth=token)
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
        if playlist['owner']['id'] == username:
            print
            print(playlist['name'])
            print('  total tracks', playlist['tracks']['total'])
            results = sp.user_playlist(username, playlist['id'],
                                       fields="tracks,next")
            tracks = results['tracks']
            show_tracks(tracks)
            while tracks['next']:
                tracks = sp.next(tracks)
                show_tracks(tracks)
else:
    print("Can't get token for", username)

