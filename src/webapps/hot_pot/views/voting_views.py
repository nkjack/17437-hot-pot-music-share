from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from hot_pot.models import Room, Song, UserVotes
from hot_pot.views.room_helper import get_all_songs_from_playlist

@login_required
@transaction.atomic
def vote_up(request):
    room_id = request.POST['room_id']
    song_id = request.POST['song_id']
    user = request.user

    room = get_object_or_404(Room, pk=room_id)
    song = get_object_or_404(Song, song_id=song_id, song_room=room)

    rows = UserVotes.objects.filter(user=user, song=song)

    if rows.count() == 0:
        song.thumbs_up += 1
        user_vote = UserVotes(user=user, song=song)
        user_vote.save()
        song.save()
        json = get_all_songs_from_playlist(room_id, request.user.id, "pool")
        return JsonResponse(data=json)
    else:
        return JsonResponse(status=404, data={'status': 'false', 'message': 'fail to vote up'})


@login_required
@transaction.atomic
def vote_down(request):
    room_id = request.POST['room_id']
    song_id = request.POST['song_id']
    user = request.user

    room = get_object_or_404(Room, pk=room_id)
    song = get_object_or_404(Song, song_id=song_id, song_room=room)
    rows = UserVotes.objects.filter(user=user, song=song)

    if rows.count() > 0:
        rows.delete()
        song.thumbs_up -= 1
        song.save()
        json = get_all_songs_from_playlist(room_id, request.user.id, "pool")
        return JsonResponse(data=json)
    else:
        return JsonResponse(status=404, data={'status': 'false', 'message': 'fail to delete vote'})

# @login_required
# @transaction.atomic
# def thumb_up(request):
#     return HTTPResponse("")

# @login_required
# @transaction.atomic
# def thumb_down(request):
#     return HTTPResponse("")
