# ABF-Web-Player
Members of Stanford's ABF Drumz have to learn parts by ear, using recordings. ABF-Web-Player makes it easier in a variety of ways.

## Features
* Play, pause, back up, jump forward
* Control tempo (speed up or slow down the recording) and volume (independently!)
* Choice of full band or part (snare or tom) recordings
* Notable sections within songs are "bookmarked"

## Dependencies
`pip install flask`

## Running
`python3 app.py`

## Updating
* The list of songs is pulled from Google Drive -- simply update the URL at the top of `app.py`
* The "bookmarks" are stored in a database -- manually edit the database to add new ones

---

# To Do
* Style
* Global settings page -- set cookie (move cookie methods to separate file)
* When preferred is disabled, select another option
* Play from Google Drive
* Deal with recordings with () differently -- snare/tom/other? (Hell beats)
* Add bookmarks
* Go through file list only once -- cache
