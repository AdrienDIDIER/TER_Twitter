from flask import Flask, render_template, url_for, request, session, redirect
from auth import isLogged
from myapp import app, mongo
from flask_pymongo import PyMongo, pymongo
from math import ceil


@app.route('/', methods=['GET'])
def index():
    userLogged = isLogged()
    user = None
    user_sessions = None
    sessionAmount = None
    page_number = None
    current_page = None
    if userLogged:
        current_page = 1
        if 'page' in request.args:
            current_page = int(request.args['page'])
        limit = 8
        offset = (current_page - 1) * limit
        users = mongo.db.users
        user = users.find_one({'email': session['email']})
        starting_session = mongo.db.sessions.find({'user_id': user['_id']}).sort(
            [("last_modification_date", pymongo.DESCENDING), ("start_date", pymongo.DESCENDING)])
        page_number = ceil(starting_session.count() / limit)  # ceil arrondit à la valeur entière supérieure
        if starting_session.count() != 0:
            last_session = starting_session[offset]["last_modification_date"]
            user_sessions = mongo.db.sessions.find(
                {'user_id': user['_id'], 'last_modification_date': {'$lte': last_session}}).sort(
                [("last_modification_date", pymongo.DESCENDING), ("star_date", pymongo.DESCENDING)]).limit(limit)
        else:
            sessionAmount = 0
    return render_template('index.html', userLogged=userLogged, user=user, user_sessions=user_sessions,
                           sessionAmount=sessionAmount, page_number=page_number, current_page=current_page)
