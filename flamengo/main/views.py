"""
main views
"""

import base64
from os import path as ospath

from avatar_generator import Avatar as TextAvatar
from flask import Blueprint, current_app, redirect, url_for, \
    request, Response
from flask import make_response
from flask.ext.login import current_user, login_required
from . import git_http_backend
from ..models import User

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
    return main.send_static_file('web/src/app.html')


@main.route('/vendor/<path:path>')
def vendor(path):
    return main.send_static_file('web/src/vendor/%s' % path)


@main.route('/bower_components/<path:path>')
def bower_components(path):
    return main.send_static_file('web/src/bower_components/%s' % path)


@main.route('/css/<path:path>')
def css(path):
    return main.send_static_file('web/src/css/%s' % path)


@main.route('/js/<path:path>')
def js(path):
    return main.send_static_file('web/src/js/%s' % path)


@main.route('/html/<path:path>')
def html(path):
    return main.send_static_file('web/src/html/%s' % path)


@main.route('/show_debug')
def show_debug():
    return '<body></body>'


@main.route("/profile/image")
@main.route("/profile/image/<string:email>")
def photo(email=None):
    if not email:
        email = current_user.username
    avatar = TextAvatar.generate(128, email)
    headers = {'Content-Type': 'image/png'}
    return make_response(avatar, 200, headers)


def serve_repository(e):
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
            return Response('', 401, {'WWW-Authenticate': 'Basic realm=""', })
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
