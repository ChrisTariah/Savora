
from server.db.database import get_db as db
from server.services.ai_service import AIEngine
from server.utils.helpers import read_json, send_json


def handle_chat(handler):
    con = db()

    user_id = handler.get_session_user()
    if not user_id:
        send_json(handler, {"error": "login required"}, 403)
        return

    data = handler.read_json()
    user_message = data.get("message")

    ai = AIEngine(user_id, con)

    handler.send_response(200)
    handler.send_header("Content-type", "text/plain")
    handler.end_headers()

    try:
        for chunk in ai.ask_stream(user_message):
            handler.wfile.write(chunk.encode("utf-8"))
            handler.wfile.flush()
    except Exception as e:
        print("STREAM ERROR:", e)