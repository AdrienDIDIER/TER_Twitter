from flask import Flask, render_template, url_for, request, session, redirect
from myapp import app, mongo
from auth import getUser, isLogged


@app.route('/session/add/', methods=['POST', 'GET'])
@app.route('/session/add/<mode>', methods=['POST', 'GET'])
def addSession(mode=None):
    if request.method == 'GET':
        return render_template('session_create_form.html', mode=mode)
    elif request.method == 'POST':
        if isLogged():
            session_collection = mongo.db.sessions
            user_logged = getUser()
            session_collection.insert({'user_id': user_logged['_id'], 'session_name': request.form['session_name']})
            return "<h1>Session created</h1>"
