-- This is used to add Ingredients to the database and can be added at any time
-- [PASSED TESSTING]
-- Ingredient and Ingredient_Line tables for SQLite

CREATE TABLE IF NOT EXISTS Ingredient (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    unit_type TEXT NOT NULL  -- Use 'g', 'ml', 'tsp', 'tbsp' as valid values in your code
);

CREATE TABLE IF NOT EXISTS Ingredient_Line (
    ingredientID INTEGER NOT NULL,
    recipeID INTEGER NOT NULL,
    quantity REAL NOT NULL,
    PRIMARY KEY (ingredientID, recipeID),
    FOREIGN KEY (ingredientID) REFERENCES Ingredient(ID),
    FOREIGN KEY (recipeID) REFERENCES Recipe(ID)
);