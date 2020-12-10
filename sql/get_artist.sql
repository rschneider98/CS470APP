/* return album name, album year, and album id for an artist id - order by year */

SELECT album.albumName, artist.artistID, album.albumID
FROM album
LEFT JOIN artist
ON artist.artistID = album.albumID
WHERE artistID = :artist_id;