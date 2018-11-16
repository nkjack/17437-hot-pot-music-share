# Create your models here.


from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=42)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
g
    create_date = models.DateTimeField(auto_now=True)
    cover_pic = models.ImageField(upload_to='room-photo', blank=True,
                                  default='room-photo/logo.png',
                                  )
    description = models.TextField(max_length=420, blank=True,
                                   )

    thumbs_up = models.IntegerField(default=0)

    # location = models.CharField(max_length=100)  # Some Google Maps API ID (e.g. coordinates)
    # place = models.CharField(max_length=100)  # Some Google Places API ID (e.g. for a business)
    # listeners = models.ManyToManyField(User)

    def __str__(self):
        return self.name


# cited from https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # short_bio = models.TextField(max_length=420,default="")
    # age = models.IntegerField(default=0)
    # picture = models.ImageField(upload_to="profile-photos", blank=True)
    # follows = models.ManyToManyField(User, related_name='follow')

    # favorite_rooms = models.ManyToManyField(Room, related_name='favorite')
    # my_rooms = models.ManyToManyField(Room, related_name='my_room')

    # spotify_username = models.TextField(max_length=30, default="")
    # token = models.TextField(max_length=420, default="")
    # web_play_back_token = models.TextField(max_length=420, default="")

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# class DjUser(models.Model):
#     user = models.OneToOneField(ProfileUser, on_delete=models.CASCADE)
#     current_playlist = models.ForeignKey(Playlist)
#     room = models.ForeignKey(Room)
#
#     def __str__(self):
#         return "{}, {}".format(self.user.username, self.room.name)
#


class Song(models.Model):
    song_id = models.CharField(max_length=100)  # song will probably have id link to a Spotify API
    song_name = models.CharField(max_length=42)

    # votes_score = models.IntegerField(default=0)

    # belongs_to_playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    # thumbs_up = models.IntegerField(blank = True, default = 0)
    # is_in_pool = models.BooleanField()  # Boolean if song is in suggestions or in actual pool of a room

    def __str__(self):
        return self.song_name


class Playlist(models.Model):
    belongs_to_room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # is_in_pool = models.BooleanField()  # Boolean if song is in suggestions or in actual pool of a room

    songs = models.ManyToManyField(Song, related_name='pl_songs')

    def __str__(self):
        return self.belongs_to_room.name


class Vote(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    vote = models.CharField(max_length=2)  # could be '-1', '0', or '+1'

    def __str__(self):
        return self.user.username


# #extend User model to have things like profile photos etc.
# class HotPotUser(models.Model):
# 	user = models.OneToOneField(User, on_delete = models.CASCADE)

########## maps

class Marker(models.Model):
    # id - django generate
    room_name = models.CharField(max_length=60, default="")
    address = models.CharField(max_length=80, default="")
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return self.room_name + " " + self.address


class RoomHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    join_date = models.DateTimeField(auto_now=True)
    has_left = models.BooleanField(default=False)
    visited_room = models.ForeignKey(Room, on_delete=models.CASCADE)

    @staticmethod
    def getCurrentListeners(room, time="1970-01-01T00:00+00:00"):
        return RoomHistory.objects.filter(room=room, has_left=False, join_date__gt=time).user_set.all()

    @staticmethod
    def getVistedRooms(user, time="1970-01-01T00:00+00:00"):
        history = RoomHistory.objects.filter(user=user, join_date__gt=time)
        rooms = []
        for i in history:
            rooms.append(i.visited_room)

    def leaveRoom(self):
        self.has_left = True
        return self.has_left

    def __str__(self):
        return self.user.username
