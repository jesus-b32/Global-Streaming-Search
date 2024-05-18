import os
# basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "it's a secret"
    #configuring a database named app.db located in the main directory of the application, which is stored in the basedir variable
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql:///global-streaming-search'
    # + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') or False
    SQLALCHEMY_ECHO = os.environ.get('SQLALCHEMY_ECHO') or False
    DEBUG_TB_INTERCEPT_REDIRECTS = os.environ.get('DEBUG_TB_INTERCEPT_REDIRECTS') or True
    DEBUG_TB_HOSTS = os.environ.get('DEBUG_TB_HOSTS') or 'dont-show-debug-toolbar'
    
    
    # 'postgresql:///global-streaming-search'