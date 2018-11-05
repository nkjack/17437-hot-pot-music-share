import json
import os
from json import JSONDecodeError
from django.contrib.auth.models import User

import spotipy
import spotipy.util as util
from django.contrib.auth.models import User
from django.http import HttpResponse

from hot_pot_music_share import models
from django.shortcuts import render

from hot_pot_music_share.models import Room, Playlist, Song

SPOTIPY_CLIENT_ID = '04fb29de4495438aa354af4a57fd47a4'
SPOTIPY_CLIENT_SECRET = '38378c5d52dc467da1feeac2f53cc6fc'
SCOPE = 'user-read-private user-read-playback-state user-modify-playback-state' + \
        ' streaming user-read-birthdate user-read-email user-read-private' # Needed for web playback SDK
WEB_PLAYBACK_TOKEN = 'BQA6z3s0KVEriyG89oB5UMI9g3p7ldOeMyN6aEMBqOFNZKkI7Hgfkhn1o4cGl13UwkoHiYW4kg3vgZGmexv4KCU_u9c2JrA6hSawyuAJ_QlxOJkMW4fR7pB5sTyDWUv4Hsm59W60w8RJaepgbeMPNPLi_kLJVYWMl3YN'


# Home view
def home(request):
    return render(request, 'hot_pot_music_share/home.html')

# Integrate actual Profile model later
def login(request):
    return render(request, 'hot_pot_music_share/login.html')

# SPOTIFY DEMO (STEP 1) - Replacing login for now
def get_spotify_username(request):
    return render(request, 'hot_pot_music_share/spotify/get-spotify-username.html')

# SPOTIFY DEMO (STEP 2) Redirect after successfully authenticating with Spotify
def spotify_post_auth(request):
    username = request.GET['spotify-username']  # FIXME: Catch key error
    print("spotify_post_auth - username: ", username)

    # Get token
    token = spotify_get_token(username)
    print("spotify_post_auth - token: ", token)

    # Create User here, if it doesn't exist
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username=username) # Same username as spotify username for now
        user.profile.spotify_username = username
        user.profile.token = token
        user.save()
    else:
        user = User.objects.get(username=username)

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

    return render(request, 'hot_pot_music_share/spotify/spotify-post-auth.html', context)

# SPOTIFY DEMO (STEP 3) - Create a simple room
def create_demo_room(request):
    room_name = request.GET['room-name']  # FIXME: Catch key error

    # Create the room
    room = Room(name=room_name, user_manager=User.objects.get(username='sampromises')) # FIXME: Who to set user_manager to?
    room.save()

    # Create the playlist
    playlist_obj = Playlist(belongs_to_room=room)
    playlist_obj.save()

    # Create a single song
    song1 = Song(song_id='66kQ7wr4d22LwwSjr7HXcyr', song_name='All The Stars', belongs_to_room=room)
    song2 = Song(song_id='6TaqooOXAEcijL6G1AWS2K', song_name='All My Friends', belongs_to_room=room)
    song1.save()
    song2.save()

    playlist_obj.songs.add(song1)
    playlist_obj.songs.add(song2)

    # Debug set just one song
    # one_song = ['66kQ7wr4d2LwwSjr7HXcyr']
    # playlist_obj.set_songs(one_song)
    # playlist_obj.songs.Objects

    token = spotify_get_token('sampromises')

    # TODO: Create an empty room
    return render(request, 'hot_pot_music_share/spotify/spotify-room.html',
                  {'room':room, 'playlist':playlist_obj,
                   'song_id':'66kQ7wr4d22LwwSjr7HXcyr',
                   'token':token})

def get_search_results(request):
    # TODO: Fill in code here to return search results
    return render()



# Simple callback after Spotify authentication is done
def spotify_callback(request):
    context = {'code': request.GET['code']}
    return render(request, 'hot_pot_music_share/spotify/spotify-callback.html', context)

def spotify_web_playback(request):
    return render(request, 'hot_pot_music_share/spotify/spotify-web-playback.html')

### HELPER FUNCTIONS

# Get a Spotify auth token
def spotify_get_token(username):
    # Erase cache and prompt for user permission
    try:
        token = util.prompt_for_user_token(username=username,
                                           scope=SCOPE,
                                           client_id=SPOTIPY_CLIENT_ID,
                                           client_secret=SPOTIPY_CLIENT_SECRET,
                                           redirect_uri='http://localhost:8000/spotify-callback')  # add scope
    except (AttributeError, JSONDecodeError):  # If reading from cache went bad
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username=username,
                                           scope=SCOPE,
                                           client_id=SPOTIPY_CLIENT_ID,
                                           client_secret=SPOTIPY_CLIENT_SECRET,
                                           redirect_uri='http://localhost:8000/spotify-callback')  # add scope

    print(token)
    return token

def spotify_play_song(request, song_id, offset=None):
    # Get token
    token = spotify_get_token('sampromises')

    # Create our spotify object with permissions
    spotify = spotipy.Spotify(auth=token)

    print("DEVICES: ", spotify.devices())

    # Change playback
    spotify.start_playback(device_id='bab9a49eb64e01a2467bda4486315865c3754ff3',
                           uris=['spotify:track:'+song_id], offset=offset)

    # Empty response
    return HttpResponse('')


# Transfer Spotify playback to specified device ID
def spotify_transfer_playback(request, device_id, username='sampromises'):
    # Get token
    token = spotify_get_token(username)

    # Create our spotify object with permissions
    spotify = spotipy.Spotify(auth=token)

    # Get current device
    spotify.transfer_playback(device_id, force_play=True)
    print(device_id)

    # Empty response
    return HttpResponse('')


