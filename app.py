from flask import Flask, render_template, request, redirect
from datetime import datetime
import sqlite3

app=Flask(__name__)

#home page
@app.route("/")
def home():
    return render_template("home.html")

#review page
@app.route("/review/<level>")
def review(level):
    conn=sqlite3.connect("vocabulary.db")
    cursor=conn.cursor()
    cursor.execute("SELECT id, original, furigana, english FROM Vocabulary WHERE level=? ORDER BY RANDOM() LIMIT 1", (level,))
    card=cursor.fetchone()
    conn.close()
    return render_template("review.html", id=card[0], original=card[1], furigana=card[2], english=card[3], level=level)

@app.route("/correct", methods=["POST"])
def correct():
    card_id=request.form["card_id"]
    level=request.form["level"]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn=sqlite3.connect("reviewHistory.db")
    cursor=conn.cursor()
    cursor.execute(f"INSERT INTO ReviewHistory(card_id, level, result, timestamp) VALUES(?, ?, ?, ?)", (card_id, level, "Correct", timestamp))

    conn.commit()
    conn.close()

    return redirect(f"/review/{level}")

@app.route("/incorrect", methods=["POST"])
def incorrect():
    card_id=request.form["card_id"]
    level=request.form["level"]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn=sqlite3.connect("reviewHistory.db")
    cursor=conn.cursor()
    cursor.execute(f"INSERT INTO ReviewHistory(card_id, level, result, timestamp) VALUES(?, ?, ?, ?)", (card_id, level, "Incorrect", timestamp))

    conn.commit()
    conn.close()

    return redirect(f"/review/{level}")

#run flask
if __name__=="__main__":
    app.run(debug=True)