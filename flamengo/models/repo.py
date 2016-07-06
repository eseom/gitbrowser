from sqlalchemy.orm import backref
from . import User
from .base import db, sa_unicode, sa_serial, sa_datetime, sa_integer, sa_text


def check_credential(credential):
    clist = []
    if credential & 1:
        clist.append('read')
    if credential & 2:
        clist.append('write')
    if credential & 4:
        clist.append('admin')


class Repo(db.Model):
    __tablename__ = 'repos'

    id = sa_serial()
    group = sa_unicode(256)
    name = sa_unicode(256)
    created_at = sa_datetime()
    updated_at = sa_datetime()
    type = sa_integer()
    description = sa_text()

    # relation
    repo_roles = db.relationship('RepoRole')

    def __repr__(self):
        return '<Repo: %s>' % (self.name,)


class RepoRole(db.Model):
    __tablename__ = 'repo_roles'

    id = sa_serial()
    repo_id = sa_integer(db.ForeignKey(Repo.id))
    user_id = sa_integer(db.ForeignKey(User.id))
    credential = sa_integer()

    # relation
    repo = db.relationship(
        'Repo', backref=backref('RepoRole', cascade="all, delete-orphan"))

    def get_credential(self):
        return self.check_credential(self.credential)

    def __repr__(self):
        return '<RepoRole: %s>' % (self.id,)
