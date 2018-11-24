function getEntryListForPoolQueue(v_id, v_name, v_thumbs_up, is_voted, is_host){
    let vote_btn_html = 'Upvote';
    if (is_voted == 'True'){
        vote_btn_html = 'Downvote';
    }

    let is_host_html = '';
    if (is_host == 'True'){
        is_host_html = '<button type="button" id="add-song-to-queue-btn">Add to Queue</button>';
    }

    return '<div class="media pt-3" id="poll_song_div">' +
                '<img src="https://img.youtube.com/vi/' + v_id + '/0.jpg" alt="" class="mr-2 rounded" width="100">' +
                '<div class="media-body pb-3 mb-0 small lh-125 border-bottom border-secondary rounded-right">' +
                '    <div class="d-flex justify-content-between align-items-center w-100">' +
                '      <strong class="text-gray-dark">' + v_name + '</strong>' +
                '    </div>' +
                is_host_html +
                '<button type="button" id="vote-song-btn" value="'+vote_btn_html+'">'+vote_btn_html+'</button>' +
                '    <div class="d-flex justify-content-between align-items-center w-100">' +
                '      <strong class="text-gray-dark">Thumbs Up: ' + v_thumbs_up + '</strong>' +
                '    </div>' +
                '       <input type="hidden" id="song_id" value="' + v_id + '"/>' +
                '       <input type="hidden" id="song_name" value="' + v_name + '"/>' +
                '</div>' +
                '</div>';
}


function getEntryListForSearchResult(v_id, v_name){
    return '<div class="media pt-3" id="search-song-div">' +
    '<img src="https://img.youtube.com/vi/' + v_id + '/0.jpg" alt="" class="mr-2 rounded" width="200">' +
    '    <div class="media-body pb-3 mb-0 small lh-125 border-bottom border-secondary rounded-right">' +
    '       <div class="d-flex justify-content-between align-items-center w-100">' +
    '       <strong class="text-gray-dark">' + v_name + '</strong>' +
    // {#'        <span class = "d-block"> {{timespan}}</span>'+#}
    '       <button type="button" id="add-song-btn">Add song</button>' +
    '       <input type="hidden" id="song_id" value="' + v_id + '"/>' +
    '       <input type="hidden" id="song_name" value="' + v_name + '"/>' +
    '     </div>' +
    '</div>' +
    '</div>';
}

function getEntryListForGlobalSongQueue(v_id, v_name, is_host){
    let is_host_html =  '';

    if (is_host == 'True'){
        is_host_html =  '<button type="button" id="dlt-song-btn">Remove song</button>' +
                        '<input type="hidden" id="song_id" value="' + v_id + '"/>' +
                        '<input type="hidden" id="song_name" value="' + v_name + '"/>';
    }

    return '<div class="media pt-3" id="entry-song-queue-div">' +
    '<img src="https://img.youtube.com/vi/' + v_id + '/0.jpg" alt="" class="mr-2 rounded" width="100">' +
    '<div class="media-body pb-3 mb-0 small lh-125 border-bottom border-secondary rounded-right">' +
    '    <div class="d-flex justify-content-between align-items-center w-100">' +
    '         <strong class="text-gray-dark">' + v_name + '</strong>' +
    '      </div>' +
        is_host_html +
    '   </div>' +
    '</div>';
}