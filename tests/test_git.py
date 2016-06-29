import json
import os.path
import unittest

from flamengo import create_app
from flask import url_for
import git
from git import *


class Tester(unittest.TestCase):
    def ae(self, a, b):
        return self.assertEquals(a, b)

    def setUp(self):
        self.app = create_app('test')
        ctx = self.app.app_context()
        ctx.push()
        self.test_client = self.app.test_client()

    def test_git_repo(self):
        repo = Repo(os.path.join(self.app.instance_path, 'nginx'))

    def test_commit(self):
        take = 10
        rv = self.test_client.get(
            url_for('main.commits', repo_path='nginx', take=take, skip=0))
        self.ae(rv.status_code, 200)
        data = json.loads(rv.get_data(as_text=True))
        print(data['commits'])
        self.ae(len(data['commits']), take)

        print()

    def test_trees(self):
        rv = self.test_client.get(
            url_for('main.trees', repo_path='nginx', hexsha=1))
        self.ae(rv.status_code, 200)
        data = json.loads(rv.get_data(as_text=True))
        for i in data['list']:
            print(i)

    def test_blob(self):
        repo = Repo(os.path.join(self.app.instance_path, 'nginx'))

        main_tree = repo.tree()
        blob = main_tree['contrib']['README']
        for b in dir(blob):
            print(b)
        print(json.dumps(blob.data_stream.read().decode('utf-8')))

    def test_tree(self):
        repo = Repo(os.path.join(self.app.instance_path, 'nginx'))
        # commits
        # t = list(repo.iter_commits('master', max_count=1, skip=0))

        tree = repo.tree()

        for t in tree:
            print(git.repo.fun.to_commit(t))
            break
            for tt in dir(t):
                print(tt, getattr(t, tt))
            break

    def test_commit(self):
        rv = self.test_client.get(
            url_for('main.commit', repo_path='nginx',
                    hexsha='ab8504b937cdbae734fb2d971fba4eea0b157f43'))
        self.ae(rv.status_code, 200)
        data = json.loads(rv.get_data(as_text=True))
        print(data)

    def test_commit_count(self):
        rv = self.test_client.get(
            url_for('main.commit_count', repo_path='nginx'))
        self.ae(rv.status_code, 200)
        data = json.loads(rv.get_data(as_text=True))
        print(data)

    def test_excercise_tree(self):
        repo = Repo(os.path.join(self.app.instance_path, 'nginx'))
        for i in repo.tags:
            print(i)
            # tree = repo.heads.master.commit.tree
            # print(tree['core'])
            # print(len(tree.trees))
