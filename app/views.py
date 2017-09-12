from datetime import timedelta
from werkzeug.security import check_password_hash
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.models import User, Bucketlists, Item
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
                expiration_time = timedelta(hours=3)
                token = create_access_token(identity=username,
                                    expires_delta=expiration_time)
                                    
                return {"Authorization": token}, 200
            else:
                return {"msg": "invalid username password combination"}, 401

class Bucketlist(Resource):
    """Adds CRUD functionality"""
    def __init__(self):
        """To initialize bucketlists endpoint arguments."""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str,
                                   help='name required', required=True)
    @jwt_required
    def post(self):
        args = self.reqparse.parse_args()
        name = args["name"]
        if not name:
            response = {
                "status" : "fail",
                "message": "Provide a bucketlist name"
            }

            return (response), 400
        elif not name.isalpha():
            response = {
                "status": "fail",
                "messege": "Name should not have special characters"
            }
            return (response), 400
        if Bucketlists.query.filter_by(name=name).first():
            response = {
                "status": "fail",
                "messege": "Bucketlist already exists"
            }
            return (response), 409
        username= get_jwt_identity()
        user=User.query.filter_by(username=username).first()
        new_bucketlist = Bucketlists(name=args["name"],created_by=user.id)
        print("************** here *******************",new_bucketlist )
        new_bucketlist.save()

        response = {
            "status": "success",
            "messege": "Bucketlist created"
        }

        return (response), 200
    @jwt_required
    def get(self):
        bucket_data = []
        username= get_jwt_identity()
        user=User.query.filter_by(username=username).first()
        print(user.id)
        bucketlist = Bucketlists.query.filter_by(created_by=user.id).all()
        print("here",bucketlist)
        if bucketlist:
            for bucket in bucketlist:
                bucket = {
                    "bucketlistId": bucket.id,
                    "name": bucket.name,
                    "created_on": str(bucket.created_on)
                }
            bucket_data.append(bucket)

            response = {
                "status": "success",
                "bucketlist": bucket_data
            }
            return (response), 200
        else:
            response = {
                "status": "success",
                "bucketlist": bucket_data
            }
            return (response), 200
    @jwt_required
    def put(self,id):
        args = self.reqparse.parse_args()
        name = args["name"]
        if not name:
            response = {
                "status" : "fail",
                "message": "Provide a bucketlist name"
            }

            return (response), 400
        # elif not name.isalpha():
        #     response = {
        #         "status": "fail",
        #         "messege": "Name should not have special characters"
        #     }
        #     return (response), 400
        if Bucketlists.query.filter_by(name=name).first():
            response = {
                "status": "fail",
                "messege": "Bucketlist already exists"
            }
            return (response), 409
        bucketlist = Bucketlists.query.filter_by(id=id).first()
        bucketlist.name = name
        db.session.add(bucketlist)
        db.session.commit()

        response = {
            "status": "success",
            "message": "Bucketlist updated",
            "data": {
                "bucketlistId": bucketlist.id,
                "name": bucketlist.name
            }
        }

        return (response), 200