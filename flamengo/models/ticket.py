from sqlalchemy import event
from .base import db, sa_unicode, sa_serial, sa_datetime, sa_text, sa_integer, \
    insert_inserted_listener, update_updated_listener
from .. import util


class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = sa_serial()
    repo_id = sa_integer(db.ForeignKey('repos.id'))
    summary = sa_unicode(256)
    content = sa_text()
    created_at = sa_datetime()
    updated_at = sa_datetime()
    user_id = sa_integer(db.ForeignKey('users.id'))

    user = db.relationship('User', backref='tickets')

    def to_dict(self, pretty_date=False):
        c = self.created_at
        u = self.updated_at
        if pretty_date:
            c = util.pretty_date(c)
            u = util.pretty_date(u)
        return dict(
            id=self.id,
            repo_id=self.repo_id,
            summary=self.summary,
            content=self.content,
            created_at=c,
            updated_at=u,
            user=self.user.to_dict(),
        )

    def __repr__(self):
        return '<Ticket: %s>' % (self.title,)

    __mapper_args__ = {
        "order_by": id.desc()
    }


event.listen(Ticket, 'before_insert', insert_inserted_listener, propagate=True)
event.listen(Ticket, 'before_update', update_updated_listener, propagate=True)
