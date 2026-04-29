def handle_nutritional_info(handler):
    data = handler.read_json()
    ing = data.get("ingredient")
    handler.send_json({"ingredient": ing, "calories": 100, "protein": 5, "carbs": 20, "fat": 2})
    return
