from urllib.request import urlopen
import json
from typing import Any
import logging
import sqlite3

logging.basicConfig(level=logging.INFO)

API_KEY : str = "1"
"""Test API key ("1") only for FREE use! 
Must buy premium if publishing app!"""

SEARCH_URL : str = f"https://www.themealdb.com/api/json/v1/{API_KEY}/search.php?f="
"""API url. Append search term to end of string."""

DATABASE_PATH: str = "Savora.db"

# If adding to a populated database, set these higher than the max ID of the respective table
RECIPE_STARTING_ID: int     = 1
INGREDIENT_STARTING_ID: int = 1

# Logging stats
total_meals: int        = 0
failed_meals: int       = 0
processed_meals: int    = 0

# Custom types
type RecipeType =  dict[str,dict[str,str|list[str]|dict[str,dict[str,str]]]]
"""The dictionary structure that holds recipe information, like\:
        {
        "NAME":
            {
            "image" : "___",
            "instructions" : "___",
            "tags" : ["___",...],
            "ingredients" : {"NAME" {"units" : "___", "quantity" : "___"}, ...}
            },
        ...
        }"""
 
# --- API Structure -----------------------------------------------------------------------------
"""
{"meals":
    [{"idMeal":<ID>,
        "strMeal":<NAME>,"strMealAlternate":<n/a>,
        "strCategory":<TAG>,"strArea":"<TAG>",
        "strInstructions":<INSTRUCTIONS>,
        "strMealThumb":<IMAGE>,"strTags":<TAG>,
        "strYoutube":<n/a>,
        "strIngredient1":<INGREDIENT NAME>,
        "strIngredient2":<INGREDIENT NAME>,
        "strIngredient3":<INGREDIENT NAME>,
        "strIngredient4":<INGREDIENT NAME>,
        "strIngredient5":<INGREDIENT NAME>,
        "strIngredient6":<INGREDIENT NAME>,
        "strIngredient7":<INGREDIENT NAME>,
        "strIngredient8":<INGREDIENT NAME>,
        "strIngredient9":<INGREDIENT NAME>,
        "strIngredient10":<INGREDIENT NAME>,
        "strIngredient11":<INGREDIENT NAME>,
        "strIngredient12":<INGREDIENT NAME>,
        "strIngredient13":<INGREDIENT NAME>,
        "strIngredient14":<INGREDIENT NAME>,
        "strIngredient15":<INGREDIENT NAME>,
        "strIngredient16":<INGREDIENT NAME>,
        "strIngredient17":<INGREDIENT NAME>,
        "strIngredient18":<INGREDIENT NAME>,
        "strIngredient19":<INGREDIENT NAME>,
        "strIngredient20":<INGREDIENT NAME>,
        "strMeasure1":<INGREDIENT QUANTITY + UNITS>,
        "strMeasure2":<INGREDIENT QUANTITY + UNITS>,
        "strMeasure3":<INGREDIENT QUANTITY + UNITS>,
        "strMeasure4":<INGREDIENT QUANTITY + UNITS>,
        "strMeasure5":<INGREDIENT QUANTITY + UNITS>,
        "strMeasure6":<INGREDIENT QUANTITY + UNITS>,
        "strMeasure7":<INGREDIENT QUANTITY + UNITS>,
        "strMeasure8":<INGREDIENT QUANTITY + UNITS>,
        "strMeasure9":<INGREDIENT QUANTITY + UNITS>,
        "strMeasure10":<INGREDIENT QUANTITY + UNITS>,
        "strMeasure11":<INGREDIENT QUANTITY + UNITS>,
        "strMeasure12":<INGREDIENT QUANTITY + UNITS>,
        "strMeasure13":<INGREDIENT QUANTITY + UNITS>,
        "strMeasure14":<INGREDIENT QUANTITY + UNITS>,
        "strMeasure15":<INGREDIENT QUANTITY + UNITS>,
        "strMeasure16":<INGREDIENT QUANTITY + UNITS>,
        "strMeasure17":<INGREDIENT QUANTITY + UNITS>,
        "strMeasure18":<INGREDIENT QUANTITY + UNITS>,
        "strMeasure19":<INGREDIENT QUANTITY + UNITS>,
        "strMeasure20":<INGREDIENT QUANTITY + UNITS>,
        "strSource":<n/a>,"strImageSource":<n/a>,"strCreativeCommonsConfirmed":<n/a>,"dateModified":<n/a>},
        ...
        ]}
"""
#------------------------------------------------------------------------------------------------

