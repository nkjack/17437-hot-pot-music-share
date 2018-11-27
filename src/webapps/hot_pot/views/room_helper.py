
from hot_pot.models import *


def get_all_songs_from_playlist(room_id, user_id, pl_type):
    room = Room.objects.get(id=room_id)
    song_pool = Playlist.objects.get(belongs_to_room=room, pl_type=pl_type)

    songs = song_pool.songs.all().order_by('-thumbs_up')
    data = {}
    data['songs'] = []

    for song in songs:
        user = User.objects.get(id=user_id)
        rows = UserVotes.objects.filter(user=user, song=song)

        song_to_json = {}
        song_to_json['id'] = song.song_id
        song_to_json['name'] = song.song_name
        song_to_json['thumbs_up'] = song.thumbs_up

        if rows.count() > 0:
            song_to_json['is_voted'] = 'True'
        else:
            song_to_json['is_voted'] = 'False'
        data['songs'].append(song_to_json)

    return data

#
# from django.db import connection
# def sql_get_all_songs_from_playlist(room_id, user_id, pl_type):
#     # sql for songs with user
#     c = connection.cursor()
#     query = "SELECT s.song_id, s.song_name, s.thumbs_up, " \
#             "case when v.user_id is NULL then 'False' else 'True' end " \
#             "FROM hot_pot_song s " \
#             "LEFT OUTER JOIN hot_pot_uservotes v " \
#             "ON (s.id = v.song_id AND v.user_id = {}) " \
#             "JOIN hot_pot_playlist_songs pls " \
#             "ON (pls.song_id = s.id)" \
#             "JOIN hot_pot_playlist pl " \
#             "ON (pl.id = pls.playlist_id AND pl.pl_type = '{}')" \
#             "WHERE s.song_room_id = {} " \
#             "ORDER BY s.thumbs_up DESC ".format(user_id, pl_type,room_id)
#
#     s = c.execute(query)
#     # s = c.execute("select pl.song_id, pl.playlist_id, pl.id from hot_pot_playlist_songs pl")
#     data = {}
#     data['songs'] = []
#     for s in s.fetchall():
#         song = {}
#         song['id'] = s[0]
#         song['name'] = s[1]
#         song['thumbs_up'] = s[2]
#         song['is_voted'] = s[3]
#
#         data['songs'].append(song)
#
#     return data
#

# Helper function to check if a user is a DJ for the specified room
def user_is_dj(user, room):
    result = user in room.djs.all()
    print(">>>>> user_is_dj(user = %s, room = %s) called and returning %s", (user, room, result))
    return result