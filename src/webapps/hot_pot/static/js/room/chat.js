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

// Periodically scroll to the bottom of the chat log
setInterval(function () {
    var objDiv = document.getElementById("chat-log");
    objDiv.scrollTop = objDiv.scrollHeight;
}, 2000);