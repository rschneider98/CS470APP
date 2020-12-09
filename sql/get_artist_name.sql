/* return artist name based on artist id */

SELECT artistName
FROM artist
WHERE artistID = :artist_id;