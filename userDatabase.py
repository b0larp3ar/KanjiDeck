import sqlite3

conn=sqlite3.connect("users.db")
cursor=conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS User(id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL)")

conn.commit()
conn.close()