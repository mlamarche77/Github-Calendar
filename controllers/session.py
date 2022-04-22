from __main__ import app
from flask import request, jsonify
from lib.github import Cohorts
from lib.config import is_password
from pathlib import Path


@app.route('/session', methods=['POST'])
def create_session():
    if 'password' in request.form:
        if is_password(request.form['password']):
            path = Path.cwd() / Path('static') / Path('github.csv')
            cohorts = Cohorts(path)
            return jsonify({'root': cohorts.root, 'students': cohorts.students})
    return jsonify({'error': "Invalid Password"})



@app.route('/authenticated', methods=['POST'])
def authenticated():
    return jsonify({'authenticated': is_password(request.form['password'])})

