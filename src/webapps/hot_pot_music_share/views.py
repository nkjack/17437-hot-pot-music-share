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



## youtube search

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
DEVELOPER_KEY = 'AIzaSyC6zJT9fu29Wj6T67uRxfnQvc9kyP4wz3Y'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def search_room(request):
    context = {}
    return render(request, 'hot_pot_music_share/youtube/room.html', context)

def search_song(request):
    context = {}
    query = request.GET['query']
    max_results = 10
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        maxResults=max_results,
        type='video',
        videoCategoryId='10', # only songs!
    ).execute()

    videos = {}

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos[search_result['id']['videoId']] = search_result['snippet']['title']


    # room = Room.objects.get(id=room_id) # FIXME: Who to set user_manager to?
    # playlist_obj = Playlist.objects.get(belongs_to_room=room)

    # pprint.pprint(result)


    context['search_results'] = videos
    return render(request, 'hot_pot_music_share/youtube/room.html', context)


def add_song_to_room_playlist(request):
    context = {}
    # user = User.objects.get(username=request.user)
    # room_id = request.POST['room_id']
    searched_song_id = request.POST['song_id']
    searched_song_name = request.POST['song_name']

    if not User.objects.filter(exact__username="noam"):
        u = User.objects.create(username="noam")
        u.save()

    if not Room.objects.filter(exact__name="noam_room"):
        u = User.objects.get(username="noam")
        r = Room.objects.create(user_manager=u, name="noam_room")
        r.save()
        p = Playlist.objects.create(belongs_to_room=r)
        p.save()


    # room = Room.objects.get(id=room_id)
    r = Room.objects.get(name="noam_room")
    p = Playlist.objects.get(belongs_to_room=r)

    s = Song(song_id=searched_song_id, song_name=searched_song_name)
    s.save()

    p.songs.add(s)

    # context['room'] = room
    context['playlist'] = p
    # context['user'] = user
    return render(request, 'hot_pot_music_share/spotify/spotify-room.html', context)

def play_song(request):
    # user = User.objects.get(username='nkjack84')
    # sp = spotipy.Spotify(auth=user.profile.spotify_get_token())
    # sp.start_playback(device_id='1171ce229321475f1c5729dfcc56265ca787d51b', uris=['spotify:track:' + request.GET['spotify-song']])

    return HttpResponse('')

def base_map(request):
    context = {}
    all_markers = Marker.objects.all()
    context['all_markers'] = all_markers
    return render(request, 'hot_pot_music_share/maps/base_map.html', context)

from hot_pot_music_share.forms import *
from django.http import Http404
from django.http import JsonResponse

def add_marker(request):
    context = {}
    form = MarkerForm(request.POST)
    if not form.is_valid():
        print (form.errors)
        raise Http404

    form.save()
    all_markers = Marker.objects.all()
    print (all_markers)
    context['all_markers'] = all_markers
    return JsonResponse(data={})
    # return render(request, 'hot_pot_music_share/maps/base_map.html', context)

# @login_required
# @transaction.atomic
def get_markers(request):
    all_markers = Marker.objects.all()
    context = {'markers': all_markers}

    return render(request, 'hot_pot_music_share/maps/markers.json', context, content_type='application/json')