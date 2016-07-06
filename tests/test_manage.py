import json

from flask import url_for
from tests.base import TestCase


class ManageTester(TestCase):
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
        # data = json.loads(rv.get_data(as_text=True))

        # delete
        rv = self.get_signed_client().delete(
            url_for('manage.repo_delete'),
            data=json.dumps(dict(group='group1', name='name1'))
        )
        self.ae(rv.status_code, 200)
