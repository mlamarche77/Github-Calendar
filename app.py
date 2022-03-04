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
    return jsonify({"src": git.contribution})


if __name__ == '__main__':
    app.run()