def get_all() -> list[dict[str,str]]:
    """
    Gets all recipes from the API alphabetically

    :returns: List of every meal as a dictionary
    """
    global total_meals
    logging.info("Connecting to API...")
    # Fetching all recipes
    meals_list : list[dict[str,str]] = []
    for letter in range(ord('a'), ord('z') + 1):
        logging.debug(f"Fetching recipes that start with: {chr(letter)}...")
        url : str = SEARCH_URL + chr(letter)
        response = urlopen(url)
        new_dict : dict[str,str] = json.loads(response.read())
        new_list : Any = new_dict["meals"]
        if type(new_list) != list: continue # No meals of that letter
        new_list = [dict(x) for x in new_list]
        meals_list += new_list

    total_meals = len(meals_list)
    return meals_list

def extract_ingredient(meal: dict[str,str], index : int) -> dict[str,str]:
    """
    Extracts information for one ingredient and returns it as a dict.

    :param meal: The meal with an ingredient to extract
    :param index: The number of the ingredient to extract (1 - 20 inclusive)
    :raises ValueError: If ingredient information can not be parsed
    :returns: dict like\: {"name": __, "unit": __, "quantity": __}
    """
    # Skip if empty
    if not meal[f"strIngredient{index}"]: return{}
    
    # Get components
    name: str           = meal[f"strIngredient{index}"].lower()
    quantity_unit: str  = meal[f"strMeasure{index}"].lower()
    quantity_str: str   = ""
    unit: str           = ""
    for fraction, decimal in {
        "½":.5,"1/2":.5,"¼":.25,"1/4":.25,"3/4":.75,"1/3":.33,"2/3":.66}.items():
        quantity_unit = quantity_unit.replace(fraction,str(decimal))
    for char in quantity_unit:
        if char == ' ': continue
        if char.isnumeric() or char == '.':
            quantity_str += char
        elif char.isalpha():
            unit += char
        else:
            raise ValueError(f"Unhandled char: {char}({ord(char)}) in meal {meal["idMeal"]}\n\t\'{meal[f"strMeasure{index}"]}\'")
    if quantity_str == "": quantity_str = "1"
    quantity: float = float(quantity_str) 

    # Extract description
    descriptions : list[str] = [ # NOTE: always put plural before singular, long before short
        # Form of ingredient
        "cloves","clove","new","large","whole","stalks","stalk","leaves","leaf","sprigs","sprig",
        "heads","head","pods","pod","slices","dried","strips","strip","sticks","stick","cm",
        "packet","zest and juice of","juice of","juice","parts","part","cans","can","zest of","package",
        "bunches","bunch","boneless","boiling","pieces","piece","jars","jar","fresh","pot",
        "skinnless","packs","pack","scoops","scoop","pinches","pinch","inch","inches","kaffir",
        "wedges","wedge","meaty","shanks","shank","stewing","skinned","skin","knobs","knob","shots",
        "shot","handfull","handful","fillets","fillet","florets","floret","bags","bag","tins","tin",
        # Adverb
        "finely","medium","small","thinly","thin","thick",
        # Preparation method
        "cut into","cut","peeled","crushed","grated","sliced","slice","ground","chopped","minced",
        "diced","beaten","quartered","quarters","shredded","cubed","cubes","chunks","mashed"
        ]
    for phrase in descriptions:
        if phrase in quantity_unit.lower():
            name += " " + phrase
            phrase_no_whitespace = phrase.replace(" ", "")
            unit = unit.replace(phrase_no_whitespace,"")

    # Return if able
    accepted_units: list[str] = ["tsp", "tbsp", "g", "ml", "cnt"]
    if unit in accepted_units:
        return {"name":name,"unit":unit,"quantity":str(quantity)}

    # Convert units if needed
    match unit:
        # Abbreviations
        case "teaspoon" | "teaspoons": unit = "tsp"
        case "tablespoon" | "tablespoons" | "tblsp" | "tbs" | "tbls" | "tbs": unit = "tbsp"
        case "gram" | "grams": unit = "g"
        case "": unit = "cnt"  
        case "milliliter": unit = "ml"
        # Conversions
        case "kg" | "kilogram":
            unit = "g"
            quantity *= 1000
        case "l" | "litre" | "litres":
            unit = "ml"
            quantity *= 1000
        case "ounces" | "oz":
            unit = "g"
            quantity *= 28.3495
        case "cups" | "cup":
            unit = "ml"
            quantity *= 236.588
        case "pounds" | "pound" | "lb" | "lbs" | "poundssliced":
            unit = "g"
            quantity *= 453.592
        # Exceptions
        case _:
            raise ValueError(f"No rule for units: {unit} in meal {meal["idMeal"]}:\n\t\'{meal[f"strMeasure{index}"]}\'")
        
    return {"name":name,"unit":unit,"quantity":str(quantity)}

