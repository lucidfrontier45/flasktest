__author__ = 'du'

from flask_script import Manager
from flask_app.application import app

manager = Manager(app)

manager.run()
