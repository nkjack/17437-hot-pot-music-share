
from django.urls import path, re_path
from hot_spot_music_share import views
from django.contrib.auth.views import LoginView, logout_then_login

# urlpatterns = [
#     path('', views.global_stream, name='global_stream'),
#     path('login', LoginView.as_view(template_name="grumblr/login.html"), name='login'),
#     path('logout', logout_then_login, name='logout'),
#     path('register', views.register, name='register'),
# ]
