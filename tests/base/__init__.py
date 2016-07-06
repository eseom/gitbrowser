import os
import re
import unittest

from flamengo import create_app, db
from flask import url_for, current_app
from flask.ext.fixtures import load_fixtures
from git import Repo


class GitUtil(object):
    def get_repo(self):
        # sample repository is fork of
        #   https://github.com/githubtraining/hellogitworld
        return Repo(os.path.join(
            os.path.dirname(current_app.root_path),
            current_app.config['REPO_DIR'], 'sample', 'sample-repo'))


class Asserter(object):
    def ae(self, a, b):
        return self.assertEquals(a, b)

    def at(self, param):
        self.assertTrue(param)


class TestCase(unittest.TestCase, Asserter):
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

    def load_fixture_from_dict(self, db, fixtures):
        return load_fixtures(db, fixtures)

    def load_users(self):
        from tests.fixtures import users as fixtures_users
        self.load_fixture_from_dict(db, fixtures_users.dataset)

    def setUp(self):
        self.app = create_app('test')
        dir = os.path.dirname(os.path.realpath(__file__))
        self.app.config['REPO_DIR'] = '%s/../fixtures/repo' % (dir,)
        self.ctx = self.app.app_context()
        self.ctx.push()

        self.cookie_client = self.app.test_client(use_cookies=True)
        self.client = self.app.test_client()
        db.create_all()

        self.load_users()
        self.signed_client = None

    def tearDown(self):
        db.session.expunge_all()
        db.drop_all()
        self.ctx.pop()
