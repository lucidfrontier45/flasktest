__author__ = 'du'

from . import app
import flask_sqlalchemy
from sqlalchemy import Column, Integer, Text
db = flask_sqlalchemy.SQLAlchemy(app)

class User(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    data = Column(Text)

    def __repr__(self):
        return "User[{0.id},{0.name},{0.data}]".format(self)

    def to_dict(self):
        return {"id":self.id, "name":self.name, "data":self.data}

db.create_all()