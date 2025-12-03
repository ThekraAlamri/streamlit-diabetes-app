import sqlite3
import os


def init_database():
    """Initialize the database with required tables"""
    # Create db directory if it doesn't exist
    os.makedirs('db', exist_ok=True)

    # Connect to database
    conn = sqlite3.connect('db/diabetes_app.db')
    c = conn.cursor()

    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create predictions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            pregnancies INTEGER,
            glucose REAL,
            blood_pressure REAL,
            skin_thickness REAL,
            insulin REAL,
            bmi REAL,
            dpf REAL,
            age INTEGER,
            prediction INTEGER,
            probability REAL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (username) REFERENCES users (username)
        )
    ''')

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print("✅ Database initialized successfully!")
    print("Created tables:")
    print("- users")
    print("- predictions")


if __name__ == "__main__":
    init_database()