from flask_restful import Resource, reqparse
from app.models import User
from app import db
class Register(Resource):
    """Register a user"""
    def __init__(self):
        self.reqparse=reqparse.RequestParser()
        self.reqparse.add_argument('username',type=str,
                                  required=True, help='Username required')
        self.reqparse.add_argument('email',type=str,
                                  required=True, help='Email required')                          
        self.reqparse.add_argument('password',type=str,
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

        # if User.query.filter_by(username=args['username']).first():
        #     response = {
        #         "status": "fail",
        #         "messege": "Username already exists"
        #     }
        #     return (response), 409
        
        new_user = User(username=args['username'], email=args['email'], password_hash=args['password'])
        # password = args['password']
        # new_user.password(password)
        new_user.save()

        response = {
                "status": "success",
                "messege": "User Registered"
            }
        
        return (response), 200
        


