import sqlite3
import os
from src.config import DB_PATH, SCHEMA_PATH

def init_db():
    """Initialize the database with the schema."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    
    conn = sqlite3.connect(DB_PATH)
    with open(SCHEMA_PATH, 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

def get_connection():
    return sqlite3.connect(DB_PATH)