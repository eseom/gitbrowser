from flask import Flask
from flask.ext.cors import CORS
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from flask_debugtoolbar import DebugToolbarExtension
from .models import db, User
from .oauth import oauth
from .tasks import celery


def create_app(env='dev'):
    app = Flask(__name__, instance_relative_config=True)
    app.config['env'] = env
    if env == 'prod':
        app.config.from_pyfile('/etc/flamengo/config.py', silent=True)
    else:
        app.config.from_pyfile('config/%s.py' % env, silent=True)
    CORS(app)

    db.init_app(app)
    login_manager = LoginManager()
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth.signin'
    login_manager.init_app(app)

    @app.before_request
    def before_request():
        return

    @login_manager.user_loader
    def user_loader(user_id):
        return User.query.get(user_id)

    oauth.init_app(app)
    celery.init_app(app)
    Mail().init_app(app)
    DebugToolbarExtension(app)
    register_blueprint(app)
    return app


def register_blueprint(app):
    from .auth.views import auth
    from .repository.views import repository
    from .issue.views import issue
    from .main.views import main, serve_repository

    app.register_blueprint(main)
    app.register_blueprint(repository, url_prefix='/repositories')
    app.register_blueprint(issue, url_prefix='/issue')
    app.register_blueprint(auth, url_prefix='/auth')

    @app.errorhandler(404)
    def page_not_found(e):
        return serve_repository(e)
