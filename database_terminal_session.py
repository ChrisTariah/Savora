import sqlite3

databasePath : str = "Savora.db"

def main() -> None:
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
                # Connect to database
                with sqlite3.connect(databasePath) as conn:
                    db : sqlite3.Cursor = conn.cursor()
                    db.execute("PRAGMA foreign_keys = ON")  # enforce foreign keys
                    db.execute(command)
                    for row in db.fetchall():
                        print(row)
                conn.close()
            except Exception as e:
                print (f"Error, command not executed:\n{e}")
            finally:
                command = ""
                prompt = "> "

if __name__ == "__main__":
    main()