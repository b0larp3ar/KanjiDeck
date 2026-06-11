import sqlite3

conn=sqlite3.connect("userProgress.db")
cursor=conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS UserProgress(id INTEGER PRIMARY KEY, user_ID INTEGER, card_ID INTEGER, level TEXT, correct INTEGER, incorrect INTEGER, position INTEGER)")

cursor.execute("CREATE TABLE IF NOT EXISTS UserQueue(user_id INTEGER, level TEXT, current_position INTEGER, PRIMARY KEY(user_id, level))")

conn.commit()
conn.close()