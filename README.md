# amMentor Backend

This is the documentation for amMentor

## Data Models

- **Members**: Represents users with mentorship relationships and track progress
- **Tracks**: Represents learning paths
- **Tasks**: Represents individual assignments within tracks
- **Curriculum**: Tracks member progress through tasks
- **Submissions**: Stores task submissions and evaluation
- **Badges**: Represents achievements
- **Badges_Members**: Links members to earned badges

## Notes

- Task deadlines are specified in days
- Points are awarded based on task completion and timeliness
- Flowchart must be opened through [draw.io](https://app.diagrams.net/)

## Endpoints

### Admin Endpoints

#### `/admin/create_track/`
**POST**

Receives: `{ 'track': <track_name> }`

Returns: `{ "Successfully created": "<track_name>" }`

#### `/admin/delete_track/`
**POST**

Receives: `{ 'track': <track_name> }`

Returns: `{ "Successfully deleted": "<track_name>" }`

#### `/admin/create_task/`
**POST**

Receives: `{ 'task_name': <name>, 'task_num': <number>, 'task_description': <description>, 'points': <points>, 'deadline': <deadline_days>, 'track': <track_name> }`

Returns: `{ "Succesfully created task: ": "<task_name>" }`

#### `/admin/delete_task/`
**POST**

Receives: `{ 'task_name': <name>, 'task_num': <number>, 'track': <track_name> }`

Returns: `{ "Succesfully deleted": "<task_name>" }`

#### `/admin/create_member/`
**POST**

Receives: `{ 'name': <name>, 'discord': <discord_handle>, 'github': <github_handle>, 'email': <email>, 'group': <group> }`

Returns: `{ "Added member: ": "<name>" }`

#### `/admin/delete_member/`
**POST**

Receives: `{ 'member': { 'name': <name> } }`

Returns: `{ "Removed member": <member_object> }`

#### `/admin/assign_mentor/`
**POST**

Receives: `{ 'mentor': <mentor_name>, 'mentee': <mentee_name> }`

Returns: `{ "Successfully assigned": "<mentor_name>" }`

#### `/admin/create_badge/`
**POST**

Receives: `{ 'badge': <badge_name>, 'icon': <icon_url> }`

Returns: `{ "Successfully created": "<badge_name>" }`

#### `/admin/delete_badge/`
**POST**

Receives: `{ 'badge': <badge_name> }`

Returns: `{ "Succesfully deleted: ": "<badge_name>" }`

### Member Endpoints

#### `/member/display_tracks/`
**GET**

Returns: `{ "tracks": [<track_list>] }`

#### `/member/select_track/`
**POST**

Receives: `{ 'track': <track_name>, 'member': <member_name> }`

Returns: `{ "Succesfully changed track": "<track_name>" }`

#### `/member/display_member_tasks/`
**POST**

Receives: `{ 'member': <member_name> }`

Returns: `{ "tasks": [{ 'task_name': <name>, 'task_num': <number>, 'points': <points>, 'deadline': <days>, 'status': <status>, 'track': <track_name> }, ...] }`

#### `/members/display_track_tasks/`
**POST**

Receives: `{ 'track': <track_name> }`

Returns: `[{ 'task_name': <name>, 'task_num': <number>, 'points': <points>, 'deadline': <days>, 'track': <track_name> }, ...]`

#### `/member/task_details/`
**POST**

Receives: `{ 'task_name': <name>, 'task_num': <number>, 'member': <member_name> }`

Returns: `{ "task_name": <name>, "task_num": <number>, "task_description": <description>, "deadline": <days>, "points": <points>, "track": <track_name>, "start_date": <date>, "end_date": <date>, "days_left": <days>, "days_worked": <days> }`

#### `/member/start_task/`
**POST**

Receives: `{ 'task_name': <name>, 'task_num': <number>, 'member': <member_name> }`

Returns: `{ "Started Task: ": "<task_name>" }`

#### `/member/pause_task/`
**POST**

Receives: `{ 'mentor': <mentor_name>, 'task_name': <name>, 'task_num': <number> }`

Returns: `{ "paused": "<task_name>" }`

#### `/member/resume_task/`
**POST**

Receives: `{ 'mentor': <mentor_name>, 'member': <member_name>, 'task_name': <name>, 'task_num': <number> }`

Returns: `{ "resumed": "<task_name>" }`

#### `/member/submit_task/`
**POST**

Receives: `{ 'mentor': <mentor_name>, 'member': <member_name>, 'task_name': <name>, 'task_num': <number>, 'sub_url': <submission_url> }`

Returns: `{ "Succesfully submitted": "<task_name>" }`

#### `/member/pending_review/`
**POST**

Receives: `{ 'mentor': <mentor_name> }`

Returns: `{ true: 'Pending review' }` or `{ false: 'No pending reviews' }`

#### `/member/display_submission/`
**POST**

Receives: `{ 'mentor': <mentor_name> }`

Returns: `{ "task_name": <name>, "task_num": <number>, "sub_url": <url>, "mentee": <mentee_name>, "submitted_on": <timestamp> }`

#### `/member/mentor_eval/`
**POST**

Receives: `{ 'mentor': <mentor_name>, 'feedback': <feedback_text>, 'accepted': <boolean>, 'task_name': <name>, 'task_num': <number> }`

Returns: `{ true: 'Completed task' }` or `{ false: 'Continue task' }`

#### `/member/task_leaderboard/`
**POST**

Receives: `{ 'task_name': <name>, 'task_num': <number>, 'track': <track_name> }`

Returns: `[{ 'name': <member_name>, 'days_spent': <days> }, ...]`

#### `/member/track_leaderboard/`
**POST**

Receives: `{ 'track': <track_name> }`

Returns: `[{ <member_name>: { "tasks_completed": <count>, "total_days": <days> } }, ...]`

#### `/member/member_details/`
**POST**

Receives: `{ "email": <email> }` or `{ "name": <name> }`

Returns: `{ 'name': <name>, 'email': <email>, 'discord': <discord>, 'github': <github>, 'mentor': <mentor_name>, 'mentee': <mentee_name>, 'year': <year>, 'points': <points>, 'group': <group>, 'track': <track_name>, 'pfp': <profile_picture_url> }`

#### `/member/customize/`
**POST**

Receives: At least one of `{ 'discord': <discord>, 'github': <github>, 'email': <email>, 'pfp': <profile_picture>, 'group': <group>, 'year': <year>, 'track': <track> }`

Returns: `{ "message": "Profile updated" }`

#### `/member/points_leaderboard/`
**GET**

Returns: `[{ 'name': <member_name>, 'points': <points> }, ...]`

#### `/member/mentee_details/`
**POST**

Receives: `{ 'mentor': <mentor_name> }`

Returns: `{ "name": <name>, "discord": <discord>, "github": <github>, "points": <points>, "group": <group>, "pfp": <profile_picture_url>, "track": <track_name> }`

#### `/member/mentee_tasks/`
**POST**

Receives: `{ 'mentor': <mentor_name> }`

Returns: `{ "tasks": [{ 'task_name': <name>, 'task_num': <number>, 'points': <points>, 'deadline': <days>, 'status': <status>, 'track': <track_name> }, ...] }`

#### `/member/assign_badge/`
**POST**

Receives: `{ "badge": <badge_name>, "member": <member_name> }`

Returns: `{ "Succesfully assigned badge": "<badge_name>" }`

#### `/member/badges_earned/`
**POST**

Receives: `{ 'member': <member_name> }`

Returns: `{ "badges earned": [<badge_list>] }`