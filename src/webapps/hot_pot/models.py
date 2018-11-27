from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=42)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner', blank=True)
    create_date = models.DateTimeField(auto_now=True)
    cover_pic = models.ImageField(upload_to='room-photo', blank=True,
                                  default='room-photo/logo.png',
                                  )
    description = models.TextField(max_length=420, blank=True,
                                   )
    isMarked = models.BooleanField(default=True, blank=True)

    thumbs_up = models.IntegerField(default=0)

    users = models.ManyToManyField(User, related_name='current_users') # Keep track of current users in the room

    # location = models.CharField(max_length=100)  # Some Google Maps API ID (e.g. coordinates)
    # place = models.CharField(max_length=100)  # Some Google Places API ID (e.g. for a business)
    # listeners = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class RoomHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    join_date = models.DateTimeField(auto_now=True)
    visited_room = models.ForeignKey(Room, on_delete=models.CASCADE)
    has_left = models.BooleanField(default=False)

    @staticmethod
    def get_current_listeners(room, time="1970-01-01T00:00+00:00"):
        history = RoomHistory.objects.filter(visited_room=room, has_left=False, join_date__gt=time)
        users = []
        for i in history:
            users.append(i.user)
        return users

    @staticmethod
    def get_visited_rooms(user, time="1970-01-01T00:00+00:00"):
        history = RoomHistory.objects.filter(user=user, join_date__gt=time)
        rooms = []
        for i in history:
            rooms.append(i.visited_room)
        return rooms

    @staticmethod
    def get_visit_history(user, time="1970-01-01T00:00+00:00"):
        return RoomHistory.objects.filter(user=user, join_date__gt=time)

    def leave_room(self):
        self.has_left = True
        return self.has_left

    @staticmethod
    def visited_before(user, room, new_time):
        try:
            history = RoomHistory.objects.get(user=user, visited_room=room)

            history.has_left = False
            history.join_date = new_time
            history.save()
            return True
        except ObjectDoesNotExist:
            return False

    def __str__(self):
        return self.user.username


class Song(models.Model):
    song_id = models.CharField(max_length=100)
    song_name = models.CharField(max_length=100)

    song_room = models.ForeignKey(Room, on_delete=models.CASCADE)
    thumbs_up = models.IntegerField(blank=True, default=0)

    rank = models.IntegerField(blank=True, default=0)
    # belongs_to_playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    # is_in_pool = models.BooleanField()  # Boolean if song is in suggestions or in actual pool of a room

    def __str__(self):
        return self.song_name


class Playlist(models.Model):
    belongs_to_room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # is_in_pool = models.BooleanField()  # Boolean if song is in suggestions or in actual pool of a room

    songs = models.ManyToManyField(Song, related_name='pl_songs')

    # Options: 'pool', 'queue'
    pl_type = models.CharField(max_length=20, default="", blank=True)

    def __str__(self):
        return self.belongs_to_room.name + '\'s song ' + self.pl_type


class UserVotes(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # room = models.ForeignKey(Room, on_delete=models.CASCADE) # Sam commented this out

    # vote = models.CharField(max_length=2)  # could be '-1', '0', or '+1'
    def __str__(self):
        return self.user.username


class Marker(models.Model):
    # id - django generate
    # address = models.CharField(max_length=80, default="")
    lat = models.FloatField()
    lng = models.FloatField()
    room = models.OneToOneField(Room, on_delete=models.CASCADE)

    def __str__(self):
        return ""
