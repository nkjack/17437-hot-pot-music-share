function getEntryListForPoolQueueForListener(v_id, v_name){
    return '<div class="media pt-3 border-bottom border-secondary" id="poll_song_div">' +
                '<img src="https://img.youtube.com/vi/' + v_id + '/0.jpg" alt="" class="mr-2 rounded" width="100">' +
                '<div class="media-body pb-3 mb-0 small lh-125  rounded-right">' +
                '    <div class="d-flex justify-content-between align-items-center w-100">' +
                '      <strong class="text-gray-dark">' + v_name + '</strong>' +
                '    </div>' +
                // '<button type="button" id="add-song-to-queue-btn">Add to Queue</button>'
                '       <input type="hidden" id="song_id" value="' + v_id + '"/>' +
                '       <input type="hidden" id="song_name" value="' + v_name + '"/>' +
                '</div>' +
                '</div>';
}

function getEntryListForPoolQueueForHost(v_id, v_name){
    return '<div class="media pt-3 border-bottom border-secondary" id="poll_song_div">' +
                '<img src="https://img.youtube.com/vi/' + v_id + '/0.jpg" alt="" class="mr-2 rounded" width="100">' +
                '<div class="media-body pb-3 mb-0 small lh-125  rounded-right">' +
                '    <div class="d-flex justify-content-between align-items-center w-100">' +
                '      <strong class="text-gray-dark">' + v_name + '</strong>' +
                '    </div>' +
                '<button type="button" id="add-song-to-queue-btn">Add to Queue</button>' +
                '       <input type="hidden" id="song_id" value="' + v_id + '"/>' +
                '       <input type="hidden" id="song_name" value="' + v_name + '"/>' +
                '</div>' +
                '</div>';
}

function getEntryListForSearchResult(v_id, v_name){
    return '<div class="media pt-3 border-bottom border-secondary" id="search-song-div">' +
    '<img src="https://img.youtube.com/vi/' + v_id + '/0.jpg" alt="" class="mr-2 rounded" width="200">' +
    '    <div class="media-body pb-3 mb-0 small lh-125 rounded-right">' +
    '       <div class="d-flex justify-content-between align-items-center w-100">' +
    '       <strong class="text-gray-dark">' + v_name + '</strong> <br/>' +
    // {#'        <span class = "d-block"> {{timespan}}</span>'+#}
    '       <button type="button" id="add-song-btn">Add song</button>' +
    '       <input type="hidden" id="song_id" value="' + v_id + '"/>' +
    '       <input type="hidden" id="song_name" value="' + v_name + '"/>' +
    '     </div>' +
    '</div>' +
    '</div>';
}

function getEntryListForGlobalSongQueue(v_id, v_name){
    return '<div class="media pt-3 border-bottom border-secondary" id="song_0">' +
    '<img src="https://img.youtube.com/vi/' + v_id + '/0.jpg" alt="" class="mr-2 rounded" width="100">' +
    '<div class="media-body pb-3 mb-0 small lh-125  rounded-right">' +
    '    <div class="d-flex justify-content-between align-items-center w-100">' +
    '         <strong class="text-gray-dark">' + v_name + '</strong>' +
    '      </div>' +
    '   </div>' +
    '</div>';
}