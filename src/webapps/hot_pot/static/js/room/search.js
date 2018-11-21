/* NOAM JS START **********************************************************************************************/


// The boilerplate code below is copied from the Django 1.10 documentation.
// It establishes the necessary HTTP header fields and cookies to use
// Django CSRF protection with jQuery Ajax requests.

$(document).ready(function () {  // Runs when the document is ready
    // using jQuery
    // https://docs.djangoproject.com/en/1.10/ref/csrf/
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

}); // End of $(document).ready

$("#panel").on("click", "#search-button", function (event) {
    var panel = $(this).closest("#panel");
    var query = panel.find("#search-query");
    var p_url = panel.find("#add-comment-url").attr("data-url");

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
            for (var i = 0; i < data.songs.length; i++) {
                var v_id = data.songs[i]['id'];
                var v_name = data.songs[i]['name'];

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

/*****************************************************************************************8
 ADD SONG FROM SEARCH TO POOL
 */
$("#search-results").on("click", "#add-song-btn", function (event) {
    event.preventDefault();
    var search_form = $(this).closest("#search-song-div");
    var room_id = $("#room_id");
    var song_id = search_form.find("#song_id");
    var song_name = search_form.find("#song_name");

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
            console.log(data);
            $("#poll_list").empty();
            for (var i = 0; i < data.songs.length; i++) {
                var v_id = data.songs[i]['id'];
                var v_name = data.songs[i]['name'];

                $('#poll_list').append(
                    '<div class="media pt-3" id="poll_song_div">' +
                    '<img src="https://img.youtube.com/vi/' + v_id + '/0.jpg" alt="" class="mr-2 rounded" width="100">' +
                    '<div class="media-body pb-3 mb-0 small lh-125 border-bottom border-secondary rounded-right">' +
                    '    <div class="d-flex justify-content-between align-items-center w-100">' +
                    '      <strong class="text-gray-dark">' + v_name + '</strong>' +
                    '    </div>' +
                    '<button type="button" id="add-song-to-queue-btn">Add to Queue</button>' +
                    '       <input type="hidden" id="song_id" value="' + v_id + '"/>' +
                    '       <input type="hidden" id="song_name" value="' + v_name + '"/>' +
                    '</div>' +
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
    /*
    $.post("/add-marker", {"room_name": room_name, "lng": lng, "lat": lat})
        .done(function(data) {
            alert("saved!");
    });
    */
});


