from server.db.database import get_db as db
from server.utils.helpers import read_json, send_json

def handle_add_fridge(handler):
    con = db()
    user_id = handler.get_session_user()
    if not user_id:
        send_json(handler, {"error": "login required"}, 403)
        return
    data = read_json(handler)
    ing_id = data.get("ingredientID")
    qty = data.get("quantity")
    if not ing_id or not qty:
        send_json(handler, {"error": "missing fields"}, 400)
        return
    con.execute(
        "INSERT OR REPLACE INTO Fridge (userID, ingredientID, quantity) VALUES (?, ?, ?)",
        (user_id, ing_id, qty)
    )
    con.commit()
    send_json(handler, {"status": "added to fridge"})

def handle_get_fridge(handler):
    con = db()
    user_id = handler.get_session_user()
    if not user_id:
        send_json(handler, {"error": "login required"}, 403)
        return
    rows = con.execute(
        "SELECT i.ID, i.name, i.unit_type, f.quantity "
        "FROM Fridge f JOIN Ingredient i ON f.ingredientID = i.ID "
        "WHERE f.userID = ?",
        (user_id,)
    ).fetchall()
    send_json(handler, [{"id": r[0], "name": r[1], "unit": r[2], "quantity": r[3]} for r in rows])