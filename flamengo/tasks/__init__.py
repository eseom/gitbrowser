from flask.ext.celery import Celery

celery = Celery()

from .task import *