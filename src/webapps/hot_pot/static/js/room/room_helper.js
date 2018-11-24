function getEntryListForPoolQueue(vId, vName, vThumbsUp, isVoted, isHost) {
    let vote_btn_html = 'Upvote';
    if (isVoted == 'True') {
        vote_btn_html = 'Downvote';
    }

    let isHostHtml = '';
    if (isHost == 'True') {
        isHostHtml = '<button type="button" id="add-song-to-queue-btn">Add to Queue</button>';
    }

    return '<div class="media pt-3" id="poll_song_div">' +
        '<img src="https://img.youtube.com/vi/' + vId + '/0.jpg" alt="" class="mr-2 rounded" width="100">' +
        '<div class="media-body pb-3 mb-0 small lh-125 border-bottom border-secondary rounded-right">' +
        '    <div class="d-flex justify-content-between align-items-center w-100">' +
        '      <strong class="text-gray-dark">' + vName + '</strong>' +
        '    </div>' +
        isHostHtml +
        '<button type="button" id="vote-song-btn" value="' + vote_btn_html + '">' + vote_btn_html + '</button>' +
        '    <div class="d-flex justify-content-between align-items-center w-100">' +
        '      <strong class="text-gray-dark">Thumbs Up: ' + vThumbsUp + '</strong>' +
        '    </div>' +
        '       <input type="hidden" id="song_id" value="' + vId + '"/>' +
        '       <input type="hidden" id="song_name" value="' + vName + '"/>' +
        '</div>' +
        '</div>';
}


function getEntryListForSearchResult(vId, vName) {
    return '<div class="media pt-3" id="search-song-div">' +
        '<img src="https://img.youtube.com/vi/' + vId + '/0.jpg" alt="" class="mr-2 rounded" width="200">' +
        '    <div class="media-body pb-3 mb-0 small lh-125 border-bottom border-secondary rounded-right">' +
        '       <div class="d-flex justify-content-between align-items-center w-100">' +
        '       <strong class="text-gray-dark">' + vName + '</strong>' +
        // {#'        <span class = "d-block"> {{timespan}}</span>'+#}
        '       <button type="button" id="add-song-btn">Add song</button>' +
        '       <input type="hidden" id="song_id" value="' + vId + '"/>' +
        '       <input type="hidden" id="song_name" value="' + vName + '"/>' +
        '     </div>' +
        '</div>' +
        '</div>';
}

function getEntryListForGlobalSongQueue(vId, vName, isHost, index) {
    // Show up/down depending on host and index in list
    let isHostHtml = '';
    let upRankHtml = '';
    let downRankHtml = '';

    // Always have ID for position
    let positionInList = '<input type="hidden" id="position" value="' + index + '" />';


    if (index > 1 && isHost === 'True') {
        upRankHtml = '<button type="button" id="up-song-btn">Up</button>';
        downRankHtml = '<button type="button" id="down-song-btn">Down</button>';

        isHostHtml = '<button type="button" id="dlt-song-btn">Remove song</button>' +
            '<input type="hidden" id="song_id" value="' + vId + '"/>' +
            '<input type="hidden" id="song_name" value="' + vName + '"/>';
    }

    if (index === 2) {
        // No 'move up' button for second song in the queue
        upRankHtml = '';
    }

    return '<div class="media pt-3" id="entry-song-queue-div">' +
        '<img src="https://img.youtube.com/vi/' + vId + '/0.jpg" alt="" class="mr-2 rounded" width="100">' +
        '<div class="media-body pb-3 mb-0 small lh-125 border-bottom border-secondary rounded-right">' +
        '    <div class="d-flex justify-content-between align-items-center w-100">' +
        '         <strong class="text-gray-dark">' + vName + '</strong>' +
        '      </div>' +
        isHostHtml +
        upRankHtml +
        downRankHtml +
        positionInList +
        '   </div>' +
        '</div>';
}