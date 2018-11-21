# Final Sprint Backlog
### Product manager for this sprint: Rui

-------------------------------------------------------------------------------
## Sam Backlog
-------------------------------------------------------------------------------

### Refactoring [3 hours]
- Clean up JS files
- Restructure dir/files

### Cloud deployment [4 hours]
- Heroku
- Redis add-on
- Email backend
- Test out sync playback

### Room Issues [2 hours]
- If queue is empty, display a message instead of youtube error
- Auto play if queue is empty and a song is added (periodic refresh to check this)
- Use channels instead of periodic refresh for updating pool/queue
- Display message if a DJ is not in the room ('dead room')

### List of users in the room [2 hours]
- Use channels to display current users in the room

-------------------------------------------------------------------------------
## Rui Backlog
-------------------------------------------------------------------------------

### UI Fixes
- Room view clean up [4 hours]
	- Work with Noam on how the pop window of search results and pool songs will use our previous ajax requests with our room.
- Better chat box, which can be expandable and support emoji

### Settings
- Create Room, Add more init. settings (i.e. location)[1 hour]
- Room Setting page (modify existing room settings) [1 hour]
	- Also, give the owner the ability to upgrate listener to dj and vice versa (work with Noam on it)
- Profile Setting page [2 hour]
	- Reset Password


### Additional Features
- Search Room by name or by tag
- Voting for rooms [2 hours]

### Nice to have
- Private/Public Room. Private room needs password, etc.
- Drag to re-order playlists

-------------------------------------------------------------------------------
## Noam Backlog
-------------------------------------------------------------------------------

### Bug Fixes From Sprint 2
- Adding from Search -> Pool ('Add to Queue' button shows up for Listeners)
- Adding from Pool -> Queue (Songs added in arbitrary order)
- After fixing bugs, work with rui of how it is going to change if we use pop up window for the search and pool boxes.

### DJ Queue
- DJ has their own private playlist
- Figure out UI so it's not cluttered/overwhelming

### Room features
- Figure out how to model the application with the new features: Up/Downvote, Remove/Hide, Reorder
	- Song
		- Up/Downvote
		- Ranking mechanism to achieve order in Playlists
	- Playlists
		- Default order of songs will be by id of songs (smaller id mean 'older' song inside the playlist)
	- Owner
		- We want more than 1 dj inside a room. Owner of a room could upgrate a listener to be a dj and vice versa.
		work with rui to implement it in the room settings.
- Implement the above model modification to work in the actual Playlists in a room: Up/Downvote, Remove/Hide, Reorder, Click-to-play
- Generate a round robin playlist (global song queue) between all the current dj's in the room.
	- Combining all of the playlists together to a big one basically
	- Need to work with Sam if it will break the existing functionality of our video synchronization between all hosts.

### Maps
- Add optional 'Business Name' field to Rooms; and possibly connect it with using google places api (depends on time).
- Add real locations to Rooms (work with Rui on Settings) - *important*

-------------------------------------------------------------------------------
## Additional Features (Nice-to-have)
-------------------------------------------------------------------------------
- Final cleanup
- Room tags (e.g. #Rock, #Jazz)
