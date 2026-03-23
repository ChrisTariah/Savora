-- User
CREATE TABLE IF NOT EXISTS User (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    privilege TEXT CHECK(privilege IN ('basic','premium','admin')) NOT NULL
);

-- Recipe
CREATE TABLE IF NOT EXISTS Recipe (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    image TEXT DEFAULT "REPLACE WITH LINK TO DEFAULT IMAGE", -- REPLACE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    instructions TEXT NOT NULL,
    userID INTEGER NOT NULL DEFAULT 0,
    mood TEXT CHECK (mood IN ('REPLACE WITH MOODS', 'DEFAULT')) DEFAULT "DEFAULT", -- REPLACE <<<<<<<<<<<<<<<<<<
    FOREIGN KEY (userID) REFERENCES User(ID)
);

-- Tags
CREATE TABLE IF NOT EXISTS Tag (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Recipe_Tag (
    recipeID INTEGER NOT NULL,
    tagID INTEGER NOT NULL,
    PRIMARY KEY (recipeID, tagID),
    FOREIGN KEY (recipeID) REFERENCES Recipe(ID),
    FOREIGN KEY (tagID) REFERENCES Tag(ID)
);

-- Ingredient
CREATE TABLE IF NOT EXISTS Ingredient (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    unit_type TEXT CHECK(unit_type IN ('g', 'ml', 'tsp', 'tbsp','cnt')) NOT NULL
    -- Uncomment (and add comma above) when these become available via the API 
    --price REAL NOT NULL,
    --energy_Kj INTEGER NOT NULL,
    --fat REAL,
    --fat_saturates REAL,
    --carbs REAL,
    --sugar REAL,
    --fibre REAL,
    --protein REAL,
    --salt REAL
);

CREATE TABLE IF NOT EXISTS Ingredient_Line (
    ingredientID INTEGER NOT NULL,
    recipeID INTEGER NOT NULL,
    quantity REAL NOT NULL,
    PRIMARY KEY (ingredientID, recipeID),
    FOREIGN KEY (ingredientID) REFERENCES Ingredient(ID),
    FOREIGN KEY (recipeID) REFERENCES Recipe(ID)
);

-- Fridge
CREATE TABLE IF NOT EXISTS Fridge (
    userID INTEGER NOT NULL,
    ingredientID INTEGER NOT NULL,
    quantity REAL NOT NULL,
    PRIMARY KEY (userID, ingredientID),
    FOREIGN KEY (userID) REFERENCES "User"(ID),
    FOREIGN KEY (ingredientID) REFERENCES Ingredient(ID)
);

-- Sessions
CREATE TABLE IF NOT EXISTS sessions (
    token TEXT PRIMARY KEY,
    userID INTEGER NOT NULL,
    FOREIGN KEY (userID) REFERENCES User(ID)
);

-- Chat Bot
CREATE TABLE IF NOT EXISTS AI_Chat (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    userID INTEGER NOT NULL,
    message TEXT NOT NULL,
    sender TEXT NOT NULL CHECK(sender IN ('user','ai')),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(userID) REFERENCES User(ID)
);