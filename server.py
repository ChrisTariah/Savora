import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sqlite3
import uuid
import hashlib
import sqlite3


DB = "database.db"


def db():
    return sqlite3.connect(DB)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


class RecipeHandler(BaseHTTPRequestHandler):
    def redirect(self, location):
        self.send_response(302)
        self.send_header("Location", location)
        self.end_headers()

    # ---------- helpers ----------

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length))

    def get_session_user(self):
        cookie = self.headers.get("Cookie")
        if not cookie:
            return None

        token = cookie.replace("session=", "")
        con = db()
        row = con.execute(
            "SELECT user_id FROM sessions WHERE token = ?",
            (token,)
        ).fetchone()
        return row[0] if row else None

    # ---------- POST ----------

    def do_POST(self):
        if self.path == "/register":
            data = self.read_json()
            con = db()
            try:
                con.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (data["username"], hash_password(data["password"]))
                )
                con.commit()
                self.send_json({"status": "registered"})
            except sqlite3.IntegrityError:
                self.send_json({"error": "username exists"}, 400)

        elif self.path == "/login":
            data = self.read_json()
            con = db()
            user = con.execute(
                "SELECT id, password FROM users WHERE username = ?",
                (data["username"],)
            ).fetchone()

            if user and user[1] == hash_password(data["password"]):
                token = str(uuid.uuid4())
                con.execute(
                    "INSERT INTO sessions (token, user_id) VALUES (?, ?)",
                    (token, user[0])
                )
                con.commit()

                self.send_response(200)
                self.send_header("Set-Cookie", f"session={token}")
                self.end_headers()
                self.wfile.write(b'{"status":"logged in"}')
            else:
                self.send_json({"error": "invalid credentials"}, 401)

        elif self.path == "/recipes":
            user_id = self.get_session_user()
            if not user_id:
                self.send_json({"error": "login required"}, 403)
                return

            data = self.read_json()
            con = db()
            con.execute(
                "INSERT INTO recipes (title, content, user_id) VALUES (?, ?, ?)",
                (data["title"], data["content"], user_id)
            )
            con.commit()
            self.send_json({"status": "recipe added"})

        else:
            self.send_json({"error": "not found"}, 404)

    # ---------- GET ----------

    import os

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.path = "/static/index.html"

        if self.path.startswith("/static/"):

            # protect recipes page
            if self.path == "/static/recipes.html":
                user_id = self.get_session_user()
                if not user_id:
                    self.redirect("/static/login.html")
                    return

            file_path = "." + self.path
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

        if self.path == "/recipes":
            user_id = self.get_session_user()
            if not user_id:
                self.send_json({"error": "login required"}, 403)
                return

            con = db()
            rows = con.execute(
                "SELECT title, content FROM recipes"
            ).fetchall()

            self.send_json([
                {"title": r[0], "content": r[1]} for r in rows
            ])
            return

        self.send_json({"error": "not found"}, 404)


if __name__ == "__main__":
    print("Server running on http://localhost:8000")
    HTTPServer(("localhost", 8000), RecipeHandler).serve_forever()
