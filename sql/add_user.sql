/* SQL to add users to the database
Note: This does not set the id, so the DB should be set up to auto increment the index */
INSERT INTO user (
    userID,
    userPassword,
    salt,
    userEmail,
    firstName,
    lastName)
VALUES (
    :user_name,
    :user_password,
    :salt,
    :email,
    :first,
    :last);
