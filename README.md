# Savora
This is the GitHub repository for Savora, by The Hungry Coders.
## Database
The database is an SQLite local disk database created from scratch using the script [setup_database.py](./static/setup_database.py) and the file [Base_Schema.sql](./static/Base_Schema.sql). Within [setup_database.py](./static/setup_database.py) is the list of files that will be run to build the database. This list must always include [Base_Schema.sql](./static/Base_Schema.sql) and may include additional files to modify or populate the database such as [Test_Data.sql](./static/Test_Data.sql):
``` python
SQL_FILES = [
    "static/Base_Schema.sql",
    "static/Test_Data.sql" 
] 
```

Within [Base_Schema.sql](./static/Base_Schema.sql) there are some lines commented out as they may not be implemented until an ingredient API is added to populate the table with the relevant information. Permanent changes to the database should be added to the [Base_Schema.sql](./static/Base_Schema.sql) file, rather than in a new separate file, but temporary changes for testing should remain in separate files and added to the SQL_FILE list in [setup_database.py](./static/setup_database.py).

#### Query Library
The file [Query_Library.sql](./static/Query_Library.sql) that has some queries that may be useful to the site, such as filtering by price or showing only recipes the user has ingredients for. More queries can be added by request. Note that each query will have a line with a comment stating where a variable should be used like:
``` sql
AND Fridge.userID = 1 -- Replace with desired user 
```
This is the search parameter or filter being applied and should be set by user interaction or account information (userID).

#### Query Database With A Terminal Session
The file [database_terminal_session.py](./database_terminal_session.py) which will allow you to open the [Savora.db](./Savora.db) file and interact with it using SQLite commands for testing and development purposes.

#### Recipes Via API 
The file [get_recipes.py](./RecipeAPI/get_recipes.py) is a script that will pull recipes from a [free api](https://www.themealdb.com/) and add them to the database. The script checks for existing recipes before adding them, so it can be run at any point with no need to rebuild the database (unlike when running [setup_database.py](./static/setup_database.py)). This API is only free for non-commercial use. 
Currently the script can only parse about 50% of the 500 or so recipes. If more are needed this could be improved. However, the code is really quite bad. If the script will need frequent maintenance it would worthwhile to refactor the whole thing.