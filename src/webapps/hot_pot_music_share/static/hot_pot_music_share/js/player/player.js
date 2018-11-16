var roomName = {
{
    room_name_json
}
}
;

var socket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/player/' + roomName + '/');

socket.onmessage = function (e) {
    var data = JSON.parse(e.data);

    if ('chat_text' in data) {
        var chat_text = data['chat_text'];
        document.querySelector('#chat-log').value += (chat_text + '\n');
    } else if ('playback_info' in data) {
        var playback_info = data['playback_info'];

        console.log('Received playback_info = ' + playback_info);

        // if (playback_info.startsWith('play:')) // }
        if (playback_info === 'play') {
            // Start playing if paused
            // const position = parseInt(playback_info.split(':')[1]);#}
            // player.seekTo(seconds = position, allowSeekAhead = true);#}

            player.playVideo();

        } else if (playback_info === 'pause') {
            player.pauseVideo();

        } else if (playback_info.startsWith('seek:')) {
            console.log('entered SEEK case...');
            const position = parseInt(playback_info.split(':')[1]);
            player.seekTo(seconds = position, allowSeekAhead = true);
        }
    }

};

socket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function (e) {
    var messageInputDom = document.querySelector('#chat-message-input');
    var message = messageInputDom.value;
    socket.send(JSON.stringify({
        'chat_message': message
    }));

    messageInputDom.value = '';
};

// YOUTUBE#}

// 2. This code loads the IFrame Player API code asynchronously.
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// 3. This function creates an <iframe> (and YouTube player)
//    after the API code downloads.
var player;

function onYouTubeIframeAPIReady() {
    player = new YT.Player('player', {
        height: '390',
        width: '640',
        videoId: '9_k_goMr5ZI',
        playerVars: {
            'start': 0,
        },
        events: {
            // 'onReady': onPlayerReady,#}
            // 'onStateChange': onPlayerStateChange#}
        }
    });
}

// 4. The API will call this function when the video player is ready.
function onPlayerReady(event) {
    event.target.playVideo();

    /// Time tracking starting here

    var lastTime = -1;
    var interval = 1000;

    var checkPlayerTime = function () {
        if (lastTime != -1) {
            if (player.getPlayerState() == YT.PlayerState.PLAYING) {
                var currPosition = player.getCurrentTime();

                //console.log(Math.abs(t - lastTime -1));

                ///expecting 1 second interval , with 500 ms margin
                if (Math.abs(currPosition - lastTime - 1) > 0.5) {
                    // there was a seek occuring
                    console.log("Seeked to " + currPosition); /// fire your event here !

                    socket.send(JSON.stringify({
                        'playback_message': 'seek:' + currPosition
                    }));
                }
            }
        }
        lastTime = player.getCurrentTime();
        setTimeout(checkPlayerTime, interval); /// repeat function call in 1 second
    }
    setTimeout(checkPlayerTime, interval); /// initial call delayed
}

function onPlayerStateChange(event) {
    const playerStatus = event.data;

    // Send message via sockets
    switch (playerStatus) {
        case YT.PlayerState.PLAYING:
            console.log("onPlayerStateChange, case: YT.PlayerState.PLAYING");
            break;
        case YT.PlayerState.PAUSED:
            console.log("onPlayerStateChange, case: YT.PlayerState.PAUSED");
            break;
        case YT.PlayerState.BUFFERING:
            console.log("onPlayerStateChange, case: YT.PlayerState.BUFFERING");
            // Do nothing.
            break;
        case YT.PlayerState.CUED:
            console.log("onPlayerStateChange, case: YT.PlayerState.CUED");
            // Do nothing.
            break;
        case YT.PlayerState.ENDED:
            console.log("onPlayerStateChange, case: YT.PlayerState.ENDED");
            // TODO: Start playing next song in the queue
            break;
    }
}

function stopVideo() {
    player.stopVideo();
}

function playVideo() {
    // Play own video first
    player.playVideo();

    // Send message via sockets
    socket.send(JSON.stringify({
        'playback_message': 'play'
    }));
}

function pauseVideo() {
    // Pause own video first
    player.pauseVideo();

    // Send message via sockets
    socket.send(JSON.stringify({
        'playback_message': 'pause'
    }));
}

function seekTo(number) {
    player.seekTo(seconds = number, allowSeekAhead = true);

    const playback_message = 'seek:' + number;
    console.log('seek sending, msg = ' + playback_message);

    // Send message via sockets
    socket.send(JSON.stringify({
        'playback_message': 'seek:' + number
    }));
}