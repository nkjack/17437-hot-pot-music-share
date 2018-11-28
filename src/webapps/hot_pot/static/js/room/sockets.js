/****************************************** SOCKET SETUP ******************************************************/
const roomId = $('input#room_id').val();

const wsStart = (window.location.protocol === "https:") ? "wss://" : "ws://";
const wsUrl = wsStart + window.location.host +
    '/ws/room/' + roomId + '/';
console.log('Creating WebSocket on URL: ' + wsUrl);
const socket = new ReconnectingWebSocket(wsUrl);


let sentSyncRequestTime;  // TODO: Possible synchronize playback with RTT/2 (but didn't work well in practice)

// On socket message received
socket.onmessage = function (e) {

    const data = JSON.parse(e.data);

    if ('chat_text' in data) {
        // This is a chat message, add to chat box
        const chat_text = data['chat_text'];
        const username = data['username'];

        // Append chat message
        $('#chat-log').append(`<span class="chat-msg"><strong>${username}: </strong>${chat_text}<br></span>`);

        // Scroll the window to the bottom every time new message is received
        const objDiv = document.getElementById("chat-log");
        objDiv.scrollTop = objDiv.scrollHeight;

        // Pulsate chat tab if chat tab isn't focused
        const chatTab = $('#nav-chat-tab');
        if (chatTab.attr('aria-selected') === 'false') {
            chatTab.addClass('chat-tab-pulse');
        }

    } else if ('sync_request' in data) {
        // This is a sync request from a Listener, Host should sync Listeners now
        console.log('Received sync_request = ' + data + 'from username: ' + data['from_username']);

        if (data['from_dj'] === 'True') {
            syncSingleRequester(data['from_username']);
        } else {
            syncListeners();
        }


    } else if ('sync_result' in data) {
        // This is a sync result from Host, Listeners should sync-up
        console.log('Received sync_result...');


        // Play the correct video
        if (String(player.getVideoData()['video_id']) !== data['video_id']) {
            console.log("\tChanging my video and going to new position + offset...");

            player.stopVideo();
            offset = getNetworkOffset(sentSyncRequestTime);
            player.cueVideoById(data['video_id'], data['position'] + offset);

        } else if (String(player.getCurrentTime()) !== data['position']) {
            console.log("\tCorrect video, but going to new position + offset...");

            // Otherwise, correct video - just jump to correct offset
            offset = getNetworkOffset(sentSyncRequestTime);
            player.seekTo(parseInt(data['position']) + offset);
        }

        // Play the video, if needed
        if (data['is_playing'] === 'true' && player.getPlayerState() != YT.PlayerState.PLAYING) {
            console.log("\tHost is playing and I am not, so I will play...");
            player.playVideo();

        } else if (data['is_playing'] === 'false' && player.getPlayerState() != YT.PlayerState.PAUSED) {
            console.log("\tHost is not playing and I am, so I will pause...");
            player.pauseVideo();
        }

        // Set global timestamp of last time this user received a 'sync with me' request
        lastTimeSyncdUp = window.performance.now();
    }
};

// On socket closed
socket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};
