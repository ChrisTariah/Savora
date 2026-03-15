import sqlite3

databasePath : str = "Savora.db"

INPUT_SYMBOL : str = "> "
NEW_LINE_SYMBOL : str = "... "
RESULT_SYMBOL : str = "----------------------------"

def main() -> None:
        # Get user commands
        command : str = ""
        prompt : str = INPUT_SYMBOL
        while True:
            try:
                command += input(prompt)
            except KeyboardInterrupt:
                print("SQLite session ended")
                break
            # Indent new line
            prompt = INPUT_SYMBOL
            for c in command:
                if c == "(": prompt += NEW_LINE_SYMBOL
                if c == ")": prompt = prompt.replace(NEW_LINE_SYMBOL, "", 1)
            # Loop input until ";" is received
            if command[-1] != ";": continue
            # Execute
            try:
                # Connect to database
                with sqlite3.connect(databasePath) as conn:
                    db : sqlite3.Cursor = conn.cursor()
                    db.execute("PRAGMA foreign_keys = ON")  # enforce foreign keys
                    db.execute(command)
                    print(RESULT_SYMBOL)
                    for row in db.fetchall():
                        print(row)
                    print(RESULT_SYMBOL)
                conn.close()
            except Exception as e:
                print (f"Error, command not executed:\n{e}")
            finally:
                command = ""

if __name__ == "__main__":
    main()