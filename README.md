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

Additionally there is a file [Query_Library.sql](./static/Query_Library.sql) that has some queries that may be useful to the site, such as filtering by price or showing only recipes the user has ingredients for. More queries can be added by request. Note that each query will have a line with a comment stating where a variable should be used like:
``` sql
AND Fridge.userID = 1 -- Replace with desired user 
```
This is the search parameter or filter being applied and should be set by user interaction or account information (userID).