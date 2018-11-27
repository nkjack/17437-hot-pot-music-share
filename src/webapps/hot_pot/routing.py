# chat/routing.py
from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/room/(?P<room_name>[^/]+)/$', consumers.PlayerConsumer),
]