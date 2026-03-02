-- This is used to add tags to recipes and can be added at any point
-- [PASSSED TESSTING]
-- Tags and Recipe_Tag tables for SQLite

CREATE TABLE IF NOT EXISTS Tag (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Recipe_Tag (
    recipeID INTEGER NOT NULL,
    tagID INTEGER NOT NULL,
    PRIMARY KEY (recipeID, tagID),
    FOREIGN KEY (recipeID) REFERENCES Recipe(ID),
    FOREIGN KEY (tagID) REFERENCES Tag(ID)
);