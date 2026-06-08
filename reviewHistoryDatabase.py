import sqlite3

conn=sqlite3.connect("reviewHistory.db")
cursor=conn.cursor()

#creating the table
cursor.execute("CREATE TABLE IF NOT EXISTS ReviewHistory(id INTEGER PRIMARY KEY,card_id INTEGER, level TEXT, result TEXT, timestamp TEXT)")

conn.commit()
conn.close()