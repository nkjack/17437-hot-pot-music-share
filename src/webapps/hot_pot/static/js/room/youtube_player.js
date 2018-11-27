/****************************************** YOUTUBE PLAYER ****************************************************/
var isHost = $('input#is_host').val() === "True";

ytApiKey = 'AIzaSyC6zJT9fu29Wj6T67uRxfnQvc9kyP4wz3Y'; // Youtube API Key
billboardPlaylistId = 'PL55713C70BA91BD6E'; // Top 200 Billboard songs (to play as fallback)

// 2. This code loads the IFrame Player API code asynchronously.
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// 3. This function creates an <iframe> (and YouTube player)  after the API code downloads.
var player;

function onYouTubeIframeAPIReady() {
    const videoId = getTopOfSongQueue();
    console.log("onYouTubeIframeAPIReady - videoId = " + videoId);

    // Different listeners depending on host or listener
    var events;
    if (isHost) {
        events = {
            'onStateChange': onHostPlayerStateChange
        }
    } else {
        events = {
            'onStateChange': onListenerPlayerStateChange,
            'onReady': onPlayerReady
        }
    }

    if (videoId == null) {
        console.log('No songs in the queue, playing Billboard playlist...');
        const randomIndex = getRandom(0, 200);

        player = new YT.Player('player', {
            height: '293',
            width: '480',
            playerVars: {
                'start': 0,
                'listType': 'playlist',
                'list': billboardPlaylistId,
                'index': randomIndex,
            },
            events: events
        });

        playRandomTrack();
    } else {
        player = new YT.Player('player', {
            height: '293',
            width: '480',
            videoId: videoId,
            playerVars: {
                'start': 0,
            },
            events: events
        });
    }

}

// 4. The API will call this function when the video player is ready.
function onPlayerReady(event) {
    // Listeners ask to sync-up to Host when their player is ready (when they first join the room)
    syncToHost();
}

function onHostPlayerStateChange(event) {
    const playerStatus = event.data;

    switch (playerStatus) {
        case YT.PlayerState.PLAYING:
            console.log("onHostPlayerStateChange, case: YT.PlayerState.PLAYING");

            // Highlight currently playing song
            //const currVideoId = cleanVideoIdInput(String(player.getVideoUrl()));
            //$(`#song_queue_${currVideoId}`).css('background-color', 'yellow');

            break;
        case YT.PlayerState.PAUSED:
            console.log("onHostPlayerStateChange, case: YT.PlayerState.PAUSED");
            break;
        case YT.PlayerState.BUFFERING:
            console.log("onHostPlayerStateChange, case: YT.PlayerState.BUFFERING");
            break;
        case YT.PlayerState.CUED:
            console.log("onHostPlayerStateChange, case: YT.PlayerState.CUED");
            break;
        case YT.PlayerState.ENDED:
            console.log("onHostPlayerStateChange, case: YT.PlayerState.ENDED");
            // TODO: Start playing next song in the queue
            // Delete currently playing song from queue and play next one
            nextVideo();
            break;
    }

    // Host syncs up Listeners whenever Host's player state changes
    syncListeners();
    return;
}

function onListenerPlayerStateChange(event) {
    const playerStatus = event.data;

    switch (playerStatus) {
        case YT.PlayerState.PLAYING:
            console.log("onListenerPlayerStateChange, case: YT.PlayerState.PLAYING");

            // Highlight currently playing song
            //const currVideoId = cleanVideoIdInput(String(player.getVideoUrl()));
            //$(`#song_queue_${currVideoId}`).css('background-color', 'yellow');

            break;
    }
}

// Host will call this function so Listeners will sync
function syncListeners() {
    var currPosition = player.getCurrentTime();

    socket.send(JSON.stringify({
        'sync_result_message': '',
        'video_id': String(player.getVideoData()['video_id']),
        'position': currPosition,
        'is_playing': String(player.getPlayerState() === YT.PlayerState.PLAYING),
    }));

    console.log('Host sent back sync_result');
}

// Listener will call this function to ask Host for video information
function syncToHost() {
    // Send message via socket
    socket.send(JSON.stringify({
        'sync_request_message': '',
        'username': $('input#username').val(),
    }));

    sentSyncRequestTime = window.performance.now();
}

// Helper function get offset in seconds
function getNetworkOffset(startTime) {
    //return (window.performance.now() / startTime) / 2 / 1000;

    /* FIXME: 0.3 - 0.5 seems to be the average offset... But is there a better way?
     * Main issue is that Listener will:
     *  1) Receive offset
     *  2) Start BUFFERING...
     *  3) Start PLAYING...
     *
     *  Cannot know how long the 'BUFFERING' state will take in the future...
     */
    return 0.5;
}

// Helper function to clean up video input from URL/ID to just ID
function cleanVideoIdInput(input) {
    console.log('cleanVideoIdInput input: ' + input);
    var videoId = input;
    console.log('cleanVideoIdInput videoId: ' + videoId);

    // It's okay if they input a URL
    if (videoId.includes('youtube.com')) {
        videoId = input.split('v=')[1];
        console.log('\tcleanVideoIdInput videoId: ' + videoId);
    } else if (videoId.includes('youtu.be')) {
        // Shortened URL form: https://youtu.be/JQbjS0_ZfJ0
        videoId = input.split('.be/')[1];
        console.log('\tcleanVideoIdInput videoId: ' + videoId);
    }

    // If there are other URL parameters
    if (videoId.includes('&')) {
        videoId = videoId.substr(0, videoId.indexOf('&'));
    }

    return videoId;
}

// Change video to submitted video
function changeVideoSubmit() {
    const input = document.getElementById('video-id-input').value;
    const videoId = cleanVideoIdInput(input);

    changeVideoById(videoId);
}

