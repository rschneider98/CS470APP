/* get name of album based on album id */

SELECT albumName
FROM album
WHERE albumID = :album_id;