/* return name of playlist based on the playlist id */

SELECT playlistName
FROM directory
WHERE playlistID = :playlist_id;