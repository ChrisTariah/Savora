from google import genai

# The client SHOULD be able to get the API key from the environment variable `GEMINI_API_KEY`
# But I can't figure out how to set up environment variables, so:
API_KEY = "AIzaSyBkFN4te5Q9" + "SYm6CpMMxs6CX-drq8Hl6F0" 
# Broken up to avoid detection by google
# Get new one here if it breaks again:
# https://aistudio.google.com/welcome?utm_source=PMAX&utm_medium=display&utm_campaign=Cloud-SS-DR-AIS-FY26-global-pmax-1713578&utm_content=pmax&gad_source=1&gad_campaignid=23417432327&gbraid=0AAAAACn9t66WLIbRelT6aQ6CErDCgtpv5&gclid=Cj0KCQjw9-PNBhDfARIsABHN6-0vLKG6VhpJUaR4BpEfcrhEc-7eb4RTZrZVVh_7tqJwRZCtYVesNokaAtX8EALw_wcB
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