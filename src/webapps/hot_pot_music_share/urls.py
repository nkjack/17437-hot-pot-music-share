from django.urls import path,re_path
from django.views.generic.base import RedirectView
from hot_pot_music_share import views

urlpatterns = [
    # path('', views.global_stream, name='global_stream'),
    # path('login', LoginView.as_view(template_name="grumblr/login.html"), name='login'),
    # path('logout', logout_then_login, name='logout'),
    # path('register', views.register, name='register'),


    # User login 
    path('', RedirectView.as_view(url = 'login'),name="go_to_login"),
    path('login', views.customLogin, name='login'),
    path('register', views.register, name= 'register'),

    # Email Confirmation
    re_path(r'^confirm-email/username=(?P<username>[0-9A-Za-z_]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    views.confirm_email, name='confirm'),

    # User Home Page
    re_path(r'^username=(?P<username>[a-z0-9_]{3,15})$',views.home, name = 'home'),

    # Create Room
    path('create-room', views.create_room, name = "create_room"),
    re_path(r'^room=(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.confirm_email, name='confirm'),



    # Spotify stuff
    # path('get-spotify-username', views.get_spotify_username),
    # path('spotify-post-auth', views.spotify_post_auth),
    # path('spotify-callback', views.spotify_callback),
    # path('create-demo-room', views.create_demo_room),

    # path('spotify-transfer-playback/<str:device_id>', views.spotify_transfer_playback),
    # path('spotify-play-song/<str:song_id>', views.spotify_play_song),

    # path('search-song', views.search_song),
    # path('add-song-to-room-playlist', views.add_song_to_room_playlist),
    # path('play-song', views.play_song),

]
