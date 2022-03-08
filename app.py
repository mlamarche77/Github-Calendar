from flask import Flask, render_template, request, jsonify
from secrets import token_urlsafe
from github import GitHub, Cohorts
from pathlib import Path
from datetime import datetime
import json
import re

app = Flask(__name__)
app.secret_key = "FkDAg7MUxxAuXe3WYICZwg"


def extract_inputs(name):
    data = {}
    for input_name in request.form:
        key = re.sub(r'\[.*?\]', '', input_name)
        if name == key:
            found = re.findall(r'\[(.*)\]', input_name)
            if len(found) > 0:
                data[found[0]] = request.form[input_name]
    return data


def session_params():
    if 'session' in request.form:
        return extract_inputs('session')


def save_session():
    path = Path.cwd() / Path("static") / Path("sessions.json")
    if path.exists():
        with open(path, 'r') as r:
            sessions = json.load(r)
    else:
        sessions = {}
    time = datetime.now().strftime("%m/%d/%Y - %H:%M:%S")
    token = token_urlsafe(16)
    sessions[token] = time
    with open(path, 'w') as w:
        json.dump(sessions, w)
    return token


def authentication():
    path = Path.cwd() / Path("static") / Path("pass.txt")
    if path.exists():
        with open(path, 'r') as r:
            return r.read()


@app.route('/session', methods=['POST'])
def create_session():
    password = request.form['password']
    print(password)
    print(authentication())
    if password != authentication():
        return jsonify({"error": "Invalid password"})
    token = save_session()
    return jsonify({"session_token": token})


@app.route('/')
def form():
    session = session_params()
    if session:
        tree = Cohorts("github.csv")
        return render_template("contribution.html", tree=tree, coaches=tree.coaches())
    return render_template('new.html')


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
