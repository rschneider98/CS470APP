/* return album name, album year, and album id for an artist id - order by year */

SELECT albumName, albumDate, albumID
FROM album
WHERE artistID = :artist_id
ORDER BY albumDate;