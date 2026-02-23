-- This line should only be needed if the server you are testing on has multiple databases
USE Savora;

------------------------------------------------------------------------------------------------
-- Recipe Display Queries ----------------------------------------------------------------------
------------------------------------------------------------------------------------------------

-- Get ingredient table of a recipe
SELECT Ingredient.name AS name, Ingredient_Line.quantity AS quantity, 
    Ingredient.unit_type AS unit
FROM Ingredient_Line 
JOIN Ingredient ON Ingredient.ID = Ingredient_Line.ingredientID
WHERE Ingredient_Line.recipeID = 1; -- Replace with desired recipe ID

-- Get nutritional value and price of a recipe
SELECT SUM(Ingredient.price * Ingredient_Line.quantity) AS cost, 
    SUM(Ingredient.energy_Kj * Ingredient_Line.quantity) AS energy_kj,
    SUM(Ingredient.fat * Ingredient_Line.quantity) AS fat,
    SUM(Ingredient.fat_saturates * Ingredient_Line.quantity) AS fat_saturates,
    SUM(Ingredient.carbs * Ingredient_Line.quantity) AS carbs,
    SUM(Ingredient.sugar * Ingredient_Line.quantity) AS sugar,
    SUM(Ingredient.fibre * Ingredient_Line.quantity) AS fibre,
    SUM(Ingredient.protein * Ingredient_Line.quantity) AS protein,
    SUM(Ingredient.salt * Ingredient_Line.quantity) AS salt
FROM Ingredient
JOIN Ingredient_Line ON Ingredient.ID = Ingredient_Line.ingredientID
WHERE Ingredient_Line.recipeID = 1; -- Replace with desired recipe ID

-- Get all tags associated with a recipe
SELECT Tag.name as tag from Tag 
JOIN Recipe_Tag ON Recipe_Tag.tagID = Tag.ID 
WHERE Recipe_Tag.recipeID = 1; -- Replace with desired recipe ID

------------------------------------------------------------------------------------------------
-- Search Queries ------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------

-- Get all recipes associated with a tag
SELECT Recipe.ID AS ID, Recipe.name AS name 
FROM Recipe_Tag
JOIN Recipe ON Recipe.ID = Recipe_Tag.recipeID
JOIN Tag ON Tag.ID = Recipe_Tag.tagID
WHERE Tag.name = 'test tag'; -- Replace with desired tag name

-- Get all recipes added by a user
SELECT Recipe.ID AS ID, Recipe.name AS name 
FROM Recipe
JOIN User ON User.ID = Recipe.userID
WHERE User.username = 'ADMIN'; -- Replace with desired username

-- Get all recipes by some filter
SELECT Recipe.ID AS ID, Recipe.name AS name,
    (Ingredient.price * Ingredient_Line.quantity) AS cost, 
    SUM(Ingredient.energy_Kj * Ingredient_Line.quantity) AS energy_kj,
    SUM(Ingredient.fat * Ingredient_Line.quantity) AS fat,
    SUM(Ingredient.fat_saturates * Ingredient_Line.quantity) AS fat_saturates,
    SUM(Ingredient.carbs * Ingredient_Line.quantity) AS carbs,
    SUM(Ingredient.sugar * Ingredient_Line.quantity) AS sugar,
    SUM(Ingredient.fibre * Ingredient_Line.quantity) AS fibre,
    SUM(Ingredient.protein * Ingredient_Line.quantity) AS protein,
    SUM(Ingredient.salt * Ingredient_Line.quantity) AS salt
FROM Ingredient
JOIN Ingredient_Line ON Ingredient.ID = Ingredient_Line.ingredientID
JOIN Recipe ON Recipe.ID = Ingredient_Line.recipeID
HAVING cost > 0; -- Replace with desired filter

-- Get all recipes that include fridge ingredients
SELECT Recipe.ID AS ID, Recipe.name AS name
FROM Ingredient_Line
JOIN Fridge ON Fridge.ingredientID = Ingredient_Line.ingredientID
JOIN Recipe ON Recipe.ID = Ingredient_Line.recipeID
WHERE Ingredient_Line.quantity <= Fridge.quantity
AND Fridge.userID = 1 -- Replace with desired user 
GROUP BY Recipe.ID;

-- Get all recipes that include ONLY fridge ingredients
SELECT Recipe.ID AS ID, Recipe.name AS name
FROM Recipe
WHERE NOT Recipe.ID = ANY (
    SELECT Ingredient_Line.recipeID
    FROM Ingredient_Line
    LEFT JOIN Fridge ON Fridge.ingredientID = Ingredient_Line.ingredientID 
    AND Fridge.userID = 1 -- Replace with desired user ID
    WHERE Ingredient_Line.quantity > Fridge.quantity OR Fridge.quantity IS NULL
);

