# import json
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer
#
#
# class ChatConsumer(WebsocketConsumer):
#     async def connect(self):
#
#         self.room_name = self.scope['url_route']['kwargs']['id_roomname']
#         self.room_group_name = 'room_%s' % self.room_name
#
#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.accept()
#         # self.accept()
#
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#
#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )
#
#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event['message']
#
#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))
#

from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer

consumer_object_list = []


class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        # Автоматически запускается, когда клиент запрашивает ссылку
        print('Запросить ссылку')
        self.accept()
        # Установите ссылку и автоматически помогите вам поддерживать каждого клиента
        # Сохранить ссылку в списке
        consumer_object_list.append(self)

    def websocket_receive(self, message):
        # Клиент отправляет данные для автоматического запуска
        print(message)
        text = message.get('text')
        # # Отправить сообщение клиенту отдельно
        # self.send(text_data=text)

        # Отправлять данные всем связанным объектам
        for obj in consumer_object_list:
            obj.send(text_data=text)

    def websocket_disconnect(self, message):
        # Автоматически запускается после отключения клиента
        print('Неработающей ссылке')
        # После отключения клиента текущий объект должен быть удален
        consumer_object_list.remove(self)
        raise StopConsumer()
