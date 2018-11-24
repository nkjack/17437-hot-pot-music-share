$("#poll_list").on("click", "#vote-song-btn", function (event) {
    event.preventDefault();
    var pool_form = $(this).closest("#poll_song_div");
    var room_id = $("#room_id");
    var song_id = pool_form.find("#song_id");

    var url = "/vote-up";
    var is_downvote = pool_form.find("#vote-song-btn");
    console.log(is_downvote.val());

    if (is_downvote.attr("value") == "Downvote"){
        url = "/vote-down"
    }
    console.log("url to down/up vote is - " + url);
     /*
        if voted than url = /vote-down else /vote-up
     */
    $.ajax({
        // The URL for the request
        url: url,
        data: {
            room_id: room_id.val(),
            song_id: song_id.val()
        },
        // Whether this is a POST or GET request
        type: "POST",
        // The type of data we expect back
        dataType: "json",
        })
        .done(function (data) {
            console.log(data);
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


