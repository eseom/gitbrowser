"""
main views
"""

import difflib
from os import listdir, path as ospath

import pygments
from flask import Blueprint, current_app, jsonify
from git import *
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import guess_lexer_for_filename
from pygments.lexers.special import TextLexer

main = Blueprint('main', __name__, static_folder='../static')


def pretty_date(time=False):
    """
    http://stackoverflow.com/questions/1551382/user-friendly-time-format-in-python
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    :type time: time object
    """
    from datetime import datetime
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(int(second_diff / 60)) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(int(second_diff / 3600)) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(int(day_diff / 7)) + " weeks ago"
    if day_diff < 365:
        return str(int(day_diff / 30)) + " months ago"
    return str(int(day_diff / 365)) + " years ago"


@main.route('/app')
def app():
    return main.send_static_file('web/app/index.html')


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
def repos(group=None):
    rpl = []
    repo_dir = ospath.join(current_app.config['REPO_DIR'], 'repo')
    if not group:
        for d in listdir(repo_dir):
            rpl.append(d)
    else:
        for d in listdir(ospath.join(repo_dir, group)):
            rpl.append(d)

    return jsonify(dict(repos=rpl))


@main.route(
    '/commits/<string:group>/<string:repo>/<string:branch>/<int:take>/<int:skip>')
def commits(group, repo, branch, take=10, skip=0):
    rp = get_repo(group, repo)
    commits = list([dict(
        hexsha=l.hexsha,
        message=l.message,
        committer=str(l.committer) + ' <' + l.committer.email + '>',
        committed_date=pretty_date(l.committed_date)
    ) for l in rp.iter_commits(branch, max_count=take, skip=skip)])
    return jsonify(dict(result=True, commits=commits))


@main.route('/tree/<string:group>/<string:repo>/<string:branch>/')
@main.route(
    '/tree/<string:group>/<string:repo>/<string:branch>/<path:path>')
def tree(group, repo, branch='master', path=''):
    rp = get_repo(group, repo)
    tree = rp.tree()

    if path:
        for p in path.split('/'):
            tree = tree[p]

    tblist = []
    for t in tree.trees:
        commit = None
        # TODO cache point
        for c in rp.iter_commits('master', paths=t.path, max_count=1, skip=0):
            commit = c
        tblist.append(dict(name=t.name, type='tree', commit=dict(
            hexsha=commit.hexsha,
            message=commit.message,
            date=pretty_date(commit.committed_date)
        )))
    for t in tree.blobs:
        commit = None
        # TODO cache point
        for c in rp.iter_commits('master', paths=t.path, max_count=1, skip=0):
            commit = c
        tblist.append(dict(name=t.name, type='blob', commit=dict(
            hexsha=commit.hexsha,
            message=commit.message,
            date=pretty_date(commit.committed_date)
        )))
    return jsonify(dict(list=tblist))


@main.route('/commit/count/<string:group>/<string:repo>/<string:branch>')
def commit_count(group, repo, branch):
    rp = get_repo(group, repo)
    return jsonify(dict(count=rp.commit().count()))


def get_repo(group, repo):
    return Repo(
        ospath.join(current_app.config['REPO_DIR'], 'repo', group, repo))


@main.route('/blob/<string:group>/<string:repo>/<string:branch>/<path:path>')
def blob(group, repo, branch, path):
    rp = get_repo(group, repo)
    tree = rp.tree()

    if path:
        for p in path.split('/'):
            tree = tree[p]

    blob_name = tree.name
    blob_content = tree.data_stream.read().decode('utf-8')

    # monkey patching
    from pygments.lexers.configs import NginxConfLexer
    NginxConfLexer.filenames = ['nginx.conf']

    # set lexer
    try:
        lexer = guess_lexer_for_filename(blob_name, blob_content)
    except pygments.util.ClassNotFound:
        lexer = TextLexer()

    # stripnl option for lexer
    lexer.stripnl = False

    blob_content = highlight(blob_content, lexer, HtmlFormatter(
        linenos='inline',
        style='colorful'))

    return jsonify(dict(blob_content=blob_content))


@main.route('/commit/<string:group>/<string:repo>/<string:hexsha>')
def commit(group, repo, hexsha):
    rp = get_repo(group, repo)

    # get commit object
    commit = rp.commit(hexsha)
    parents = [str(p) for p in commit.parents]

    # get diff
    diffs = commit.diff(parents[0])
    diff_contents = []
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

    return jsonify(dict(
        commit=dict(
            message=commit.message,
            committer=str(
                commit.committer) + ' <' + commit.committer.email + '>',
            committed_date=pretty_date(commit.committed_date)
        ),
        diff_contents=diff_contents,
        parents=parents,
    ))
