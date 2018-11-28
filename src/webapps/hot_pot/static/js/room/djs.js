// Fill in dropdown select for adding DJs form
function fillSelectAddDj() {

    // Get non DJ users
    $.ajax({
        // The URL for the request
        url: "/get-all-non-djs-in-room",
        data: {
            room_id: $("#room_id").val(),
        },
        // Whether this is a POST or GET request
        type: "POST",
        // The type of data we expect back
        dataType: "json",
    })
        .done(function (data) {
            console.log("fillSelectAddDj - success from get-all-non-djs-in-room");

            // Go through select and add non-DJs
            const select = $("#select-add-dj");

            select.empty();

            for (let i = 0; i < data.users.length; i++) {
                let username = data.users[i];
                select.append(`<option value="${username}">${username}</option>`);
            }
        })
        .fail(function (xhr, status, errorThrown) {
            console.log("Error: " + errorThrown);
            console.log("Status: " + status);
            console.dir(xhr);
        })
}

// Fill in dropdown select for removing DJs form
function fillSelectRemoveDj() {
    // Get all DJ users
    $.ajax({
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
            // Go through select and add non-DJs
            const select = $("#select-remove-dj");

            select.empty();

            for (let i = 0; i < data.users.length; i++) {
                let username = data.users[i];
                select.append(`<option value="${username}">${username}</option>`);
            }
        })
        .fail(function (xhr, status, errorThrown) {
            console.log("Error: " + errorThrown);
            console.log("Status: " + status);
            console.dir(xhr);
        })
}

// Add the specified username as a DJ
function addUsernameAsDj(username) {

    var room_id = $("#room_id");

    // TODO: Either pass username as function parameter or get username from text input with jQuery
    if (username === undefined) {
        var username = $("#select-add-dj").val();
    }

    console.log('addUserNameAsDj selected: ' + username);

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

            // Update dropdown menus
            fillSelectAddDj();
            fillSelectRemoveDj();
        })
        .fail(function (xhr, status, errorThrown) {
            console.log("Error: " + errorThrown);
            console.log("Status: " + status);
            console.dir(xhr);
        })
}

// Remove the specified username as a DJ
function removeUsernameAsDj() {
    var room_id = $("#room_id");

    // TODO: Either pass username as function parameter or get username from text input with jQuery
    var username = $("#select-remove-dj").val();

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

            // Update dropdown menus
            fillSelectAddDj();
            fillSelectRemoveDj();
        })
        .fail(function (xhr, status, errorThrown) {
            console.log("Error: " + errorThrown);
            console.log("Status: " + status);
            console.dir(xhr);
        })
}

// Called on document/room ready - make this user a DJ if this room is in 'Friend Mode'
function checkFriendMode() {
    const is_dj = $("#is_dj").val();
    const is_hotpot_mode = $("#is_hotpot_mode").val();
    const username = $("#username").val();

    console.log('is_dj: ' + is_dj);
    console.log('is_hotpot_mode: ' + is_hotpot_mode);
    console.log('username: ' + username);

    if (is_hotpot_mode === "True" && is_dj === "False") {
        console.log("checkFriendMode - Making this user a DJ and reloading page...");
        addUsernameAsDj(username);
        location.reload(); // Reload the page - user won't notice b/c page is loading, anyway.
    }
}