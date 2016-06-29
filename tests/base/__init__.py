import os
import unittest

from flamengo import create_app, db
from flask.ext.fixtures import load_fixtures


class TestCase(unittest.TestCase):
    def load_fixture_from_dict(self, db, fixtures):
        return load_fixtures(db, fixtures)

    def ae(self, a, b):
        return self.assertEquals(a, b)

    def load_users(self):
        from tests.fixtures import users as fixtures_users
        self.load_fixture_from_dict(db, fixtures_users.dataset)

    def setUp(self):
        self.app = create_app('test')
        dir = os.path.dirname(os.path.realpath(__file__))
        self.app.config['REPO_DIR'] = '%s/../fixtures/repo' % (dir,)
        ctx = self.app.app_context()
        ctx.push()

        self.cookie_client = self.app.test_client(use_cookies=True)
        self.client = self.app.test_client()
        db.create_all()

        self.load_users()

        self.signed_client = None
