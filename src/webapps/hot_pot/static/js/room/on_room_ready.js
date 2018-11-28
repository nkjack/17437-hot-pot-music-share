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

    // instead of extra code in html all done in ajax -- commented by noam
    get_pool_songs_from_room();
    get_queue_songs_from_room();

    // Call this immediately (don't wait 5 seconds to get current list of users)
    updateCurrentUsersList();

    // Fill adding/removing DJ select dropdown lists
    fillSelectAddDj();
    fillSelectRemoveDj();

    // If room is 'Friend Mode', make this user a DJ if they aren't already
    checkFriendMode();

    // Tooltip for 'Hotpot Mode'
    if ($('#is_hotpot_mode').val() === "True") {
        $('[data-toggle="tooltip"]').tooltip();
    }


}); // End of $(document).ready