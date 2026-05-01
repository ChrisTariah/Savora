import sqlite3
import os
from typing import Tuple

DB_NAME : str = "Savora.db"
'''Name of database to be created'''

DB_PATH : str = ""
'''Path to database location. Empty if root'''

SQL_FILES : Tuple[str,...] = (
    # Note that the order listed is the order they will run
    "static/Base_Schema.sql",
    "static/Test_Data.sql"
)
'''List of sql files used to create and populate the new database.'''

def execute_sql_file(con : sqlite3.Cursor, filename: str) -> None:
    '''
    Executes the given sql on the given database

    :param con: Database to be modified
    :param filename: SQL file to be run
    :returns: None
    '''
    print(f"Running {filename}...")
    with open(filename, "r", encoding="utf-8") as f:
        sql_script = f.read()
    con.executescript(sql_script)
    print(f"{filename} completed.\n")

def main():
    if len(SQL_FILES) == 0: raise ValueError("No sql files provided")

    print("Creating new database file...")
    NEW_DB : str = "temp.db"
    with sqlite3.connect(DB_PATH+NEW_DB) as conn:
        db : sqlite3.Cursor = conn.cursor()
        conn.execute("PRAGMA foreign_keys = ON")  # enforce foreign keys

        print("Populating database with files...")
        for file in SQL_FILES:
            execute_sql_file(db, file)
    conn.close() # Explicit closing needed even with context manager (?!)
        
    print("Replacing old database file with new...")
    try:
        os.remove(DB_PATH+DB_NAME)
    except FileNotFoundError:
        print("WARNING: Old database not found")
    os.rename(DB_PATH+NEW_DB, DB_PATH+DB_NAME)

    print("✅ Database setup completed successfully!")

if __name__ == "__main__":
    main()