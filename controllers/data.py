from __main__ import app
from flask import request, jsonify
from lib.config import latest_updates, save_update
from pathlib import Path


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