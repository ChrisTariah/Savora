-- This adds new information to the ingredients table for use with the API
-- SQLite version

ALTER TABLE Ingredient ADD COLUMN price REAL NOT NULL;
ALTER TABLE Ingredient ADD COLUMN energy_Kj INTEGER NOT NULL;
ALTER TABLE Ingredient ADD COLUMN fat REAL;
ALTER TABLE Ingredient ADD COLUMN fat_saturates REAL;
ALTER TABLE Ingredient ADD COLUMN carbs REAL;
ALTER TABLE Ingredient ADD COLUMN sugar REAL;
ALTER TABLE Ingredient ADD COLUMN fibre REAL;
ALTER TABLE Ingredient ADD COLUMN protein REAL;
ALTER TABLE Ingredient ADD COLUMN salt REAL;