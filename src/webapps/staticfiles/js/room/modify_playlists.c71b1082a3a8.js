/*****************************************************************************************
 ADD SONG FROM POOL TO QUEUE
 */
$("#poll_list").on("click", "#add-song-to-queue-btn", function (event) {
    event.preventDefault();
    var search_form = $(this).closest("#poll_song_div");
    var room_id = $("#room_id");
    var song_id = search_form.find("#song_id");
    var song_name = search_form.find("#song_name");

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