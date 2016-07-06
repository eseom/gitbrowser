import json

from git import *
from tests.base import TestCase, GitUtil


class GitTester(TestCase, GitUtil):
    def test_git_repo(self):
        sample_repo = self.get_repo()
        self.at(isinstance(sample_repo, Repo))

    def test_blob(self):
        repo = self.get_repo()
        blob = repo.tree()['src']['Main.groovy']
        self.ae(621, len(json.dumps(blob.data_stream.read().decode('utf-8'))))
