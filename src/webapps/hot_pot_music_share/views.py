import json
import os
from json import JSONDecodeError
from django.contrib.auth.models import User

# import spotipy
# import spotipy.util as util
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse
from hot_pot_music_share import models
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from hot_pot_music_share.models import *

SPOTIPY_CLIENT_ID = '04fb29de4495438aa354af4a57fd47a4'
SPOTIPY_CLIENT_SECRET = '38378c5d52dc467da1feeac2f53cc6fc'
SCOPE = 'user-read-private user-read-playback-state user-modify-playback-state' + \
        ' streaming user-read-birthdate user-read-email user-read-private' # Needed for web playback SDK
WEB_PLAYBACK_TOKEN = 'BQA6z3s0KVEriyG89oB5UMI9g3p7ldOeMyN6aEMBqOFNZKkI7Hgfkhn1o4cGl13UwkoHiYW4kg3vgZGmexv4KCU_u9c2JrA6hSawyuAJ_QlxOJkMW4fR7pB5sTyDWUv4Hsm59W60w8RJaepgbeMPNPLi_kLJVYWMl3YN'


# Home view
@login_required
def home(request, username):
    return render(request, 'hot_pot_music_share/home.html')

# Integrate actual Profile model later
def login(request):
    context = {'login_active':'active', 'register_active':'',}
    # If already logged in, redirect to home
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home',args=[request.user.username]))

    if request.method =='GET':
        context['login_form'] = LoginForm()
        
        return render(request, 'hot_pot_music_share/login.html', context)

    if request.POST.get('login'):
        form = LoginForm(request.POST)
        context['login_form'] = form

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            
            user = authenticate(request, username = username, password = password)
            
            if user is not None:

                if not hasattr(user, 'profile'):
                    profile = Profile(user = user, bio = 'my short bio', age = 0)
                    profile.save()

                login(request, user)
                return HttpResponseRedirect(reverse('home',args=[username]))
            else:
                context['error'] = 'Invalid login. Password doesnot match the user or user doesnot exist'
                return render(request, 'hot_pot_music_share/login.html', context)
        else:
            return render(request, 'hot_pot_music_share/login.html', context)

    
    elif 'resetPassword' in request.POST or request.POST['resetPassword']:
        return HttpResponseRedirect(reverse('forgetPassword'))


    else:
        context['error'] = "Please press Login button to register an account"
        return render(request, 'hot_pot_music_share/login.html', context)


def register(request):
    context = {'title':'Register for Hot Pot Music Share', 'register_active': 'active', 'login_active' : ''}

    if request.method =='GET':
        context['registration_form'] = RegistrationForm()
    
        return render(request, 'login.html', context)
    else:
        if 'register' in request.POST or request.POST['register']:
            form = RegistrationForm(request.POST)
            context['registration_form'] = form 
            if form.is_valid():
                new_user = User.objects.create_user(username = form.cleaned_data['username'],
                                                    password = form.cleaned_data['password1'],
                                                    name = form.cleaned_data['name'],
                                            
                                                    email = form.cleaned_data['email'])

                new_user.is_active = False
                new_user.save()
                profile = Profile(user = new_user, bio = 'my short bio', age = 0)
                profile.save()

                token = default_token_generator.make_token(new_user)
                email_body = """
                Welcome to Grumblr. Please click the link below to verify your email address and complete registration:
                http://%s%s
                """ % (request.get_host(),
                    reverse('confirm', args=(new_user.username, token)))

                send_mail(subject = "Verify Your Email Adress",
                        message = email_body,
                        from_email = "ruilit@andrew.cmu.edu",
                        recipient_list = [new_user.email])

                context["email"] = "Welcome to Grumblr. Please check your mailbox to find verification link to complete registration"
                return render(request,'needs_confirmation.html',context)

                # login(request, new_user)
                # return HttpResponseRedirect(reverse('home',args=[new_user.username]))
            else:
                context['error'] = "Please check if all the field satisfy requirements or the username is already taken"
                return render(request, 'login.html', context)
        else:
            context['error'] = "Please press Register button to register an account"
            return render(request, 'login.html', context)



