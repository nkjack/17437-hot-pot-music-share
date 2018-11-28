
// Allow enter key to search
document.querySelector('#search-query').onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#search-button').click();
    }
};

$("#panel").on("click", "#search-button", function (event) {
    const panel = $(this).closest("#panel");
    const query = panel.find("#search-query");
    const p_url = panel.find("#add-comment-url").attr("data-url");

    $.ajax({
        // The URL for the request
        url: p_url,
        data: {
            query: query.val()
        },
        // Whether this is a POST or GET request
        type: "GET",
        // The type of data we expect back
        dataType: "json",
    })
        .done(function (data) {
            console.log(data);
            $("#search-results").empty();
            for (let i = 0; i < data.songs.length; i++) {
                const v_id = data.songs[i]['id'];
                const v_name = data.songs[i]['name'];

                $('#search-results').append(getEntryListForSearchResult(v_id, v_name));
            }
        })
        .fail(function (xhr, status, errorThrown) {
            console.log("Error: " + errorThrown);
            console.log("Status: " + status);
            console.dir(xhr);
        })
        // Code to run regardless of success or failure;
        .always(function (xhr, status) {
            console.log("fetch songs request is finished!");
        });
});

// ADD SONG FROM SEARCH TO POOL
$("#search-results").on("click", "#add-song-btn", function (event) {
    event.preventDefault();
    const search_form = $(this).closest("#search-song-div");
    const room_id = $("#room_id");
    const song_id = search_form.find("#song_id");
    const song_name = search_form.find("#song_name");

    $.ajax({
        // The URL for the request
        url: "/add-song-to-room-playlist-ajax",
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
            updateChangesPoolSongs(data);
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


