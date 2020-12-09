/* remove a user's playlist
   Note: MySQL Server will automatically rollback transaction if error */

START TRANSACTION;
DELETE FROM playlist
WHERE playlistID = :playlist_id;

DELETE FROM directory
WHERE playlistID = :playlist_id;
COMMIT;