-- This is used to add Ingredients to the database and can be added at any time
-- [PASSED TESSTING]
USE Savora;

CREATE TABLE Ingredient (
    ID INT NOT NULL AUTO_INCREMENT,
    Name VARCHAR(25) NOT NULL,
    Unit_Type ENUM('g', 'ml', 'tsp', 'tbsp') NOT NULL, 
    -- Note this means that "4 tomatoes" is invalid. Regardless of how it is displayed
    -- to the user, the server will need to understand it as "250g tomatoes".
    PRIMARY KEY (ID)
);
CREATE TABLE Ingredient_Line (
    IngredientID INT NOT NULL,
    RecipeID INT NOT NULL,
    Quantity INT NOT NULL,
    CONSTRAINT PK_Ingredient_Line PRIMARY KEY (IngredientID, RecipeID),
    FOREIGN KEY (IngredientID) REFERENCES Ingredient(ID),
    FOREIGN KEY (RecipeID) REFERENCES Recipe(ID)
);