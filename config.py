import os
from os.path import join, dirname


class Config(object):
    """Production configurations."""

    BASE_DIR = dirname(__file__)
    DEBUG = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Development(Config):
    """Development configurations."""
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ.get("SECRET_KEY")


class Testing(Config):
    """Testing configurations."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + Config.BASE_DIR \
                              + "/tests/test_db.sqlite"
    SECRET_KEY = os.environ.get('SECRET_KEY')


app_configuration = {
    'production': Config,
    'development': Development,
    'testing': Testing
}
