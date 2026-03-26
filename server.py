import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sqlite3
import uuid
import hashlib
import urllib.parse
from google import genai
from enum import Enum
import sqlite3
from typing import Any
import logging

logging.basicConfig(level="ERROR")

API_KEY = "AIzaSyBkFN4te5Q9" + "SYm6CpMMxs6CX-drq8Hl6F0"

DB = "savora.db"  # database file

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
        elif self.path == "/logout":
            cookie_header = self.headers.get("Cookie")

            if cookie_header:
                cookies = cookie_header.split(";")
                session_token = None

                for c in cookies:
                    c = c.strip()
                    if c.startswith("session="):
                        session_token = c[len("session="):]
                        break

                if session_token:
                    con.execute("DELETE FROM sessions WHERE token = ?", (session_token,))
                    con.commit()


            self.send_response(200)
            self.send_header("Set-Cookie", "session=; Path=/; Max-Age=0")
            self.end_headers()
            self.wfile.write(b'{"status":"logged out"}')

        # ---------- ADD RECIPE ----------
        elif self.path == "/recipes":
            user_id = self.get_session_user()
            if not user_id:
                self.send_json({"error": "login required"}, 403)
                return

            data = self.read_json()
            name = data.get("name")
            instructions = data.get("instructions")
            ing_list = data.get("ingredients", [])
            image = data.get("image")
            if not name or not instructions:
                self.send_json({"error": "missing fields: name or instructions"}, 400)
                return

            try:
                # Insert recipe
                cursor = con.execute(
                    "INSERT INTO Recipe (name, instructions, userID, image) VALUES (?, ?, ?, ?)",
                    (name, instructions, user_id, image)
                )
                recipe_id = cursor.lastrowid

                # Insert ingredients
                for ing in ing_list:
                    ing_name = ing.get("name")
                    ing_qty = ing.get("quantity")
                    if not ing_name or not ing_qty:
                        continue

                    # Make sure quantity is numeric
                    try:
                        ing_qty = float(ing_qty)
                    except ValueError:
                        continue  # skip invalid quantity

                    # Check if ingredient exists
                    row = con.execute("SELECT ID, unit_type FROM Ingredient WHERE name = ?", (ing_name,)).fetchone()
                    if row:
                        ing_id, unit_type = row
                    else:
                        # Default unit type; you can customize if you have a unit map
                        unit_type = "cnt"
                        cur = con.execute("INSERT INTO Ingredient (name, unit_type) VALUES (?, ?)",
                                          (ing_name, unit_type))
                        con.commit()
                        ing_id = cur.lastrowid

                    # Insert into Ingredient_Line
                    con.execute(
                        "INSERT INTO Ingredient_Line (ingredientID, recipeID, quantity) VALUES (?, ?, ?)",
                        (ing_id, recipe_id, ing_qty)
                    )

                # tags
                tags_list = data.get("tags", [])
                for tag_name in tags_list:
                    tag_name = tag_name.strip().lower()
                    if not tag_name:
                        continue
                    tag_row = con.execute("SELECT ID FROM Tag WHERE name = ?", (tag_name,)).fetchone()
                    if tag_row:
                        tag_id = tag_row[0]
                    else:
                        cur = con.execute("INSERT INTO Tag (name) VALUES (?)", (tag_name,))
                        con.commit()
                        tag_id = cur.lastrowid
                    con.execute("INSERT OR IGNORE INTO Recipe_Tag (recipeID, tagID) VALUES (?, ?)",
                                (recipe_id, tag_id))

                # Commit everything
                con.commit()
                self.send_json({"status": "recipe added", "recipe_id": recipe_id})

            except Exception as e:
                print("Error adding recipe:", e)
                self.send_json({"error": "internal server error"}, 500)
        # --------- ADD FRIDGE ITEM ---------
        elif self.path == "/fridge":
            user_id = self.get_session_user()
            if not user_id:
                self.send_json({"error": "login required"}, 403)
                return

            data = self.read_json()
            ing_id = data.get("ingredientID")
            qty = data.get("quantity")

            if not ing_id or not qty:
                self.send_json({"error": "missing fields"}, 400)
                return

            con.execute(
                "INSERT OR REPLACE INTO Fridge (userID, ingredientID, quantity) VALUES (?, ?, ?)",
                (user_id, ing_id, qty)
            )
            con.commit()
            self.send_json({"status": "added to fridge"})
            
            #Nutrional info 
        elif self.path == "/nutritional-info":
            data = self.read_json()
            ing = data.get("ingredient")
            self.send_json({"ingredient": ing, "calories": 100, "protein": 5, "carbs": 20, "fat": 2})
            return
        elif self.path == "/chat":
            user_id = self.get_session_user()
            if not user_id:
                self.send_json({"error": "login required"}, 403)
                return

            data = self.read_json()
            user_message = data.get("message")
            if not user_message:
                self.send_json({"error": "missing message"}, 400)
                return

            # Save user message
            con.execute(
                "INSERT INTO AI_Chat (userID, message, sender) VALUES (?, ?, ?)",
                (user_id, user_message, "user")
            )

            # Get recipes and tags to provide context
            recipes = con.execute(
                "SELECT Recipe.name, Tag.name FROM Recipe "
                "JOIN Recipe_Tag ON Recipe.ID = Recipe_Tag.recipeID "
                "JOIN Tag ON Tag.ID = Recipe_Tag.tagID;"
            )

            recipe_context = {}
            for r_name, tag in recipes:
                recipe_context.setdefault(r_name, []).append(tag)

            context_text = "\n".join(
                f"{name}: {', '.join(tags)}" for name, tags in recipe_context.items()
            )

            # Prepare AI prompt
            prompt = f"""
            You are a helpful recipe AI assistant. 
            Here is a list of recipes and their tags:
            {context_text}

            User says: {user_message}
            Provide a helpful recommendation or answer.
            """

            try:
                client = genai.Client(api_key=API_KEY)
                response_obj = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=prompt
                )
                ai_message = response_obj.text or "Sorry, I couldn't generate a response."

                # Save AI response
                con.execute(
                    "INSERT INTO AI_Chat (userID, message, sender) VALUES (?, ?, ?)",
                    (user_id, ai_message, "ai")
                )
                con.commit()
                self.send_json({"response": ai_message})
            except Exception as e:
                logging.error(f"AI API call failed: {e}")
                self.send_json({"error": "AI service failed"}, 500)
    # ---------- GET ----------
    def do_GET(self):
        con = db()
        user_id = self.get_session_user()

        # ---------- STATIC FILES ----------
        if self.path.startswith("/static/") or self.path in ["/", "/index.html"]:
            if self.path in ["/", "/index.html"]:
                self.path = "/static/index.html"

            file_path = "." + urllib.parse.urlparse(self.path).path


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
        elif self.path == "/me":
            if not user_id:
                self.send_json({"error": "Not logged in"}, 401)
                return

            user = con.execute(
                "SELECT username FROM User WHERE ID = ?",
                (user_id,)
            ).fetchone()

            if not user:
                self.send_json({"error": "User not found"}, 404)
                return

            self.send_json({
                "id": user_id,
                "username": user[0]
            })
            return
        elif self.path.startswith("/ingredients"):
            query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            search = query.get("q", [""])[0].lower()

            rows = con.execute(
                "SELECT ID, name, unit_type FROM Ingredient WHERE name LIKE ? LIMIT 5",
                (f"%{search}%",)
            ).fetchall()

            result = [
                {"id": r[0], "name": r[1], "unit": r[2]}
                for r in rows
            ]

            self.send_json(result)
            return
        # ---------- RECIPES API ----------
        elif self.path.startswith("/recipes"):

            parsed = urllib.parse.urlparse(self.path)
            query = urllib.parse.parse_qs(parsed.query)
            recipe_id = query.get("id", [None])[0]

            if recipe_id:
                # FETCH SINGLE RECIPE
                r = con.execute(
                    "SELECT id, name, instructions, image FROM Recipe WHERE id = ?", (recipe_id,)
                ).fetchone()
                if not r:
                    self.send_json({"error": "recipe not found"}, 404)
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

                self.send_json({
                    "id": rid,
                    "name": name,
                    "instructions": instructions,
                    "ingredients": [{"name": i[0], "quantity": i[1]} for i in ingredients],
                    "tags": [t[0] for t in tags],
                    "image": image
                })
                return

            else:
                # FETCH ALL RECIPES
                recipes = con.execute("SELECT id, name, instructions, image FROM Recipe").fetchall()
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
                self.send_json(result)
                return

        # GET FRIDGE
        elif self.path == "/my-recipes":

            user_id = self.get_session_user()
            print(user_id)
            if not user_id:
                self.send_json({"error": "login required"}, 403)

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

            self.send_json(result)

            return
        if self.path == "/fridge":
            if not user_id:
                self.send_json({"error": "login required"}, 403)
                return

            rows = con.execute(
                """
                SELECT i.ID, i.name, i.unit_type, f.quantity
                FROM Fridge f
                JOIN Ingredient i ON f.ingredientID = i.ID
                WHERE f.userID = ?
                """,
                (user_id,)
            ).fetchall()

            # Return id, name, unit, quantity
            self.send_json([
                {"id": r[0], "name": r[1], "unit": r[2], "quantity": r[3]}
                for r in rows
            ])
            return

        self.send_json({"error": "not found"}, 404)


# ---------- RUN SERVER ----------
if __name__ == "__main__":
    print("Server running on http://localhost:8000")
    HTTPServer(("localhost", 8000), RecipeHandler).serve_forever()