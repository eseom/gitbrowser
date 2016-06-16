import os
from celery.bin.celery import main as celery_main
from flamengo import create_app
from flamengo.tasks import task


def parse_options():
    env = os.environ.get('ENV')
    return 'prod' if env == 'prod' else 'dev'


def run():
    task  # alive import
    app = create_app(parse_options())
    celery_args = ['celery', 'worker', '-B', '-s', '/tmp/celery.db',
                   '--concurrency=5', '--loglevel', 'INFO']
    with app.app_context():
        return celery_main(celery_args)
