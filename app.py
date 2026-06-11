from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from datetime import datetime
import sqlite3

app=Flask(__name__)
app.secret_key="kanjideck_secretkey"

#home page
@app.route("/")
def home():
    if "user_id" in session:
        #getting username
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM User WHERE id=?", (session["user_id"],))
        username = cursor.fetchone()[0]
        conn.close()

        return render_template("home.html", username=username)

    return render_template("home.html")

#review page
@app.route("/review/<level>")
def review(level):
    if "user_id" not in session:
        return redirect("/login")

    user_id=session["user_id"]

    conn=sqlite3.connect("userProgress.db")
    cursor=conn.cursor()

    cursor.execute("SELECT current_position FROM UserQueue WHERE (user_id, level)=(?, ?)", (user_id, level))
    current_position=cursor.fetchone()[0]
    card=()

    if current_position==0:
        cursor.execute("SELECT id from UserProgress WHERE position=? AND user_id=? AND level=? ORDER BY RANDOM() LIMIT 1", (0, user_id, level)) #if cp=0, choose any card whose position=0
        id=cursor.fetchone()[0]
        cursor.execute("UPDATE UserProgress SET position=? WHERE id=?", (1, id)) #set its position to 1
        current_position+=1

    if card==(): 
        cursor.execute("SELECT * from UserProgress WHERE position=? AND user_id=? AND level=? ORDER BY RANDOM()", (current_position, user_id, level)) #choose a card whose position=cp
        card=cursor.fetchone()
        
        if card is None:
            cursor.execute("SELECT * FROM UserProgress WHERE position=0 AND user_id=? AND level=? ORDER BY RANDOM() LIMIT 1", (user_id, level)) #if no card has position=cp, choose any card whose position=0
            card=cursor.fetchone()
            cursor.execute("UPDATE UserProgress SET position=? WHERE id=?", (current_position, card[0])) #set its position to a
        current_position+=1

    cursor.execute("UPDATE UserQueue SET current_position=? WHERE (user_id, level)=(?, ?)", (current_position, user_id, level))

    conn.commit()
    conn.close()

    conn=sqlite3.connect("vocabulary.db")
    cursor=conn.cursor()
    cursor.execute("SELECT original, furigana, english FROM Vocabulary WHERE id=?", (card[2],))
    vocab=cursor.fetchone()
    conn.close()
    
    return render_template("review.html", id=card[2], original=vocab[0], furigana=vocab[1], english=vocab[2], level=level, correct=card[4], incorrect=card[5], position=card[6])

#Updates reviewHistory.db when user reviews a card
@app.route("/correct", methods=["POST"])
def correct():
    user_id=session["user_id"]
    card_id=request.form["card_id"]
    level=request.form["level"]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    correct=int(request.form["correct"])+1
    incorrect=int(request.form["incorrect"])

    #Updates queue position of the card reviewed
    conn=sqlite3.connect("userProgress.db")
    cursor=conn.cursor()
 
    cursor.execute("UPDATE UserProgress SET correct=? WHERE (user_id, card_id)=(?, ?)", (correct, user_id, card_id))
    
    cursor.execute("SELECT current_position FROM UserQueue WHERE (user_id, level)=(?, ?)", (user_id, level))
    current_position=cursor.fetchone()[0]

    total=correct+incorrect
    correct_percentage=(correct/total)*100
    position = max(5, round(10 * (1.05 ** (correct_percentage - 50)))) #finds position
    
    global a
    cursor.execute("UPDATE UserProgress SET position=? WHERE (user_id, card_id)=(?, ?)", (position+current_position, user_id, card_id)) #updates position of reviewed cardz

    conn.commit()
    conn.close()

    return redirect(f"/review/{level}")

@app.route("/incorrect", methods=["POST"])
def incorrect():
    user_id=session["user_id"]
    card_id=request.form["card_id"]
    level=request.form["level"]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    correct=int(request.form["correct"])
    incorrect=int(request.form["incorrect"])+1

    #Updates queue position of the card reviewed
    conn=sqlite3.connect("userProgress.db")
    cursor=conn.cursor()

    cursor.execute("UPDATE UserProgress SET incorrect=? WHERE (user_id, card_id)=(?, ?)", (incorrect, user_id, card_id))
    cursor.execute("SELECT current_position FROM UserQueue WHERE (user_id, level)=(?, ?)", (user_id, level))
    current_position=cursor.fetchone()[0]

    total=correct+incorrect
    correct_percentage=(correct/total)*100

    position = max(5, round(10 * (1.05 ** (correct_percentage - 50))))
    
    global a
    cursor.execute("UPDATE UserProgress SET position=? WHERE (user_id, card_id)=(?, ?)", (position+current_position, user_id, card_id))
    conn.commit()
    conn.close()

    return redirect(f"/review/{level}")

