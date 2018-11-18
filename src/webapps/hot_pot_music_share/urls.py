from django.conf.urls import url
from django.urls import path, re_path
from django.views.generic.base import RedirectView

from hot_pot_music_share import views, player_views

urlpatterns = [

    # Search urls
    path('search-song', views.search_song, name='search-song'),
    path('add-song-to-room-playlist-ajax', views.add_song_to_room_playlist_ajax),
    path('add-song-from-pool-to-queue', views.add_song_from_pool_to_queue),
    path('get-pool-songs-from-room', views.get_pool_songs_from_room),
    path('get-queue-songs-from-room', views.get_queue_songs_from_room),
    path('map-of-rooms', views.map_of_rooms, name = 'map_of_rooms'),

    # Maps urls
    path('add-marker', views.add_marker),
    path('get-markers', views.get_markers),

    # User login
    path('', RedirectView.as_view(url='login'), name="go_to_login"),
    path('login', views.custom_login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.custom_logout, name='logout'),

    # Email Confirmation
    re_path(r'^confirm-email/username=(?P<username>[0-9A-Za-z_]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.confirm_email, name='confirm'),

    # User Home Page
    re_path(r'^username/(?P<username>[a-zA-Z0-9_]{3,15})/$', views.home, name='home'),
    re_path(r'^room/(?P<room_id>[^/]+)/$', views.room, name='room'),

    # history
    path('myRooms', views.history, name="history"),

    # Sam Player stuff TODO: Delete
    re_path(r'^player/(?P<room_name>[^/]+)/$', player_views.room, name='player-room'),
    path('player', player_views.youtube_player),


    #img
    re_path(r'^profile-photo/room/(?P<pk>\w+)/$', views.get_img, name = 'img'),

]
