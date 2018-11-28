from mimetypes import guess_type

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from hot_pot.forms import RoomForm, ProfileForm
from hot_pot.models import Room, RoomHistory, Playlist, Marker, Profile


@login_required
def home(request, username):
    context = {'title': 'home', 'error': '', 'username': username}

    if request.method == "GET":
        context['form'] = RoomForm(initial={'owner': request.user})

        popular_rooms = Room.objects.all().order_by('thumbs_up')[:6]
        context["popular"] = popular_rooms

        print(popular_rooms)
        return render(request, 'home.html', context)

    elif request.POST.get('create_room'):
        form = RoomForm(request.POST, request.FILES, initial={'owner': request.user})
        context['form'] = form

    if form.is_valid():
        print("Creating Room...")
        new_room = Room.objects.create(owner=request.user,
                                       name=form.cleaned_data['name'],
                                       description=form.cleaned_data['description'],
                                       cover_pic=form.cleaned_data['cover_pic'],
                                       is_hotpot_mode=form.cleaned_data['is_hotpot_mode'],
                                       )
        new_room.save()

        # Add self as a DJ
        new_room.djs.add(request.user)

        # Initialize and save history
        new_history = RoomHistory.objects.create(user=request.user,
                                                 visited_room=new_room)
        new_history.save()

        song_pool = Playlist.objects.create(belongs_to_room=new_room, pl_type="pool")
        song_pool.save()
        song_queue = Playlist.objects.create(belongs_to_room=new_room, pl_type="queue")

        song_queue.save()

        return HttpResponseRedirect(reverse('room', args=[new_room.id]))
    else:
        return render(request, 'home.html', context)


@login_required
def room_history(request):
    context = {'owned': '', 'history': '', 'username': request.user.username}
    owned = Room.objects.filter(owner=request.user)
    history = RoomHistory.get_visited_rooms(request.user)
    context['owned'] = owned
    context['history'] = history
    if request.method == 'GET':

        context['form'] = RoomForm(initial={'owner': request.user})


    elif request.POST.get('create_room'):
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

            # create a room history
            new_history = RoomHistory.objects.create(user=request.user,
                                                     visited_room=new_room)
            new_history.save()

            # create marker for the room
            import random
            lat = random.uniform(0, 1) + 40
            lng = random.uniform(0, 1) - 80
            m = Marker.objects.create(lat=lat, lng=lng, room=new_room)
            m.save()
            # 40.440624, -79.995888 pitt
            return HttpResponseRedirect(reverse('room', args=[new_room.id]))

    return render(request, 'room_history.html', context)


@login_required
def get_room_img(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if not room.cover_pic:
        raise Http404
    content_type = guess_type(room.cover_pic.name)
    return HttpResponse(room.cover_pic, content_type=content_type)


@login_required
def get_user_img(request, username):
    user_from_url = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user_from_url)
    if not profile.img:
        raise Http404
    content_type = guess_type(profile.img.name)
    return HttpResponse(profile.img, content_type=content_type)


@login_required
def edit_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    context = {'room': room, 'username': request.user.username, "room_id": room_id}
    if request.method == 'GET':
        room_form = RoomForm(instance=room)
        context['roomForm'] = room_form
        return render(request, 'hot_pot/profile/room_profile.html', context)

    elif request.POST.get('room_profile'):
        room_form = RoomForm(request.POST, request.FILES, instance=room)

        if room_form.is_valid():
            room_form.save()
            return HttpResponseRedirect(reverse('home', args=[request.user.username]))
        else:
            context['roomForm'] = room_form
            return render(request, 'profile/room_profile.html', context)
    else:
        context['error'] = 'Invalid Post Request'
        return render(request, 'hot_pot/profile/room_profile.html', context)


@login_required
def edit_user(request):
    context = {'username': request.user.username}
    if request.method == 'GET':
        profile_form = ProfileForm(instance=request.user.profile)
        owned = Room.objects.filter(owner=request.user)
        context['profileForm'] = profile_form
        context['owned'] = owned

        return render(request, 'hot_pot/profile/user_profile.html', context)

    elif request.POST.get("user_profile"):
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return HttpResponseRedirect(reverse('home', args=[request.user.username]))
        else:
            context['profileForm'] = profile_form
            return render(request, 'profile/user_profile.html', context)
    else:
        context['error'] = 'Invalid Post Request'
        return render(request, 'hot_pot/profile/user_profile.html', context)


@login_required
@transaction.atomic
def add_marker_to_room(request):
    room_id = request.POST['room_id']
    lat = request.POST['lat']
    lng = request.POST['lng']

    room = get_object_or_404(Room, id=room_id)

    m = Marker.objects.filter(room=room)
    if m.count() > 0:
        m.delete()

    m = Marker.objects.create(lat=lat, lng=lng, room=room)
    m.save()

    return JsonResponse(data={'status': 'true', 'message': 'updated location'})


@login_required
@transaction.atomic
def delete_marker_from_room(request):
    room_id = request.POST['room_id']

    room = get_object_or_404(Room, id=room_id)

    m = Marker.objects.filter(room=room)
    if m.count() > 0:
        m.delete()

    return JsonResponse(data={'status': 'true', 'message': 'deleted location'})
