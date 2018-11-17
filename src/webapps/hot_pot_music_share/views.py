# import spotipy
# import spotipy.util as util
import json

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
# send mail
from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
# Home view
from django.utils.safestring import mark_safe


@login_required
def home(request, username):
    context = {'title': 'home', 'error': ''}
    context['username'] = username
    user_from_url = get_object_or_404(User, username=username)

    if (request.method == "GET"):
        context['form'] = RoomForm(initial={'owner': request.user})

        popular_rooms = Room.objects.all().order_by('thumbs_up')[:6]
        context["popular"] = popular_rooms

        print(popular_rooms)
        return render(request, 'home.html', context)

    elif (request.POST.get('create_room')):
        form = RoomForm(request.POST, request.FILES, initial={'owner': request.user})
        context['form'] = form

        if form.is_valid():
            # Create empty song_queue and song_pool
            print("Initializing song_queue and song_pool...")
            song_queue = Playlist.objects.create()
            song_pool = Playlist.objects.create()

            # TODO: For debugging, just add a couple songs
            song_0 = Song.objects.create(song_id='JQbjS0_ZfJ0', song_name='Kendrick Lamar, SZA - All The Stars')
            song_1 = Song.objects.create(song_id='6ONRf7h3Mdk', song_name='Travis Scott - SICKO MODE ft. Drake')
            song_2 = Song.objects.create(song_id='xTvyyoF_LZY', song_name='Ed Sheeran - Shape of You')
            song_3 = Song.objects.create(song_id='GTe57jQX5Eg', song_name='Jay Rock - Wow Freestyle ft. Kendrick Lamar')

            song_pool.songs.add(song_2)
            song_pool.songs.add(song_3)

            song_queue.songs.add(song_0)
            song_queue.songs.add(song_1)

            song_queue.save()
            song_pool.save()

            print("Creating Room...")
            new_room = Room.objects.create(owner=request.user,
                                           name=form.cleaned_data['name'],
                                           description=form.cleaned_data['description'],
                                           cover_pic=form.cleaned_data['cover_pic'],
                                           song_queue=song_queue,
                                           song_pool=song_pool,
                                           )
            new_room.save()
            new_history = RoomHistory.objects.create(user=request.user,
                                                     visited_room=new_room)
            new_history.save()

            return HttpResponseRedirect(reverse('room', args=[new_room]))
        else:

            return render(request, 'home.html', context)


# Integrate actual Profile model later
# def login(request):
#     return render(request, 'hot_pot_music_share/login.html')


## youtube search

from googleapiclient.discovery import build

DEVELOPER_KEY = 'AIzaSyC6zJT9fu29Wj6T67uRxfnQvc9kyP4wz3Y'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def search_room(request):
    context = {}
    r = Room.objects.get(name="noam_room")
    p = Playlist.objects.get(belongs_to_room=r)
    context['playlist'] = p

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
        videoCategoryId='10',  # only songs!
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

    r = Room.objects.get(name="noam_room")
    p = Playlist.objects.get(belongs_to_room=r)
    context['playlist'] = p

    context['search_results'] = videos
    return render(request, 'hot_pot_music_share/youtube/room.html', context)


def add_song_to_room_playlist(request):
    context = {}
    # user = User.objects.get(username=request.user)
    # room_id = request.POST['room_id']
    searched_song_id = request.POST['song_id']
    searched_song_name = request.POST['song_name']

    if not User.objects.filter(username__exact="noam"):
        u = User.objects.create(username="noam")
        u.save()

    if not Room.objects.filter(name__exact="noam_room"):
        u = User.objects.get(username="noam")
        r = Room.objects.create(user_manager=u, name="noam_room")
        r.save()
        p = Playlist.objects.create(belongs_to_room=r)
        p.save()

    # room = Room.objects.get(id=room_id)
    r = Room.objects.get(name="noam_room")
    p = Playlist.objects.get(belongs_to_room=r)

    if not Song.objects.filter(song_id__exact=searched_song_id):
        s = Song(song_id=searched_song_id, song_name=searched_song_name)
        s.save()

    s = Song.objects.get(song_id=searched_song_id)

    if not Playlist.objects.filter(songs__song_id__exact=searched_song_id):
        p.songs.add(s)

    # context['room'] = room
    context['playlist'] = p
    # context['user'] = user
    return render(request, 'hot_pot_music_share/youtube/room.html', context)


