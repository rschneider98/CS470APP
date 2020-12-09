/* return list of playlists and playlist ids with input of user id */

SELECT playlistName, playlistID
FROM directory
WHERE userID = :user_id;