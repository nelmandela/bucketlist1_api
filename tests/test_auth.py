import json
from tests import BaseTestCase


class AuthRTestCase(BaseTestCase):
    """Test for authorization"""

    def test_user_registration(self):
        """Test creation of users"""
        user_credentials = {
                                "username" : "mbaka",
                                 "email" : "mbaka@nel.com",
                                 "password" : "password123"
                                }
        response = self.client.post('/api/v1/auth/register', data= user_credentials,
                                    headers=self.headers)
        response_msg = json.loads(response.data.decode('utf8'))
        self.assertIn(response_msg['message'],"User Registered")
        self.assertEqual(response.status_code, 201)

    def test_already_user_registration(self):
        """Test creation of users"""
        response = self.client.post('/api/v1/auth/register', data= self.user_credentials,
                                    headers=self.headers)
        response_msg = json.loads(response.data.decode('utf8'))
        self.assertIn(response_msg['message'],"Username already exists")
        self.assertEqual(response.status_code, 409)

    def test_registration_empty_name(self):
        """Test registration with an empty name"""
        user_credentials = {
                                "username" : "",
                                 "email" : "mbaka@nel.com",
                                 "password" : "password123"
                                }
        response = self.client.post('/api/v1/auth/register', data= user_credentials,
                                    headers=self.headers)
        response_msg = json.loads(response.data.decode('utf8'))
        self.assertIn(response_msg['message'],"Provide a username")
        self.assertEqual(response.status_code, 400)

    def test_invalid_password_registration(self):
        """Test creation of users"""
        user_credentials = {
                                "username" : "mbaka",
                                 "email" : "mbaka@nel.com",
                                 "password" : "pass"
                                }
        response = self.client.post('/api/v1/auth/register', data= user_credentials,
                                    headers=self.headers)
        response_msg = json.loads(response.data.decode('utf8'))
        self.assertIn(response_msg['message'],"Password must have atleast 8 characters")
        self.assertEqual(response.status_code, 400)

    def test_existing_email_registration(self):
            """Test registering with existing email"""
            user_credentials = {
                                "username" : "andela",
                                "email" : "mandela@nel.com",
                                "password" : "password123"
                                    }
            response = self.client.post('/api/v1/auth/register', data= user_credentials,
                                        headers=self.headers)
            response_msg = json.loads(response.data.decode('utf8'))
            self.assertIn(response_msg['message'],"Email already exists")
            self.assertEqual(response.status_code, 409)

    def test_user_login(self):
        """Test login successful"""
        response = self.client.post('/api/v1/auth/login',
                                         data=self.user_credentials)
        response_msg = json.loads(response.data.decode('utf8'))
        self.assertIn(response_msg['message'],"Log in Successful")
        self.assertEqual(response.status_code, 200)

    def test_invalid_credentials(self):
        """Test login using invalid credentials"""
        user_credentials = {
                            "username" : "nelson",
                            "password" : "password123"
                            }
        response = self.client.post('/api/v1/auth/login',
                                         data=user_credentials)
        response_msg = json.loads(response.data.decode('utf8'))
        self.assertIn(response_msg['message'],"invalid username password combination")
        self.assertEqual(response.status_code, 401)
