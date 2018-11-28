from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from django.views.generic.base import RedirectView

from hot_pot.views import auth_views, room_views, map_views, home_views, voting_views

urlpatterns = \
    [
        ########
        # Auth #
        ########
        path('', RedirectView.as_view(url='login'), name="go_to_login"),
        path('login', auth_views.custom_login, name='login'),
        path('register', auth_views.register, name='register'),
        re_path(
            r'^confirm-email/username=(?P<username>[0-9A-Za-z_]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            auth_views.confirm_email, name='confirm'),

        path('logout', auth_views.custom_logout, name='logout'),

        ########
        # Home #
        ########
        re_path(r'^username/(?P<username>[a-zA-Z0-9_]{3,15})/$', home_views.home, name='home'),
        path('myRooms', home_views.room_history, name="history"),

        ########
        # Room #
        ########

        # Init
        re_path(r'^room/(?P<room_id>[^/]+)/$', room_views.room, name='room'),
        
        # Search for songs
        path('search-song', room_views.search_song, name='search-song'),

        # Playlist manipulation
        path('add-song-to-room-playlist-ajax', room_views.add_song_to_room_playlist_ajax),
        path('add-song-from-pool-to-queue', room_views.add_song_from_pool_to_queue),
        path('get-pool-songs-from-room', room_views.get_pool_songs_from_room),
        path('get-queue-songs-from-room', room_views.get_queue_songs_from_room),
        re_path(r'^get-top-of-song-queue/(?P<room_id>[^/]+)/$', room_views.get_top_of_song_queue,
                name='get-top-of-song-queue'),
        re_path(r'^delete-from-song-queue/(?P<room_id>[^/]+)/(?P<song_id>[^/]+)$',
                room_views.delete_from_song_queue, name='delete-from-song-queue'),
        re_path(r'^get-users-from-room/(?P<room_name>[^/]+)/$', room_views.get_users_in_room,
                name='get-users-from-room'),
        path('delete-from-song-queue-post', room_views.delete_from_song_queue_post),
        path('change-song-queue-order', room_views.change_song_queue_order),

        # Voting
        path('vote-up', voting_views.vote_up),
        path('vote-down', voting_views.vote_down),

        # Add/Remove DJs
        path('add-dj-to-room', room_views.add_dj_to_room),
        path('remove-dj-from-room', room_views.remove_dj_from_room),
        path('get-all-non-djs-in-room', room_views.get_all_non_djs_in_room),
        path('get-djs-in-room', room_views.get_djs_in_room),

        ########
        # Maps #
        ########
        path('map-of-rooms', map_views.map_of_rooms, name='map_of_rooms'),
        path('add-marker', map_views.add_marker),
        path('get-markers', map_views.get_markers),

            # img
        re_path(r'^profile-photo/room/(?P<room_id>\w+)/$', home_views.get_room_img, name = 'room_img'),
        re_path(r'^profile-photo/user/(?P<username>[a-zA-Z0-9_]{3,15})/$', home_views.get_user_img, name = 'user_img'),

        # profiles
        re_path(r'^edit-room/(?P<room_id>[^/]+)/$', home_views.edit_room, name = 'edit_room'),
        path('edit-user', home_views.edit_user, name = 'user_profile'),
        path('delete-marker-from-room', home_views.delete_marker_from_room),
        path('add-marker-to-room', home_views.add_marker_to_room),

    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
