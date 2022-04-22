from __main__ import app
from flask import request, jsonify
from lib.github import GitHub


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
