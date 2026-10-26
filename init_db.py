import sqlite3

def setup_database():
    conn = sqlite3.connect("auto_ceo_memory.sqlite")
    cursor = conn.cursor()
    
    # Create a table for users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    
    # Insert default test accounts (IGNORE if they already exist)
    cursor.execute('INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)', 
                   ('admin', 'password123', 'admin'))
    cursor.execute('INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)', 
                   ('client1', 'demo123', 'user'))
    
    conn.commit()
    conn.close()
    print("User database initialized successfully.")

if __name__ == "__main__":
    setup_database()