def build_ingredients(meals: list[dict[str,str]]) -> dict[str,int]:
    """
    Extracts and IDs all ingredients used in recipes from API

    :param meals: List of all meals from API
    :returns: Set of all ingredients used in recipes like:\n
            {"carrot(g)" \: 1,\n
             "carrot(cnt)" \: 2,\n
             "milk(ml)" \: 3}
    """
    # Extract all ingredients in all recipes
    all_ingredients : list[str]= []
    for meal in meals:
        try:
            for i in range(1,21): # 20 ingredients per recipe
                ingredient : dict[str,str] = extract_ingredient(meal, i)
                if not ingredient: continue
                all_ingredients.append(f"{ingredient["name"]}({ingredient["unit"]})")
        except ValueError as e:
            logging.debug(e)
            continue
    
    # Add only unique ingredients to dictionary
    unique_ingredients : set[str] = set(all_ingredients)
    identified_ingredients : dict[str,int] = {}
    next_ID : int = INGREDIENT_STARTING_ID
    for name in unique_ingredients:
        identified_ingredients[name] = next_ID
        next_ID += 1
    
    return identified_ingredients
    
def build_tags(meals: list[dict[str,str]]) -> dict[str,int]:
    """
    Extracts and IDs all tags from recipes

    :param meals: List of all meals from API
    :returns: Set of all tags used by recipes like\:
                {"vegan":1, "halal":2,...}
    """
    all_tags: list[str] = []
    for meal in meals:
        category: str|None  = meal["strCategory"]
        area: str|None      = meal["strArea"]
        tags: str|None      = meal["strTags"]
        if category:    all_tags.extend(category.split(","))
        if area:        all_tags.extend(area.split(","))
        if tags:        all_tags.extend(tags.split(","))
    
    unique_tags: set[str] = set(all_tags)
    identified_tags: dict[str,int] = {}
    next_ID: int = 1
    for tag in unique_tags:
        if tag == "" or tag == " ": continue
        identified_tags[tag] = next_ID
        next_ID += 1
    return identified_tags

def build_recipes(meals: list[dict[str,str]]) -> RecipeType:
    """
    Extracts all relevant information from API meals and returns it as a dictionary

    :param meals: List of all meals from API
    :returns: Recipe dictionary like\:
        {
        "NAME":
            {
            "image" : "___",
            "instructions" : "___",
            "tags" : ["___",...],
            "ingredients" : {"NAME" {"units" : "___", "quantity" : "___"}, ...}
            },
        ...
        }
    """
    global failed_meals

    recipes: RecipeType = {}
    for meal in meals:
        try:
            
            # Get Ingredients
            meal_ingredients: dict[str,dict[str,str]] = {}
            for i in range(1,21): # 20 possible ingredient lines
                ingredient: dict[str,str] = extract_ingredient(meal,i)
                if not ingredient: continue
                meal_ingredients[ingredient["name"]] = {
                    "unit":ingredient["unit"],
                    "quantity":ingredient["quantity"]}
            
            # Get tags
            tags: list[str] = [tag for tag in build_tags([meal]).keys()]

            #Get recipe strings
            name: str = meal["strMeal"]
            image: str = meal["strMealThumb"]
            instructions: str = meal["strInstructions"]

            recipes[name] = {
                "image":image,
                "instructions":instructions,
                "tags":tags,
                "ingredients":meal_ingredients
            }
        
        # Count failed recipes
        except ValueError as e:
            failed_meals += 1
            logging.debug(e)

    return recipes

