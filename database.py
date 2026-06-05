import sqlite3

conn=sqlite3.connect("vocabulary.db")
cursor=conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS Vocabulary (id INTEGER PRIMARY KEY, word TEXT, meaning TEXT, level TEXT)")

cursor.execute("INSERT INTO Vocabulary(word, meaning, level) VALUES(?, ?, ?)", ("友達", "friend", "N5"))
cursor.execute("INSERT INTO Vocabulary(word, meaning, level) VALUES(?, ?, ?)", ("水曜日", "Wednesday", "N5"))
cursor.execute("INSERT INTO Vocabulary(word, meaning, level) VALUES(?, ?, ?)", ("今夜", "tonight", "N5"))
cursor.execute("INSERT INTO Vocabulary(word, meaning, level) VALUES(?, ?, ?)", ("動物", "animal", "N4"))
cursor.execute("INSERT INTO Vocabulary(word, meaning, level) VALUES(?, ?, ?)", ("文化", "culture", "N4"))
cursor.execute("INSERT INTO Vocabulary(word, meaning, level) VALUES(?, ?, ?)", ("発見", "discover", "N3"))
cursor.execute("INSERT INTO Vocabulary(word, meaning, level) VALUES(?, ?, ?)", ("発明", "invention", "N3"))
cursor.execute("INSERT INTO Vocabulary(word, meaning, level) VALUES(?, ?, ?)", ("足跡", "footprint", "N2"))
cursor.execute("INSERT INTO Vocabulary(word, meaning, level) VALUES(?, ?, ?)", ("花火", "fireworks", "N2"))
cursor.execute("INSERT INTO Vocabulary(word, meaning, level) VALUES(?, ?, ?)", ("売り出し", "sale", "N1"))
cursor.execute("INSERT INTO Vocabulary(word, meaning, level) VALUES(?, ?, ?)", ("本の", "mere, only", "N1"))


conn.commit()

conn.close()