from mimetypes import guess_type

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime, now
from googleapiclient.discovery import build

from hot_pot.models import Room, RoomHistory, Playlist, Song
from hot_pot.views.room_helper import get_all_songs_from_playlist, user_is_dj

# YouTube API metadata needed for search
import os
DEVELOPER_KEY = os.environ.get("YOUTUBE_API_KEY")
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
MAX_SEARCH_RESULTS = 10


@login_required
@transaction.atomic
def room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    room_name = room.name
    is_dj = user_is_dj(request.user, room)
    song_pool = Playlist.objects.get(belongs_to_room=room, pl_type="pool")
    song_queue = Playlist.objects.get(belongs_to_room=room, pl_type="queue")

    # Update user room history if this user has never been to this room
    if not RoomHistory.visited_before(request.user, room, localtime(now())):
        history = RoomHistory.objects.create(user=request.user, visited_room=room)
        history.save()
    listeners = RoomHistory.get_current_listeners(room)

    context = {'username': request.user.username,
               'room_id': room_id,
               'room_name': room_name,
               'title': 'Room ' + room_name,
               'is_dj': is_dj,
               'song_pool': song_pool.songs.all().order_by('id'),
               'song_queue': song_queue.songs.all().order_by('id'),
               }

    return render(request, 'room/room.html', context)


@login_required
def get_img(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if not room.cover_pic:
        raise Http404
    content_type = guess_type(room.cover_pic.name)
    return HttpResponse(room.cover_pic, content_type=content_type)


def search_song(request):
    print("Entered search_song")
    context = {}
    query = request.GET['query']
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    print("youtube thing was built...")

    print("Making search_response...")
    print("\t query = ", query)
    # Call the search.list method to retrieve results matching the specified query term.
    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        maxResults=MAX_SEARCH_RESULTS,
        type='video',
        videoCategoryId='10',  # only songs!
    ).execute()
    print("Made search_response...")

    videos = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append(Song(song_id=search_result['id']['videoId'],
                               song_name=search_result['snippet']['title']))

    context['songs'] = videos

    print("videos after = " + str(videos))

    return render(request, 'hot_pot/room/songs.json', context, content_type='application/json')


@login_required
@transaction.atomic
def add_song_to_room_playlist_ajax(request):
    room_id = request.POST['room_id']
    searched_song_id = request.POST['song_id']
    searched_song_name = request.POST['song_name']

    room = Room.objects.get(id=room_id)
    song_pool = Playlist.objects.get(belongs_to_room=room, pl_type="pool")

    # Don't create the song if it already exists in room
    if not Song.objects.filter(song_id__exact=searched_song_id, song_room=room):
        song = Song(song_id=searched_song_id,
                    song_name=searched_song_name,
                    song_room=room)
        song.save()

    # Don't add the song if it already exists in the playlist
    song = Song.objects.get(song_id=searched_song_id, song_room=room)
    if not Playlist.objects.filter(songs__song_id__exact=searched_song_id,
                                   belongs_to_room=room,
                                   pl_type="pool"):
        song_pool.songs.add(song)

    json = get_all_songs_from_playlist(room_id, request.user.id, "pool")
    return JsonResponse(data=json)


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

    # Don't create the song if it already exists in room
    if not Song.objects.filter(song_id__exact=searched_song_id,
                               song_room=room):
        song = Song(song_id=searched_song_id,
                    song_name=searched_song_name,
                    song_room=room)
        song.save()

    # Don't add the song if it already exists in the playlist
    song = Song.objects.get(song_id=searched_song_id)
    if not Playlist.objects.filter(songs__song_id__exact=searched_song_id,
                                   belongs_to_room=room,
                                   pl_type="queue"):
        song_queue.songs.add(song)

    song.rank = song_queue.songs.all().count()
    song.save()

    context['songs'] = song_queue.songs.all().order_by('rank')
    return render(request, 'hot_pot/room/songs.json', context, content_type='application/json')


@login_required
@transaction.atomic
def get_pool_songs_from_room(request):
    room_id = request.GET['room_id']
    json = get_all_songs_from_playlist(room_id, request.user.id, "pool")
    return JsonResponse(data=json)


@login_required
@transaction.atomic
def get_queue_songs_from_room(request):
    context = {}
    room_id = request.GET['room_id']
    room = Room.objects.get(id=room_id)
    song_queue = Playlist.objects.get(belongs_to_room=room, pl_type="queue")
    context['songs'] = song_queue.songs.all().order_by('rank')
    return render(request, 'hot_pot/room/songs.json', context, content_type='application/json')


# Return name of top song and remove from song queu
@transaction.atomic
def get_top_of_song_queue(request, room_id):
    # Get song queue for this room
    room = Room.objects.get(id=room_id)
    song_queue = Playlist.objects.get(belongs_to_room=room, pl_type="queue")

    # If empty, return nothing
    if song_queue.songs.count() == 0:
        print('[room_views.get_top_of_song_queue] No more songs!')

        return HttpResponse(status=204)  # Successful, but no more content
    else:
        song_queue_ordered = song_queue.songs.all().order_by('rank')  # Need to order by manual sort order
        top_song = song_queue_ordered.first()

        print('[room_views.get_top_of_song_queue] Got top song: ' + top_song.song_name)

        context = {'song': top_song}

        """ song.json is as follows:
        {
            "id" : "{{song.song_id}}",
            "name" : "{{song.song_name}}"
        }
        """

        return render(request, 'hot_pot/room/song.json', context, content_type='application/json')


