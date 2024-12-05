import logging

import connexion
from flask_testing import TestCase
from openapi_server.__main__ import create_app  
from openapi_server.DAL.database import db

class BaseTestCase(TestCase):

    def create_app(self):
        connexion_app, flask_app = create_app()

        return flask_app

    def setUp(self):
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()