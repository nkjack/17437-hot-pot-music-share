from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from hot_pot.models import Room, Song, UserVotes
from hot_pot.views.room_helper import get_all_songs_from_playlist

@login_required
@transaction.atomic
def vote_up(request):
    room_id = request.POST['room_id'] # may not need it
    song_id = request.POST['song_id']
    user = request.user

    room = get_object_or_404(Room, pk=room_id)
    song = get_object_or_404(Song, song_id=song_id, song_room=room)

    # user = User.objects.get(pk=user_id)
    # song = Song.objects.get(pk=vote_id)
    # pl = Playlist.objects.get(pk=pl_id)

    rows = UserVotes.objects.filter(user=user, song=song)

    if rows.count() == 0:
        song.thumbs_up += 1
        user_vote = UserVotes(user=user, song=song)
        user_vote.save()
        song.save()
        # return JsonResponse(data={'status': 'true', 'message': 'voted up'})
        json = (room_id, request.user.id, "pool")
        return JsonResponse(data=json)
    else:
        return JsonResponse(status=404, data={'status': 'false', 'message': 'fail to vote up'})



@login_required
@transaction.atomic
def vote_down(request):
    room_id = request.POST['room_id']  # may not need it
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
        # return JsonResponse(data={'status': 'true', 'message': 'deleted vote'})
        return JsonResponse(data=json)
    else:
        return JsonResponse(status=404, data={'status': 'false', 'message': 'fail to delete vote'})


# def vote_count(request):
#     room_id = request.POST['room_id']  # may not need it
#     song_pk = request.POST['song_pk']  # not the youtube id but the django pk!
#     user = request.user
#
#     song = get_object_or_404(Song, pk=song_pk)
#     rows = UserVotes.objects.filter(user=user, song=song)
#
#     return rows.count()

# from django.db.models import Case, When, F, IntegerField
#
# Song.objects.annotate(f=Case(When(record__user=johnny,
#                                   then=F('record__value')),
#                              output_field=IntegerField())).order_by('id', 'name', 'f').distinct('id', 'name').values_list('name', 'f')

