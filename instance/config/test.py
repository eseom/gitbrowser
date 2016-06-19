DEBUG = True
SERVER_NAME = 'localhost'
SECRET_KEY = 'flamengo dev secret key'
SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
SQLALCHEMY_TRACK_MODIFICATIONS = False

OAUTH2_PROVIDER_TOKEN_EXPIRES_IN = 5

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

GIT_EXECUTABLE = '/usr/bin/git'
REPO_DIR = './instance'
