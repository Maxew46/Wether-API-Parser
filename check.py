import sqlite3
conn = sqlite3.connect("whether.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM forecast")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
