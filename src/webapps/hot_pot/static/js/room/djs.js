// TODO: (Delete this comment) - Made this file for room settings (Rui), but not sure if it will be done via JS or forms

// Add the specified username as a DJ
function addUsernameAsDj(username) {
    var room_id = $("#room_id");

    // TODO: Either pass username as function parameter or get username from text input with jQuery

    $.ajax({
        // The URL for the request
        url: "/add-dj-to-room",
        data: {
            room_id: room_id.val(),
            username: username,
        },
        type: "POST",
    })
        .done(function () {
            console.log("Succesfully added " + username + " as DJ.");
        })
        .fail(function (xhr, status, errorThrown) {
            console.log("Error: " + errorThrown);
            console.log("Status: " + status);
            console.dir(xhr);
        })
}

// Remove the specified username as a DJ
function removeUsernameAsDj(username) {
    var room_id = $("#room_id");

    // TODO: Either pass username as function parameter or get username from text input with jQuery

    $.ajax({
        // The URL for the request
        url: "/remove-dj-from-room",
        data: {
            room_id: room_id.val(),
            username: username,
        },
        type: "POST",
    })
        .done(function () {
            console.log("Succesfully removed " + username + " as DJ.");
        })
        .fail(function (xhr, status, errorThrown) {
            console.log("Error: " + errorThrown);
            console.log("Status: " + status);
            console.dir(xhr);
        })
}