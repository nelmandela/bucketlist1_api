from flask import Blueprint
from flask_restful import Api

from app.views import Register, Login

blue_print = Blueprint('bucket_api', __name__)

bucket_api = Api(blue_print)

bucket_api.add_resource(Register, '/api/v1/auth/register')
bucket_api.add_resource(Login, '/api/v1/auth/login')