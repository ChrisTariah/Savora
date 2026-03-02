-- This adds a "Fridge Function" table to the database.
-- SQLite version

CREATE TABLE IF NOT EXISTS Fridge (
    userID INTEGER NOT NULL,
    ingredientID INTEGER NOT NULL,
    quantity REAL NOT NULL,
    PRIMARY KEY (userID, ingredientID),
    FOREIGN KEY (userID) REFERENCES "User"(ID),
    FOREIGN KEY (ingredientID) REFERENCES Ingredient(ID)
);