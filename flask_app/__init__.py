__author__ = 'du'

import flask
import os

app = flask.Flask(__name__)
dir = os.path.dirname(os.path.dirname(__file__))
db_path = os.path.join(dir, "test.db")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

app.config.from_object("config")