def execute_sql(*command, db: str) -> list[Any]:
    """
    Runs an SQLite command on the database

    :param command: command to be run
    :param db: Path to database
    :returns: Results of query or empty list
    """
    result: list[Any] = []
    try:
        # Connect to database
        with sqlite3.connect(db) as conn:
            cursor : sqlite3.Cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")  # enforce foreign keys
            cursor.execute(*command)
            result = cursor.fetchall()
            conn.commit()
        conn.close()
    except Exception as e:
        logging.critical(f"Error, command not executed:\n{e}\nCommand: {command}")
    return result

def findID(table: str, field: str, value: str) -> str:
    """
    Generates SQLite to search a given table for a record where the 
    given field has the given value.

    :param table: Table to search
    :param field: Field to search
    :param value: Value to find. 
    :returns: SQLite query
    """
    return f"""SELECT ID FROM {table} WHERE {field} = {value};"""

def add_recipes(recipes: RecipeType, db: str) -> None:
    """
    Adds only unique recipes, tags, and ingredients to database.

    :param recipes: Recipes to be added
    :param db: Path to database to be added to
    :returns: None 
    """
    global processed_meals
    loading_chunks: int = 20
    percent_loaded: int = 0

    for name,info in recipes.items():
        # Loading bar -ish
        processed_meals += 1
        if processed_meals % round((total_meals-failed_meals)/loading_chunks) == 0:
            percent_loaded += round(100 / loading_chunks)
            logging.info(f"Loaded: {percent_loaded}%")

        # Check for recipe
        find_recipe_query: str = findID("Recipe", "name", "?")
        if execute_sql(find_recipe_query, (name,),db=db):
            logging.debug(f"Recipe \'{name}\' already exists")
            continue
        
        # Add recipe
        add_recipe: str = "INSERT INTO Recipe (name, image, instructions) VALUES (?, ?, ?);"
        execute_sql(add_recipe, (name, info["image"], info["instructions"]), db=db)
        recipeID: str = execute_sql(find_recipe_query, (name,), db=db)[0][0]

        # Add ingredients
        for ingredient, measurement in info["ingredients"].items(): # Ignore typechecking failure
            find_ingredient_query: str = findID("Ingredient", "name", "?")
            if not execute_sql(find_ingredient_query, (ingredient,), db=db):
                # Add ingredient if new
                execute_sql("INSERT INTO Ingredient (name, unit_type) VALUES (?, ?);", 
                            (ingredient, measurement["unit"]), db=db)
            else: logging.debug(f"Ingredient \"{ingredient}\" already exists")

            # Add Ingredient_Line
            ingredientID: str = execute_sql(find_ingredient_query, (ingredient,), db=db)[0][0]
            add_ingredient_line: str = """
                INSERT INTO Ingredient_Line (recipeID, ingredientID, quantity)
                VALUES(?,?,?);
                """
            execute_sql(add_ingredient_line, (recipeID, ingredientID, measurement["quantity"]), db=db)
        
        # Add tags
        for tag in info["tags"]:
            find_tag_query: str = findID("Tag", "name", "?")
            if not execute_sql(find_tag_query, (tag,), db=db):
                # Add tag if new
                add_tag: str = "INSERT INTO Tag (name) VALUES (?);"
                execute_sql(add_tag, (tag,), db=db)
            else: logging.debug(f"Tag \"{tag}\" already exists")

            # Add Recipe_Tag
            tagID: str = execute_sql(find_tag_query, (tag,), db=db)[0][0]
            add_recipe_tag: str = "INSERT INTO Recipe_Tag (recipeID, tagID) VALUES (?,?)"
            execute_sql(add_recipe_tag, (recipeID,tagID), db=db)
            


def main() -> None:
    # Get and process info from API
    meals: list[dict[str,str]] = get_all()
    recipes: RecipeType = build_recipes(meals)

    # Add info to database
    add_recipes(recipes, DATABASE_PATH)
    logging.info(f"Meals extracted: {round(((total_meals-failed_meals)/total_meals)*100)}% [{total_meals-failed_meals}/{total_meals}]")
    

if __name__ == "__main__":
    main()