/* with a one-word search string we want to find songs that contain the string
   and return the song title, artist, album, song id, artist id, and album id */

SELECT song.songName, artist.artistName, album.albumName, song.songID, artist.artistID, album.albumID
FROM song
LEFT JOIN album
    ON song.albumID = album.albumID
    WHERE UPPER(song) like :search_string
INNER JOIN artist
    ON song.artistID = artist.artistID;