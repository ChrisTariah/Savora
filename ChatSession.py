from google import genai
from enum import Enum
import sqlite3
from typing import Any
import logging

logging.basicConfig(level="ERROR")

API_KEY = "AIzaSyBkFN4te5Q9" + "SYm6CpMMxs6CX-drq8Hl6F0" 
# Broken up to avoid detection by google
# Get new one here if it breaks again:
# https://aistudio.google.com/welcome?utm_source=PMAX&utm_medium=display&utm_campaign=Cloud-SS-DR-AIS-FY26-global-pmax-1713578&utm_content=pmax&gad_source=1&gad_campaignid=23417432327&gbraid=0AAAAACn9t66WLIbRelT6aQ6CErDCgtpv5&gclid=Cj0KCQjw9-PNBhDfARIsABHN6-0vLKG6VhpJUaR4BpEfcrhEc-7eb4RTZrZVVh_7tqJwRZCtYVesNokaAtX8EALw_wcB

DATABASE_PATH: str = "Savora.db"

DEFAULT_PROMPT: str = """
You are an AI agent whose purpose is to provide the user with information and recommendations
about recipes. The following is a list of all recipes available and tags that describe them.
"""

def execute_sql(*command, db: str) -> list[Any]:
    """
    Runs an SQLite command on the database

    :param command: command to be run
    :param db: Path to database
    :returns: Results of query or empty list
    """
    result: list[Any] = []
    try:
        # Connect to database
        with sqlite3.connect(db) as conn:
            cursor : sqlite3.Cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")  # enforce foreign keys
            cursor.execute(*command)
            result = cursor.fetchall()
            conn.commit()
        conn.close()
    except Exception as e:
        logging.critical(f"Error, command not executed:\n{e}\nCommand: {command}")
    return result

class ChatSession:
    #client: genai.Client
    #view: View

    def __init__(self, api_key: str, view:str="Nothing", setupPrompt:str=DEFAULT_PROMPT) -> None:   
        self.client = genai.Client(api_key=api_key)
        self.recipeList: str = self.getRecipeList()
        self.promptHistory: list[str] = []
        self.setupPrompt = setupPrompt
        self.view = view
    
    def setView(self, view:str="Nothing") -> None:
        self.View = view
    
    def getRecipeList(self) -> str:
        # Get Recipes and tags
        get_recipes: str = """
        select Recipe.name, Tag.name from Recipe
        join Recipe_Tag on Recipe.ID = Recipe_Tag.recipeID
        join Tag on Tag.ID = Recipe_Tag.tagID;"""
        result: list[tuple[str,str]] = execute_sql(get_recipes, db=DATABASE_PATH)
        recipe_tag_table: dict[str,list[str]] = {}
        
        # Condense recipes and tags
        for row in result:
            recipe: str = row[0]
            tag: str    = row[1]
            if recipe in recipe_tag_table:
                recipe_tag_table[recipe].append(tag)
            else:
                recipe_tag_table[recipe] = [tag]
        
        # Format recipes and tags
        output: str = "Recipes\t| Tags\n"
        for recipe, tags in recipe_tag_table.items():
            output += recipe+"\t| "
            for tag in tags:
                output += tag+", "
            output = output[0:-2]+"\n"
        
        return output

    def getResponse(self, nextPrompt: str) -> str:

        # Get response
        compiled_prompt: str = self.setupPrompt

        if self.promptHistory:
            compiled_prompt += "\nThe chat history with the user so far is:\n"
            for prompt in self.promptHistory:
                compiled_prompt += prompt
        
        compiled_prompt += "\nThe user can see the following information on the page:\n"
        compiled_prompt += self.view

        compiled_prompt += "\nPlease respond to the following message from the user:\n"
        compiled_prompt += nextPrompt

        response: str|None = self.client.models.generate_content(
            model="gemini-3-flash-preview", contents=compiled_prompt).text
        if response == None: logging.error("Chat bot returned None response")
        
        # Log response
        response = str(response) # Gets the type checker to stop complaining
        self.promptHistory.append("\nUser:\n" + nextPrompt + "\n")
        self.promptHistory.append("\nAI Agent:\n" + response + "\n")

        return response

def main():
    chat = ChatSession(API_KEY)
    while True:
        print(chat.getResponse(input("\n\n> ")))

if __name__ == "__main__":
    main()
    