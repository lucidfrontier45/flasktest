from flask_restful import Api
import logging

from . import app, model, api

app.logger.setLevel(logging.DEBUG)
db_session = model.db.session


@app.route('/')
def hello_world():
    app.logger.debug("hello")
    return 'Hello World!'


rest_api = Api(app)
rest_api.add_resource(api.User, "/user/", "/user/<name>/")

