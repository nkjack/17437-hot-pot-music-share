from django.db import models

# Create your models here.
"""
Models
HotSpot Music Share will have 7 main models:
- User
    - The default model of a user in django.
- ProfileUser
    - An extension of the User model to add more data for each user in our app. Every profile
	will have is favorite rooms, rooms she created and so on.
- Room
    - A room is active or not and related to a specific user manager.
	- Room is owned by a User.
	- Room has x amount of user with dj's privilege.
	- Room has it's own current pool of songs which being voted by users.
	- It has a list of suggestions from users.
	- Has a location (relevant if GPS is specified when room created).
- Song
    - A song is related to a specific rooms.
	- Has amount of votes from the room it belongs to.
- PlayList
    - This is a model to help us simplify the idea of collecting few songs into one group and link it to
	a dj user.
	- Each song will have a rank which will represent the songs order in the playlist.
- Vote
    - Vote is a model but will represent in the database as a table of votes.
	- Each vote is related to a specific user and a specific song in a certain pool.
- DJ
    - Extension of ProfileUser with ability to save a playlist for a particular room
Below is a rough Python draft of the above models.
"""


class ProfileUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    spotify_id =  ## foreginKey to spotify profile user
    picture = models.ImageField(upload_to="profile-photos", blank=True)

    favorite_rooms = models.ManyToManyField(room, related_name='favorite')
    my_rooms = models.ManyToManyField(Room, related_name='my_room')

    def __str__(self):
        return self.user.username


class DjUser(models.Model):
    user = models.OneToOneField(ProfileUser, on_delete=models.CASCADE)
    current_playlist = models.ForeignKey(Playlist)
    room = models.ForeignKey(Room)

    def __str__(self):
        return "{}, {}".format(user.username, room.name)


class Room(models.Model):
    name = models.CharField(max_length=42)
    user_manager = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)  # Some Google Maps API ID (e.g. coordinates)
    place = models.CharField(max_length=100)  # Some Google Places API ID (e.g. for a business)


    def __str__(self):
        return self.name


class Song(models.Model):
    spotify_song_id = models.CharField(max_length=100)  # song will probably have id link to a Spotify API

    song_name = models.CharField(max_length=42)
    votes_score = models.IntegerField()

    belongs_to_room = models.ForeignKey(Room, on_delete=models.CASCADE)
    is_in_pool = models.BooleanField()  # Boolean if song is in suggestions or in actual pool of a room


def __str__(self):
    return self.song_name


class Playlist(models.Model):
    belongs_to_user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_in_pool = models.BooleanField()  # Boolean if song is in suggestions or in actual pool of a room

    songs = models.ManyToManyField(Song, related_name='pl_songs')

    def __str__(self):
        return self.belongs_to_user.username


class Vote(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    vote = models.CharField(max_length=2)  # could be '-1', '0', or '+1'

    def __str__(self):
        return self.user.username


