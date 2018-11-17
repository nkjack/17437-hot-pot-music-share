import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from hot_pot_music_share.models import Room


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
        self.user = self.scope['user']
        print(self.room_name)
        self.is_host = Room.objects.get(name=self.room_name).owner == self.user

        print('connected user: {}, is_host = {}'.format(self.user, self.is_host))

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )

        # Join channel group for this single user
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name + '-' + str(self.user.username),
            self.channel_name,
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        print('consumers.receive: ' + str(text_data_json))
        if 'chat_message' in text_data_json:
            chat_text = text_data_json['chat_message']
            username = text_data_json['username']

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
                    'chat_text': chat_text,
                    'username': username,
                }
            )
        elif 'playback_message' in text_data_json:
            playback_info = text_data_json['playback_message']
            username = text_data_json['username']

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'playback_message',
                    'playback_info': playback_info,
                    'username': username,
                }
            )
        elif 'sync_request_message' in text_data_json:

            username = text_data_json['username']

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'sync_request_message',
                    'sync_request': '',
                    'from_username': username,
                }
            )
        elif 'sync_result_message' in text_data_json:

            print('broadcasting sync_result_message...')

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'sync_result_message',
                    'video_id': text_data_json['video_id'],
                    'position': text_data_json['position'],
                    'is_playing': text_data_json['is_playing'],
                }
            )

    # Receive chat message from room group
    def chat_message(self, event):
        print('chat_message handler called, event = ' + str(event))
        chat_text = event['chat_text']
        username = event['username']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'chat_text': chat_text,
            'username': username,
        }))

    # Receive playback message from room group
    def playback_message(self, event):
        print('playback_message handler called, event = ' + str(event))
        playback_info = event['playback_info']
        username = event['username']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'playback_info': playback_info,
            'username': username,
        }))

    # Receive sync request message
    def sync_request_message(self, event):
        # FIXME: Currently only the *owner* is handling sync requests
        if self.is_host:
            print('[{}] sync_request_message handler called, event = {}'.format(self.user, str(event)))

            username = event['from_username']

            # Send message to WebSocket
            self.send(text_data=json.dumps({
                'sync_request': '',
                'from_username': username,
            }))

    # Receve sync request message
    def sync_result_message(self, event):
        # FIXME: Currently only the *owner* is handling sync requests
        # Note: Host just sent out sync_result, so no point in handling this as the host
        if not self.is_host:
            print('[{}] sync_result handler called, event = {}'.format(self.user, str(event)))

            self.send(text_data=json.dumps({
                'sync_result': '',
                'video_id': event['video_id'],
                'position': event['position'],
                'is_playing': event['is_playing'],
            }))
