from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def sa_serial(**kwargs):
    if kwargs.get('nullable') is None:
        kwargs['nullable'] = False
    kwargs['primary_key'] = True
    return db.Column(db.Integer, **kwargs)


def sa_unicode(length=256, **kwargs):
    if kwargs.get('default') is None:
        kwargs['default'] = ''
    if kwargs.get('nullable') is None:
        kwargs['nullable'] = False
    return db.Column(db.Unicode(length), **kwargs)


def sa_integer(*args, **kwargs):
    if kwargs.get('default') is None:
        kwargs['default'] = 0
    if kwargs.get('nullable') is None:
        kwargs['nullable'] = False
    return db.Column(db.Integer, *args, **kwargs)


def sa_boolean(**kwargs):
    if kwargs.get('default') is None:
        kwargs['default'] = False
    if kwargs.get('nullable') is None:
        kwargs['nullable'] = False
    return db.Column(db.Boolean, **kwargs)


def sa_text(**kwargs):
    if kwargs.get('default') is None:
        kwargs['default'] = ''
    if kwargs.get('nullable') is None:
        kwargs['nullable'] = False
    return db.Column(db.UnicodeText, **kwargs)


def sa_datetime(**kwargs):
    if kwargs.get('default') is None:
        kwargs['default'] = datetime.now
    if kwargs.get('nullable') is None:
        kwargs['nullable'] = False
    return db.Column(db.DateTime(timezone=True), **kwargs)


def insert_inserted_listener(mapper, connection, target):
    target.created_at = datetime.now()


def update_updated_listener(mapper, connection, target):
    target.updated_at = datetime.now()
