from flask import Flask, render_template, url_for, request, session, redirect
from database import app, mongo
from auth import *

@app.route('/')
def index():
    return render_template('index.html')

@app.route('')

if __name__ == '__main__':
    app.run(debug=True)
