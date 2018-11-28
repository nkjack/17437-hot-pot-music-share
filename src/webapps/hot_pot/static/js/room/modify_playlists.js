/*****************************************************************************************
 ADD SONG FROM POOL TO QUEUE
 */
$("#poll_list").on("click", "#add-song-to-queue-btn", function (event) {
    event.preventDefault();
    const search_form = $(this).closest("#poll_song_div");
    const room_id = $("#room_id");
    const song_id = search_form.find("#song_id");
    const song_name = search_form.find("#song_name");

    $.ajax({
        // The URL for the request
        url: "/add-song-from-pool-to-queue",
        data: {
            room_id: room_id.val(),
            song_id: song_id.val(),
            song_name: song_name.attr('value')
        },
        // Whether this is a POST or GET request
        type: "POST",
        // The type of data we expect back
        dataType: "json",
    })
        .done(function (data) {
            updateChangesQueueSongs(data);
        })
        .fail(function (xhr, status, errorThrown) {
            console.log("Error: " + errorThrown);
            console.log("Status: " + status);
            console.dir(xhr);
        })
        // Code to run regardless of success or failure;
        .always(function (xhr, status) {
            console.log("fetch songs from poll request is finished!");
        });
});

/*****************************************************************************************
 DELETE SONG FROM QUEUE
 */

$("#dj_list").on("click", "#dlt-song-btn", function (event) {
    event.preventDefault();
    const entry_div = $(this).closest("#entry-song-queue-div");
    const room_id = $("#room_id");
    const song_id = entry_div.find("#song_id");
    const song_name = entry_div.find("#song_name");

    console.log(room_id);
    $.ajax({
        // The URL for the request
        url: "/delete-from-song-queue-post",
        data: {
            room_id: room_id.val(),
            song_id: song_id.val(),
            song_name: song_name.attr('value')
        },
        // Whether this is a POST or GET request
        type: "POST",
        // The type of data we expect back
        dataType: "json",
    })
        .done(function (data) {
            updateChangesQueueSongs(data);
        })
        .fail(function (xhr, status, errorThrown) {
            console.log("Error: " + errorThrown);
            console.log("Status: " + status);
            console.dir(xhr);
        })
        // Code to run regardless of success or failure;
        .always(function (xhr, status) {
            console.log("fetch songs from poll request is finished!");
        });
});

/*****************************************************************************************
 REORDER SONG_QUEUE
 */
$("#dj_list").on("click", "#up-song-btn", function (event) {
    event.preventDefault();
    const entry_div = $(this).closest("#entry-song-queue-div");
    const room_id = $("#room_id");

    // var index = parseInt(entry_div.find( "#position" ).val());
    const index = parseInt(entry_div.find("#song_rank").val());
    // alert( "Index: " + index );

    $.ajax({
        // The URL for the request
        url: "/change-song-queue-order",
        data: {
            room_id: room_id.val(),
            prev_position: index,
            new_position: index - 1,
        },
        // Whether this is a POST or GET request
        type: "POST",
        // The type of data we expect back
        dataType: "json",
    })
        .done(function (data) {
            updateChangesQueueSongs(data);
        })
        .fail(function (xhr, status, errorThrown) {
            console.log("Error: " + errorThrown);
            console.log("Status: " + status);
            console.dir(xhr);
        })
        // Code to run regardless of success or failure;
        .always(function (xhr, status) {
            console.log("fetch songs from poll request is finished!");
        });
});

$("#dj_list").on("click", "#down-song-btn", function (event) {
    event.preventDefault();
    const entry_div = $(this).closest("#entry-song-queue-div");
    const room_id = $("#room_id");

    const index = parseInt(entry_div.find("#song_rank").val());

    // alert(typeof index);
    // alert( "Index: " + index );

    $.ajax({
        // The URL for the request
        url: "/change-song-queue-order",
        data: {
            room_id: room_id.val(),
            prev_position: index,
            new_position: index + 1,
        },
        // Whether this is a POST or GET request
        type: "POST",
        // The type of data we expect back
        dataType: "json",
    })
        .done(function (data) {
            updateChangesQueueSongs(data);
        })
        .fail(function (xhr, status, errorThrown) {
            console.log("Error: " + errorThrown);
            console.log("Status: " + status);
            console.dir(xhr);
        })
        // Code to run regardless of success or failure;
        .always(function (xhr, status) {
            console.log("fetch songs from poll request is finished!");
        });
});