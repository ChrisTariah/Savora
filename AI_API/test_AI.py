from google import genai

# The client SHOULD be able to get the API key from the environment variable `GEMINI_API_KEY`
# But I can't figure out how to set up environment variables, so:
API_KEY = "AIzaSyDNf-Z7N6RScv68y06cGAYC5wQ5V-VeZCg"
client = genai.Client(api_key=API_KEY)

# The prompt for the AI should contain as much context as possible. 
# Get this information from the database.
prompt: str = """
The user can see a list of recipes that includes:
Baked Chicken
Spaghetti and Red Sauce
Curry
Fried Fish

The user has selected the following recipe:
Baked Chicken
Tags: Tasty, Baked, Protein, Cheap
Ingredients:
1 chicken breast
1 cup bread crumbs
2 eggs
Instructions:
Bread the chicken then bake it for 30 min at 250F. Enjoy.

Using this context, respond to the following prompt from the user:\n
"""

# The user input to the chat bot is appended to the prompt
prompt += "What should I cook tonight?"

# Send prompt to AI
response = client.models.generate_content(
    model="gemini-3-flash-preview", contents=prompt
)

# Display the response
print(response.text)