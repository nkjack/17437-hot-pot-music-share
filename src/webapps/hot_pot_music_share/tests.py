from django.test import TestCase
# from django.test import Client

from django.contrib.auth.models import User
from hot_pot_music_share.models import Room, Song, Playlist, Vote, Profile # , DjUser



# Create your tests here.
class ProfileTestCase(TestCase):
    def setUp(self):
        new_user = User.objects.create_user(username="noam", \
                                            password="pass",
                                            first_name="noam",
                                            last_name="kahan",
                                            email="n@gmail.com")
        new_user.profile.spotify_id = 1111

    def test_create_profile(self):
        p = User.objects.get(username="noam")
        self.assertEqual(p.username,"noam")
        # self.assertEqual(p.password, "")
        self.assertEqual(p.first_name, "noam")
        self.assertEqual(p.last_name, "kahan")
        self.assertEqual(p.email, "n@gmail.com")


class Room(TestCase):
    def setUp(self):
        Room.objects.create(name="room_1", location="test_1", place="test_1",)
        # Student.objects.create(name="cat", sound="meow")
        # self.client = Client()

        def test_create_room(self):
            nkahan = Room.objects.get(name="room_1")

            self.assertEqual(nkahan.name, "room_1")
            self.assertEqual(nkahan.location, "test_1")
            self.assertEqual(nkahan.place, "test_1")

class Playlist(TestCase):
    playlist = None

    def setUp(self):
        global playlist

        # Create a dummy room
        Room.objects.create(name="room_1", location="test_1", place="test_1",)

        # Create the playlist
        playlist = Playlist(belongs_to_room=Room.objects.get(name="room_1"))
        playlist.save()

    def test_create_simple(self):
        global playlist

        expected = ['66kQ7wr4d2LwwSjr7HXcyr']
        playlist.set_songs(expected)

        result = playlist.get_songs()

        self.assertEquals(expected, result)