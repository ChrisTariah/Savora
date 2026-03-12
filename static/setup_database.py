import sqlite3
import os

DB_FILE = "../Savora.db"

# Order matters: Minimum schema first, then users, ingredients, tags, fridge, API columns
SQL_FILES = [
    "Minimum_Viable_Schema.sql",
    "user_schema.sql",
    "Ingredient_Schema.sql",
    "Ingredinent_API_Schema.sql",
    "tags_schema.sql",
    "Fridge_schema.sql"
]

def connect_db():
    return sqlite3.connect(DB_FILE)

def execute_sql_file(con, filename):
    print(f"Running {filename}...")
    with open(filename, "r", encoding="utf-8") as f:
        sql_script = f.read()
    cursor = con.cursor()
    cursor.executescript(sql_script)
    con.commit()
    cursor.close()
    print(f"{filename} completed.\n")

def main():
    # Remove old database for a clean slate
    if os.path.exists(DB_FILE):
        print("Removing old database file...")
        os.remove(DB_FILE)

    con = connect_db()
    print("Creating new database...")

    for file in SQL_FILES:
        if os.path.exists(file):
            execute_sql_file(con, file)
        else:
            print(f"WARNING: {file} not found!")

    # Make sure the Recipe table has userID (avoid duplicate column)
    cursor = con.cursor()
    cursor.execute("PRAGMA table_info(Recipe);")
    columns = [c[1] for c in cursor.fetchall()]
    if "userID" not in columns:
        cursor.execute("ALTER TABLE Recipe ADD COLUMN userID INTEGER NOT NULL DEFAULT 0;")
        con.commit()
        print("Added userID column to Recipe table")

    # Create sessions table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            userID INTEGER
        );
    """)
    con.commit()
    cursor.close()
    con.close()

    print("✅ Database setup completed successfully!")

if __name__ == "__main__":
    main()