# Delete song with specified song_id from song_queue of specified room_id (Noam version POST)
@transaction.atomic
@login_required
def delete_from_song_queue_post(request):
    # Get song queue for this room
    song_id = request.POST['song_id']
    room_id = request.POST['room_id']
    room = get_object_or_404(Room, id=room_id)
    song_queue = Playlist.objects.get(belongs_to_room=room, pl_type="queue")

    # Delete from song queue
    song = Song.objects.get(song_id=song_id, song_room=room)
    song_queue.songs.remove(song)

    all_queue_songs = song_queue.songs.all().order_by('rank')

    rank_itr = 1
    for song in all_queue_songs:
        song.rank = rank_itr
        rank_itr += 1
        song.save()

    context = {}
    context['songs'] = song_queue.songs.all().order_by('rank')
    return render(request, 'hot_pot/room/songs.json', context, content_type='application/json')


# Add user to room's current_users when they join (called by consumers.py - don't need a request parameter)
def add_user_to_room(username, room_name):
    room = Room.objects.get(name=room_name)
    user = User.objects.get(username=username)
    room.users.add(user)


# Remove user from room's current_users when they leave (called by consumers.py - don't need a request parameter)
def remove_user_from_room(username, room_name):
    room = Room.objects.get(name=room_name)
    user = User.objects.get(username=username)
    room.users.remove(user)


# Get all the users in the room
def get_users_in_room(request, room_name):
    room = Room.objects.get(name=room_name)
    context = {'users': room.users.all()}
    return render(request, 'hot_pot/room/users.json', context, content_type='application/json')


# Delete song with specified song_id from song_queue of specified room_id
@transaction.atomic
def delete_from_song_queue(request, room_id, song_id):
    # Get song queue for this room
    room = Room.objects.get(id=room_id)
    song_queue = Playlist.objects.get(belongs_to_room=room, pl_type="queue")

    # If empty, return nothing
    if song_queue.songs.count() == 0:
        print('[room_views.delete_from_song_queue] No more songs!')

        return HttpResponse(status=204)  # Successful, but no more content
    else:
        # Delete from song queue
        song = Song.objects.get(song_id=song_id, song_room=room)
        song_queue.songs.remove(song)
        print('Deleted song with song_id: ' + song_id)

        # TODO: Optional error logging if song doesn't exist anymore (possible if concurrent deletes)
    return HttpResponse('')


# Change position of song, given a previous position and a new position
@transaction.atomic
@login_required
def change_song_queue_order(request):
    room_id = request.POST['room_id']
    prev_position = int(request.POST['prev_position'])
    new_position = int(request.POST['new_position'])

    room = Room.objects.get(id=room_id)
    song_queue = Playlist.objects.get(belongs_to_room=room, pl_type="queue")
    all_queue_songs = song_queue.songs.all().order_by("rank")

    print("new_pos - {}, prev_pos = {}, amount_songs".format(new_position, prev_position, all_queue_songs.count()))

    if (1 < new_position <= all_queue_songs.count()
            and 1 < prev_position <= all_queue_songs.count()):
        # downvote
        if prev_position < new_position:
            print("downvote")
            all_queue_songs = song_queue.songs.all().order_by("rank")

            for song in all_queue_songs:
                if song.rank < prev_position:
                    continue
                elif song.rank == prev_position:
                    song.rank = new_position
                elif song.rank <= new_position:
                    song.rank -= 1
                elif song.rank > new_position:
                    continue
                song.save()

        # upvote
        elif prev_position > new_position:
            print("upvote")
            all_queue_songs = song_queue.songs.all().order_by("-rank")
            for song in all_queue_songs:
                if song.rank > prev_position:
                    continue
                elif song.rank == prev_position:
                    song.rank = new_position
                elif song.rank >= new_position:
                    song.rank += 1
                elif song.rank < new_position:
                    continue
                song.save()

    context = {}
    context['songs'] = song_queue.songs.all().order_by('rank')
    return render(request, 'hot_pot/room/songs.json', context, content_type='application/json')


# Add user to room's list of DJs
def add_dj_to_room(request):
    username = request.POST['username']
    room_id = request.POST['room_id']

    user = User.objects.get(username=username)
    room = Room.objects.get(id=room_id)

    room.djs.add(user)

    print('>>>> add_dj_to_room for user = %s, room = %s... successful', (user, room_id))
    return HttpResponse('')


# Remove user from room's list of DJs
def remove_dj_from_room(request):
    username = request.POST['username']
    room_id = request.POST['room_id']

    user = User.objects.get(username=username)
    room = Room.objects.get(id=room_id)

    # Cannot remove owner of the room as a DJ
    if user == room.owner:
        print('>>>> remove_dj_from_room for user = %s, room = %s... cannot remove owner as DJ', (user, room_id))
        return HttpResponseBadRequest

    room.djs.remove(user)

    print('>>>> remove_dj_from_room for user = %s, room = %s... successful', (user, room_id))
    return HttpResponse('')

