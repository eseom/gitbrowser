import json

from flask import url_for
from tests.base import TestCase, GitUtil


class MainViewTester(TestCase, GitUtil):
    def test_index_commits(self):
        take = 10
        rv = self.get_signed_client().get(
            url_for('main.commits', group='sample', repo='sample-repo',
                    branch='master', take=10, skip=0))
        self.ae(rv.status_code, 200)
        data = json.loads(rv.get_data(as_text=True))
        self.ae(len(data['commits']), 10)  # empty repository

    def test_index_tree(self):
        rv = self.get_signed_client().get(
            url_for('main.tree', group='sample', repo='sample-repo',
                    path='master/'))
        self.ae(rv.status_code, 200)
        data = json.loads(rv.get_data(as_text=True))
        self.ae(len(data['list']), 10)  # empty repository

    def test_index_commit(self):
        # show first commit
        rv = self.get_signed_client().get(
            url_for('main.commit', group='sample', repo='sample-repo',
                    hexsha='755fd577edcfd9209d0ac072eed3b022cbe4d39b'))
        self.ae(rv.status_code, 200)
        data = json.loads(rv.get_data(as_text=True))
        self.ae(data['parents'][0], '4b825dc642cb6eb9a060e54bf8d69288fbee4904')

        # show second commit
        # 32c273781bab599b955ce7c59d92c39bedf35db0 second comit
        # 755fd577edcfd9209d0ac072eed3b022cbe4d39b first comit
        rv = self.get_signed_client().get(
            url_for('main.commit', group='sample', repo='sample-repo',
                    hexsha='32c273781bab599b955ce7c59d92c39bedf35db0'))
        self.ae(rv.status_code, 200)
        data = json.loads(rv.get_data(as_text=True))
        self.ae(data['parents'][0], '755fd577edcfd9209d0ac072eed3b022cbe4d39b')

    def test_commit_count(self):
        rv = self.get_signed_client().get(
            url_for('main.commit_count', group='sample', repo='sample-repo',
                    path='master'))
        self.ae(rv.status_code, 200)
        data = json.loads(rv.get_data(as_text=True))
        self.ae(data['count'], 26)
