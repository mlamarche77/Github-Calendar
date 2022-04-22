from flask import Flask

app = Flask(__name__)
app.secret_key = "FkDAg7MUxxAuXe3WYICZwg"

from controllers import *


if __name__ == '__main__':
    app.run(host="0.0.0.0")
