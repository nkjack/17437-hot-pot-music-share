import json
from mimetypes import guess_type

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
from django.utils.timezone import localtime, now
from googleapiclient.discovery import build

from hot_pot.models import Room, RoomHistory, Playlist, Song

# YouTube API metadata needed for search
DEVELOPER_KEY = 'AIzaSyC6zJT9fu29Wj6T67uRxfnQvc9kyP4wz3Y'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
MAX_SEARCH_RESULTS = 10


@login_required
def room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    room_name = room.name
    is_host = room.owner == request.user
    song_pool = Playlist.objects.get(belongs_to_room=room, pl_type="pool")
    song_queue = Playlist.objects.get(belongs_to_room=room, pl_type="queue")

    # Update user room history if this user has never been to this room
    if not RoomHistory.visitedBefore(request.user, room, localtime(now())):
        history = RoomHistory.objects.create(user=request.user, visited_room=room)
        history.save()
    listeners = RoomHistory.getCurrentListeners(room)

    context = {'username': request.user.username,
               'room_id': room_id,
               'room_name_json': mark_safe(json.dumps(room_name)),
               'title': 'Room ' + room_name,
               'is_host': is_host,
               'song_pool': song_pool.songs.all(),
               'song_queue': song_queue.songs.all(),
               }

    return render(request, 'room_base.html', context)


@login_required
def get_img(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if not room.cover_pic:
        raise Http404
    content_type = guess_type(room.cover_pic.name)
    return HttpResponse(room.cover_pic, content_type=content_type)


def search_song(request):
    context = {}
    query = request.GET['query']
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified query term.
    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        maxResults=MAX_SEARCH_RESULTS,
        type='video',
        videoCategoryId='10',  # only songs!
    ).execute()

    videos = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append(Song(song_id=search_result['id']['videoId'],
                               song_name=search_result['snippet']['title']))

    context['songs'] = videos

    return render(request, 'hot_pot/youtube/songs.json', context, content_type='application/json')


@login_required
@transaction.atomic
def add_song_to_room_playlist_ajax(request):
    context = {}

    room_id = request.POST['room_id']
    searched_song_id = request.POST['song_id']
    searched_song_name = request.POST['song_name']

    room = Room.objects.get(id=room_id)
    song_pool = Playlist.objects.get(belongs_to_room=room, pl_type="pool")

    # Don't create the song if it already exists (TODO: Is this what we want though?)
    if not Song.objects.filter(song_id__exact=searched_song_id):
        song = Song(song_id=searched_song_id, song_name=searched_song_name)
        song.save()

    # Don't add the song if it already exists in the playlist
    song = Song.objects.get(song_id=searched_song_id)
    if not Playlist.objects.filter(songs__song_id__exact=searched_song_id, belongs_to_room=room, pl_type="pool"):
        song_pool.songs.add(song)

    context['songs'] = song_pool.songs.all()
    return render(request, 'hot_pot/youtube/songs.json', context, content_type='application/json')


# Add a single song
@login_required
@transaction.atomic
def add_song_from_pool_to_queue(request):
    context = {}

    room_id = request.POST['room_id']
    searched_song_id = request.POST['song_id']
    searched_song_name = request.POST['song_name']

    room = Room.objects.get(id=room_id)
    song_queue = Playlist.objects.get(belongs_to_room=room, pl_type="queue")

    # Don't create the song if it already exists (TODO: Is this what we want though?)
    if not Song.objects.filter(song_id__exact=searched_song_id):
        song = Song(song_id=searched_song_id, song_name=searched_song_name)
        song.save()

    # Don't add the song if it already exists in the playlist
    song = Song.objects.get(song_id=searched_song_id)
    if not Playlist.objects.filter(songs__song_id__exact=searched_song_id, belongs_to_room=room, pl_type="queue"):
        song_queue.songs.add(song)

    context['songs'] = song_queue.songs.all()
    return render(request, 'hot_pot/youtube/songs.json', context, content_type='application/json')


@login_required
def get_pool_songs_from_room(request):
    context = {}
    room_id = request.GET['room_id']
    room = Room.objects.get(id=room_id)
    song_pool = Playlist.objects.get(belongs_to_room=room, pl_type="pool")
    context['songs'] = song_pool.songs.all()
    return render(request, 'hot_pot/youtube/songs.json', context, content_type='application/json')


@login_required
@transaction.atomic
def get_queue_songs_from_room(request):
    context = {}
    room_id = request.GET['room_id']
    room = Room.objects.get(id=room_id)
    song_queue = Playlist.objects.get(belongs_to_room=room, pl_type="queue")
    context['songs'] = song_queue.songs.all()
    return render(request, 'hot_pot/youtube/songs.json', context, content_type='application/json')


# Return name of top song and remove from song queue
def get_top_of_song_queue(request, room_id):
    # TODO: What to do if no more songs in song_queue

    # Get song queue for this room
    room = Room.objects.get(id=room_id)
    song_queue = Playlist.objects.get(belongs_to_room=room, pl_type="queue")

    # If empty, return nothing
    if song_queue.songs.count() == 0:
        return HttpResponse('')
    else:
        top_song = song_queue.songs.first()

        print('Got top song: ' + top_song.song_name)

        context = {'song': top_song}

        """ song.json is as follows:
        {
            "id" : "{{song.song_id}}",
            "name" : "{{song.song_name}}"
        }
        """

        return render(request, 'hot_pot/youtube/song.json', context, content_type='application/json')


# Delete song with specified song_id from song_queue of specified room_id
def delete_from_song_queue(request, room_id, song_id):
    # Get song queue for this room
    room = Room.objects.get(id=room_id)
    song_queue = Playlist.objects.get(belongs_to_room=room, pl_type="queue")

    # Delete from song queue
    song_queue.songs.filter(song_id=song_id).delete()
    print('Deleted song with song_id: ' + song_id)

    # TODO: Optional error logging if song doesn't exist anymore (possible if concurrent deletes)

    return HttpResponse('')
