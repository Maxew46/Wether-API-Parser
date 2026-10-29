import sqlite3
conn = sqlite3.connect("whether.db")
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS forecast (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT NOT NULL,
    temperature REAL,
    wind_speed REAL,
    relative_humidity REAL,
    rain TEXT,
    snow TEXT,
    date TEXT NOT NULL
)
    """
)
conn.commit()
conn.close()