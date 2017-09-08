from flask import Blueprint
from flask_restful import Api

from app.views import Register

bluePrint = Blueprint('buck_api', __name__)

buck_api = Api(bluePrint)

buck_api.add_resource(Register, '/api/v1/register')