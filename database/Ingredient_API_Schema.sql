-- This adds new information to the ingredients table for use with the API
-- and can only be added once the Ingredient table exists
-- [PASSED TESSTING]
USE Savora;

ALTER TABLE Ingredient
ADD price FLOAT NOT NULL,
ADD energy_Kj INT NOT NULL,
-- Consider allowing the following to be null for easier use
ADD fat FLOAT NOT NULL,
ADD fat_saturates FLOAT NOT NULL,
ADD carbs FLOAT NOT NULL,
ADD sugar FLOAT NOT NULL,
ADD fibre FLOAT NOT NULL,
ADD protein FLOAT NOT NULL,
ADD salt FLOAT NOT NULL;