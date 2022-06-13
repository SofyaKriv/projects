from django.urls import re_path

import app.consumers

websocket_urlpatterns = [
    re_path(r':^chat/rooms/(?P<room_name>\w+)/$', app.consumers.ChatConsumer.as_asgi()),
]
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.conf.urls import url
# from app import consumers
#
# application = ProtocolTypeRouter({
#     'websocket': URLRouter([
#         # маршрутизация, связанная с websocket
#         url(r'^chat/rooms', consumers.ChatConsumer)
#     ])
# })
