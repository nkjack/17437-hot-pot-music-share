Project Specification Feedback
==================

Commit graded:

### The product backlog (10/10)

- Spreadsheet-like format is easier to read for backlogs. You can explore existing online tools for generating and tracking work on a project.
- What are time estimates for each task? If one task requires more than 5 hours, you should break into subtasks.

### Data models (10/10)

Some comments in your models.py,
- Line 35: is `spotify_id` a foreign key? Wouldn't it be a CharField?
- Song: I understand your design with `Song`, but there may be more efficient & intuitive way. If the same song is added to multiple rooms, do you need to represent this differently in the database? Currently you do because of `belongs_to_room` (which is a ForeignKey) and `votes_score`. This is just a suggestion, your current design is fine.
- Room: Room is missing information about maximum number of DJs.
- DJ: `ability to save a playlist for a particular room` seems confusing and may confuse the user too.
- DJ: one user cannot be DJ for multiple room in your design.
- Defining static methods in model will be especially helpful.

### Wireframes or mock-ups (10/10)

- It is unclear how DJ would update a song in a room. How do you find a song? How do you deal with other DJs in the room? How do you assign a playlist to a room? Would there be any buttons?

### Additional Information

- If you support too many ways to modify song queue, it will confuse the user. Try to have one definite way to modify a song queue.

---
#### Total score (30/30)
---
Graded by: Sean D Kim (sdk1)

To view this file with formatting, visit the following page: https://github.com/CMU-Web-Application-Development/Team26/blob/master/feedback/specification-feedback.md
