from app import app

from flask import Flask, render_template

@app.route('/')
def homepage():
    return render_template("homepage.html")

@app.route('/index')
def index():
    return "Hello, World!"