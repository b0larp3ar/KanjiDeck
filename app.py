from flask import Flask, render_template, request
import sqlite3
import random

app=Flask(__name__)

#home page
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/review/<level>")
def review(level):
    conn=sqlite3.connect("vocabulary.db")
    cursor=conn.cursor()
    cursor.execute("SELECT word, meaning FROM Vocabulary WHERE level=? ORDER BY RANDOM() LIMIT 1", (level,))
    card=cursor.fetchone()
    conn.close()
    return render_template("review.html", word=card[0], meaning=card[1], level=level)

#run flask
if __name__=="__main__":
    app.run(debug=True)