from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from hot_pot.forms import RoomForm
from hot_pot.models import Room, RoomHistory, Song, Playlist, Marker


@login_required
def home(request, username):
    context = {'title': 'home', 'error': ''}
    context['username'] = username
    user_from_url = get_object_or_404(User, username=username)

    if (request.method == "GET"):
        context['form'] = RoomForm(initial={'owner': request.user})

        popular_rooms = Room.objects.all().order_by('thumbs_up')[:6]
        context["popular"] = popular_rooms

        print(popular_rooms)
        return render(request, 'home.html', context)

    elif (request.POST.get('create_room')):
        form = RoomForm(request.POST, request.FILES, initial={'owner': request.user})
        context['form'] = form

    if form.is_valid():
        print("Creating Room...")
        new_room = Room.objects.create(owner=request.user,
                                       name=form.cleaned_data['name'],
                                       description=form.cleaned_data['description'],
                                       cover_pic=form.cleaned_data['cover_pic']
                                       )
        new_room.save()
        new_history = RoomHistory.objects.create(user=request.user,
                                                 visited_room=new_room)
        new_history.save()

        # DEMO SONGS TODO: Delete later
        song_1 = Song.objects.create(song_id='JQbjS0_ZfJ0',
                                     song_name='Kendrick Lamar, SZA - All The Stars',
                                     song_room=new_room)
        song_1.save()
        song_2 = Song.objects.create(song_id='09R8_2nJtjg',
                                     song_name='Maroon 5 - Sugar',
                                     song_room=new_room)
        song_2.save()
        song_3 = Song.objects.create(song_id='nfWlot6h_JM',
                                     song_name='Taylor Swift - Shake It Off',
                                     song_room=new_room)
        song_3.save()

        song_pool = Playlist.objects.create(belongs_to_room=new_room, pl_type="pool")
        song_pool.save()
        song_queue = Playlist.objects.create(belongs_to_room=new_room, pl_type="queue")

        # song_queue.songs.add(song_1)
        # song_queue.songs.add(song_2)
        # song_queue.songs.add(song_3)

        song_queue.save()

        # DEMO RANDOM LOCATION TODO: Delete later
        import random
        lat = random.uniform(0, 1) + 40
        lng = random.uniform(0, 1) - 80
        m = Marker.objects.create(lat=lat, lng=lng, room=new_room)
        m.save()
        # 40.440624, -79.995888 pitt

        return HttpResponseRedirect(reverse('room', args=[new_room.pk]))
    else:
        return render(request, 'home.html', context)


@login_required
def room_history(request):
    context = {'owned': '', 'visited': '', 'username': request.user.username}
    if request.method == 'GET':
        owned = Room.objects.filter(owner=request.user)
        history = RoomHistory.get_visit_history(request.user)

        context['owned'] = owned
        context['visited'] = history

    return render(request, 'room_history.html', context)
