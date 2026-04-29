import urllib
from re import search
from server.db.database import get_db
from urllib.parse import urlparse, parse_qs

def handle_search_ingredient(handler):
    query = urllib.parse.parse_qs(urllib.parse.urlparse(handler.path).query)
    search = query.get("q", [""])[0].lower()
    con = get_db()
    rows = con.execute(
        "SELECT ID, name, unit_type FROM Ingredient WHERE name LIKE ? LIMIT 5",
        (f"%{search}%",)
    ).fetchall()

    result = [
        {"id": r[0], "name": r[1], "unit": r[2]}
        for r in rows
    ]

    handler.send_json(result)
    return


def handle_get_recipes(handler):


    con = get_db()

    parsed = urlparse(handler.path)
    query = parse_qs(parsed.query)
    recipe_id = query.get("id", [None])[0]

    # -------- SINGLE RECIPE --------
    if recipe_id:
        r = con.execute(
            "SELECT id, name, instructions, image FROM Recipe WHERE id = ?",
            (recipe_id,)
        ).fetchone()

        if not r:
            handler.send_json({"error": "recipe not found"}, 404)
            return

        rid, name, instructions, image = r

        ingredients = con.execute(
            "SELECT Ingredient.name, Ingredient_Line.quantity FROM Ingredient_Line "
            "JOIN Ingredient ON Ingredient.ID = Ingredient_Line.ingredientID "
            "WHERE Ingredient_Line.recipeID = ?",
            (rid,)
        ).fetchall()

        tags = con.execute(
            "SELECT Tag.name FROM Recipe_Tag "
            "JOIN Tag ON Tag.ID = Recipe_Tag.tagID "
            "WHERE Recipe_Tag.recipeID = ?",
            (rid,)
        ).fetchall()

        handler.send_json({
            "id": rid,
            "name": name,
            "instructions": instructions,
            "ingredients": [{"name": i[0], "quantity": i[1]} for i in ingredients],
            "tags": [t[0] for t in tags],
            "image": image
        })
        return

    # -------- ALL RECIPES --------
    recipes = con.execute(
        "SELECT id, name, instructions, image FROM Recipe"
    ).fetchall()

    result = []

    for r in recipes:
        rid, name, instructions, image = r

        ingredients = con.execute(
            "SELECT Ingredient.name, Ingredient_Line.quantity FROM Ingredient_Line "
            "JOIN Ingredient ON Ingredient.ID = Ingredient_Line.ingredientID "
            "WHERE Ingredient_Line.recipeID = ?",
            (rid,)
        ).fetchall()

        tags = con.execute(
            "SELECT Tag.name FROM Recipe_Tag "
            "JOIN Tag ON Tag.ID = Recipe_Tag.tagID "
            "WHERE Recipe_Tag.recipeID = ?",
            (rid,)
        ).fetchall()

        result.append({
            "id": rid,
            "name": name,
            "instructions": instructions,
            "ingredients": [{"name": i[0], "quantity": i[1]} for i in ingredients],
            "tags": [t[0] for t in tags],
            "image": image
        })

    handler.send_json(result)

def handle_get_my_recipes(handler):
    from server.db.database import get_db

    con = get_db()
    user_id = handler.get_session_user()

    if not user_id:
        handler.send_json({"error": "login required"}, 403)
        return

    recipes = con.execute(
        "SELECT id, name, instructions, image FROM Recipe WHERE userID = ?",
        (user_id,)
    ).fetchall()

    result = []

    for r in recipes:
        rid, name, instructions, image = r

        ingredients = con.execute(
            "SELECT Ingredient.name, Ingredient_Line.quantity FROM Ingredient_Line "
            "JOIN Ingredient ON Ingredient.ID = Ingredient_Line.ingredientID "
            "WHERE Ingredient_Line.recipeID = ?",
            (rid,)
        ).fetchall()

        tags = con.execute(
            "SELECT Tag.name FROM Recipe_Tag "
            "JOIN Tag ON Tag.ID = Recipe_Tag.tagID "
            "WHERE Recipe_Tag.recipeID = ?",
            (rid,)
        ).fetchall()

        result.append({
            "id": rid,
            "name": name,
            "instructions": instructions,
            "ingredients": [{"name": i[0], "quantity": i[1]} for i in ingredients],
            "tags": [t[0] for t in tags],
            "image": image
        })

    handler.send_json(result)

def handle_create_recipe(handler):
    from server.db.database import get_db

    con = get_db()
    user_id = handler.get_session_user()

    if not user_id:
        handler.send_json({"error": "login required"}, 403)
        return

    data = handler.read_json()

    name = data.get("name")
    instructions = data.get("instructions")
    ing_list = data.get("ingredients", [])
    image = data.get("image")

    if not name or not instructions:
        handler.send_json({"error": "missing fields"}, 400)
        return

    try:
        cursor = con.execute(
            "INSERT INTO Recipe (name, instructions, userID, image) VALUES (?, ?, ?, ?)",
            (name, instructions, user_id, image)
        )

        recipe_id = cursor.lastrowid

        # ingredients
        for ing in ing_list:
            ing_name = ing.get("name")
            ing_qty = ing.get("quantity")

            if not ing_name or not ing_qty:
                continue

            try:
                ing_qty = float(ing_qty)
            except:
                continue

            row = con.execute(
                "SELECT ID FROM Ingredient WHERE name = ?",
                (ing_name,)
            ).fetchone()

            if row:
                ing_id = row[0]
            else:
                cur = con.execute(
                    "INSERT INTO Ingredient (name, unit_type) VALUES (?, ?)",
                    (ing_name, "cnt")
                )
                ing_id = cur.lastrowid

            con.execute(
                "INSERT INTO Ingredient_Line (ingredientID, recipeID, quantity) VALUES (?, ?, ?)",
                (ing_id, recipe_id, ing_qty)
            )

        # tags
        for tag_name in data.get("tags", []):
            tag_name = tag_name.strip().lower()
            if not tag_name:
                continue

            row = con.execute(
                "SELECT ID FROM Tag WHERE name = ?",
                (tag_name,)
            ).fetchone()

            if row:
                tag_id = row[0]
            else:
                cur = con.execute(
                    "INSERT INTO Tag (name) VALUES (?)",
                    (tag_name,)
                )
                tag_id = cur.lastrowid

            con.execute(
                "INSERT OR IGNORE INTO Recipe_Tag (recipeID, tagID) VALUES (?, ?)",
                (recipe_id, tag_id)
            )

        con.commit()

        handler.send_json({
            "status": "recipe added",
            "recipe_id": recipe_id
        })
        from server.services.search_indexer import rebuild_index_async
        rebuild_index_async()

    except Exception as e:
        print("Error:", e)
        handler.send_json({"error": "internal server error"}, 500)