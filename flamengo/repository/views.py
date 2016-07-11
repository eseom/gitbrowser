"""
repository views
"""

import difflib
import json
import os
import shutil
from os import path as ospath

import git
import pygments
from flask import Blueprint, current_app, jsonify, request, make_response
from flask.ext.login import current_user
from git import Repo as GitRepo
from git import exc
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import guess_lexer_for_filename
from pygments.lexers.special import TextLexer
from .. import util
from ..models import Repo, db, RepoRole

repository = Blueprint('repository', __name__, static_folder='../static')


@repository.route('', methods=['GET'])
@util.login_required_restful
def index():
    repos = {}
    groups = []

    # no nickname
    if current_user.nickname == '':
        return make_response('', 301)

    nickname = current_user.nickname

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

        current_repo = dict(
            id=r.repo.id,
            name=r.repo.name,
            description=r.repo.description,
        )
        try:
            repos[r.repo.group].append(current_repo)
        except KeyError:
            repos[r.repo.group] = [current_repo]

    if not len(groups):
        groups = [nickname]
        repos[nickname] = []

    return jsonify(dict(groups=groups, repos=repos))


@repository.route('', methods=['POST'])
@util.login_required_restful
def create():
    form = json.loads(request.data.decode('utf-8'))

    # temporary
    form['type'] = 'public'

    # repo dir
    GitRepo.init(ospath.join(
        current_app.config['REPO_DIR'], form['group'], form['name']), bare=True)

    # repo model
    repo = Repo(
        group=form['group'],
        name=form['name'],
        type=form['type'],
        description=form.get('description', ''),
        repo_roles=[
            RepoRole(user_id=current_user.id)
        ]
    )

    db.session.add(repo)
    db.session.commit()

    return jsonify(dict(result=True))


@repository.route('/<int:id>', methods=['DELETE'])
@util.login_required_restful
def destroy(id):
    repo = Repo.query.get(id)

    # repo dir
    # TODO defered remove
    # TODO remove the group
    shutil.rmtree(
        ospath.join(current_app.config['REPO_DIR'], repo.group, repo.name))

    # delete repo model
    db.session.delete(repo)
    db.session.commit()

    return jsonify(dict(result=True))


@repository.route('/commit/count/<string:group>/<string:name>/<path:path>')
@util.login_required_restful
def commit_count(group, name, path):
    rp = util.get_repo(group, name)
    try:
        rp.head.ref = util.select_branch(rp, path)
        return jsonify(dict(count=rp.commit().count()))
    except ValueError:  # select_branch return None
        # default master
        return jsonify(dict(count=0))


@repository.route(
    '/commits/<string:group>/<string:name>/<path:branch>/<int:take>/<int:skip>')
@util.login_required_restful
def commits(group, name, branch, take=10, skip=0):
    rp = util.get_repo(group, name)
    try:
        commits = list([dict(
            hexsha=l.hexsha,
            message=l.message,
            committer=str(l.committer) + ' <' + l.committer.email + '>',
            committed_date=util.pretty_date(l.committed_date)
        ) for l in rp.iter_commits(branch, max_count=take, skip=skip)])
    except exc.GitCommandError:  # no commits
        commits = []
    branches = [str(h) for h in rp.heads]
    return jsonify(dict(result=True, commits=commits, branches=branches))


