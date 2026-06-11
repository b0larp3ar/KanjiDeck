from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import os

load_dotenv() 
#helper function to connect to supabase
def getdb():
    return psycopg2.connect(os.environ["DATABASE_URL"])
#setting up flask
app=Flask(__name__)
app.secret_key=os.environ["SECRET_KEY"]

#home page
@app.route("/")
def home():
    if "user_id" in session:
        #getting username
        conn=getdb()
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM user_account WHERE id=%s", (session["user_id"],))
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

    conn=getdb()
    cursor=conn.cursor()

    cursor.execute("SELECT current_queue_position FROM user_queue WHERE (user_id, level)=(%s, %s)", (user_id, level))
    current_position=cursor.fetchone()[0]
    card=()

    if current_position==0:
        cursor.execute("SELECT id from user_progress WHERE position=%s AND user_id=%s AND level=%s ORDER BY RANDOM() LIMIT 1", (0, user_id, level)) #if cp=0, choose any card whose position=0
        id=cursor.fetchone()[0]
        cursor.execute("UPDATE user_progress SET position=%s WHERE id=%s", (1, id)) #set its position to 1
        current_position+=1

    if card==(): 
        cursor.execute("SELECT * from user_progress WHERE position=%s AND user_id=%s AND level=%s ORDER BY RANDOM()", (current_position, user_id, level)) #choose a card whose position=cp
        card=cursor.fetchone()
        
        if card is None:
            cursor.execute("SELECT * FROM user_progress WHERE position=0 AND user_id=%s AND level=%s ORDER BY RANDOM() LIMIT 1", (user_id, level)) #if no card has position=cp, choose any card whose position=0
            card=cursor.fetchone()
            cursor.execute("UPDATE user_progress SET position=%s WHERE id=%s", (current_position, card[0])) #set its position to a
        current_position+=1

    cursor.execute("UPDATE user_queue SET current_queue_position=%s WHERE (user_id, level)=(%s, %s)", (current_position, user_id, level))

    cursor.execute("SELECT original, furigana, english FROM vocabulary WHERE id=%s", (card[2],))
    vocab=cursor.fetchone()
    
    conn.commit()
    conn.close()
    
    return render_template("review.html", id=card[2], original=vocab[0], furigana=vocab[1], english=vocab[2], level=level, correct=card[4], incorrect=card[5], position=card[6])

#Updates reviewHistory.db when user reviews a card
@app.route("/correct", methods=["POST"])
def correct():
    user_id=session["user_id"]
    card_id=request.form["card_id"]
    level=request.form["level"]
    correct=int(request.form["correct"])+1
    incorrect=int(request.form["incorrect"])

    #Updates queue position of the card reviewed
    conn=getdb()
    cursor=conn.cursor()
 
    cursor.execute("UPDATE user_progress SET correct=%s WHERE (user_id, card_id)=(%s, %s)", (correct, user_id, card_id))
    
    cursor.execute("SELECT current_queue_position FROM user_queue WHERE (user_id, level)=(%s, %s)", (user_id, level))
    current_position=cursor.fetchone()[0]

    total=correct+incorrect
    correct_percentage=(correct/total)*100
    position = max(5, round(10 * (1.05 ** (correct_percentage - 50)))) #finds position
    
    cursor.execute("UPDATE user_progress SET position=%s WHERE (user_id, card_id)=(%s, %s)", (position+current_position, user_id, card_id)) #updates position of reviewed cardz

    conn.commit()
    conn.close()

    return redirect(f"/review/{level}")

