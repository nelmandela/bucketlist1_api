from datetime import timedelta
from werkzeug.security import check_password_hash
from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from app.models import User, Bucketlists, Item
from app import db


class Register(Resource):
    """Register a user"""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str,
                                   required=True, help='Username required')
        self.reqparse.add_argument('email', type=str,
                                   required=True, help='Email required')
        self.reqparse.add_argument('password', type=str,
                                   required=True, help='Password required')

        print ("\n------- WE ARE HERE-----")

    def post(self):
        args = self.reqparse.parse_args()

        if len(args['username']) == 0:
            response = {
                "status": "fail",
                "message": "Provide a username"
            }

            return (response), 400

        elif len(args['password']) < 8:
            response = {
                "status": "fail",
                "message": "Password must have atleast 8 characters"
            }

            return (response), 400

        if User.query.filter_by(username=args['username']).first():
            # to check if user with the given username exists
            response = {
                "status": "fail",
                "message": "Username already exists"
            }
            return (response), 409
        if User.query.filter_by(email=args['email']).first():
            # to check if user with the given username exists
            response = {
                "status": "fail",
                "message": "Email already exists"
            }
            return (response), 409

        new_user = User(
            username=args['username'], email=args['email'], password=args['password'])
        new_user.save()

        response = {
            "status": "success",
            "message": "User Registered"
        }

        return (response), 201


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
                expiration_time = timedelta(hours=24)
                token = create_access_token(identity=username,
                                            expires_delta=expiration_time)

                return {"status" : "success",
                        "message" : "Log in Successful",
                        "Authorization": token}, 200
            else:
                return {"message": "invalid username password combination"}, 401


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
                "status": "fail",
                "message": "Provide a bucketlist name"
            }

            return (response), 400
        elif not name.isalpha():
            response = {
                "status": "fail",
                "message": "Name should not have special characters"
            }
            return (response), 400
        if Bucketlists.query.filter_by(name=name).first():
            response = {
                "status": "fail",
                "message": "Bucketlist already exists"
            }
            return (response), 409
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        new_bucketlist = Bucketlists(name=args["name"], created_by=user.id)
        new_bucketlist.save()

        response = {
            "status": "success",
            "message": "Bucketlist created"
        }

        return (response), 201

    @jwt_required
    def get(self):
        # get page,limit & search
        page = request.args.get('page')
        limit = request.args.get('limit')
        search = request.args.get('q')
        bucket_data = []
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        bucketlist_paginate = None
        if search:
            bucketlist_paginate = Bucketlists.query.filter(
                Bucketlists.created_by == user.id, Bucketlists.name.like(search + "%")).paginate(page=int(page), per_page=limit)
        else:
            bucketlist_paginate = Bucketlists.query.filter(
                Bucketlists.created_by == user.id).paginate(page=page, per_page=limit)

        if bucketlist_paginate:
            for bucket in bucketlist_paginate.items:
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
    def put(self, id):

        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        bucket = Bucketlists.query.filter_by(id=id, created_by=user.id).first()
        if not bucket:
            response = {
                "status": "fail",
                "message": "Bucketlist not found"
            }
            return (response), 404
        args = self.reqparse.parse_args()
        name = args["name"]
        if not name:
            response = {
                "status": "fail",
                "message": "Provide a bucketlist name"
            }

            return (response), 400
        if Bucketlists.query.filter_by(name=name).first():
            response = {
                "status": "fail",
                "message": "Bucketlist already exists"
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

    @jwt_required
    def delete(self, id):
        """To delete a bucketlist"""
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        bucket = Bucketlists.query.filter_by(id=id, created_by=user.id).first()
        if not bucket:
            response = {
                "status": "fail",
                "message": "Bucketlist not found"
            }
            return (response), 404
        else:
            try:
                db.session.delete(bucket)
                db.session.commit()
                
                response = {
                    "status": "success",
                    "message": "Item deleted"
                }

                return (response), 200
            except Exception as error:
                return ({"error": "Bucketlist not found"}, 404)


class Items(Resource):
    """Adds CRUD functionality"""

    def __init__(self):
        """To initialize items endpoint arguments."""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str,
                                   help='name required', required=True)

    @jwt_required
    def post(self, id):
        args = self.reqparse.parse_args()
        name = args["name"]
        if not name:
            response = {
                "status": "fail",
                "message": "Provide an item name"
            }

            return (response), 400
        if Item.query.filter_by(name=name).first():
            response = {
                "status": "fail",
                "message": "Item already exists"
            }
            return (response), 409
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        new_item = Item(name=args["name"], bucketlist_id=id)
        new_item.save()

        response = {
            "status": "success",
            "message": "Item created"
        }

        return (response), 201

    @jwt_required
    def get(self, id):
        """fetch items,get page,limit & search"""
        limit = request.args.get('limit')
        page = request.args.get('page')
        print(request)
        search = request.args.get('q')        
        item_data = []
        #username = get_jwt_identity()
        #user = User.query.filter_by(username=username).first()
        item = Item.query.filter_by(bucketlist_id=id).all()
        item_paginate = None
        if search:
            item_paginate = Item.query.filter(
                Item.bucketlist_id == id, Item.name.like(search + "%")).paginate(page=page, per_page=limit)
        else:
            item_paginate = Item.query.filter(
                Item.bucketlist_id == id).paginate(page=page, per_page=limit)
        if item_paginate:
            for items in item_paginate.items:
                item_dict = {}
                item_dict['id'] = items.id
                item_dict['name'] = items.name
                item_dict['created_on'] = str(items.created_on)
                item_data.append(item_dict)

            return (item_data), 200

    @jwt_required
    def put(self, id, item_id):
        args = self.reqparse.parse_args()
        name = args["name"]
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        bucket = Bucketlists.query.filter_by(id=id, created_by=user.id).first()
        item = Item.query.filter_by(id=item_id, bucketlist_id=id).first()
        if not item:
            response = {
                "status": "fail",
                "message": "Item not found"
            }
            return (response), 404
        if not name:
            response = {
                "status": "fail",
                "message": "Provide an item name"
            }

            return (response), 400
        if item:
            # compare new name with existing one
            if name == item.name:
                response = {
                    "status": "fail",
                    "message": "Cannot update item with the same name."
                }
                return (response), 409
            item.name = name
            item.save()
            response = {
                "status": "success",
                "message": "Item updated",
                "data": {
                    "itemId": item.id,
                    "name": item.name
                }
            }

            return (response), 200

        response = {
            "status": "fail",
            "message": "Item not found"
        }
        return (response), 404

    @jwt_required
    def delete(self, id, item_id):
        """To delete an item"""
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        bucket = Bucketlists.query.filter_by(id=id, created_by=user.id).first()
        item = Item.query.filter_by(id=item_id, bucketlist_id=id).first()
        if not item:
            response = {
                "status": "fail",
                "message": "Item not found"
            }
            return (response), 404
        else:
            try:
                db.session.delete(item)
                db.session.commit()

                response = {
                    "status": "success",
                    "message": "Item deleted"
                }

                return (response), 200

            except Exception as error:
                return ({"error": "Item not found"}, 404)