@repository.route('/trees/<string:group>/<string:name>/<path:path>')
@util.login_required_restful
def trees(group, name, path=''):
    """
    :param group:
    :param name:
    :param path: include the branch as prefix
    :return:
    """
    rp = util.get_repo(group, name)

    # get branch
    branch = path.split('/')[0]

    # get last commit
    try:
        commit = next(rp.iter_commits(branch, max_count=1))
        last_commit = dict(
            hexsha=commit.hexsha,
            message=commit.message,
            email=commit.committer.email,
            committer=str(
                commit.committer) + ' <' + commit.committer.email + '>',
            committed_date=util.pretty_date(commit.committed_date)
        )
    except git.exc.GitCommandError:  # no commit and branch
        last_commit = None
        pass

    # change head to the branch
    ref = util.select_branch(rp, branch)
    try:
        rp.head.ref = ref
    except ValueError:  # select_branch return None
        # default master
        return jsonify(
            dict(list=[], current_branch='master', branches=['master']))

    path = path.replace(ref.name, '').strip('/')
    branch = ref.name
    tree = rp.tree()
    branches = [str(h) for h in rp.heads]

    if path and path != '/':  # ignore trailing slash
        for p in path.split('/'):
            tree = tree[p]

    tblist = []
    for t in tree.trees:
        commit = None
        # TODO cache point
        for c in rp.iter_commits(branch, paths=t.path, max_count=1, skip=0):
            commit = c
        tblist.append(dict(name=t.name, type='tree', commit=dict(
            hexsha=commit.hexsha,
            message=commit.message,
            date=util.pretty_date(commit.committed_date)
        )))
    for t in tree.blobs:
        commit = None
        # TODO cache point
        for c in rp.iter_commits(branch, paths=t.path, max_count=1, skip=0):
            commit = c
        tblist.append(dict(name=t.name, type='blob', commit=dict(
            hexsha=commit.hexsha,
            message=commit.message,
            date=util.pretty_date(commit.committed_date)
        )))
    return jsonify(dict(list=tblist, current_branch=branch, branches=branches,
                        last_commit=last_commit))


@repository.route('/commit/<string:group>/<string:name>/<string:hexsha>')
@util.login_required_restful
def commit(group, name, hexsha):
    rp = util.get_repo(group, name)

    # get commit object
    commit = rp.commit(hexsha)
    parents = [str(p) for p in commit.parents]

    # get diff
    # empty_tree=$(git hash-object -t tree /dev/null)
    # git diff-tree -p ${empty_tree} $MY_COMMIT [${files}...]
    if len(parents) == 0:
        parents = ['4b825dc642cb6eb9a060e54bf8d69288fbee4904']
    diffs = commit.diff(parents[0])
    diff_contents = []
    count = 0
    truncated = False
    for diff in diffs:
        try:
            b_content = diff.b_blob.data_stream.read().decode('utf-8').split(
                '\n')
            b_path = '/%s' % diff.b_blob.path
        except:
            b_content = ''
            b_path = ''
        try:
            a_content = diff.a_blob.data_stream.read().decode('utf-8').split(
                '\n')
            a_path = '/%s' % diff.a_blob.path
        except:
            a_content = ''
            a_path = ''

        opcodes = difflib.SequenceMatcher(
            None, b_content, a_content).get_opcodes()
        diff_contents.append(
            dict(baseTextLines=b_content, newTextLines=a_content,
                 opcodes=opcodes, baseTextName=b_path, newTextName=a_path))
        count += 1
        if count > 20:
            truncated = True
            break

    return jsonify(dict(
        truncated=truncated,
        count_of_diffs=len(diffs),
        commit=dict(
            message=commit.message,
            committer=str(
                commit.committer) + ' <' + commit.committer.email + '>',
            committed_date=util.pretty_date(commit.committed_date)
        ),
        diff_contents=diff_contents,
        parents=parents,
    ))


@repository.route('/blob/<string:group>/<string:name>/<path:path>')
@util.login_required_restful
def blob(group, name, path):
    rp = util.get_repo(group, name)
    ref = util.select_branch(rp, path)
    branch = ref.name
    path = path.replace(ref.name, '').strip('/')
    tree = rp.tree()

    if path:
        for p in path.split('/'):
            tree = tree[p]

    blob_name = tree.name
    blob_content = tree.data_stream.read().decode('utf-8')

    # monkey patching
    from pygments.lexers.configs import NginxConfLexer
    from pygments.lexers.html import HtmlLexer
    NginxConfLexer.filenames = ['nginx.conf']
    HtmlLexer.filenames += ['*.ejs']

    # set lexer
    try:
        lexer = guess_lexer_for_filename(blob_name, blob_content)
    except pygments.util.ClassNotFound:
        lexer = TextLexer()

    # stripnl option for lexer
    lexer.stripnl = False

    blob_content = highlight(blob_content, lexer, HtmlFormatter(
        linenos='table',
        style='colorful'))

    return jsonify(dict(blob_content=blob_content, path=path, branch=branch))
