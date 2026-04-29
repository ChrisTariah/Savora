import urllib

from server.db.database import get_db as db
from server.utils.helpers import read_json, send_json, get_session_user

def handle_view_profile(handler):
    con = db()
    viewer = handler.get_session_user()
    data = read_json(handler)
    viewed = data.get("userID")
    if viewer and viewed:
        con.execute("INSERT INTO Profile_View (viewerID, viewedUserID) VALUES (?, ?)", (viewer, viewed))
        con.commit()
    send_json(handler, {"status": "ok"})

def handle_like_profile(handler):
    con = db()
    user = handler.get_session_user()
    data = read_json(handler)
    if not user:
        send_json(handler, {"error": "login required"}, 403)
        return
    con.execute("INSERT OR IGNORE INTO Profile_Like (userID, likedUserID) VALUES (?, ?)", (user, data["userID"]))
    con.commit()
    send_json(handler, {"status": "liked"})

def handle_follow(handler):
    con = db()
    user = handler.get_session_user()
    data = read_json(handler)
    target = data.get("userID")
    if not user:
        send_json(handler, {"error": "login required"}, 403)
        return
    if user == target:
        send_json(handler, {"error": "cannot follow yourself"}, 400)
        return
    con.execute("INSERT OR IGNORE INTO Follow (followerID, followingID) VALUES (?, ?)", (user, target))
    con.commit()
    send_json(handler, {"status": "followed"})

def handle_unfollow(handler):
    con = db()
    user = handler.get_session_user()
    data = read_json(handler)
    if not user:
        send_json(handler, {"error": "login required"}, 403)
        return
    con.execute("DELETE FROM Follow WHERE followerID = ? AND followingID = ?", (user, data["userID"]))
    con.commit()
    send_json(handler, {"status": "unfollowed"})


def handle_is_following(handler):
    user = get_session_user(handler)
    con =db()
    parsed = urllib.parse.urlparse(handler.path)
    query = urllib.parse.parse_qs(parsed.query)
    target = query.get("id", [None])[0]

    if not user or not target:
        send_json(handler,{"following": False})
        return

    row = con.execute(
        "SELECT 1 FROM Follow WHERE followerID = ? AND followingID = ?",
        (user, target)
    ).fetchone()

    send_json(handler,{"following": bool(row)})
    return

def handle_get_profile(handler):
    parsed = urllib.parse.urlparse(handler.path)
    query = urllib.parse.parse_qs(parsed.query)
    user_id = query.get("id", [None])[0]

    if not user_id:
        send_json({"error": "missing id"}, 400)
        return
    con = db()
    # user info
    user = con.execute(
        "SELECT username FROM User WHERE ID = ?",
        (user_id,)
    ).fetchone()

    # recipes
    recipes = con.execute(
        "SELECT id, name, image FROM Recipe WHERE userID = ?",
        (user_id,)
    ).fetchall()

    # profile likes
    likes = con.execute(
        "SELECT COUNT(*) FROM Profile_Like WHERE likedUserID = ?",
        (user_id,)
    ).fetchone()[0]

    # profile views
    views = con.execute(
        "SELECT COUNT(*) FROM Profile_View WHERE viewedUserID = ?",
        (user_id,)
    ).fetchone()[0]

    send_json(handler,{
        "username": user[0],
        "likes": likes,
        "views": views,
        "recipes": [
            {"id": r[0], "name": r[1], "image": r[2]}
            for r in recipes
        ]
    })
    return

def handle_get_users(handler):
    con = db()
    parsed = urllib.parse.urlparse(handler.path)
    query = urllib.parse.parse_qs(parsed.query)
    search = query.get("q", [""])[0]

    users = con.execute(
        "SELECT ID, username FROM User WHERE username LIKE ? LIMIT 10",
        (f"%{search}%",)
    ).fetchall()

    send_json(handler,[
        {"id": u[0], "username": u[1]}
        for u in users
    ])
    return
