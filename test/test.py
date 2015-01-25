from flask_app import application
import unittest
import logging
import json
import uuid

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

def make_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    return logger


class FlaskTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.app = application.app
        self.app.config["TESTING"] = True
        self.logger = make_logger(self.__class__.__name__)

    def setUp(self):
        self.client = self.app.test_client()

    def test_index(self):
        r = self.client.get("/")
        self.logger.debug("code={0}, data={1}".format(r.status_code, r.data))
        assert r.status_code == 200

    def test_user_model(self):
        model = application.model
        u = model.User(name="Tom", data="hoge")
        assert str(u) == "User[None,Tom,hoge]"


    def test_put_user(self):
        r = self.client.put("/user/")
        assert r.status_code == 200
        data = json.loads(r.data)
        assert data["code"] == 400

        name = str(uuid.uuid4())

        r = self.client.put("/user/{0}/".format(name), data={"data":"fuga2"})
        assert r.status_code == 200
        data = json.loads(r.data)
        assert data["code"] == 200
        assert data["result"]["data"] == "fuga2"

        r = self.client.put("/user/{0}/".format(name), data={"data":"fuga2"})
        self.logger.info(r.status_code)
        assert r.status_code == 200
        data = json.loads(r.data)
        assert data["code"] == 200
        assert data["result"]["data"] == "fuga2"

    def test_get_user(self):
        r = self.client.get("/user/")
        assert r.status_code == 200
        data = json.loads(r.data)
        assert data["code"] == 200
        assert isinstance(data["result"], list)

        self.client.put("/user/tom/", data={"data":"test"})
        r = self.client.get("/user/tom/")
        self.logger.info(r.status_code)
        assert r.status_code == 200
        data = json.loads(r.data)
        self.logger.info(data)
        assert data["code"] == 200

        r = self.client.get("/user/tom2/")
        assert r.status_code == 200
        data = json.loads(r.data)
        assert data["code"] == 404


if __name__ == "__main__":
    unittest.main()