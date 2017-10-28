import os

class BaseConfig(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SECRET_KEY = os.environ['SECRET_KEY']

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False