#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
# SPOTIFY DEMO (STEP 1) - Replacing login for now
# def get_spotify_username(request):
#     return render(request, 'hot_pot_music_share/spotify/get-spotify-username.html')

# # SPOTIFY DEMO (STEP 2) Redirect after successfully authenticating with Spotify
# def spotify_post_auth(request):
#     username = request.GET['spotify-username']  # FIXME: Catch key error
#     print("spotify_post_auth - username: ", username)

#     # Get token
#     token = spotify_get_token(username)

#     # Create User here, if it doesn't exist
#     if not User.objects.filter(username=username).exists():
#         user = User.objects.create_user(username=username) # Same username as spotify username for now
#         user.profile.spotify_username = username
#         user.profile.token = token
#         user.save()
#     else:
#         user = User.objects.get(username=username)

#     # Create our spotify object with permissions
#     spotify = spotipy.Spotify(auth=token)

#     # Get current device
#     devices = spotify.devices()
#     if len(devices['devices']) > 0:
#         deviceID = devices['devices'][0]['id']

#     # Current track information
#     track = spotify.current_user_playing_track()
#     currently_playing = None
#     if track is not None:
#         artist = track['item']['artists'][0]['name']
#         track = track['item']['name']

#         if artist != "":
#             currently_playing = "Currently playing " + artist + " - " + track

#     # User information
#     user = spotify.current_user()
#     displayName = user['display_name']
#     followers = user['followers']['total']

#     # Get user playlists
#     user_playlists = []
#     searchResults = spotify.current_user_playlists()
#     for searchResult in searchResults['items']:
#         user_playlists.append((searchResult['name'], searchResult['id']))

#     context = {'username':displayName, 'currently_playing':currently_playing, 'user_playlists':user_playlists}
#     context['user'] = user
#     print(context)
#     return render(request, 'hot_pot_music_share/spotify/spotify-post-auth.html', context)

# # SPOTIFY DEMO (STEP 3) - Create a simple room
# def create_demo_room(request):
#     room_name = request.GET['room-name']  # FIXME: Catch key error

#     # Create the room
#     room = Room(name=room_name, user_manager=User.objects.get(username='nkjack84')) # FIXME: Who to set user_manager to?
#     room.save()

#     # Create the playlist
#     playlist_obj = Playlist(belongs_to_room=room)
#     playlist_obj.save()

#     # Create a single song
#     # song1 = Song(song_id='66kQ7wr4d22LwwSjr7HXcyr', song_name='All The Stars', belongs_to_room=room)
#     # song2 = Song(song_id='6TaqooOXAEcijL6G1AWS2K', song_name='All My Friends', belongs_to_room=room)
#     # song1.save()
#     # song2.save()
#     #
#     # playlist_obj.songs.add(song1)
#     # playlist_obj.songs.add(song2)

#     # Debug set just one song
#     # one_song = ['66kQ7wr4d2LwwSjr7HXcyr']
#     # playlist_obj.set_songs(one_song)
#     # playlist_obj.songs.Objects

#     token = spotify_get_token('sampromises')

#     # TODO: Create an empty room
#     return render(request, 'hot_pot_music_share/spotify/spotify-room.html',
#                   {'room':room, 'playlist':playlist_obj,
#                    'song_id':'66kQ7wr4d22LwwSjr7HXcyr',
#                    'token':token})


# # Simple callback after Spotify authentication is done
# def spotify_callback(request):
#     context = {'code': request.GET['code']}
#     return render(request, 'hot_pot_music_share/spotify/spotify-callback.html', context)

# def spotify_web_playback(request):
#     return render(request, 'hot_pot_music_share/spotify/spotify-web-playback.html')

# ### HELPER FUNCTIONS

