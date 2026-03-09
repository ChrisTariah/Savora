-- This adds new information to the ingredients table for use with the API
-- and can only be added once the Ingredient table exists
-- [PASSED TESSTING]
USE Savora;

ALTER TABLE Ingredient
ADD price DECIMAL(6,2),
ADD energy_kj INT,
ADD fat DECIMAL(5,2),
ADD fat_saturates DECIMAL(5,2),
ADD carbs DECIMAL(5,2),
ADD sugar DECIMAL(5,2),
ADD fibre DECIMAL(5,2),
ADD protein DECIMAL(5,2),
ADD salt DECIMAL(5,2);
