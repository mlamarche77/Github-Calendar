from flask import Flask, render_template, request, jsonify, session
from secrets import token_urlsafe
from github import GitHub, Cohorts
from pathlib import Path
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = "FkDAg7MUxxAuXe3WYICZwg"


def save_session():
    path = Path.cwd() / Path("static") / Path("sessions.json")
    if path.exists():
        with open(path, 'r') as r:
            sessions = json.load(r)
    else:
        sessions = {}
    time = datetime.now().strftime("%m/%d/%Y - %H:%M:%S")
    token = token_urlsafe(16)
    session['session_token'] = token
    sessions[token] = time
    with open(path, 'w') as w:
        json.dump(sessions, w)


def valid_session():
    path = Path.cwd() / Path("static") / Path("sessions.json")
    if 'session_token' not in session or not path.exists():
        return False
    with open(path, 'r') as r:
        return session['session_token'] in json.load(r)


def authenticate(password):
    path = Path.cwd() / Path("static") / Path("password.txt")
    if path.exists():
        with open(path, 'r') as r:
            return password == r.read()


@app.route('/session', methods=['POST'])
def create_session():
    if 'password' in request.form:
        if authenticate(request.form['password']):
            save_session()
            path = Path.cwd() / Path('static') / Path('github.csv')
            cohorts = Cohorts(path)
            return jsonify(cohorts.root)
    return jsonify({'error': "Invalid Password"})


@app.route('/')
def home():
    loggedin = valid_session()
    tree = loggedin and Cohorts('github.csv') or Cohorts()
    return render_template("contribution.html", tree=tree)



@app.route('/logout')
def logout():
    tree = Cohorts()
    del session['session_token']
    return render_template("contribution.html", tree=tree)




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
