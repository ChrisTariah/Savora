from server.db.database import get_db

class RecipeService:

    @staticmethod
    def create_recipe(user_id, data):
        con = get_db()

        name = data.get("name")
        instructions = data.get("instructions")

        if not name or not instructions:
            return {"error": "missing fields"}, 400

        cursor = con.execute(
            "INSERT INTO Recipe (name, instructions, userID, image) VALUES (?, ?, ?, ?)",
            (name, instructions, user_id, data.get("image"))
        )

        recipe_id = cursor.lastrowid
        con.commit()

        return {"status": "recipe added", "recipe_id": recipe_id}