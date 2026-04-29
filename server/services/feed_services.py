from server.db.database import get_db as db

from server.utils.helpers import read_json, send_json


def handle_feed_services(handler):
    user = handler.get_session_user()
    if not user:
        send_json(handler, {"error": "login required"}, 403)
        return

    con = db()

    recipes = con.execute("""
        SELECT r.id, r.name, r.image, u.username,
               (SELECT COUNT(*) FROM "Like" WHERE recipeID = r.id) as likes
        FROM Recipe r
        JOIN Follow f ON r.userID = f.followingID
        JOIN User u ON r.userID = u.ID
        WHERE f.followerID = ?
        ORDER BY r.id DESC
    """, (user,)).fetchall()

    result = []

    for r in recipes:
        recipe_id = r[0]

        comments = con.execute("""
            SELECT c.text, u.username
            FROM Comment c
            JOIN User u ON u.ID = c.userID
            WHERE c.recipeID = ?
            ORDER BY c.ID DESC
            LIMIT 5
        """, (recipe_id,)).fetchall()

        result.append({
            "id": recipe_id,
            "name": r[1],
            "image": r[2],
            "username": r[3],
            "likes": r[4],
            "comments": [
                {"text": c[0], "username": c[1]} for c in comments
            ]
        })

    send_json(handler, result)

def handle_post_comment(handler):
    user = handler.get_session_user()
    if not user:
        send_json(handler, {"error": "login required"}, 403)
        return

    data = handler.read_json()
    recipe_id = data.get("recipe_id")
    text = data.get("text")

    con = db()
    con.execute(
        "INSERT INTO Comment (userID, recipeID, text) VALUES (?, ?, ?)",
        (user, recipe_id, text)
    )
    con.commit()

    send_json(handler, {"status": "ok"})


def handle_like_services(handler):
    user = handler.get_session_user()
    if not user:
        send_json(handler, {"error": "login required"}, 403)
        return

    data = handler.read_json()
    recipe_id = data.get("recipe_id")

    con = db()

    # toggle like
    existing = con.execute(
        "SELECT 1 FROM Like WHERE userID=? AND recipeID=?",
        (user, recipe_id)
    ).fetchone()

    if existing:
        con.execute("DELETE FROM Like WHERE userID=? AND recipeID=?", (user, recipe_id))
        liked = False
    else:
        con.execute("INSERT INTO Like (userID, recipeID) VALUES (?, ?)", (user, recipe_id))
        liked = True

    con.commit()

    count = con.execute(
        "SELECT COUNT(*) FROM Like WHERE recipeID=?",
        (recipe_id,)
    ).fetchone()[0]

    send_json(handler, {"liked": liked, "count": count})