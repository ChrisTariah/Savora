# server/services/ai_engine.py

import json
from google import genai
from server.config import API_KEY


class AIEngine:
    def __init__(self, user_id, db):
        self.user_id = user_id
        self.db = db
        self.client = genai.Client(api_key=API_KEY)

        self.fridge = []
        self.user_recipes = []
        self.chat = self.load_chat_history()
    # ---------------- LOAD LIGHT DATA ----------------
    def load_chat_history(self, limit=10):
        rows = self.db.execute("""
            SELECT message, sender
            FROM AI_Chat
            WHERE userID = ?
            ORDER BY id DESC
            LIMIT ?
        """, (self.user_id, limit)).fetchall()

        # reverse so oldest → newest
        rows.reverse()

        return [
            {"role": r[1], "content": r[0]}
            for r in rows
        ]
    def load_context(self):
        self.fridge = self._load_fridge()
        self.user_recipes = self._load_user_recipes()

    def _load_fridge(self):
        rows = self.db.execute("""
            SELECT Ingredient.name 
            FROM Fridge
            JOIN Ingredient ON Ingredient.ID = Fridge.ingredientID
            WHERE Fridge.userID = ?
        """, (self.user_id,)).fetchall()

        return [r[0] for r in rows]

    def _load_user_recipes(self):
        rows = self.db.execute("""
            SELECT id, name FROM Recipe WHERE userID = ?
        """, (self.user_id,)).fetchall()

        return [{"id": r[0], "name": r[1]} for r in rows]

    # ---------------- STEP 1: INTENT ----------------

    def extract_intent(self, user_message):
        history_text = "\n".join([
            f"{m['role'].capitalize()}: {m['content']}"
            for m in self.chat
        ])
        prompt = f"""
You are a parser.

Extract user intent into JSON.

Return ONLY valid JSON.

Format:
{{
  "ingredients": [],
  "tags": [],
  "name": null,
  "use_fridge": true/false
}}

User conversation:
{history_text}

Latest message:
{user_message}
"""

        res = self.client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )

        try:
            return json.loads(res.text)
        except:
            return {
                "ingredients": [],
                "tags": [],
                "name": None,
                "use_fridge": False
            }

    # ---------------- STEP 2: QUERY ----------------

    def search_recipes(self, filters):
        query_parts = []

        if filters["ingredients"]:
            query_parts.append(filters["ingredients"][0])

        if filters["tags"]:
            query_parts.append(filters["tags"][0])

        if filters["name"]:
            query_parts.append(filters["name"])

        if filters.get("use_fridge") and self.fridge:
            query_parts.extend(self.fridge[:5])  # limit to avoid huge queries

        if not query_parts:
            search_query = ""
        else:
            search_query = " ".join(query_parts)

        if not search_query.strip():
            rows = self.db.execute("""
                SELECT recipe_id, name
                FROM recipe_search
                LIMIT 20
            """).fetchall()
        else:
            rows = self.db.execute("""
                SELECT recipe_id, name
                FROM recipe_search
                WHERE recipe_search MATCH ?
                LIMIT 20
            """, (search_query,)).fetchall()

        return rows

    # ---------------- STEP 3: RESPONSE ----------------

    def stream_response(self, user_message, results):
        results = results[:10]

        recipes_text = "\n".join([
            f"{r[0]} | {r[1]} | link: /static/recipe.html?id={r[0]}"
            for r in results
        ]) if results else "None"

        fridge_text = ", ".join(self.fridge) or "Empty"

        history_text = "\n".join([
            f"{m['role'].capitalize()}: {m['content']}"
            for m in self.chat
        ])

        prompt = f"""
    You are Savora, a smart recipe assistant.

    Conversation:
    {history_text}

    User fridge:
    {fridge_text}

    User asked:
    {user_message}

    Matching recipes:
    {recipes_text}

    RULES:
    - Only use given recipes
    - Include link: http://localhost:8000/static/recipe.html?id=ID
    - Keep it short

    Answer:
    """

        stream = self.client.models.generate_content_stream(
            model="gemini-3-flash-preview",
            contents=prompt
        )

        for chunk in stream:
            if chunk.text:
                yield chunk.text

    def build_response(self, user_message, results):
        if not results:
            recipes_text = "None"
        else:
            recipes_text = "\n".join([
                f"{r[0]} | {r[1]} | link: /static/recipe.html?id={r[0]}"
                for r in results
            ])

        fridge_text = ", ".join(self.fridge) or "Empty"

        user_recipes_text = "\n".join([
            f"{r['name']} (id: {r['id']})"
            for r in self.user_recipes
        ]) or "None"
        history_text = "\n".join([
            f"{m['role'].capitalize()}: {m['content']}"
            for m in self.chat
        ])
        prompt = f"""
You are Savora, a smart recipe assistant.
Conversation so far:
{history_text}

User fridge:
{fridge_text}

User's own recipes:
{user_recipes_text}

User asked:
{user_message}

Matching recipes:
{recipes_text}

STRICT RULES:
- Only recommend recipes from the list above
- ALWAYS include a clickable link in this format:
  http://localhost:8000/static/recipe.html?id=ID
- Keep answers short and helpful
- If no recipes found, say it clearly

Format example:

Recipe Name  
Link: http://localhost:8000/static/recipe.html?id=1  
Short explanation

Now answer:
"""

        res = self.client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )

        return res.text or "No response"

    # ---------------- MAIN ----------------
    def ask_stream(self, user_message):
        self.load_context()

        # save user message
        self.db.execute(
            "INSERT INTO AI_Chat (userID, message, sender) VALUES (?, ?, ?)",
            (self.user_id, user_message, "user")
        )
        self.db.commit()

        self.chat = self.load_chat_history()

        intent = self.extract_intent(user_message)
        results = self.search_recipes(intent)

        full_response = ""

        for chunk in self.stream_response(user_message, results):
            full_response += chunk
            yield chunk

        # save final response AFTER streaming
        self.db.execute(
            "INSERT INTO AI_Chat (userID, message, sender) VALUES (?, ?, ?)",
            (self.user_id, full_response, "ai")
        )
        self.db.commit()

    def ask(self, user_message):
        self.load_context()


        self.db.execute(
            "INSERT INTO AI_Chat (userID, message, sender) VALUES (?, ?, ?)",
            (self.user_id, user_message, "user")
        )
        self.db.commit()

        # reload memory
        self.chat = self.load_chat_history()


        intent = self.extract_intent(user_message)
        print("INTENT:", intent)

        results = self.search_recipes(intent)
        print("RESULTS:", results)

        response = self.build_response(user_message, results)


        self.db.execute(
            "INSERT INTO AI_Chat (userID, message, sender) VALUES (?, ?, ?)",
            (self.user_id, response, "ai")
        )
        self.db.commit()

        return response