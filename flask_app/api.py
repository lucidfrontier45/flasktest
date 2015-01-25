__author__ = 'du'
from flask import request
from flask_restful import Resource
from sqlalchemy.orm.exc import NoResultFound
from . import model, app

db_session = model.db.session

class User(Resource):
    def get(self, name=None):
        if name == None:
            ret =  [u.to_dict() for u in db_session.query(model.User)]
            return {"code":200, "msg":"OK", "result":ret}
        else:
            try:
                u = db_session.query(model.User).filter_by(name=name).one()
                return {"code":200, "msg":"OK", "result":u.to_dict()}
            except NoResultFound as e:
                return {"code":404, "msg":"Not Found", "result":str(e)}

    def put(self, name=None):
        if not name:
            return {"code":400, "msg":"Bad Request"}
        data = request.form.get("data")
        app.logger.debug(data)

        try:
            u = db_session.query(model.User).filter_by(name=name).one()
            u.data = data
        except NoResultFound as e:
            app.logger.warn(str(e))
            u = model.User(name=name, data=data)
            db_session.add(u)

        db_session.commit()
        return {"code":200, "msg":"OK", "result":u.to_dict()}
