from flask import Flask
from flask_migrate import Migrate

from config import app_configuration
from .models import db
from  app.endpoints import blue_print

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True, static_folder=None)
    app.config.from_object(app_configuration[config_name])
    app.register_blueprint(blue_print)
    db.init_app(app)
    migrate = Migrate(app, db)

    return app
