## (10/25 - 11/05) Sprint

### Spotify User login
- [Sam][1 hour] Research Spotify Authentication API
- [Sam][1 hour] With Spotify API, be able to: log in with user, display a user's public playlist, and play a song

### Views Html Templates
- [Rui][2 hour] Design UI/UX with wireframes, and get feedback of the user story from team, then confirm the UI concept keywords(such as: *playful*,  *hich-tech*,  *simple & elegant*)
- [Rui][6 hours] Implement necessary static file(s) (HTML/CSS/JS); focusing on extensibility for future changes (e.g. more settings, different room modes). implement the following static page drafts: 
	- Login/Register
	- Room(with current playlist, room information, settings of the room)
		- Create Room, Generic Room (Template), Listener Room
	- Home/Map page(search room, create room and generate keys to invite people)
	- Explore(find public new/popular room nearby)
- Priority for html static pages (so Sam and Noam could work on it when creating the Room views):
	- Listener Room View
	- DJ Room View
	- 'My' Rooms View
	- All the rest

### Modelize the app
- [Sam][1 hour] Profile User and suggest models updates according to spotify behavior (songs, playlists)
- [Rui][1 hour] Suggest models updates according to design issues she is encountring with.
- [Noam][2 hours] How to represent all of the models of our app that will be used in our different views. Makse sure our basic models.py is working fluently.

### Room Views
Using the model structure we construct early in the sprint we can now implement the following views.

#### 'DJ Room' View
- [Noam][2 hours] Implement 'My Suggestions' list (Django code, bare-bones HTML)
- [Noam][2 hours] Implement 'Song Pool' voting list (Django code, bare-bones HTML)
- [Noam][2 hours] Implement voting up/down for a currently played song (Django code, bare-bones HTML)
- [Noam][] Make sure Rui knows what *context* from DJ room views contains.

