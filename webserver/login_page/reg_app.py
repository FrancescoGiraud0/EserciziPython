from flask import Flask, render_template, redirect, url_for, request
import sqlite3

reg_app = Flask(__name__)

def validateRegistration(username):
    completion = True
    with sqlite3.connect('static/db.db') as con:
        cur = con.cursor()
        cur.execute("SELECT Username FROM Users")
        rows = cur.fetchall()
        while True:
            if rows == username:
                completion = False
                break
            
    return completion

def insertDB(username, password):
    with sqlite3.connect('static/db.db') as con:
        cur = con.cursor()
        cur.execute(f"INSERT INTO USERS (USERNAME, PASSWORD) VALUES {username}, {password}")

def check_password(hashed_password, user_password):
    return hashed_password == user_password


@reg_app.route('/', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        completion = validateRegistration(username)
        if completion ==False:
            error = 'This username already exists. Please try again.'
        else:
            insertDB(username, password)
            return redirect(url_for('secret'))

    return render_template('login.html', error=error)

@reg_app.route('/secret')
def secret():
    return "This is a secret page!"

if __name__== "__main__":
    reg_app.run()