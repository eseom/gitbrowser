import base64
import hashlib
from datetime import datetime

from sqlalchemy import event
from sqlalchemy.orm import relationship, synonym
from .base import db, sa_unicode, sa_serial, sa_boolean, sa_datetime, \
    insert_inserted_listener, update_updated_listener


def _get_encrypted_password(password):
    sha = hashlib.sha512()
    sha.update(password.encode('utf-8'))
    return '{SHA512}%s' % base64.b64encode(sha.digest()).decode('utf-8')


class User(db.Model):
    __tablename__ = 'users'

    id = sa_serial()
    username = sa_unicode(255)
    nickname = sa_unicode(255, default='')
    name = sa_unicode(255, default='')
    _password = sa_unicode(255, default='')
    _is_active = sa_boolean(default=False)
    created_at = sa_datetime()
    updated_at = sa_datetime()
    validation_code = sa_unicode(255)

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = _get_encrypted_password(password)

    password_descriptor = property(_get_password, _set_password)
    password = synonym('_password', descriptor=password_descriptor)

    def check_password(self, password):
        if not self.password:
            return False
        return self.password == _get_encrypted_password(password)

    @classmethod
    def authenticate(cls, email, password):
        user = User.query.filter(User.username == email).first()
        if user is None:
            return None, False
        return user, user.check_password(password)

    def is_authenticated(self):
        return True

    def get_id(self):
        return self.id

    def is_active(self):
        return self._is_active

    def to_dict(self):
        return dict(
            id=self.id,
            username=self.username,
            nickname=self.nickname,
            name=self.name,
            created_at=self.created_at,
            is_active=self._is_active,
        )

    def __repr__(self):
        return '<User: %s>' % (self.username,)


event.listen(User, 'before_insert', insert_inserted_listener, propagate=True)
event.listen(User, 'before_update', update_updated_listener, propagate=True)


class Alias(db.Model):
    __tablename__ = 'aliases'

    id = db.Column(db.Integer, primary_key=True)

    alias = db.Column(db.Unicode(256), nullable=False)
    email = db.Column(db.Unicode(256), nullable=False)


class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(40))

    # human readable description, not required
    description = db.Column(db.Unicode(400))

    # creator of the client, not required
    user_id = db.Column(db.Unicode(200))

    client_id = db.Column(db.Unicode(40), unique=True)
    client_secret = db.Column(db.Unicode(55), index=True, nullable=False)

    # public or confidential
    is_confidential = db.Column(db.Boolean)

    redirect_uris_text = db.Column(db.UnicodeText)
    default_scopes_text = db.Column(db.UnicodeText)

    @property
    def client_type(self):
        if self.is_confidential:
            return 'confidential'
        return 'public'

    @property
    def redirect_uris(self):
        if self.redirect_uris_text:
            return self.redirect_uris_text.split()
        return ['']

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self.default_scopes_text:
            return self.default_scopes_text.split()
        return []

    def __repr__(self):
        return '<{self.__class__.__name__}: {self.id}>'.format(self=self)


class Grant(db.Model):
    __tablename__ = 'grants'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False, )
    client_id = db.Column(db.Unicode(40), db.ForeignKey(Client.client_id),
                          nullable=False, )
    code = db.Column(db.Unicode(255), index=True, nullable=False)
    redirect_uri = db.Column(db.Unicode(255))
    expires = db.Column(db.DateTime)
    _scopes = db.Column(db.UnicodeText)

    user = relationship('User', backref="Grant")
    client = relationship('Client', backref="Grant")

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []


class Token(db.Model):
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(
        db.Unicode(40),
        db.ForeignKey(Client.client_id),
        nullable=False,
    )
    client = relationship('Client')

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(User.id),
        nullable=False, )
    user = relationship('User')

    # currently only bearer is supported
    token_type = db.Column(db.Unicode(40))

    access_token = db.Column(db.Unicode(255), unique=True)
    refresh_token = db.Column(db.Unicode(255), unique=True)
    expires = db.Column(db.DateTime)
    _scopes = db.Column(db.UnicodeText)

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []

    def _get_scope(self):
        if self._scopes:
            return self._scopes.split()
        return []

    def _set_scope(self, scope):
        if scope:
            scope = scope
        self._scopes = scope

    scope_descriptor = property(_get_scope, _set_scope)
    scope = synonym('_scopes', descriptor=scope_descriptor)

    def __repr__(self):
        return '<{self.__class__.__name__}: {self.id}>'.format(self=self)
