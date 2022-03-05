from flask import Flask, render_template, request, jsonify
from github import GitHub, Cohorts
app = Flask(__name__)


@app.route('/')
def form():
    tree = Cohorts("static/github.csv")
    return render_template("contribution.html", tree=tree, coaches=tree.coaches())


@app.route('/contribution', methods=['POST', 'GET'])
def contribution():
    if request.method == "GET":
        username = request.values['username']
    elif request.method == "POST":
        username = request.form['username']
    else:
        return ""
    git = GitHub(username)
    git.fetch()
    return jsonify({
        "graph_image": git.graph,
        "url": git.url,
        "profile_image": git.profile_image,
        "username": git.username
    })


if __name__ == '__main__':
    app.run()
