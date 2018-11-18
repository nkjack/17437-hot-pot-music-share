import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from hot_pot_music_share.models import Room, Song, Playlist


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

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'sync_result_message',
                    'video_id': text_data_json['video_id'],
                    'position': text_data_json['position'],
                    'is_playing': text_data_json['is_playing'],
                }
            )

        elif 'add_to_song_queue_message' in text_data_json or 'add_to_song_pool_message' in text_data_json:
            playlist = 'queue' if 'add_to_song_queue_message' in text_data_json else 'pool'
            print('add_to_song_[queue|pool]_message received on backend')

            # Create new song
            # FIXME: Creating replicate songs... Exact same song_id and song_name... But in DB have diff pk's... OK?
            new_song = Song.objects.create(song_id=text_data_json['song_id'], song_name=text_data_json['song_name'])
            new_song.save()

            # Add to room's song queue, if it doesn't exist
            room = Room.objects.get(name=self.room_name)

            song_queue = Playlist.objects.get(belongs_to_room=room, pl_type="queue")
            song_pool = Playlist.objects.get(belongs_to_room=room, pl_type="pool")

            # IMPORTANT: Only add the song if it doesn't already exist - otherwise multiple values for same key
            if playlist is 'queue' and not song_queue.songs.filter(song_id=new_song.song_id).exists():
                print('Created and added new song: ' + str(new_song) + ' to queue')
                song_queue.songs.add(new_song)
            elif playlist is 'pool' and not song_pool.songs.filter(song_id=new_song.song_id).exists():
                print('Created and added new song: ' + str(new_song) + ' to pool')
                song_pool.songs.add(new_song)

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

    # Receive sync request message
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
