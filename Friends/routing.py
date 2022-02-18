from django.urls import re_path

from .Consumers import *

websocket_urlpatterns = [
    re_path(r'^ws/friend-request-notification/$', FriendRequestConsumer.as_asgi()),
]
