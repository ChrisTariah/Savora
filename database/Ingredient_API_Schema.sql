-- This adds new information to the ingredients table for use with the API
-- and can only be added once the Ingredient table exists
-- [PASSED TESSTING]
USE Savora;

ALTER TABLE Ingredient
ADD Price FLOAT NOT NULL,
ADD Energy_Kj INT NOT NULL,
-- Consider allowing the following to be null for easier use
ADD Fat FLOAT NOT NULL,
ADD Fat_Saturates FLOAT NOT NULL,
ADD Carbs FLOAT NOT NULL,
ADD Sugar FLOAT NOT NULL,
ADD Fibre FLOAT NOT NULL,
ADD Protein FLOAT NOT NULL,
ADD Salt FLOAT NOT NULL;