import hashlib
import json
from server.db.database import get_db as db

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def parse_json(handler):
    length = int(handler.headers.get("Content-Length", 0))
    return json.loads(handler.rfile.read(length))

def send_json(handler, data, status=200):
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.end_headers()
    handler.wfile.write(json.dumps(data).encode())

def read_json(handler):
    length = int(handler.headers.get("Content-Length", 0))
    if length == 0:
        return {}

    try:
        return json.loads(handler.rfile.read(length))
    except json.JSONDecodeError:
        return {}

def get_session_user(handler):
    cookie_header = handler.headers.get("Cookie")
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


def get_cookie(handler, name):
    cookie_header = handler.headers.get("Cookie")
    if not cookie_header:
        return None

    for c in cookie_header.split(";"):
        c = c.strip()
        if c.startswith(name + "="):
            return c[len(name)+1:]
    return None