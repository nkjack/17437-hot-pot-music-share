import json
import os
from json import JSONDecodeError
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.http import HttpResponse

from hot_pot_music_share import models
from django.shortcuts import render

from hot_pot_music_share.models import Room, Playlist, Song




# Home view
def home(request):
    return render(request, 'hot_pot_music_share/home.html')

# Integrate actual Profile model later
def login(request):
    return render(request, 'hot_pot_music_share/login.html')

# SPOTIFY DEMO (STEP 3) - Create a simple room
def create_demo_room(request):
    room_name = request.GET['room-name']  # FIXME: Catch key error

    # Create the room
    room = Room(name=room_name, user_manager=User.objects.get(username='nkjack84')) # FIXME: Who to set user_manager to?
    room.save()

    # Create the playlist
    playlist_obj = Playlist(belongs_to_room=room)
    playlist_obj.save()

    # Create a single song
    # song1 = Song(song_id='66kQ7wr4d22LwwSjr7HXcyr', song_name='All The Stars', belongs_to_room=room)
    # song2 = Song(song_id='6TaqooOXAEcijL6G1AWS2K', song_name='All My Friends', belongs_to_room=room)
    # song1.save()
    # song2.save()
    #
    # playlist_obj.songs.add(song1)
    # playlist_obj.songs.add(song2)

    # Debug set just one song
    # one_song = ['66kQ7wr4d2LwwSjr7HXcyr']
    # playlist_obj.set_songs(one_song)
    # playlist_obj.songs.Objects


    # TODO: Create an empty room
    return render(request, 'hot_pot_music_share/spotify/spotify-room.html',
                  {'room':room, 'playlist':playlist_obj,
                   'song_id':'66kQ7wr4d22LwwSjr7HXcyr',
                   'token':token})

## youtube search
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
DEVELOPER_KEY = 'AIzaSyC6zJT9fu29Wj6T67uRxfnQvc9kyP4wz3Y'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def search_song(request, query, max_results=10):
    context = {}

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        maxResults=max_results
    ).execute()

    videos = {}

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos[search_result['id']['videoId']] = search_result['snippet']['title']


    room = Room.objects.get(id=room_id) # FIXME: Who to set user_manager to?
    playlist_obj = Playlist.objects.get(belongs_to_room=room)

    search_song = request.GET['song_name']
    # pprint.pprint(result)


    dic_songs = {}
    for item in items:
        dic_songs[item['id']] = item['name']

    # print(dic_songs)

    context['room'] = room
    context['search_results'] = dic_songs
    context['playlist'] = playlist_obj
    context['user'] = user
    return render(request, 'hot_pot_music_share/spotify/spotify-room.html', context)


def add_song_to_room_playlist(request):
    user = User.objects.get(username='nkjack84')

    context = {}
    room_id = request.POST['room_id']
    searched_song_id = request.POST['song_id']
    searched_song_name = request.POST['song_name']

    room = Room.objects.get(id=room_id) # FIXME: Who to set user_manager to?
    playlist = Playlist.objects.get(belongs_to_room=room)

    song = Song(song_id=searched_song_id, song_name=searched_song_name, belongs_to_room=room)
    song.save()

    playlist.songs.add(song)
    context['room'] = room
    context['playlist'] = playlist
    context['user'] = user
    return render(request, 'hot_pot_music_share/spotify/spotify-room.html', context)

def play_song(request):
    # user = User.objects.get(username='nkjack84')
    # sp = spotipy.Spotify(auth=user.profile.spotify_get_token())
    # sp.start_playback(device_id='1171ce229321475f1c5729dfcc56265ca787d51b', uris=['spotify:track:' + request.GET['spotify-song']])

    return HttpResponse('')

