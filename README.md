# Savora
This is the GitHub repository for Savora, by The Hungry Coders.
## Database
The database directory holds all of the sql files needed to create and expand the database. The files are separated into incremental additions to the database based on feature implementation. The following table lists the file name, the feature it implements, and the dependencies on other files as some require other tables to be added first.

| File | Feature | Dependencies |
|:-----|:-------:|-------------:|
| Minimum_Viable_Schema.sql | Creates the database and adds the recipe table | None |
| Ingredient_Schema.sql | Adds the basic ingredient tables to the database | Minimum_Viable_Schema.sql |
| Ingredient_API_Schema.sql | Extends the ingredient table to include info pulled from APIs | Minimum_Viable_Schema.sql<br>Ingredient_Schema.sql |
| Tag_Schema.sql | Adds the tag tables to the database | Minimum_Viable_Schema.sql |
| User_Schema.sql | Adds the user table to the database and extends recipe table to include user ID | Minimum_Viable_Schema.sql |
| Fridge_Schema.sql | Adds the fridge table to the database | Minimum_Viable_Schema.sql<br>User_Schema.sql<br>Ingredient_Schema.sql |
| Mood_Schema.sql | Adds mood field to recipes for spotify integration | Minimum_Viable_Schema.sql |

Additionally there is a file Query_Library.sql that has some queries that may be usseful to the site, such as filtering by price or showing only recipes the user has ingredients for. More queries can be added by request. Note that each query will have a line with a comment stating where a variable should be used like:
``` sql
AND Fridge.userID = 1 -- Replace with desired user 
```
This is the search parameter or filter being applied and should be set by user interaction or account information (userID).