from server.db.database import get_db as db
from server.utils.helpers import read_json, send_json

def handle_delete_user(handler):
    con = db()
    user_id = handler.get_session_user()
    if not user_id or not handler.is_admin(user_id):
        send_json(handler, {"error": "admin only"}, 403)
        return

    data = read_json(handler)
    target_id = data.get("userID")
    if not target_id:
        send_json(handler, {"error": "missing userID"}, 400)
        return

    con.execute("DELETE FROM Recipe WHERE userID = ?", (target_id,))
    con.execute("DELETE FROM Fridge WHERE userID = ?", (target_id,))
    con.execute("DELETE FROM sessions WHERE userID = ?", (target_id,))
    con.execute("DELETE FROM User WHERE ID = ?", (target_id,))
    con.commit()
    send_json(handler, {"status": "user deleted"})

def handle_make_admin(handler):
    con = db()
    user_id = handler.get_session_user()
    if not handler.is_admin(user_id):
        send_json(handler, {"error": "admin only"}, 403)
        return

    data = read_json(handler)
    target_id = data.get("userID")
    if not target_id:
        send_json(handler, {"error": "missing userID"}, 400)
        return

    con.execute("UPDATE User SET privilege = 'admin' WHERE ID = ?", (target_id,))
    con.commit()
    send_json(handler, {"status": "user promoted to admin"})

def handle_edit_recipe(handler):
    con = db()
    user_id = handler.get_session_user()
    if not user_id or not handler.is_admin(user_id):
        send_json(handler, {"error": "admin only"}, 403)
        return

    data = read_json(handler)
    recipe_id = data.get("recipeID")
    name = data.get("name")
    instructions = data.get("instructions")

    con.execute(
        "UPDATE Recipe SET name = ?, instructions = ? WHERE ID = ?",
        (name, instructions, recipe_id)
    )
    con.commit()
    send_json(handler, {"status": "recipe updated"})
    from server.services.search_indexer import rebuild_index_async
    rebuild_index_async()