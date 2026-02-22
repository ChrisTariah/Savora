-- Adds user table to database, can be implementaed at any time
-- [PASSED TESTING]
USE Savora;

CREATE TABLE User(
    ID INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(25) NOT NULL,
    password VARCHAR(50) NOT NULL,
    privilege ENUM('basic', 'premium', 'admin') NOT NULL,
    PRIMARY KEY (ID)
);

ALTER TABLE Recipe
ADD userID INT NOT NULL DEFAULT 0,
ADD FOREIGN KEY (UserID) REFERENCES User(ID);
