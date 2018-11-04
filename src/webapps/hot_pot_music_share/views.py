import os
from json import JSONDecodeError
from django.contrib.auth.models import User

import spotipy
import spotipy.util as util
from django.shortcuts import render


SPOTIPY_CLIENT_ID = '04fb29de4495438aa354af4a57fd47a4'
SPOTIPY_CLIENT_SECRET = '38378c5d52dc467da1feeac2f53cc6fc'
SCOPE = 'user-read-private user-read-playback-state user-modify-playback-state' + \
        ' streaming user-read-birthdate user-read-email user-read-private' # Needed for web playback SDK
WEB_PLAYBACK_TOKEN = 'BQA6z3s0KVEriyG89oB5UMI9g3p7ldOeMyN6aEMBqOFNZKkI7Hgfkhn1o4cGl13UwkoHiYW4kg3vgZGmexv4KCU_u9c2JrA6hSawyuAJ_QlxOJkMW4fR7pB5sTyDWUv4Hsm59W60w8RJaepgbeMPNPLi_kLJVYWMl3YN'


# Home view
def home(request):
    return render(request, 'hot_pot_music_share/home.html')

def login(request):
    return render(request, 'hot_pot_music_share/login.html')

# TODO: JUST TO KEEP WORKING
def get_spotify_username(request):
    return render(request, 'hot_pot_music_share/get-spotify-username.html')

# Begin spotify authentication
def spotify_auth(request):
    username = request.GET['spotify-username']  # FIXME: Catch key error

    # Get token
    token = spotify_get_token(username)

    # Create our spotify object with permissions
    spotify = spotipy.Spotify(auth=token)

    # Get current device
    devices = spotify.devices()
    if len(devices['devices']) > 0:
        deviceID = devices['devices'][0]['id']

    # Current track information
    track = spotify.current_user_playing_track()
    currently_playing = None
    if track is not None:
        artist = track['item']['artists'][0]['name']
        track = track['item']['name']

        if artist != "":
            currently_playing = "Currently playing " + artist + " - " + track

    # User information
    user = spotify.current_user()
    displayName = user['display_name']
    followers = user['followers']['total']

    # Get user playlists
    user_playlists = []
    searchResults = spotify.current_user_playlists()
    for searchResult in searchResults['items']:
        user_playlists.append((searchResult['name'], searchResult['id']))

    context = {'username':displayName, 'currently_playing':currently_playing, 'user_playlists':user_playlists}
    return render(request, 'spotify-user-playlists.html', context)

# Simple callback after Spotify authentication is done
def spotify_callback(request):
    context = {'code': request.GET['code']}
    new_user = User.objects.create_user(username="noam", \
                                        password="pass",
                                        first_name="noam",
                                        last_name="kahan",
                                        email="n@gmail.com")
    new_user.profile.spotify_id = 1111
    return render(request, 'spotify-callback.html', context)

def spotify_web_playback(request):
    return render(request, 'spotify-web-playback.html')

### HELPER FUNCTIONS

# Get a Spotify auth token
def spotify_get_token(username):
    # Erase cache and prompt for user permission
    try:
        token = util.prompt_for_user_token(username,
                                           scope=SCOPE,
                                           client_id=SPOTIPY_CLIENT_ID,
                                           client_secret=SPOTIPY_CLIENT_SECRET,
                                           redirect_uri='http://localhost:8000/spotify-callback/')  # add scope
    except (AttributeError, JSONDecodeError):  # If reading from cache went bad
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username,
                                           scope=SCOPE,
                                           client_id=SPOTIPY_CLIENT_ID,
                                           client_secret=SPOTIPY_CLIENT_SECRET,
                                           redirect_uri='http://localhost:8000/spotify-callback/')  # add scope

    return token

# Transfer Spotify playback to specified device ID
def spotify_transfer_playback(device_id, username='sampromises'):
    # Get token
    token = spotify_get_token(username)

    # Create our spotify object with permissions
    spotify = spotipy.Spotify(auth=token)

    # Get current device
    spotify.transfer_playback(device_id, force_play=True)




