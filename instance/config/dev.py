DEBUG = True
SECRET_KEY = 'flamengo dev secret key'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/flamengo.database'

DEBUG_TB_INTERCEPT_REDIRECTS = False

OAUTH2_PROVIDER_TOKEN_EXPIRES_IN = 3600

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

REPO_DIR = './instance'
