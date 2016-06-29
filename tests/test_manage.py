import json
import re

from flask import url_for
from tests.base import TestCase


class Tester(TestCase):
    def get_signed_client(self):
        if self.signed_client:
            return self.signed_client

        cookie_client = self.app.test_client(use_cookies=True)
        rv = cookie_client.post(url_for('auth.signin'), data=dict(
            email='sample@test.com',
            password='secret'))
        match = re.match(r'session=(.*?);', rv.headers['Set-Cookie'])
        cookie = match.group(1)

        cookie_client.set_cookie('localhost', 'session', cookie)
        self.signed_client = cookie_client
        return self.signed_client

    def test_create_delete_repo(self):
        # create
        rv = self.get_signed_client().post(
            url_for('manage.repo_create'),
            data=json.dumps(dict(
                group='group1',
                name='name1',
                type=1,
                description=''))
        )
        self.ae(rv.status_code, 200)

        # list
        rv = self.get_signed_client().get(url_for('manage.repos'))
        self.ae(rv.status_code, 200)
        data = json.loads(rv.get_data(as_text=True))
        print(data)

        # delete
        rv = self.get_signed_client().delete(
            url_for('manage.repo_delete'),
            data=json.dumps(dict(group='group1', name='name1'))
        )
        self.ae(rv.status_code, 200)
