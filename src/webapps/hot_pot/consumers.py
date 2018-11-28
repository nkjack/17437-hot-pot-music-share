import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from hot_pot.models import Room, Song, Playlist
from hot_pot.views.room_helper import user_is_dj
from hot_pot.views.room_views import add_user_to_room, remove_user_from_room


class PlayerConsumer(WebsocketConsumer):
    def connect(self):
        """
        self.scope[‘url_route’][‘kwargs’][‘room_id’]
        Obtains the 'room_id' parameter from the URL route in chat/routing.py that opened the WebSocket connection to
        the consumer.
        Every consumer has a scope that contains information about its connection, including in particular any positional
        or keyword arguments from the URL route and the currently authenticated user if any.
        """
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'room_%s' % self.room_id
        self.user = self.scope['user']
        self.is_dj = user_is_dj(self.user, Room.objects.get(id=self.room_id))

        print('[consumers.py] Connected user: {}, is_dj = {}'.format(self.user, self.is_dj))

        # Call views function to add user to the room
        add_user_to_room(self.user.username, self.room_id)

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
        print("[consumers.py] User %s disconnected from the room" % self.user.username)

        # Call views function to remove user from the room
        remove_user_from_room(self.user.username, self.room_id)

        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)

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

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'sync_request_message',
                    'sync_request': '',
                    'from_username': text_data_json['from_username'],
                    'from_dj': text_data_json['from_dj'],
                }
            )
        elif 'sync_result_message' in text_data_json:
            # Send sync result to everyone or just the single requester
            if text_data_json['broadcast'].lower() == 'true':
                channel_group_name = self.room_group_name
            else:
                channel_group_name = self.room_group_name + '-' + text_data_json['request_from']

            async_to_sync(self.channel_layer.group_send)(
                channel_group_name,
                {
                    'type': 'sync_result_message',
                    'video_id': text_data_json['video_id'],
                    'position': text_data_json['position'],
                    'is_playing': text_data_json['is_playing'],
                    'request_from': text_data_json['request_from'],
                    'from_username': text_data_json['from_username'],
                    'djs_ignore': text_data_json['djs_ignore'],
                }
            )

        elif 'add_to_song_queue_message' in text_data_json or 'add_to_song_pool_message' in text_data_json:
            playlist = 'queue' if 'add_to_song_queue_message' in text_data_json else 'pool'

            # Get the room to associate the song with and get the queue/pool
            room = Room.objects.get(id=self.room_id)

            # Don't create the song if it already exists in room
            if not Song.objects.filter(song_id__exact=text_data_json['song_id'],
                                       song_room=room):
                new_song = Song.objects.create(song_id=text_data_json['song_id'],
                                               song_name=text_data_json['song_name'],
                                               song_room=room)
                new_song.save()

            # Whether we created the new song or already existed, get the song
            song = Song.objects.get(song_id=text_data_json['song_id'], song_room=room)

            song_queue = Playlist.objects.get(belongs_to_room=room, pl_type="queue")
            song_pool = Playlist.objects.get(belongs_to_room=room, pl_type="pool")

            # IMPORTANT: Only add the song if it doesn't already exist - otherwise multiple values for same key
            if playlist is 'queue' and not song_queue.songs.filter(song_id=song.song_id).exists():
                song_queue.songs.add(song)

                # Make sure song goes to bottom of the queue
                song.rank = song_queue.songs.all().count()
                song.save()

            elif playlist is 'pool' and not song_pool.songs.filter(song_id=song.song_id).exists():
                song_pool.songs.add(song)

    # Receive chat message from room group
    def chat_message(self, event):
        print('[consumers.py] chat_message handler called, event = ' + str(event))
        chat_text = event['chat_text']
        username = event['username']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'chat_text': chat_text,
            'username': username,
        }))

    # Receive playback message from room group
    def playback_message(self, event):
        print('[consumers.py] playback_message handler called, event = ' + str(event))
        playback_info = event['playback_info']
        username = event['username']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'playback_info': playback_info,
            'username': username,
        }))

    # Receive sync request message
    def sync_request_message(self, event):
        print('[consumers.py][%s] sync_request_message handler called, event = %s' % (self.user, str(event)))

        # Only DJ(s) send out sync requests (requests sent to multiple DJs - but OK in practice)
        if self.is_dj and event['from_username'] != self.user.username:  # Don't handle own request
            # Send message to WebSocket
            self.send(text_data=json.dumps({
                'sync_request': '',
                'from_username': event['from_username'],
                'from_dj': event['from_dj'],
            }))

    # Receive sync request message
    def sync_result_message(self, event):
        print('[consumers.py][%s] sync_result_message handler called, event = %s' % (self.user, str(event)))

        # Ignore this if I'm a DJ and packet says to ignore as a DJ
        if self.is_dj and (event['djs_ignore'] == 'true'):
            return

        # Listen to any sync_result that wasn't from myself
        if event['from_username'] != self.user.username:
            self.send(text_data=json.dumps({
                'sync_result': '',
                'video_id': event['video_id'],
                'position': event['position'],
                'is_playing': event['is_playing'],
                'request_from': event['request_from'],
            }))
