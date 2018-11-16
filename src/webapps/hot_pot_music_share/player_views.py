import json

from django.shortcuts import render
from django.utils.safestring import mark_safe


def youtube_player(request):
    return render(request, 'hot_pot_music_share/player/lobby.html')


def room(request, room_name):
    return render(request, 'hot_pot_music_share/player/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })
