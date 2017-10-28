import os

class BaseConfig(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
<<<<<<< HEAD
    # SECRET_KEY = os.environ['SECRET_KEY']
=======
    SECRET_KEY = os.environ['SECRET_KEY']
>>>>>>> b885cf43980a516867086f6acfdd7104dc26e64d

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False
