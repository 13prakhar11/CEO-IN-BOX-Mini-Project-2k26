import sqlite3

# Connect to the local SQLite database created by main.py
conn = sqlite3.connect("auto_ceo_memory.sqlite")
cursor = conn.cursor()

# Query all tables automatically created by LangGraph
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("--- Database Tables Found ---")
for t in tables:
    print(f"- {t[0]}")

# Count saved checkpoints/sessions
cursor.execute("SELECT COUNT(*) FROM checkpoints;")
count = cursor.fetchone()[0]
print(f"\nTotal Saved State Checkpoints: {count}")

conn.close()