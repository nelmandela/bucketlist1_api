import os
from os.path import join, dirname

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)




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
    SECRET_KEY = os.environ.get('SECRET_KEY')

class Testing(Config):
    """Testing configurations."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + Config.BASE_DIR \
                              + "/tests/test_db.sqlite"

app_configuration = {
    'production': Config,
    'development': Development,
    'testing': Testing
}
