"""
main views
"""

import base64
import difflib
from os import listdir, path as ospath

import pygments
from flask import Blueprint, current_app, jsonify, redirect, url_for, \
    request, Response
from flask.ext.login import current_user, login_required
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import guess_lexer_for_filename
from pygments.lexers.special import TextLexer
from . import git_http_backend
from .. import util
from ..models import User
from git import exc

main = Blueprint('main', __name__, static_folder='../static')


@main.route('/')
def index():
    if current_user.get_id():
        return redirect(url_for('main.app'))
    else:
        return redirect(url_for('auth.signin'))


@main.route('/app')
@login_required
def app():
    return main.send_static_file('web/app/app.html')


@main.route('/vendor/<path:path>')
def vendor(path):
    return main.send_static_file('web/app/vendor/%s' % path)


@main.route('/bower_components/<path:path>')
def bower_components(path):
    return main.send_static_file('web/app/bower_components/%s' % path)


@main.route('/css/<path:path>')
def css(path):
    return main.send_static_file('web/app/css/%s' % path)


@main.route('/js/<path:path>')
def js(path):
    return main.send_static_file('web/app/js/%s' % path)


@main.route('/html/<path:path>')
def html(path):
    return main.send_static_file('web/app/html/%s' % path)


@main.route('/show_debug')
def show_debug():
    return '<body></body>'


@main.route('/repos')
@main.route('/repos/<string:group>')
@util.login_required_restful
def repos(group=None):
    rpl = []
    repo_dir = current_app.config['REPO_DIR']
    if not group:
        for d in listdir(repo_dir):
            rpl.append(d)
    else:
        for d in listdir(ospath.join(repo_dir, group)):
            rpl.append(d)

    return jsonify(dict(repos=rpl))


@main.route(
    '/commits/<string:group>/<string:repo>/<path:branch>/<int:take>/<int:skip>')
@util.login_required_restful
def commits(group, repo, branch, take=10, skip=0):
    rp = util.get_repo(group, repo)
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


@main.route('/tree/<string:group>/<string:repo>/<path:path>')
@util.login_required_restful
def tree(group, repo, path=''):
    """
    :param group:
    :param repo:
    :param path: include the branch as prefix
    :return:
    """
    rp = util.get_repo(group, repo)
    # change head to the branch
    ref = util.select_branch(rp, path)
    try:
        rp.head.ref = ref
    except ValueError:  # select_branch return None
        # default master
        return jsonify(dict(list=[], current_branch='master', branches=['master']))

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
    return jsonify(dict(list=tblist, current_branch=branch, branches=branches))


@main.route('/commit/count/<string:group>/<string:repo>/<path:path>')
@util.login_required_restful
def commit_count(group, repo, path):
    rp = util.get_repo(group, repo)
    try:
        rp.head.ref = util.select_branch(rp, path)
        return jsonify(dict(count=rp.commit().count()))
    except ValueError:  # select_branch return None
        # default master
        return jsonify(dict(count=0))


@main.route('/blob/<string:group>/<string:repo>/<path:path>')
@util.login_required_restful
def blob(group, repo, path):
    rp = util.get_repo(group, repo)
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


@main.route('/commit/<string:group>/<string:repo>/<string:hexsha>')
@util.login_required_restful
def commit(group, repo, hexsha):
    rp = util.get_repo(group, repo)

    # get commit object
    commit = rp.commit(hexsha)
    parents = [str(p) for p in commit.parents]

    # get diff
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


def check_repo(e):
    repo_dir = current_app.config['REPO_DIR']
    environ = dict(request.environ)
    p = environ['PATH_INFO'].strip('/').split('/')

    try:
        path = ospath.join(repo_dir, p[0], p[1])
        if not ospath.exists(path):
            return e
    except IndexError:
        # not repository path_info
        return e

    authentication = request.headers.get(
        'Authorization', '').replace('Basic ', '')

    if not authentication:
        # @TODO classify browser request and git request more accurately
        if request.headers.get('User-Agent', '').startswith('git'):  # git
            return Response('', 401, {'WWW-Authenticate': 'Basic realm=""',})
        else:  # browser
            return redirect(url_for('main.app'))

    authorization = base64.b64decode(authentication).decode('utf-8')
    (username, password) = authorization.split(':', maxsplit=1)
    username = username.strip()

    user, authenticated = User.authenticate(username, password)
    if not authenticated:
        return Response('', 401)

    (status_line, headers, response_body_generator) = \
        git_http_backend.wsgi_to_git_http_backend(
            environ, ospath.join(repo_dir))
    response = Response(response_body_generator, status_line, headers)

    if response.status_code == 404:  # Request not supported
        # @TODO redirect with hash for angular
        return redirect(url_for('main.app'))
    return response
