# # Create your models here.
# """
# Models
# HotSpot Music Share will have 7 main models:
# - User
#     - The default model of a user in django.
# - ProfileUser
#     - An extension of the User model to add more data for each user in our app. Every profile
# 	will have is favorite rooms, rooms she created and so on.
# - Room
#     - A room is active or not and related to a specific user manager.
# 	- Room is owned by a User.
# 	- Room has x amount of user with dj's privilege.
# 	- Room has it's own current pool of songs which being voted by users.
# 	- It has a list of suggestions from users.
# 	- Has a location (relevant if GPS is specified when room created).
# - Song
#     - A song is related to a specific rooms.
# 	- Has amount of votes from the room it belongs to.
# - PlayList
#     - This is a model to help us simplify the idea of collecting few songs into one group and link it to
# 	a dj user.
# 	- Each song will have a rank which will represent the songs order in the playlist.
# - Vote
#     - Vote is a model but will represent in the database as a table of votes.
# 	- Each vote is related to a specific user and a specific song in a certain pool.
# - DJ
#     - Extension of ProfileUser with ability to save a playlist for a particular room
# Below is a rough Python draft of the above models.
# """
# import json

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

import os
# from json import JSONDecodeError
# # import spotipy.util as util

# SPOTIPY_CLIENT_ID = '04fb29de4495438aa354af4a57fd47a4'
# SPOTIPY_CLIENT_SECRET = '38378c5d52dc467da1feeac2f53cc6fc'
# SCOPE = 'user-read-private user-read-playback-state user-modify-playback-state' + \
#         ' streaming user-read-birthdate user-read-email user-read-private' # Needed for web playback SDK
# WEB_PLAYBACK_TOKEN = 'BQA6z3s0KVEriyG89oB5UMI9g3p7ldOeMyN6aEMBqOFNZKkI7Hgfkhn1o4cGl13UwkoHiYW4kg3vgZGmexv4KCU_u9c2JrA6hSawyuAJ_QlxOJkMW4fR7pB5sTyDWUv4Hsm59W60w8RJaepgbeMPNPLi_kLJVYWMl3YN'



# class Room(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=42)
#     user_manager = models.ForeignKey(User, on_delete=models.CASCADE)
#     location = models.CharField(max_length=100)  # Some Google Maps API ID (e.g. coordinates)
#     place = models.CharField(max_length=100)  # Some Google Places API ID (e.g. for a business)
#     listeners = models.ManyToManyField(User, on_delete = models.CASCADE)
    
#     def __str__(self):
#         return self.name


# # cited from https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     spotify_id = models.IntegerField(default=0)
#     # short_bio = models.TextField(max_length=420,default="")
#     # age = models.IntegerField(default=0)
#     # picture = models.ImageField(upload_to="profile-photos", blank=True)
#     # follows = models.ManyToManyField(User, related_name='follow')

#     # favorite_rooms = models.ManyToManyField(Room, related_name='favorite')
#     # my_rooms = models.ManyToManyField(Room, related_name='my_room')

#     spotify_username = models.TextField(max_length=30, default="")
#     token = models.TextField(max_length=420, default="")
#     web_play_back_token = models.TextField(max_length=420, default="")


#     def __str__(self):
#         return self.user.username

#     # Get a Spotify auth token
#     def spotify_get_token(self):

#         username = self.spotify_username
#         # Erase cache and prompt for user permission
#         try:
#             token = util.prompt_for_user_token(username,
#                                                scope=SCOPE,
#                                                client_id=SPOTIPY_CLIENT_ID,
#                                                client_secret=SPOTIPY_CLIENT_SECRET,
#                                                redirect_uri='http://localhost:8000/spotify-callback/')  # add scope
#         except (AttributeError, JSONDecodeError):  # If reading from cache went bad
#             os.remove(f".cache-{username}")
#             token = util.prompt_for_user_token(username,
#                                                scope=SCOPE,
#                                                client_id=SPOTIPY_CLIENT_ID,
#                                                client_secret=SPOTIPY_CLIENT_SECRET,
#                                                redirect_uri='http://localhost:8000/spotify-callback/')  # add scope
#         return token


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


# # class DjUser(models.Model):
# #     user = models.OneToOneField(ProfileUser, on_delete=models.CASCADE)
# #     current_playlist = models.ForeignKey(Playlist)
# #     room = models.ForeignKey(Room)
# #
# #     def __str__(self):
# #         return "{}, {}".format(self.user.username, self.room.name)
# #


# class Song(models.Model):
#     song_id = models.CharField(max_length=100)  # song will probably have id link to a Spotify API
#     song_name = models.CharField(max_length=42)
#     # votes_score = models.IntegerField(default=0)

#     belongs_to_room = models.ForeignKey(Room, on_delete=models.CASCADE)
#     thumbs_up = models.IntegerField(blank = True, default = 0)
#     # is_in_pool = models.BooleanField()  # Boolean if song is in suggestions or in actual pool of a room

#     def __str__(self):
#         return self.song_name


# class Playlist(models.Model):
#     belongs_to_room = models.ForeignKey(Room, on_delete=models.CASCADE)
#     # is_in_pool = models.BooleanField()  # Boolean if song is in suggestions or in actual pool of a room

#     songs = models.ManyToManyField(Song, related_name='pl_songs')

#     def __str__(self):
#         return self.belongs_to_room.username

#     def add_song(self, song):
#         self.songs.add(song)


# class Vote(models.Model):
#     song = models.ForeignKey(Song, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     room = models.ForeignKey(Room, on_delete=models.CASCADE)

#     vote = models.CharField(max_length=2)  # could be '-1', '0', or '+1'

#     def __str__(self):
#         return self.user.username






