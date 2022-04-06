from flask import Flask, render_template, request, jsonify, session
from werkzeug.utils import secure_filename
from secrets import token_urlsafe
from github import GitHub, Cohorts
from config import latest_updates, is_password, save_update
from pathlib import Path
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = "FkDAg7MUxxAuXe3WYICZwg"



@app.route('/session', methods=['POST'])
def create_session():
    if 'password' in request.form:
        if is_password(request.form['password']):
            path = Path.cwd() / Path('static') / Path('github.csv')
            cohorts = Cohorts(path)
            return jsonify({'root': cohorts.root, 'students': cohorts.students})
    return jsonify({'error': "Invalid Password"})


@app.route('/')
def home():
    return render_template("contribution.html")


@app.route('/authenticated', methods=['POST'])
def authenticated():
    return jsonify({'authenticated': is_password(request.form['password'])})


@app.route('/updates', methods=['GET'])
def updates():
    return jsonify(latest_updates())


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify("No file was found"), 500
    file = request.files['file']
    if file.filename == '' or not file:
        return jsonify("No selected file"), 500
    path = Path.cwd() / Path('static') / Path('github.csv')
    file.save(path)
    save_update()
    return jsonify({"status": True})


@app.route('/contribution', methods=['POST', 'GET'])
def contribution():
    if request.method == "GET":
        username = request.values['username']
    elif request.method == "POST":
        username = request.form['username']
    else:
        return ""
    git = GitHub(username)
    count = 0
    fetched = False
    while not fetched and count < 2:
        try:
            git.fetch()
            fetched = True
        except Exception:
            pass
        count += 1
    if not fetched:
        return jsonify({
            "graph_image": git.graph,
            "url": git.url,
            "profile_image": git.profile_image,
            "username": git.username
        }), 500
    return jsonify({
        "graph_image": git.graph,
        "url": git.url,
        "profile_image": git.profile_image,
        "username": git.username
    })


if __name__ == '__main__':
    app.run()
