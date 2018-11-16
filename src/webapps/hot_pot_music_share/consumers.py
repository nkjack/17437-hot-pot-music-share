from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

class PlayerConsumer(WebsocketConsumer):
    def connect(self):
        """
        self.scope[‘url_route’][‘kwargs’][‘room_name’]
        Obtains the 'room_name' parameter from the URL route in chat/routing.py that opened the WebSocket connection to
        the consumer.
        Every consumer has a scope that contains information about its connection, including in particular any positional
        or keyword arguments from the URL route and the currently authenticated user if any.
        """
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'room_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        print(text_data_json)
        if 'chat_message' in text_data_json:
            chat_text = text_data_json['chat_message']

            # Send message to room group
            """
            Sends an event to a group.
            An event has a special 'type' key corresponding to the name of the method that should be invoked on consumers 
            that receive the event.
            """
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'chat_text': chat_text
                }
            )
        elif 'playback_message' in text_data_json:
            playback_info = text_data_json['playback_message']

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'playback_message',
                    'playback_info': playback_info
                }
            )

    # Receive chat message from room group
    def chat_message(self, event):
        print('chat_message handler called')
        chat_text = event['chat_text']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'chat_text': chat_text
        }))

    # Receive playback message from room group
    def playback_message(self, event):
        print('playback_message handler called')
        playback_info = event['playback_info']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'playback_info': playback_info
        }))