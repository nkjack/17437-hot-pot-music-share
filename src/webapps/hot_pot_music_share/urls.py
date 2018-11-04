from django.urls import path

from hot_pot_music_share import views

urlpatterns = [
    # path('', views.global_stream, name='global_stream'),
    # path('login', LoginView.as_view(template_name="grumblr/login.html"), name='login'),
    # path('logout', logout_then_login, name='logout'),
    # path('register', views.register, name='register'),
    path('', views.home, name='home'),
    path('login', views.login, name='login'),

    # Spotify stuff
    path('get-spotify-username', views.get_spotify_username),
    path('spotify-post-auth', views.spotify_post_auth),
    path('spotify-callback', views.spotify_callback),
    path('create-demo-room', views.create_demo_room),
]
