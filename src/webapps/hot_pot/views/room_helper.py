
from django.db import connection


def sql_get_all_songs_from_playlist(room_id, user_id, pl_type):
    # sql for songs with user
    c = connection.cursor()
    query = "SELECT s.song_id, s.song_name, s.thumbs_up, " \
            "case when v.user_id is NULL then 'False' else 'True' end " \
            "FROM hot_pot_song s " \
            "LEFT OUTER JOIN hot_pot_uservotes v " \
            "ON (s.id = v.song_id AND v.user_id = {}) " \
            "JOIN hot_pot_playlist_songs pls " \
            "ON (pls.song_id = s.id)" \
            "JOIN hot_pot_playlist pl " \
            "ON (pl.id = pls.playlist_id AND pl.pl_type = '{}')" \
            "WHERE s.song_room_id = {} " \
            "ORDER BY s.thumbs_up DESC ".format(user_id, pl_type,room_id)

    s = c.execute(query)
    # s = c.execute("select pl.song_id, pl.playlist_id, pl.id from hot_pot_playlist_songs pl")
    data = {}
    data['songs'] = []
    for s in s.fetchall():
        song = {}
        song['id'] = s[0]
        song['name'] = s[1]
        song['thumbs_up'] = s[2]
        song['is_voted'] = s[3]

        data['songs'].append(song)

    return data