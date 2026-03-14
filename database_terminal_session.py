import sqlite3

databasePath : str = "Savora.db"

def main() -> None:
    # Connect to database
    with sqlite3.connect(databasePath) as conn:
        db : sqlite3.Cursor = conn.cursor()
        db.execute("PRAGMA foreign_keys = ON")  # enforce foreign keys

        # Get user commands
        command : str = ""
        prompt : str = "> "
        while True:
            command += input(prompt)
            # New line
            if command[-1] != ";":
                prompt += "... "
                continue
            # Execute
            try:
                db.execute(command)
                for row in db.fetchall():
                    print(row)
            except Exception as e:
                command = ""
                prompt = "> "
                print (f"Error, command not executed:\n{e}")

if __name__ == "__main__":
    main()