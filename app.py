from flask import Flask, render_template, request, redirect
from datetime import datetime
import sqlite3

app=Flask(__name__)

#home page
@app.route("/")
def home():
    return render_template("home.html")

#review page

a=0 #current queue position
@app.route("/review/<level>")
def review(level):
    conn=sqlite3.connect("vocabulary.db")
    cursor=conn.cursor()

    global a
    card=()

    if a==0:
        cursor.execute("SELECT id from Vocabulary WHERE position=? ORDER BY RANDOM() LIMIT 1", (a,)) #if a=0, choose any card whose position=0
        elementid=cursor.fetchone()[0]
        cursor.execute("UPDATE Vocabulary SET position=? WHERE id=?", (1, elementid)) #set its position to 1
        a+=1

    if card==():
        cursor.execute("SELECT * from Vocabulary WHERE position=? ORDER BY RANDOM()", (a,)) #choose a card whose position=a
        card=cursor.fetchone()
        
        if card is None:
            cursor.execute("SELECT * FROM Vocabulary WHERE position=0 ORDER BY RANDOM() LIMIT 1") #if no card has position=a, choose any card whose position=0
            card=cursor.fetchone()
            cursor.execute("UPDATE Vocabulary SET position=? WHERE id=?", (a, card[0])) #set its position to a

        a+=1

    conn.commit()
    conn.close()
    
    return render_template("review.html", id=card[0], original=card[1], furigana=card[2], english=card[3], level=level, correct=card[4], incorrect=card[5], position=card[6])

#Updates reviewHistory.db when user reviews a card
@app.route("/correct", methods=["POST"])
def correct():
    card_id=request.form["card_id"]
    level=request.form["level"]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    correct=int(request.form["correct"])+1
    incorrect=int(request.form["incorrect"])

    #Updates review history
    conn=sqlite3.connect("reviewHistory.db")
    cursor=conn.cursor()
    cursor.execute(f"INSERT INTO ReviewHistory(card_id, level, result, timestamp) VALUES(?, ?, ?, ?)", (card_id, level, "Correct", timestamp))
    conn.commit()
    conn.close()

    #Updates queue position of the card reviewed
    conn=sqlite3.connect("vocabulary.db")
    cursor=conn.cursor()
    cursor.execute("UPDATE Vocabulary SET correct=? WHERE id=?", (correct, card_id))

    total=correct+incorrect
    correct_percentage=(correct/total)*100

    position = max(1, round(10 * (1.05 ** (correct_percentage - 50)))) #finds position
    
    global a
    cursor.execute("UPDATE Vocabulary SET position=? WHERE id=?", (position+a, card_id)) #updates position of reviewed cardz

    conn.commit()
    conn.close()

    return redirect(f"/review/{level}")

@app.route("/incorrect", methods=["POST"])
def incorrect():
    card_id=request.form["card_id"]
    level=request.form["level"]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    correct=int(request.form["correct"])
    incorrect=int(request.form["incorrect"])+1

    #Updates review history
    conn=sqlite3.connect("reviewHistory.db")
    cursor=conn.cursor()
    cursor.execute(f"INSERT INTO ReviewHistory(card_id, level, result, timestamp) VALUES(?, ?, ?, ?)", (card_id, level, "Incorrect", timestamp))
    conn.commit()
    conn.close()

    #Updates queue position of the card reviewed
    conn=sqlite3.connect("vocabulary.db")
    cursor=conn.cursor()
    cursor.execute("UPDATE Vocabulary SET incorrect=? WHERE id=?", (incorrect, card_id))

    total=correct+incorrect
    correct_percentage=(correct/total)*100

    position = max(1, round(10 * (1.05 ** (correct_percentage - 50))))
    
    global a
    cursor.execute("UPDATE Vocabulary SET position=? WHERE id=?", (position+a, card_id))
    conn.commit()
    conn.close()

    return redirect(f"/review/{level}")

#statistics page
@app.route("/statistics")
def statistics():
    conn=sqlite3.connect("reviewHistory.db")
    cursor=conn.cursor()

    #number of correct reviews
    cursor.execute("SELECT COUNT(*) FROM ReviewHistory WHERE result='Correct'")
    correct=cursor.fetchone()[0]

    #number of incorrect reviews
    cursor.execute("SELECT COUNT(*) FROM ReviewHistory WHERE result='Incorrect'")
    incorrect=cursor.fetchone()[0]

    #number of N5 reviews
    cursor.execute("SELECT COUNT(*) FROM ReviewHistory WHERE level='N5'")
    n5=cursor.fetchone()[0]

    #number of N4 reviews
    cursor.execute("SELECT COUNT(*) FROM ReviewHistory WHERE level='N4'")
    n4=cursor.fetchone()[0]

    #number of N3 reviews
    cursor.execute("SELECT COUNT(*) FROM ReviewHistory WHERE level='N3'")
    n3=cursor.fetchone()[0]

    #number of N2 reviews
    cursor.execute("SELECT COUNT(*) FROM ReviewHistory WHERE level='N2'")
    n2=cursor.fetchone()[0]

    #number of N1 reviews
    cursor.execute("SELECT COUNT(*) FROM ReviewHistory WHERE level='N1'")
    n1=cursor.fetchone()[0]

    conn.close()

    total=correct+incorrect

    if total!=0:
        correct_percentage=round((correct/total)*100, 2)
        incorrect_percentage=round((incorrect/total)*100, 2)
    else:
        correct_percentage=0
        incorrect_percentage=0

    return render_template("statistics.html", correct=correct, incorrect=incorrect, total=total, n5=n5, n4=n4, n3=n3, n2=n2, n1=n1, correct_percentage=correct_percentage, incorrect_percentage=incorrect_percentage)

#run flask
if __name__=="__main__":
    app.run(debug=True)