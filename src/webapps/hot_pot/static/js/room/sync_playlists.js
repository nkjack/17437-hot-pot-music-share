function get_pool_songs_from_room() {
    var room_id = $("#room_id").attr('value');
    // console.log(room_id);
    $.ajax({
        // The URL for the request
        url: "/get-pool-songs-from-room",

        // The data to send (will be converted to a query string)
        data: {
            room_id: room_id
        },

        // Whether this is a POST or GET request
        type: "GET",

        // The type of data we expect back
        dataType: "json",
    })
        .done(function (json) {
            updateChangesPoolSongs(json)
        })
        .fail(function (xhr, status, errorThrown) {
            console.log("Sorry, there was a problem!");
            console.log("Error: " + errorThrown);
            console.log("Status: " + status);
            console.dir(xhr);
        })
        // Code to run regardless of success or failure;
        .always(function (xhr, status) {
            // console.log("The request is complete!");
            // console.alert( "The request is complete!" );
        });
}

function updateChangesPoolSongs(data) {
    // console.log(data);
    $("#poll_list").empty();
    for (var i = 0; i < data.songs.length; i++) {
        var v_id = data.songs[i]['id'];
        var v_name = data.songs[i]['name'];

        const isHost = $('#is_host').val();
        // console.log('inside sync_playlists.js...' + isHost);

        let addToQueueButtonHtml = '';
        if (isHost === 'True') {
            addToQueueButtonHtml = '<button type="button" id="add-song-to-queue-btn">Add to Queue</button>';
        }

        $('#poll_list').append(
            '<div class="media pt-3" id="poll_song_div">' +
            '<img src="https://img.youtube.com/vi/' + v_id + '/0.jpg" alt="" class="mr-2 rounded" width="100">' +
            '<div class="media-body pb-3 mb-0 small lh-125 border-bottom border-secondary rounded-right">' +
            '    <div class="d-flex justify-content-between align-items-center w-100">' +
            '      <strong class="text-gray-dark">' + v_name + '</strong>' +
            '    </div>' +
            // '<button type="button" id="add-song-to-queue-btn">Add to Queue</button>' +
            addToQueueButtonHtml +
            '       <input type="hidden" id="song_id" value="' + v_id + '"/>' +
            '       <input type="hidden" id="song_name" value="' + v_name + '"/>' +
            '</div>' +
            '</div>');
    }
}

function get_queue_songs_from_room() {
    var room_id = $("#room_id").attr('value');

    $.ajax({
        // The URL for the request
        url: "/get-queue-songs-from-room",

        // The data to send (will be converted to a query string)
        data: {
            room_id: room_id
        },

        // Whether this is a POST or GET request
        type: "GET",

        // The type of data we expect back
        dataType: "json",
    })
        .done(function (json) {
            updateChangesQueueSongs(json)
        })
        .fail(function (xhr, status, errorThrown) {
            // console.log("Sorry, there was a problem!");
            // console.log("Error: " + errorThrown);
            // console.log("Status: " + status);
            console.dir(xhr);
        })
        // Code to run regardless of success or failure;
        .always(function (xhr, status) {
            // console.log("The request is complete!");
            // console.alert( "The request is complete!" );
        });
}

function updateChangesQueueSongs(data) {
    // console.log(data);
    $("#dj_list").empty();
    for (var i = 0; i < data.songs.length; i++) {
        var v_id = data.songs[i]['id'];
        var v_name = data.songs[i]['name'];

        var elementId = 'song_queue_' + v_id;
        $('#dj_list').append(
            '<div class="media pt-3" id="' + elementId + '">' +
            '<img src="https://img.youtube.com/vi/' + v_id + '/0.jpg" alt="" class="mr-2 rounded" width="100">' +
            '<div class="media-body pb-3 mb-0 small lh-125 border-bottom border-secondary rounded-right">' +
            '    <div class="d-flex justify-content-between align-items-center w-100">' +
            '         <strong class="text-gray-dark">' + v_name + '</strong>' +
            '      </div>' +
            '   </div>' +
            '</div>');
    }
}

window.setInterval(get_pool_songs_from_room, 5000);
window.setInterval(get_queue_songs_from_room, 5000);