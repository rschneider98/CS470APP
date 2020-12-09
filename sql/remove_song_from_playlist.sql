/* remove a song from a user's playlist */

DELETE FROM playlist
WHERE playlistID = :playlist_id
AND songID = :song_id;