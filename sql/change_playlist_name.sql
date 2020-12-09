/* allow a user to update a playlist's name */

UPDATE directory
SET playlistName = :playlist_name
WHERE playlistID = :playlist_id;