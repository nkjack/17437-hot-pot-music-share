/****************************************** CHAT ROOM  ********************************************************/

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function (e) {
    var messageInputDom = document.querySelector('#chat-message-input');
    var message = messageInputDom.value;
    console.log('sending...');
    socket.send(JSON.stringify({
        'chat_message': message,
        'username': $('input#username').val(),
    }));

    messageInputDom.value = '';
};

// If chat button is clicked, remove pulse notification
document.querySelector('#nav-chat-tab').onclick = function (e) {
    $('#nav-chat-tab').removeClass('chat-tab-pulse');
};