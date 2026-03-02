-- This is the minimum viable database and must come first.
--[PASSED TESTING]
-- This is the minimum viable database and must come first.
-- SQLite version

CREATE TABLE IF NOT EXISTS Recipe (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    image TEXT,
    instructions TEXT NOT NULL
);