import sqlite3
import csv

conn = sqlite3.connect("vocabulary.db")
cursor = conn.cursor()

#creating the table
cursor.execute("CREATE TABLE IF NOT EXISTS Vocabulary(id INTEGER PRIMARY KEY, original TEXT, furigana TEXT, english TEXT, level TEXT) ")

#inserting every row into the database
with open("jlpt_vocab.csv", encoding="utf-8") as file:
    reader=csv.DictReader(file)

    for row in reader:
        cursor.execute("INSERT INTO Vocabulary(original, furigana, english, level) VALUES(?, ?, ?, ?)", (row["Original"], row["Furigana"], row["English"], row["JLPT Level"]))

conn.commit()
conn.close()


