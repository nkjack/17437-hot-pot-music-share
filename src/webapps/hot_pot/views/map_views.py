from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import render

from hot_pot.forms import *


@login_required
def map_of_rooms(request):
    context = {'username': request.user.username}
    all_markers = Marker.objects.all()
    context['all_markers'] = all_markers
    return render(request, 'hot_pot/maps/room_map.html', context)


def add_marker(request):
    context = {}
    form = MarkerForm(request.POST)
    if not form.is_valid():
        print(form.errors)
        raise Http404

    form.save()
    all_markers = Marker.objects.all()
    context['all_markers'] = all_markers
    return JsonResponse(data={})


def get_markers(request):
    all_markers = Marker.objects.all()
    context = {'markers': all_markers}
    return render(request, 'hot_pot/maps/markers.json', context, content_type='application/json')