#statistics page
@app.route("/statistics")
def statistics():
    if "user_id" not in session:
        return redirect("/login")

    user_id=session["user_id"]

    conn=sqlite3.connect("userProgress.db")
    cursor=conn.cursor()

    #number of correct reviews
    cursor.execute("SELECT SUM(correct) FROM UserProgress WHERE user_id=?", (user_id,))
    correct=cursor.fetchone()[0]

    #number of incorrect reviews
    cursor.execute("SELECT SUM(incorrect) FROM UserProgress WHERE user_id=?", (user_id,))
    incorrect=cursor.fetchone()[0]

    #number of N5 reviews
    cursor.execute("SELECT SUM(correct+incorrect) FROM UserProgress WHERE user_id=? AND level='N5'", (user_id,))
    n5=cursor.fetchone()[0]

    #number of N4 reviews
    cursor.execute("SELECT SUM(correct+incorrect) FROM UserProgress WHERE user_id=? AND level='N4'", (user_id,))
    n4=cursor.fetchone()[0]

    #number of N3 reviews
    cursor.execute("SELECT SUM(correct+incorrect) FROM UserProgress WHERE user_id=? AND level='N3'", (user_id,))
    n3=cursor.fetchone()[0]

    #number of N2 reviews
    cursor.execute("SELECT SUM(correct+incorrect) FROM UserProgress WHERE user_id=? AND level='N2'", (user_id,))
    n2=cursor.fetchone()[0]

    #number of N1 reviews
    cursor.execute("SELECT SUM(correct+incorrect) FROM UserProgress WHERE user_id=? AND level='N1'", (user_id,))
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

#register page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method=="GET":
        return render_template("register.html")

    username=request.form["username"]

    #check if username already exists
    conn=sqlite3.connect("users.db")
    cursor=conn.cursor()
    cursor.execute("SELECT username FROM User WHERE username=?", (username, ))
    username_db=cursor.fetchone()[0]
    conn.close()

    if username_db:
        error="Username already exists"
        return render_template("register.html", error=error)

    #check if password matches confirm password
    password=request.form["password"]
    confirm_password=request.form["confirm-password"]

    if password!=confirm_password:
        error="Passwords do not match"
        return render_template("register.html", error=error)

    password_hash=generate_password_hash(password)

    #store the new user's credentials in users
    conn=sqlite3.connect("users.db")
    cursor=conn.cursor()
    cursor.execute("INSERT INTO User(username, password_hash) VALUES(?, ?)", (username, password_hash))
    user_id=cursor.lastrowid
    conn.commit()
    conn.close()

    #create rows for every card for this user in userProgress and initialize current queue positions for each level
    conn=sqlite3.connect("vocabulary.db")
    cursor=conn.cursor()
    cursor.execute("SELECT id, level FROM Vocabulary") #getting every card from Vocabulary
    cards=cursor.fetchall()
    conn.close()

    conn=sqlite3.connect("userProgress.db")
    cursor=conn.cursor()
    for card in cards:
        cursor.execute("INSERT INTO UserProgress(user_id, card_id, level, correct, incorrect, position) VALUES(?, ?, ?, ?, ?, ?)", (user_id, card[0], card[1], 0, 0, 0)) #uploading every card in userProgress for this user
    
    for level in ["N5", "N4", "N3", "N2", "N1"]:
        cursor.execute("INSERT INTO UserQueue(user_id, level, current_position) VALUES(?, ?, ?)", (user_id, level, 0))
    
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="GET":
        return render_template("login.html")

    username=request.form["username"]
    password=request.form["password"]

    conn=sqlite3.connect("users.db")
    cursor=conn.cursor()

    cursor.execute("SELECT id, password_hash FROM User WHERE username=?", (username, ))

    user=cursor.fetchone()

    conn.commit()
    conn.close()

    if user is None:
        error="Username does not exist"
        return render_template("login.html", error=error)
    
    if check_password_hash(user[1], password):
        session["user_id"]=user[0]
    else:
        error="Incorrect password"
        return render_template("login.html", error=error)
    
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

#run flask
if __name__=="__main__":
    app.run(debug=True)