def add_song_to_room_playlist_ajax(request):
    context = {}
    # user = User.objects.get(username=request.user)
    # room_id = request.POST['room_id']
    searched_song_id = request.POST['song_id']
    searched_song_name = request.POST['song_name']

    if not User.objects.filter(username__exact="noam"):
        u = User.objects.create(username="noam")
        u.save()

    if not Room.objects.filter(name__exact="noam_room"):
        u = User.objects.get(username="noam")
        r = Room.objects.create(user_manager=u, name="noam_room")
        r.save()
        p = Playlist.objects.create(belongs_to_room=r)
        p.save()

    # room = Room.objects.get(id=room_id)
    r = Room.objects.get(name="noam_room")
    p = Playlist.objects.get(belongs_to_room=r)

    if not Song.objects.filter(song_id__exact=searched_song_id):
        s = Song(song_id=searched_song_id, song_name=searched_song_name)
        s.save()

    s = Song.objects.get(song_id=searched_song_id)
    if not Playlist.objects.filter(songs__song_id__exact=searched_song_id):
        p.songs.add(s)

    # context['room'] = room
    context['songs'] = p.songs.all()
    # print (context['songs'])
    # context['user'] = user
    return render(request, 'hot_pot_music_share/youtube/songs.json', context, content_type='application/json')


# Integrate actual Profile model later
def customLogin(request):
    context = {'login_active': 'active', 'register_active': '', }
    # If already logged in, redirect to home
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home', args=[request.user.username]))

    if request.method == 'GET':
        context['login_form'] = LoginForm()

        return render(request, 'user_auth/login.html', context)

    if request.POST.get('login'):
        form = LoginForm(request.POST)
        context['login_form'] = form

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('home', args=[username]))
            else:
                context['error'] = 'Invalid login. Password doesnot match the user or user doesnot exist'
                return render(request, 'user_auth/login.html', context)
        else:
            return render(request, 'user_auth/login.html', context)


    elif 'resetPassword' in request.POST or request.POST['resetPassword']:
        return HttpResponseRedirect(reverse('forgetPassword'))


    else:
        context['error'] = "Please press Login button to register an account"
        return render(request, 'user_auth/login.html', context)


def register(request):
    context = {'register_active': 'active', 'login_active': ''}

    if request.method == 'GET':
        context['registration_form'] = RegistrationForm()

        return render(request, 'user_auth/login.html', context)
    else:
        if 'register' in request.POST or request.POST['register']:
            form = RegistrationForm(request.POST)
            context['registration_form'] = form
            if form.is_valid():
                new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                                    password=form.cleaned_data['password1'],
                                                    email=form.cleaned_data['email'])

                new_user.is_active = False
                new_user.save()

                token = default_token_generator.make_token(new_user)
                email_body = """
                Welcome to hot_pot_music_share. Please click the link below to verify your email address and complete registration:
                http://%s%s
                """ % (request.get_host(),
                       reverse('confirm', args=(new_user.username, token)))

                send_mail(subject="Verify Your Email Adress",
                          message=email_body,
                          from_email="..",
                          recipient_list=[new_user.email])

                context[
                    "email"] = "Welcome to Hot Pot Music Share. Please check your mailbox to find verification link to complete registration"
                return render(request, 'user_auth/email_confirmation.html', context)

                # login(request, new_user)
                # return HttpResponseRedirect(reverse('home',args=[new_user.username]))
            else:
                context['error'] = "Please check if all the field satisfy requirements or the username is already taken"
                return render(request, 'user_auth/login.html', context)
        else:
            context['error'] = "Please press Register button to register an account"
            return render(request, 'user_auth/login.html', context)


def customLogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


@transaction.atomic
def confirm_email(request, username, token):
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, token):

        user.is_active = True
        user.save()

        return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponse('Invalid Link')


@login_required
def room(request, room_name):
    room = Room.objects.get(name=room_name)
    is_host = room.owner == request.user
    print(">>>>>>>>" + str(is_host))

    context = {'username': request.user.username,
               'room_name_json': mark_safe(json.dumps(room_name)),
               'title': 'Room ' + room_name,
               'is_host': is_host,
               'song_pool': room.song_pool,
               'song_queue': room.song_queue,
               }

    return render(request, 'room_base.html', context)


@login_required
def history(request):
    context = {'owned': '', 'visited': '', 'username': request.user.username}
    if request.method == 'GET':
        owned = Room.objects.filter(owner=request.user)
        visited = RoomHistory.getVistedRooms(request.user)

        context['owned'] = owned
        context['visited'] = visited

    return render(request, 'room_history.html', context)


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
        print(form.errors)
        raise Http404

    form.save()
    all_markers = Marker.objects.all()
    print(all_markers)
    context['all_markers'] = all_markers
    return JsonResponse(data={})
    # return render(request, 'hot_pot_music_share/maps/base_map.html', context)


# @login_required
# @transaction.atomic
def get_markers(request):
    all_markers = Marker.objects.all()
    context = {'markers': all_markers}

    return render(request, 'hot_pot_music_share/maps/markers.json', context, content_type='application/json')
