from __main__ import app
from flask import render_template


@app.route('/')
def home():
    return render_template("contribution.html")
