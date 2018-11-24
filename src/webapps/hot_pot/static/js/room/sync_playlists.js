// THIS FILE HAS TO USE sync_playlists.js file.
// THIS FILE ASSUME CORRECT ids in room_base.html


function get_pool_songs_from_room() {
    var room_id = $("#room_id").attr('value');
    console.log(room_id);
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
            console.log("The request is complete!");
            // console.alert( "The request is complete!" );
        });
}

function updateChangesPoolSongs(data) {
    console.log(data);
    $("#poll_list").empty();
    for (var i = 0; i < data.songs.length; i++) {
        var v_id = data.songs[i]['id'];
        var v_name = data.songs[i]['name'];
        var v_thumbs_up = data.songs[i]['thumbs_up'];
        var is_voted = data.songs[i]['is_voted'];

        const isHost = $('#is_host').val();
        console.log('inside sync_playlists.js...' + isHost);

        if (isHost === 'True') {
            $('#poll_list').append(getEntryListForPoolQueueForHost(v_id,
                v_name,
                v_thumbs_up,
                is_voted));
        }
        else {
            $('#poll_list').append(getEntryListForPoolQueueForListener(v_id,
                v_name,
                v_thumbs_up,
                is_voted));
        }
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
            console.log("Sorry, there was a problem!");
            console.log("Error: " + errorThrown);
            console.log("Status: " + status);
            console.dir(xhr);
        })
        // Code to run regardless of success or failure;
        .always(function (xhr, status) {
            console.log("The request is complete!");
            // console.alert( "The request is complete!" );
        });
}

function updateChangesQueueSongs(data) {
    console.log(data);
    $("#dj_list").empty();
    for (var i = 0; i < data.songs.length; i++) {
        var v_id = data.songs[i]['id'];
        var v_name = data.songs[i]['name'];

        $('#dj_list').append(getEntryListForGlobalSongQueue(v_id, v_name));

    }
}


window.setInterval(get_pool_songs_from_room, 5000);
window.setInterval(get_queue_songs_from_room, 5000);