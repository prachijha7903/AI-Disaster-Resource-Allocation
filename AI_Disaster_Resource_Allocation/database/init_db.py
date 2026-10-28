
import sqlite3
from pathlib import Path

# Store the database inside the database folder
DB_PATH = Path(__file__).with_name("disaster.db")


def initialize_database():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS disaster_zones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            severity TEXT NOT NULL,
            people_affected INTEGER NOT NULL,
            resources_available INTEGER NOT NULL,
            priority INTEGER NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM disaster_zones")
    count = cursor.fetchone()[0]

    if count == 0:
        sample_zones = [
            ("Zone A - Flood Affected", "Ludhiana", "High", 200, 50, 90),
            ("Zone B - Heavy Rainfall", "Chandigarh", "Medium", 80, 100, 65),
            ("Zone C - Storm Warning", "Delhi", "Low", 30, 75, 35)
        ]

        cursor.executemany("""
            INSERT INTO disaster_zones
            (name, location, severity, people_affected,
             resources_available, priority)
            VALUES (?, ?, ?, ?, ?, ?)
        """, sample_zones)

    connection.commit()
    connection.close()
    print("Database initialized successfully!")


if __name__ == "__main__":
    initialize_database()
