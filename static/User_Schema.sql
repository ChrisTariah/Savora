-- Adds user table to database, can be implementaed at any time
-- [PASSED TESTING]
-- User table for SQLite

CREATE TABLE IF NOT EXISTS "User" (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    privilege TEXT CHECK(privilege IN ('basic','premium','admin')) NOT NULL
);

-- Add userID column to Recipe table
ALTER TABLE Recipe ADD COLUMN userID INTEGER NOT NULL DEFAULT 0;

-- Add foreign key constraint in SQLite (must be done manually if needed)
-- SQLite allows only one column addition at a time, foreign keys are enforced via PRAGMA
-- So make sure PRAGMA foreign_keys=ON is set in Python