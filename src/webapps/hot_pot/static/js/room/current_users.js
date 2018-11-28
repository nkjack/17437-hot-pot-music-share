// Helper function to return a string array containing usernames of all users in the room
function getCurrentUsersInRoom() {
    let current_users;

    // Get all users in the room (AJAX)
    console.log('AJAX making call get-users-from-room...');
    $.ajax({
        async: false, // Wait for GET request to finish
        url: '/get-users-from-room/' + $('input#room_name').val(),
        type: "GET",
        dataType: "json",
    })
        .done(function (data) {
            current_users = data.users;

            console.log("Got get-users-from-room response: " + current_users);
        })
        .fail(function (xhr, status, errorThrown) {
            console.log("Error: " + errorThrown);
            console.log("Status: " + status);
            console.dir(xhr);
        });

    return current_users;
}

// Update the room's current user list
function updateCurrentUsersList() {
    const current_users = getCurrentUsersInRoom();

    // Get all DJs for this room
    let djs;
    $.ajax({
        async: false,
        // The URL for the request
        url: "/get-djs-in-room",
        data: {
            room_id: $("#room_id").val(),
        },
        // Whether this is a POST or GET request
        type: "POST",
        // The type of data we expect back
        dataType: "json",
    })
        .done(function (data) {
            djs = data.users;
        })
        .fail(function (xhr, status, errorThrown) {
            console.log("Error: " + errorThrown);
            console.log("Status: " + status);
            console.dir(xhr);
        });

    // Update HTML of user and DJ lists (empty both first
    $('#listeners').empty();
    $('#djs').empty();

    for (let username of current_users) {
        // Copied/pasted HTML template left by Rui in room.html (TODO: Change later?)
        let singleUserHtml =
            '<div class="media text-muted pt-3" id="user_1">\n' +
            '    <!-- The profile img -->\n' +
            '    <!--  <img src="SOME URL" alt="" class="mr-2 rounded" width="25"> -->\n' +
            '    <div class="media-body pb-3 mb-0 small lh-125 border-bottom border-gray">\n' +
            '        <div class="d-flex justify-content-between align-items-center w-100">\n' +
            '            <strong class="text-gray-dark">' + username + '</strong>\n' +
            '        </div>\n' +
            '    </div>\n' +
            '</div>';

        // Add to Listeners or DJ list
        if (djs.includes(username)) {
            $('#djs').append(singleUserHtml);
        } else {
            $('#listeners').append(singleUserHtml);

        }
    }
}

window.setInterval(updateCurrentUsersList, 2000);
