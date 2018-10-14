# Modified Project Proposal Description
**Note:** HotPot Music Share is our original project proposal, but we've modified the original specification a bit.

## Team Members:
- Noam Kahan (nkahan@)
- Ruili Tang (ruilit@)
- Samuel Kim (ssk1@)

## Objective:
We want to create a web application that allows multiple users to vote for and listen to songs together in real-time. The web application would allow users to create their own rooms that other users can join.

### What is a room?
- A room is created by a single administrator, who decides various room options from the beginning (and can later modify as well):
    - Private/Public: Private rooms for group of friends
    - Location mapping: Useful for businesses to host their own room
    - Allowed DJs: Users who are allowed to be DJs in this room (can also just be 'anyone').
    - Maximum number of DJs at a time: So there won't be too many DJs trying to play music
    - Song Pool: Initial pool of songs allowed to be played in this room (can also just be 'all songs on Spotify').
- Rooms can have DJs and Listeners.
    - DJs choose what song will be played.
    - Listeners cannot choose what song will be played, but can upvote/downvote the currently played song as well as suggest new songs to the DJ(s).
- All rooms have a 'Song Pool'.
    - Room administrator initializes this in room creation. The 'song pool' is useful if the room owner wants to restrict the playable songs to a specific subset (e.g. at a family restaurant, only want clean songs to be played).
    - DJs have full control of the 'Song Pool' and can see all Listeners' song suggestions.
    - Listeners can _suggest_ songs to the 'Song Pool'.
    - Listeners can browse the 'Song Pool' and upvote songs that they like - the DJs can see the most upvoted songs and play them at their discretion.
- How songs are played
    - If there are DJs in the room
        - Round robin fashion, playing the top song from each of the DJ's playlists. Other fairness algorithms can be specified by the admin (e.g. 2 songs per DJ)
    - Auto-pilot mode
        - Play the highest upvoted songs (by Listeners) from the 'Song Pool'
        - If there aren't enough upvotes, simply shuffle play the 'Song Pool'

## Linking a Room to a Physical Venue
- Room administrator can specify a geographical location to their room
    - Useful for businesses that want to create a public HotPot Music Share room and share their room for customers to join (e.g. Most likely, in this case, the song-play mode would be 'Auto-pilot' so customers can upvote songs they'd like to hear and the room would automatically play the most voted songs.)
    - Useful for parties/public events (e.g. Create a room and link it to the physical location of the party. Party host can be the single DJ, party attendees can be Listeners that suggest songs to the DJ.)


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