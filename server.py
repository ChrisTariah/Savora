import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sqlite3
import uuid
import hashlib
import urllib.parse
DB = "savora.db"  # new database file

# ---------- DATABASE ----------

def db():
    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys = ON")  # enforce foreign keys
    return con

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------- SERVER ----------

class RecipeHandler(BaseHTTPRequestHandler):
    def redirect(self, location):
        self.send_response(302)
        self.send_header("Location", location)
        self.end_headers()

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length))

    def get_session_user(self):
        cookie_header = self.headers.get("Cookie")
        if not cookie_header:
            return None

        # Split all cookies by ';' and find the session token
        cookies = cookie_header.split(";")
        session_token = None
        for c in cookies:
            c = c.strip()
            if c.startswith("session="):
                session_token = c[len("session="):]
                break

        if not session_token:
            return None

        con = db()
        row = con.execute(
            "SELECT userID FROM sessions WHERE token = ?",
            (session_token,)
        ).fetchone()
        return row[0] if row else None
    # ---------- POST ----------

    def do_POST(self):
        con = db()

        # --------- REGISTER ---------
        if self.path == "/register":
            data = self.read_json()
            try:
                con.execute(
                    "INSERT INTO User (username, password, privilege) VALUES (?, ?, ?)",
                    (data["username"], hash_password(data["password"]), "basic")
                )
                con.commit()
                self.send_json({"status": "registered"})
            except sqlite3.IntegrityError:
                self.send_json({"error": "username exists"}, 400)

        # --------- LOGIN ---------
        elif self.path == "/login":
            data = self.read_json()
            user = con.execute(
                "SELECT ID, password FROM User WHERE username = ?",
                (data["username"],)
            ).fetchone()
            if user and user[1] == hash_password(data["password"]):
                token = str(uuid.uuid4())
                con.execute("INSERT INTO sessions (token, userID) VALUES (?, ?)", (token, user[0]))
                con.commit()
                self.send_response(200)
                self.send_header("Set-Cookie", f"session={token}")
                self.end_headers()
                self.wfile.write(b'{"status":"logged in"}')
            else:
                self.send_json({"error": "invalid credentials"}, 401)

        # --------- ADD RECIPE ---------
        elif self.path == "/recipes":
            user_id = self.get_session_user()
            if not user_id:
                self.send_json({"error": "login required"}, 403)
                return

            data = self.read_json()
            name = data.get("name")
            instructions = data.get("instructions")
            ing_list = data.get("ingredients", [])

            if not name or not instructions:
                self.send_json({"error": "missing fields: name or instructions"}, 400)
                return

            con = db()
            try:
                # 1️⃣ Insert recipe
                cursor = con.execute(
                    "INSERT INTO Recipe (name, instructions, userID) VALUES (?, ?, ?)",
                    (name, instructions, user_id)
                )
                recipe_id = cursor.lastrowid

                # 2️⃣ Insert ingredients
                for ing in ing_list:
                    # expecting ing as {name: "Tomato", quantity: "200g"} or similar
                    ing_name = ing.get("name")
                    ing_qty = ing.get("quantity")
                    if not ing_name or not ing_qty:
                        continue  # skip invalid

                    # Check if ingredient exists
                    row = con.execute("SELECT ID FROM Ingredient WHERE name = ?", (ing_name,)).fetchone()
                    if row:
                        ing_id = row[0]
                    else:
                        cur = con.execute(
                            "INSERT INTO Ingredient (name, unit_type) VALUES (?, ?)",
                            (ing_name, "g")  # default unit; adjust if needed
                        )
                        ing_id = cur.lastrowid

                    # Link ingredient to recipe
                    con.execute(
                        "INSERT INTO Ingredient_Line (ingredientID, recipeID, quantity) VALUES (?, ?, ?)",
                        (ing_id, recipe_id, float(ing_qty))
                    )

                tags_list = data.get("tags", [])  # expecting ["vegan", "halal", "vegetarian", ...]
                for tag_name in tags_list:
                    tag_name = tag_name.strip().lower()
                    if not tag_name:
                        continue

                    # Check if tag already exists
                    tag_row = con.execute("SELECT ID FROM Tag WHERE name = ?", (tag_name,)).fetchone()
                    if tag_row:
                        tag_id = tag_row[0]
                    else:
                        cur = con.execute("INSERT INTO Tag (name) VALUES (?)", (tag_name,))
                        tag_id = cur.lastrowid

                    # Link tag to recipe
                    con.execute("INSERT OR IGNORE INTO Recipe_Tag (recipeID, tagID) VALUES (?, ?)",
                                (recipe_id, tag_id))
                con.commit()
                self.send_json({"status": "recipe added", "recipe_id": recipe_id})
                return

            except Exception as e:
                print("Error adding recipe:", e)
                self.send_json({"error": "internal server error"}, 500)
                return

        # --------- ADD FRIDGE ITEM ---------
        elif self.path == "/fridge":
            user_id = self.get_session_user()
            if not user_id:
                self.send_json({"error": "login required"}, 403)
                return
            data = self.read_json()
            con.execute(
                "INSERT OR REPLACE INTO Fridge (userID, ingredientID, quantity) VALUES (?, ?, ?)",
                (user_id, data["ingredientID"], data["quantity"])
            )
            con.commit()
            self.send_json({"status": "fridge updated"})
            return

        else:
            self.send_json({"error": "not found"}, 404)
            return

    # ---------- GET ----------
    def do_GET(self):
        con = db()
        user_id = self.get_session_user()

        # ---------- STATIC FILES ----------
        if self.path.startswith("/static/") or self.path in ["/", "/index.html"]:
            if self.path in ["/", "/index.html"]:
                self.path = "/static/index.html"

            # Strip query string for static file lookup
            file_path = "." + urllib.parse.urlparse(self.path).path

            # Protect recipes page
            if file_path.endswith("recipes.html") and not user_id:
                self.redirect("/static/login.html")
                return

            if os.path.exists(file_path):
                self.send_response(200)
                if file_path.endswith(".html"):
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                elif file_path.endswith(".js"):
                    self.send_header("Content-Type", "application/javascript")
                elif file_path.endswith(".css"):
                    self.send_header("Content-Type", "text/css")
                self.end_headers()
                with open(file_path, "rb") as f:
                    self.wfile.write(f.read())
                return

        # ---------- RECIPES API ----------
        elif self.path.startswith("/recipes"):
            if not user_id:
                self.send_json({"error": "login required"}, 403)
                return

            parsed = urllib.parse.urlparse(self.path)
            query = urllib.parse.parse_qs(parsed.query)
            recipe_id = query.get("id", [None])[0]

            if recipe_id:
                # ---------- FETCH SINGLE RECIPE ----------
                r = con.execute(
                    "SELECT id, name, instructions FROM Recipe WHERE id = ?", (recipe_id,)
                ).fetchone()
                if not r:
                    self.send_json({"error": "recipe not found"}, 404)
                    return

                recipe_id, name, instructions = r
                ingredients = con.execute(
                    "SELECT Ingredient.name, Ingredient_Line.quantity FROM Ingredient_Line "
                    "JOIN Ingredient ON Ingredient.ID = Ingredient_Line.ingredientID "
                    "WHERE Ingredient_Line.recipeID = ?",
                    (recipe_id,)
                ).fetchall()
                ing_list = [{"name": i[0], "quantity": i[1]} for i in ingredients]

                tags = con.execute(
                    "SELECT Tag.name FROM Recipe_Tag "
                    "JOIN Tag ON Tag.ID = Recipe_Tag.tagID "
                    "WHERE Recipe_Tag.recipeID = ?",
                    (recipe_id,)
                ).fetchall()

                tag_list = [t[0] for t in tags]

                # Include in response
                self.send_json({
                    "id": recipe_id,
                    "name": name,
                    "instructions": instructions,
                    "ingredients": ing_list,
                    "tags": tag_list
                })

                return  # stop here for single recipe

            else:
                # ---------- FETCH ALL RECIPES ----------
                recipes = con.execute("SELECT id, name, instructions FROM Recipe").fetchall()
                result = []
                for r in recipes:
                    rid, name, instructions = r
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
                        (recipe_id,)
                    ).fetchall()

                    tag_list = [t[0] for t in tags]

                    result.append({
                        "id": rid,
                        "name": name,
                        "instructions": instructions,
                        "ingredients": ingredients,
                        "tags": tag_list
                    })

                self.send_json(result)
                return
        # --------- GET USER FRIDGE ---------
        if self.path == "/fridge":
            if not user_id:
                self.send_json({"error": "login required"}, 403)
                return
            rows = con.execute("SELECT ingredientID, quantity FROM Fridge WHERE userID = ?", (user_id,)).fetchall()
            self.send_json([{"ingredientID": r[0], "quantity": r[1]} for r in rows])
            return

        self.send_json({"error": "not found"}, 404)
        return


# ---------- RUN SERVER ----------

if __name__ == "__main__":
    print("Server running on http://localhost:8000")
    HTTPServer(("localhost", 8000), RecipeHandler).serve_forever()