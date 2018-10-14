# Product Backlog

## Core functionality

### User registration/login (**Sam**)
- User registration/login will _require_ authorization with Spotify.

### Creating a room (**Sam/Noam/Rui** - work together to agree on Django Model)
- Create a view so a logged-in user can create a room with the settings they desire.
- Settings might include (but not limited to):
	- `Public/Private`: Whether the room will be public or private (required)
	- `Room Name`: Name of the room (required)
	- `Song Pool`: A pool of the only songs that can be played in this room (required)
	- `Room Description`: Brief room description
	- `List of allowed DJs`: Record of HotPot users who can be a DJ in this room
	- `Location`: GPS location of room 

### Room views
- Admin control panel (**Sam/Noam/Rui** - to agree on feel/style of room views)
	- The admin can modify existing room settings.
- Create listener view (**Sam**)
	- Add song(s) to 'My Suggestions' list - a list of songs that the user would like to see in the song pool
	- Vote for songs currently in the 'Song Pool' - a pool of songs defined for that room
	- Like/Dislike for currently played song - songs with enough dislikes will be skipped
- Create DJ view (**Noam**)
	- DJ can see 'Suggestions' list, view how many votes each song has, and add suggested songs to the 'Song Pool'
	- DJ can enqueue songs from the 'Song Pool' to their own 'Queue'.

### 'Discover' rooms
- Create 'Explore Places' view (**Noam**)
	- Leverage Google Maps API to display public venues with HotPot rooms, and be able to enter those HotPot rooms
- Create 'Explore Rooms' view (**Rui**)
	- View the current, most popular rooms on the HotPot Music Share platform

### 'My' rooms (**Sam**)
- Create view for all rooms that I
	- manage
	- can DJ for
	- recently joined
	- have marked as 'favorite'

## Division of Work
- In the beginning, we will most likely have to have a couple of meetings to go over the Models and page layouts
- With a 3-person group, we decided that Noam and Sam would work on 'backend' Django views while Rui will work on 'frontend' HTML/CSS templating.
	- This isn't a strict division (i.e. Noam/Sam/Rui will all work on all parts, eventually)
	- But the idea was that:
		- Noam/Sam can work on backend views and return the appropriate 'contexts'
		- Rui can develop the starting point for the HTML/CSS styles so all pages have a unified feel to them

## Stretch goals
- Be able to save Spotify playlists of current session
- Other 3rd party streaming service integration
	e.g. YouTube, SoundCloud, Apple Music (lol), etc.
- Advertisement opportunities ($$$)
	- Commercials -> Premium Mode (no commercials)
	- Link to artist to purchase songs/albums
- Better 'room discovery' mechanisms
	- Filter rooms by music genre (e.g. a room that plays a lot of Pop music)
	- Find rooms of users near me
	- Filter rooms by geographic location
- Better social networking functionality
	- Be able to chat in rooms
	- Follow friends/users
	- Room statistics
	- User statistics
- More 'room' modes/presets
	- e.g. Party, Cafe, Restaurant, etc.

# Example Templates Structure
* `static`
	* `templates`
		* `logged_out_base.html`
		    * `login.html`
		    * `register.html`
		    * `forgot_password.html`
		* `logged_in_base.html`
			* `create_room.html`
			* `discover_base.html`
				* `discover_places.html`
				* `discover_rooms.html`
			* `my_space.html`
				* `my_favorites.html`
				* `my_created_rooms.html`
				* `my_dj_rooms.html`
			* `room_base.html`
				* `room_as_dj.html`
				* `room_as_listener.html`