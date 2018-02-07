from flask import Flask, render_template, url_for, request, session, redirect
from myapp import app, mongo
import bcrypt


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'email': request.form['email']})
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'first_name': request.form['first_name'], 'last_name': request.form['last_name'],
                          'email': request.form['email'], 'password': hashpass})
            session['email'] = request.form['email']
            return redirect(url_for('index'))
        else:
            return 'That username already exists!'
    else:
        return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'email': request.form['email']})

        if login_user:
            if bcrypt.checkpw(request.form['password'].encode('utf-8'), login_user['password']):
                session['email'] = request.form['email']
                return redirect(url_for('index'))
        else:
            return 'Invalid email/password combination'
    else:
        return render_template('login.html')


@app.route('/session')
def createSession():
    session['username'] = 'Solal'
    return 'Session page'


@app.route('/getSession')
def getSession():
    if 'username' in session:
        return session['username']
    else:
        return 'Not logged in !'


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


def isLogged():
    return 'email' in session

def getUser():
    if isLogged():
        return mongo.db.users.find_one({'email' : session['email']})