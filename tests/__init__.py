import json
import unittest

from app import create_app
from app.models import db
from app.views import (Register, Login, Bucketlist, Items)
from config import app_configuration

class BaseTestCase(unittest.TestCase):
    """Test for API endpoints."""

    def create_app(self):
        app = create_app('testing')
        return app

    def setUp(self):
        """To declare test-wide variables."""

        self.app = self.create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        
        self.user_credentials = {
                                "username" : "nel",
                                 "email" : "nel@nel.com",
                                 "password" : "password123"
                                }
        self.user_credentials_2 = {
                                "username" : "mandela",
                                   "email" : "mandela@nel.com",
                                 "password" : "password123"
                                }
        self.bucketlist = {
                            "name" : "travel"
                          }
        self.item = {
                            "name" : "CapeTown"
                          }
        
        # register a user
        self.client.post('/api/v1/auth/register', data=self.user_credentials)
        self.client.post('/api/v1/auth/register', data=self.user_credentials_2)

        self.response = self.client.post('/api/v1/auth/login',
                                         data=self.user_credentials)
        self.response_2 = self.client.post('/api/v1/auth/login',
                                           data=self.user_credentials_2)
        self.response_data_in_json_format = json.loads(
            self.response.data.decode('utf-8'))

        self.response_data_in_json_format_2 = json.loads(
            self.response_2.data.decode('utf-8'))

        # get auth token
        self.token = (self.response_data_in_json_format['Authorization'])
        self.headers = {'Authorization': 'Bearer ' + self.token}

        # create bucketlist for first user
        self.client.post('/api/v1/bucketlists',
                         data=self.bucketlist,
                         headers=self.headers)

        # token for user 2
        self.token_2 = (self.response_data_in_json_format_2['Authorization'])
        self.headers_2 = {'Authorization': 'Bearer ' + self.token_2}

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


if __name__ == '__main__':
    unittest.main()