/* remove a user's playlist */

DELETE FROM playlist
WHERE playlistID = :playlist_id;

DELETE FROM directory
WHERE playlistID = :playlist_id;