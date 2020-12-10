/* return song name, artist name, album name, artist id, and album id based on the playlist id */

SELECT song.songName, artist.artistName, album.albumName, artist.artistID, album.albumID
FROM playlist
LEFT JOIN song
    ON playlist.songID = song.songID
INNER JOIN artist
    ON song.artistID = artist.artistID
INNER JOIN album
    ON song.albumID = album.albumID
    WHERE playlistID = :playlist_id;