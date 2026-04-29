import threading
from server.db.database import get_db
import threading

def build_search_index():
    con = get_db()

    print("Building search index...")

    recipes = con.execute("""
        SELECT Recipe.id, Recipe.name,
               GROUP_CONCAT(DISTINCT Ingredient.name),
               GROUP_CONCAT(DISTINCT Tag.name)
        FROM Recipe
        LEFT JOIN Ingredient_Line ON Recipe.ID = Ingredient_Line.recipeID
        LEFT JOIN Ingredient ON Ingredient.ID = Ingredient_Line.ingredientID
        LEFT JOIN Recipe_Tag ON Recipe.ID = Recipe_Tag.recipeID
        LEFT JOIN Tag ON Tag.ID = Recipe_Tag.tagID
        GROUP BY Recipe.id
    """).fetchall()

    con.execute("DELETE FROM recipe_search")

    for r in recipes:
        content = f"{r[1]} {r[2] or ''} {r[3] or ''}"
        con.execute(
            "INSERT INTO recipe_search (recipe_id, name, content) VALUES (?, ?, ?)",
            (r[0], r[1], content)
        )

    con.commit()
    con.close()

    print(f"Indexed {len(recipes)} recipes.")

def create_search_table():
    con = get_db()
    con.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS recipe_search
        USING fts5(recipe_id, name, content)
    """)
    con.commit()
    con.close()
    return

def rebuild_index_async(con=get_db()):
    threading.Thread(target=build_search_index, args=(con,), daemon=True).start()


def start_indexer():
    create_search_table()
    thread = threading.Thread(target=build_search_index)
    thread.daemon = True
    thread.start()


