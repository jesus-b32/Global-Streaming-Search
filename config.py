import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    """Set Flask configuration from .env file.
    """
    #General Config
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # set this to 'False,' otherwise an obnoxious warning appears every time you run your app reminding you that this option takes a lot of system resources.
    SQLALCHEMY_ECHO = False # When set to 'True', Flask-SQLAlchemy will log all database activity to Python's stderr for debugging purposes.
    
    #FLask debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False # makes redirect explicit, which can be useful for dubugging. I generally find it annoying so I turn it off
    # DEBUG_TB_HOSTS = 'dont-show-debug-toolbar'