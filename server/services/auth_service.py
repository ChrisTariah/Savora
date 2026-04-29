import sqlite3, uuid
from server.db.database import get_db
from server.utils.helpers import hash_password

def handle_register(handler):
    con = get_db()
    data = handler.read_json()
    try:
        con.execute(
            "INSERT INTO User (username, password, privilege) VALUES (?, ?, ?)",
            (data["username"], hash_password(data["password"]), "basic")
        )
        con.commit()
        handler.send_json({"status": "registered"})
    except sqlite3.IntegrityError:
        handler.send_json({"error": "username exists"}, 400)

def handle_login(handler):
    con = get_db()
    data = handler.read_json()
    user = con.execute(
        "SELECT ID, password FROM User WHERE username = ?", (data["username"],)
    ).fetchone()
    if user and user[1] == hash_password(data["password"]):
        token = str(uuid.uuid4())
        con.execute("INSERT INTO sessions (token, userID) VALUES (?, ?)", (token, user[0]))
        con.commit()
        handler.send_response(200)
        handler.send_header("Set-Cookie", f"session={token}")
        handler.end_headers()
        handler.wfile.write(b'{"status":"logged in"}')
    else:
        handler.send_json({"error": "invalid credentials"}, 401)

def handle_logout(handler):
    con = get_db()
    cookie_header = handler.headers.get("Cookie")
    session_token = None
    if cookie_header:
        for c in cookie_header.split(";"):
            c = c.strip()
            if c.startswith("session="):
                session_token = c[len("session="):]
                break
    if session_token:
        con.execute("DELETE FROM sessions WHERE token = ?", (session_token,))
        con.commit()
    handler.send_response(200)
    handler.send_header("Set-Cookie", "session=; Path=/; Max-Age=0")
    handler.end_headers()
    handler.wfile.write(b'{"status":"logged out"}')

def handle_me(handler):
    con = get_db()
    user_id = handler.get_session_user()
    if not user_id:
        handler.send_json({"error": "Not logged in"}, 401)
        return
    user = con.execute("SELECT username, privilege FROM User WHERE ID = ?", (user_id,)).fetchone()
    if not user:
        handler.send_json({"error": "User not found"}, 404)
        return
    handler.send_json({"id": user_id, "username": user[0], "privilege": user[1]})