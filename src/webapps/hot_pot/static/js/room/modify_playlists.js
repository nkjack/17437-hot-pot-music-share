/*****************************************************************************************8
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
            console.log(data);
            $("#dj_list").empty();
            for (var i = 0; i < data.songs.length; i++) {
                var v_id = data.songs[i]['id'];
                var v_name = data.songs[i]['name'];

                $('#dj_list').append(
                    '<div class="media pt-3" id="song_0">' +
                    '<img src="https://img.youtube.com/vi/' + v_id + '/0.jpg" alt="" class="mr-2 rounded" width="100">' +
                    '<div class="media-body pb-3 mb-0 small lh-125 border-bottom border-secondary rounded-right">' +
                    '    <div class="d-flex justify-content-between align-items-center w-100">' +
                    '         <strong class="text-gray-dark">' + v_name + '</strong>' +
                    '      </div>' +
                    '   </div>' +
                    '</div>');

            }
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

/*
function ajaxAddSongToListRequest(method_url, method_data, metod, htmlEntry, newList){
    $.ajax({
        // The URL for the request
        url: method_url,
        data : method_data,
        // Whether this is a POST or GET request
        type: method,
        // The type of data we expect back
        dataType: "json",
    })
        .done(function (data) {
            console.log(data);
            newList.empty();
            for (var i = 0; i < data.songs.length; i++) {
                var v_id = data.songs[i]['id'];
                var v_name = data.songs[i]['name'];
                newList.append(htmlEntry);

            }
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
}
*/