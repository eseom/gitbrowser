"""
manage views
"""

import json
import os
from os import listdir, path as ospath

from flask import Blueprint, current_app, jsonify, request
from flask.ext.login import current_user
from git import Repo as GitRepo
from .. import util
from ..models import Repo, db, RepoRole

manage = Blueprint('manage', __name__, static_folder='../static')


def check_listable(repo, user):
    return False


@manage.route('/repos')
@util.login_required_restful
def manage_repos():
    repos = {}
    groups = []

    # username: nickname@domain.com
    nickname = current_user.username.split('@')[0]

    # no own directory
    repo_dir = ospath.join(current_app.config['REPO_DIR'], nickname)
    if not ospath.exists(repo_dir):
        os.mkdir(repo_dir)

    # query repo_roles
    repo_roles = RepoRole.query.filter(
        RepoRole.user_id == current_user.id).all()

    for r in repo_roles:
        if r.repo.group not in groups:
            groups.append(r.repo.group)
        try:
            repos[r.repo.group].append(r.repo.name)
        except KeyError:
            repos[r.repo.group] = [r.repo.name]

    if not len(groups):
        groups = [nickname]
        repos[nickname] = []

    return jsonify(dict(groups=groups, repos=repos))


@manage.route('/repo/create', methods=['POST'])
@util.login_required_restful
def repo_create():
    data = json.loads(request.data.decode('utf-8'))

    # temporary
    data['type'] = 'public'

    # repo dir
    GitRepo.init(ospath.join(
        current_app.config['REPO_DIR'], data['group'], data['name']), bare=True)

    # repo model
    repo = Repo(
        group=data['group'],
        name=data['name'],
        type=data['type'],
        description=data['description'],
        repo_roles=[
            RepoRole(user_id=current_user.id)
        ]
    )

    db.session.add(repo)
    db.session.commit()

    return jsonify(dict(result=True))


@manage.route('/repo/delete', methods=['DELETE'])
@util.login_required_restful
def repo_delete():
    data = json.loads(request.data.decode('utf-8'))

    # repo dir
    # TODO defered remove
    # TODO remove the group
    import shutil
    shutil.rmtree(ospath.join(current_app.config['REPO_DIR'], data['group'],
                              data['name']))

    # repo model
    repo = Repo.query.filter(
        Repo.group == data['group']
    ).filter(
        Repo.name == data['name']
    ).first()
    db.session.delete(repo)
    db.session.commit()

    return jsonify(dict(result=True))
