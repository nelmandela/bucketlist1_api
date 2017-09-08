from flask import Flask
from flask_migrate import Migrate

from config import app_configuration
from .models import db


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True, static_folder=None)
    app.config.from_object(app_configuration[config_name])

    db.init_app(app)
    migrate = Migrate(app, db)

    return app
