/* SQL stored procedure for sqlalchemy to get the user's hashed password and salt for id */
select userID, userPassword, salt
from user
where userID = :user