# # Get a Spotify auth token
# def spotify_get_token(username):
#     # Erase cache and prompt for user permission
#     try:
#         token = util.prompt_for_user_token(username=username,
#                                            scope=SCOPE,
#                                            client_id=SPOTIPY_CLIENT_ID,
#                                            client_secret=SPOTIPY_CLIENT_SECRET,
#                                            redirect_uri='http://localhost:8000/spotify-callback')  # add scope



#     except (AttributeError, JSONDecodeError):  # If reading from cache went bad
#         os.remove(f".cache-{username}")
#         token = util.prompt_for_user_token(username=username,
#                                            scope=SCOPE,
#                                            client_id=SPOTIPY_CLIENT_ID,
#                                            client_secret=SPOTIPY_CLIENT_SECRET,
#                                            redirect_uri='http://localhost:8000/spotify-callback')  # add scope
#     return token

# def spotify_play_song(request, song_id, offset=None):
#     # Get token
#     token = spotify_get_token('sampromises')

#     # Create our spotify object with permissions
#     spotify = spotipy.Spotify(auth=token)

#     print("DEVICES: ", spotify.devices())

#     # Change playback
#     spotify.start_playback(device_id='bab9a49eb64e01a2467bda4486315865c3754ff3',
#                            uris=['spotify:track:'+song_id], offset=offset)

#     # Empty response
#     return HttpResponse('')


# # Transfer Spotify playback to specified device ID
# def spotify_transfer_playback(request, device_id, username='sampromises'):
#     # Get token
#     token = spotify_get_token(username)

#     # Create our spotify object with permissions
#     spotify = spotipy.Spotify(auth=token)

#     # Get current device
#     spotify.transfer_playback(device_id, force_play=True)
#     print(device_id)

#     # Empty response
#     return HttpResponse('')

# #search song in spotify
# def search_song(request):
#     user = User.objects.get(username="nkjack84")

#     context = {}
#     room_id = request.GET['room']
#     print(room_id)
#     room = Room.objects.get(id=room_id) # FIXME: Who to set user_manager to?
#     playlist_obj = Playlist.objects.get(belongs_to_room=room)

#     search_song = request.GET['spotify-song']

#     user = User.objects.get(username='nkjack84')
#     sp = spotipy.Spotify(auth=user.profile.spotify_get_token())
#     result = sp.search(search_song, limit=10, type="track")
#     # pprint.pprint(result)

#     # print(type(result))
#     items = result['tracks']['items']

#     dic_songs = {}
#     for item in items:
#         dic_songs[item['id']] = item['name']

#     # print(dic_songs)

#     context['room'] = room
#     context['search_results'] = dic_songs
#     context['playlist'] = playlist_obj
#     context['user'] = user
#     return render(request, 'hot_pot_music_share/spotify/spotify-room.html', context)


# def add_song_to_room_playlist(request):
#     user = User.objects.get(username='nkjack84')

#     context = {}
#     room_id = request.POST['room_id']
#     searched_song_id = request.POST['song_id']
#     searched_song_name = request.POST['song_name']

#     room = Room.objects.get(id=room_id) # FIXME: Who to set user_manager to?
#     playlist = Playlist.objects.get(belongs_to_room=room)

#     song = Song(song_id=searched_song_id, song_name=searched_song_name, belongs_to_room=room)
#     song.save()

#     playlist.songs.add(song)
#     context['room'] = room
#     context['playlist'] = playlist
#     context['user'] = user
#     return render(request, 'hot_pot_music_share/spotify/spotify-room.html', context)

# def play_song(request):
#     user = User.objects.get(username='nkjack84')
#     sp = spotipy.Spotify(auth=user.profile.spotify_get_token())
#     sp.start_playback(device_id='1171ce229321475f1c5729dfcc56265ca787d51b', uris=['spotify:track:' + request.GET['spotify-song']])

#     return HttpResponse('')

