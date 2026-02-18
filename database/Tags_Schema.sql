-- This is used to add tags to recipes and can be added at any point
-- [PASSSED TESSTING]
USE Savora;

CREATE TABLE Tag (
    ID INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(25) NOT NULL,
    PRIMARY KEY (ID)
);
CREATE TABLE Recipe_Tag (
    RecipeID INT NOT NULL,
    TagID INT NOT NULL,
    CONSTRAINT PK_Recipe_Tag PRIMARY KEY (RecipeID, TagID),
    FOREIGN KEY (RecipeID) REFERENCES Recipe(ID),
    FOREIGN KEY (TagID) REFERENCES Tag(ID)
);