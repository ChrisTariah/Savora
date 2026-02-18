-- This adds a "Fridge Function" table to the database. User and Ingredient tables must exist first.
-- [PASSED TESTING]
USE Savora;

CREATE TABLE Fridge (
    UserID INT NOT NULL,
    IngredientID INT NOT NULL,
    Quantity FLOAT NOT NULL,
    CONSTRAINT PK_Fridge PRIMARY KEY (UserID, IngredientID),
    FOREIGN KEY (UserID) REFERENCES User(ID),
    FOREIGN KEY (IngredientID) REFERENCES Ingredient(ID)
);