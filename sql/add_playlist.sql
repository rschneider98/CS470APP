/* insert a new playlist name for a user
   Note: playlistID will auto increment */

INSERT INTO directory (userID, playlistName)
VALUES (:user_id, :playlist_name);