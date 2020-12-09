/* add song to a playlist
   Note: verification that we are updating  */

INSERT INTO playlist (playlistID, songID)
VALUES (:playlist_id, :song_id);