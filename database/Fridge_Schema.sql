-- This adds a "Fridge Function" table to the database. User and Ingredient tables must exist first.
-- [PASSED TESTING]
USE Savora;

CREATE TABLE Fridge (
    userID INT NOT NULL,
    ingredientID INT NOT NULL,
    quantity FLOAT NOT NULL,
    CONSTRAINT PK_Fridge PRIMARY KEY (userID, ingredientID),
    FOREIGN KEY (userID) REFERENCES User(ID),
    FOREIGN KEY (ingredientID) REFERENCES Ingredient(ID)
);