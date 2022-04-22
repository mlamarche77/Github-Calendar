from flask import Flask

app = Flask(__name__)
app.secret_key = "FkDAg7MUxxAuXe3WYICZwg"


from controllers import home
from controllers import contribution
from controllers import upload
from controllers import authenticated
from controllers import updates
from controllers import create_session


if __name__ == '__main__':
    app.run(host="0.0.0.0")

