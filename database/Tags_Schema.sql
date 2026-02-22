-- This is used to add tags to recipes and can be added at any point
-- [PASSSED TESSTING]
USE Savora;

CREATE TABLE Tag (
    ID INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(25) NOT NULL,
    PRIMARY KEY (ID)
);
CREATE TABLE Recipe_Tag (
    recipeID INT NOT NULL,
    tagID INT NOT NULL,
    CONSTRAINT PK_Recipe_Tag PRIMARY KEY (recipeID, tagID),
    FOREIGN KEY (recipeID) REFERENCES Recipe(ID),
    FOREIGN KEY (tagID) REFERENCES Tag(ID)
);