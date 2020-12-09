/* return song name, artist name, album name, artist id, and album id based on album */

SELECT song.songName, artist.artistName, album.albumName, artist.artistID, album.albumID
FROM album
LEFT JOIN song
    ON album.albumID = song.albumID
    WHERE album.albumID = :album_id
INNER JOIN artist
    ON album.artistID = artist.artistID;