@app.route("/incorrect", methods=["POST"])
def incorrect():
    user_id=session["user_id"]
    card_id=request.form["card_id"]
    level=request.form["level"]
    correct=int(request.form["correct"])
    incorrect=int(request.form["incorrect"])+1

    #Updates queue position of the card reviewed
    conn=getdb()
    cursor=conn.cursor()

    cursor.execute("UPDATE user_progress SET incorrect=%s WHERE (user_id, card_id)=(%s, %s)", (incorrect, user_id, card_id))
    cursor.execute("SELECT current_queue_position FROM user_queue WHERE (user_id, level)=(%s, %s)", (user_id, level))
    current_position=cursor.fetchone()[0]

    total=correct+incorrect
    correct_percentage=(correct/total)*100

    position = max(5, round(10 * (1.05 ** (correct_percentage - 50))))
    
    cursor.execute("UPDATE user_progress SET position=%s WHERE (user_id, card_id)=(%s, %s)", (position+current_position, user_id, card_id))

    conn.commit()
    conn.close()

    return redirect(f"/review/{level}")

#statistics page
@app.route("/statistics")
def statistics():
    if "user_id" not in session:
        return redirect("/login")

    user_id=session["user_id"]

    conn=getdb()
    cursor=conn.cursor()

    #number of correct reviews
    cursor.execute("SELECT SUM(correct) FROM user_progress WHERE user_id=%s", (user_id,))
    correct=cursor.fetchone()[0]

    #number of incorrect reviews
    cursor.execute("SELECT SUM(incorrect) FROM user_progress WHERE user_id=%s", (user_id,))
    incorrect=cursor.fetchone()[0]

    #number of N5 reviews
    cursor.execute("SELECT SUM(correct+incorrect) FROM user_progress WHERE user_id=%s AND level='N5'", (user_id,))
    n5=cursor.fetchone()[0]

    #number of N4 reviews
    cursor.execute("SELECT SUM(correct+incorrect) FROM user_progress WHERE user_id=%s AND level='N4'", (user_id,))
    n4=cursor.fetchone()[0]

    #number of N3 reviews
    cursor.execute("SELECT SUM(correct+incorrect) FROM user_progress WHERE user_id=%s AND level='N3'", (user_id,))
    n3=cursor.fetchone()[0]

    #number of N2 reviews
    cursor.execute("SELECT SUM(correct+incorrect) FROM user_progress WHERE user_id=%s AND level='N2'", (user_id,))
    n2=cursor.fetchone()[0]

    #number of N1 reviews
    cursor.execute("SELECT SUM(correct+incorrect) FROM user_progress WHERE user_id=%s AND level='N1'", (user_id,))
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
    password=request.form["password"]
    confirm_password=request.form["confirm-password"]

    conn=getdb() #connected to supabase
    cursor=conn.cursor()

    #check if username already exists
    cursor.execute("SELECT username FROM user_account WHERE username=%s", (username, ))
    username_db=cursor.fetchone()

    if username_db is not None:
        error="Username already exists"
        return render_template("register.html", error=error)

    #check if password matches confirm password
    if password!=confirm_password:
        error="Passwords do not match"
        return render_template("register.html", error=error)

    password_hash=generate_password_hash(password)

    #store the new user's credentials in users
    cursor.execute("INSERT INTO user_account(username, password_hash) VALUES(%s, %s) RETURNING id", (username, password_hash))
    user_id=cursor.fetchone()[0]

    #create rows for every card for this user in userProgress and initialize current queue positions for each level
    cursor.execute("SELECT id, level FROM vocabulary") #getting every card from Vocabulary
    cards=cursor.fetchall()

    rows=[]
    for card in cards:
        rows.append((user_id, card[0], card[1], 0, 0, 0))
    execute_values(cursor, "INSERT INTO user_progress(user_id, card_id, level, correct, incorrect, position) VALUES %s", rows)
    
    for level in ["N5", "N4", "N3", "N2", "N1"]:
        cursor.execute("INSERT INTO user_queue(user_id, level, current_queue_position) VALUES(%s, %s, %s)", (user_id, level, 0))

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="GET":
        return render_template("login.html")

    username=request.form["username"]
    password=request.form["password"]

    conn=getdb()
    cursor=conn.cursor()
    cursor.execute("SELECT id, password_hash FROM user_account WHERE username=%s", (username, ))
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