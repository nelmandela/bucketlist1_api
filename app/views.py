from flask_restful import Resource, reqparse

from app.models import User, Bucketlists, Item
from werkzeug.security import check_password_hash
from app import db


class Register(Resource):
    """Register a user"""
    def __init__(self):
        self.reqparse=reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str,
                                   required=True, help='Username required')
        self.reqparse.add_argument('email', type=str,
                                   required=True, help='Email required')                          
        self.reqparse.add_argument('password', type=str,
                                   required=True, help='Password required')

    def post(self):
        args = self.reqparse.parse_args()

        if len(args['username']) == 0:
            response = {
                "status" : "fail",
                "message": "Provide a username"
            }

            return (response), 400

        elif len(args['password']) < 8:
            response = {
                "status": "fail",
                "message": "Password must have atleast 8 characters"
            }

            return (response), 400

        elif not (args['username']).isalpha():
            response = {
                "status": "fail",
                "messege": "Username should not have special characters"
            }
            return (response), 400

        if User.query.filter_by(username=args['username']).first():
            #to check if user with the given username exists
            response = {
                "status": "fail",
                "messege": "Username already exists"
            }
            return (response), 409
        if User.query.filter_by(email=args['email']).first():
            #to check if user with the given username exists
            response = {
                "status": "fail",
                "messege": "Email already exists"
            }
            return (response), 409

        new_user = User(username=args['username'], email=args['email'], password=args['password'])
        new_user.save()

        response = {
            "status": "success",
            "messege": "User Registered"
        }

        return (response), 200


class Login(Resource):
    """User sign in."""
    def __init__(self):
        """To add login endpoint arguments."""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str,
                                   help='Username required', required=True)
        self.reqparse.add_argument('password', type=str,
                                   help='Password required', required=True)

    def post(self):
        args = self.reqparse.parse_args()
        username = args["username"]
        password = args["password"]
        if not username or not password:
            return {'status': 'fail', 'message': 'username and password requied for login.'}, 400
        else:
            user = User.query.filter_by(username=args['username']).first()
            if user:
                return {"message": "success"}, 200
            else:
                return {"msg": "invalid username password combination"}, 401