/*
                <button onclick="addToSongQueue()">Add to Song Queue</button><br>
    { endif %}

    <!-- Both Hosts and Listeners can add to Song Pool -->
    Video ID or URL:
    <input id="add-to-song-pool-input" type="text" size="10"/>
    <button onclick="addToSongPool()">Add to Song Pool</button>
*/

function addToSongQueue() {
    const input = document.getElementById('add-to-song-queue-input').value;
    const videoId = cleanVideoIdInput(input);

    // Clear the input
    document.getElementById('add-to-song-queue-input').value = '';

    // Get Song Title
    const videoTitle = getVideoTitleFromId(videoId);

    // Update Django DB via sockets
    socket.send(JSON.stringify({
        'add_to_song_queue_message': '',
        'song_id': videoId,
        'song_name': videoTitle,
    }));

    // Give success message
    if (videoTitle) {
        $("#direct-input-success").css({"color": "#31c122"});
        $("#direct-input-success").text("Successfully added " + videoTitle);
    }

    // Sync up song queue
    get_queue_songs_from_room();
}

function addToSongPool() {
    const input = document.getElementById('add-to-song-pool-input').value;
    const videoId = cleanVideoIdInput(input);

      // Clear the input
    document.getElementById('add-to-song-pool-input').value = '';

    // Get Song Title
    const videoTitle = getVideoTitleFromId(videoId);

    // Update Django DB via sockets
    socket.send(JSON.stringify({
        'add_to_song_pool_message': '',
        'song_id': videoId,
        'song_name': videoTitle,
    }));

    // Give success message
    if (videoTitle) {
        $("#direct-input-success").css({"color": "#31c122"});
        $("#direct-input-success").text("Successfully added " + videoTitle);
    }

    // Sync up song pool
    get_pool_songs_from_room();
}

// Helper function to get youtube song title from ID
function getVideoTitleFromId(videoId) {
    var videoTitle;
    $.ajax({
        async: false, // Wait for GET request to finish to return song title
        type: 'GET',
        url: "https://www.googleapis.com/youtube/v3/videos?part=snippet&id=" + videoId + "&key=" + ytApiKey,
        success: function (data) {
            videoTitle = data.items[0].snippet.title;
            console.log('new videoTitle: ' + videoTitle);
        }
    });

    console.log('returning videoTitle: ' + videoTitle);
    return videoTitle;
}


// Helper function to change the player itself to the new video ID
function changeVideoById(videoId) {
    player.stopVideo();
    player.cueVideoById(videoId);
    player.playVideo();
}

// On the event the Host wants to go to the next video OR end of currently playing video
function nextVideo() {
    // Make GET request to delete song from top of song queue
    const currVideoId = cleanVideoIdInput(String(player.getVideoUrl()));
    if (!player.getPlaylist()) {
        // Only attempt to delete from song queue if not playing the fallback playlist
        deleteFromSongQueue(currVideoId);
    }

    // Make GET request to get top song
    const videoId = getTopOfSongQueue();

    if (videoId) {
        // Got a video from the queue
        changeVideoById(videoId);

    } else if (player.getPlaylist()) {
        // Didn't get a video from the queue, and playing the fallback playlist
        console.log('Still no songs in the queue, playing next song in Billboard playlist...');

        playRandomTrack();
    } else {
        // Didn't get a video from the queue, start the fallback playlist
        console.log('No songs in the queue, loading and playing Billboard playlist...');

        player.stopVideo();

        player.stopVideo();

        const randomIndex = getRandom(0, 200);

        player.loadPlaylist({
            listType: 'playlist',
            list: billboardPlaylistId,
            index: randomIndex,
        });

        player.playVideo();
    }

    // Sync up song queue
    get_queue_songs_from_room();
}

// Make GET call to 'delete-from-song-queue'
function deleteFromSongQueue(videoId) {
    $.ajax({
        async: false, // Wait for GET request to finish
        url: '/delete-from-song-queue/' + $('input#room_id').val() + '/' + videoId,
        type: "GET",
    })
        .done(function (data, statusText, xhr) {
            if (xhr.status === 204) {
                // Means NO more songs in the queue
                return;
            }
            videoId = String(data.id);
            videoName = String(data.name);

            console.log("Got delete-from-song-queue response: " + videoId + ", " + videoName);
        })
        .fail(function (xhr, status, errorThrown) {
            console.log("Error: " + errorThrown);
            console.log("Status: " + status);
            console.dir(xhr);
        });
}

// Make GET call to 'get-top-of-song-queue'
function getTopOfSongQueue() {
    var videoId;
    $.ajax({
        async: false, // Wait for GET request to finish
        url: '/get-top-of-song-queue/' + $('input#room_id').val(),
        type: "GET",
        dataType: "json",
    })
        .done(function (data, statusText, xhr) {
            if (xhr.status === 204) {
                // Means NO more songs in the queue
                console.log('Got get-top-of-song-queue response: NONE');
                return false;
            }

            videoId = String(data.id);
            videoName = String(data.name);

            console.log("Got get-top-of-song-queue response: " + videoId + ", " + videoName);
        })
        .fail(function (xhr, status, errorThrown) {
            console.log("Error: " + errorThrown);
            console.log("Status: " + status);
            console.dir(xhr);
        });

    return videoId;
}

// Get random integer in range
var getRandom = function (min, max) {
    return Math.floor(Math.random() * (max - min) + min);
};

// Helper function to play random video in the playlist
function playRandomTrack() {
    const randomIndex = getRandom(0, 200);
    console.log('playRandomTrack at randomIndex:' + randomIndex);
    player.playVideoAt(randomIndex);
};