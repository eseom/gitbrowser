import json

from flask import url_for
from tests.base import TestCase


class RepositoryTester(TestCase):
    def test_create_delete_repository(self):
        # create
        rv = self.get_signed_client().post(
            url_for('repository.create'),
            data=json.dumps(dict(
                group='group1',
                name='name1',
                type=1,
                description=''))
        )
        self.ae(rv.status_code, 200)

        # index
        rv = self.get_signed_client().get(url_for('repository.index'))
        self.ae(rv.status_code, 200)

        # repositories 요청 dict 키 화인
        data = json.loads(rv.get_data(as_text=True))
        self.assertListEqual(list(data['repos']['group1'][0].keys()),
                             ['id', 'name', 'description'])

        # destroy
        rv = self.get_signed_client().delete(
            url_for('repository.destroy', id=1))
        self.ae(rv.status_code, 200)

    def test_index_commits(self):
        take = 10
        rv = self.get_signed_client().get(
            url_for('repository.commits',
                    group='sample',
                    name='sample-repo',
                    branch='master',
                    take=take,
                    skip=0))
        self.ae(rv.status_code, 200)
        data = json.loads(rv.get_data(as_text=True))
        self.ae(len(data['commits']), 10)  # empty repository

    def test_index_tree(self):
        rv = self.get_signed_client().get(
            url_for('repository.trees',
                    group='sample',
                    name='sample-repo',
                    path='master/'))
        self.ae(rv.status_code, 200)
        data = json.loads(rv.get_data(as_text=True))
        self.ae(len(data['list']), 10)  # empty repository

    def test_index_commit(self):
        # show first commit
        rv = self.get_signed_client().get(
            url_for('repository.commit',
                    group='sample',
                    name='sample-repo',
                    hexsha='755fd577edcfd9209d0ac072eed3b022cbe4d39b'))
        self.ae(rv.status_code, 200)
        data = json.loads(rv.get_data(as_text=True))
        self.ae(data['parents'][0], '4b825dc642cb6eb9a060e54bf8d69288fbee4904')

        # show second commit
        # 32c273781bab599b955ce7c59d92c39bedf35db0 second comit
        # 755fd577edcfd9209d0ac072eed3b022cbe4d39b first comit
        rv = self.get_signed_client().get(
            url_for('repository.commit',
                    group='sample',
                    name='sample-repo',
                    hexsha='32c273781bab599b955ce7c59d92c39bedf35db0'))
        self.ae(rv.status_code, 200)
        data = json.loads(rv.get_data(as_text=True))
        self.ae(data['parents'][0], '755fd577edcfd9209d0ac072eed3b022cbe4d39b')

    def test_commit_count(self):
        rv = self.get_signed_client().get(
            url_for('repository.commit_count',
                    group='sample',
                    name='sample-repo',
                    path='master'))
        self.ae(rv.status_code, 200)
        data = json.loads(rv.get_data(as_text=True))
        self.ae(data['count'], 26)
