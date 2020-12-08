/* SQL to add users to the database
Note: This does not set the id, so the DB should be set up to auto increment the index */
INSERT user
SET userID = :user_name,
    userPassword = :user_password,
    salt = :salt,
    userEmail = :email,
    userFirst = :first,
    userLast = :last;
