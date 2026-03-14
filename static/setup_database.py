import sqlite3
import os

DB_FILE = "../Savora.db"

SQL_FILES = [
    "static/Base_Schema.sql",
    "static/Test_Data.sql" 
    # For some reason this script is searching the parent directory ??
    # "static/" required to read files
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
            raise FileNotFoundError(f"WARNING: {file} not found!")

    print("✅ Database setup completed successfully!")

if __name__ == "__main__":
    #print(os.listdir()) # Why is it searching parent directory ???
    main()