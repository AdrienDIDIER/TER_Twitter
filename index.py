from flask import Flask, render_template, url_for, request, session, redirect
from database import app, mongo
from auth import *

@app.route('/')
def index():
    userLogged = isLogged()
    user = None
    if userLogged:
        users = mongo.db.users
        user = users.find_one({'email': session['email']})
    return render_template('index.html', userLogged=userLogged, user=user)

if __name__ == '__main__':
    app.run(debug=True)
