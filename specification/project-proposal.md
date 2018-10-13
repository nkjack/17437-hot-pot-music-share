# Original Project Proposal Description
>We want to create a web application that allows multiple users to vote for and listen to songs together in real-time. The web application would allow users to create their own rooms that other users can join.  

>There would be two types of rooms’: a ‘private’ room and a ‘public venue’ room.

>A private room would be for users at different locations, on different devices. This kind of room would be for friends who want to listen to the same songs together, virtually and in real-time. The virtual room will be in charge of selecting the song and playing it across all distributed devices. The room can play songs in a fair, round-robin fashion (popping the top song of each person’s song list). Users in the room can ‘like’ or ‘dislike’ the current song being played and the current song can be skipped if there are too many ‘dislikes’ (to discourage trolling). The room creator can configure various options for the room (voting process, anonymous likes/dislikes, a default playlist, kicking people out, etc.)
> A public venue room would be for users at the same location. This kind of room would be for places like restaurants, bars, clubs, cafes; where the music would be played through a single medium, probably the room creator’s device (i.e. the public speakers that everyone can hear at a cafe). Users can join public venue rooms to vote for songs they’d like to be played. Our application would ensure that people are actually at the public venue they are voting for. Just like for private rooms, the room creator can configure various options for the room (songs only from a certain playlist, voting, likes/dislikes, song filters, clean/explicit songs, chatroom, etc.).

# Technologies and APIs
* **Django Framework**
  * Using default Django database backend (SQLite)
* **[Spotify API](https://developer.spotify.com/documentation/web-api/)**
  * JavaScript, Node, and Python wrappers available
  * Functionality needed:
    * [User authorization](https://developer.spotify.com/documentation/general/guides/authorization-guide/)
    * [Access/create user playlists](https://developer.spotify.com/documentation/web-api/reference/playlists/get-playlists-tracks/)
    * [Stream to browser](https://developer.spotify.com/documentation/web-api/reference/player/)
    * [Search music](https://developer.spotify.com/documentation/web-api/reference/search/search/)
* **[Google Maps API](https://developers.google.com/maps/documentation/)**
  * [Embedded JavaScript map](https://developers.google.com/maps/documentation/javascript/tutorial)
* **[Google Places API](https://developers.google.com/places/web-service/intro)**
  * [Used to locate specific businesses](https://developers.google.com/places/web-service/intro)