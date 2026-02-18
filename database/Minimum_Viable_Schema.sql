-- This is the minimum viable database and must come first.
--[PASSED TESTING]
CREATE DATABASE Savora;
USE Savora;

CREATE Table Recipe (
ID INT NOT NULL AUTO_INCREMENT,
name VARCHAR(50) NOT NULL,
image VARCHAR(50),
instructions TEXT NOT NULL,
PRIMARY KEY (ID)
);
