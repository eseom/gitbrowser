"""
unittest of repository view
"""

import json

from flamengo.models import Ticket
from flask import url_for
from tests.base import TestCase


class IssueTester(TestCase):
    def test_tickets(self):
        # list
        self.load_users()
        self.load_repos_fixture()
        self.load_tickets_fixture()

        rv = self.get_signed_client().get(
            url_for('issue.index', rgroup='samplegroup', rname='samplename'))
        self.ae(rv.status_code, 200)
        data = json.loads(rv.get_data(as_text=True))
        self.ae(len(data['tickets']), 1)
        self.ae(data['tickets'][0]['id'], 1)
        self.ae(data['tickets'][0]['repo_id'], 1)
        self.ae(data['tickets'][0]['user']['id'], 1)

        # insert
        rv = self.get_signed_client().post(
            url_for('issue.create', rgroup='samplegroup', rname='samplename'),
            data=json.dumps(dict(
                summary='summary2',
                content='content2'
            )))
        self.ae(rv.status_code, 200)
        self.ae(Ticket.query.count(), 2)

        # check list order
        rv = self.get_signed_client().get(
            url_for('issue.index', rgroup='samplegroup', rname='samplename'))
        data = json.loads(rv.get_data(as_text=True))
        self.ae(data['tickets'][0]['id'], 2)
        self.ae(data['tickets'][1]['id'], 1)

        # update
        rv = self.get_signed_client().put(
            url_for('issue.update', id=2), data=json.dumps(dict(
                summary='summary_updated',
                content='content3'
            )))
        self.ae(rv.status_code, 200)
        self.ae(Ticket.query.get(2).summary, 'summary_updated')
        self.ae(Ticket.query.get(2).repo_id, 1)
        self.ae(Ticket.query.get(1).repo_id, 1)

        # delete
        rv = self.get_signed_client().delete(url_for('issue.destroy', id=2))
        self.ae(rv.status_code, 200)
        self.assertIsNone(Ticket.query.get(2))
