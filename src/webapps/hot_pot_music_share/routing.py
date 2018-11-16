# chat/routing.py
from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/player/(?P<room_name>[^/]+)/$', consumers.PlayerConsumer),
]