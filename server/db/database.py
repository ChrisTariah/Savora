import sqlite3
from server.config import DB_PATH

def get_db():
    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA foreign_keys = ON")
    return con