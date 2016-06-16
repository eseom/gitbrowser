import logging
from datetime import datetime

from . import celery


@celery.task
def keephouse():
    logging.warning('keep house: %s', datetime.now())
