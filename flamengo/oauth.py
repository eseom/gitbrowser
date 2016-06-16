from datetime import datetime, timedelta

from flask import jsonify
from flask.ext.login import current_user
from flask.ext.oauthlib.provider import OAuth2Provider
from .models import Client, Grant, User, Token
from .models import db

oauth = OAuth2Provider()


@oauth.clientgetter
def load_user_client(client_id):
    return Client.query.filter_by(client_id=client_id).first()


@oauth.grantgetter
def load_user_grant(client_id, code):
    return Grant.query.filter_by(client_id=client_id, code=code).first()


def get_current_user():
    return User.query.get(current_user.id)


@oauth.grantsetter
def save_user_grant(client_id, code, request, *args, **kwargs):
    # decide the expires time yourself
    expires = datetime.utcnow() + timedelta(seconds=100)
    grant = Grant(
        client_id=client_id,
        code=code['code'],
        redirect_uri=request.redirect_uri,
        _scopes=' '.join(request.scopes),
        user_id=get_current_user().id,
        expires=expires
    )
    db.session.add(grant)
    db.session.commit()
    return grant


@oauth.tokengetter
def load_user_token(access_token=None, refresh_token=None):
    if access_token:
        tok = Token.query.filter_by(access_token=access_token).first()
        if tok and tok.user_id:
            tok.user = User.query.get(tok.user_id)
        return tok
    elif refresh_token:
        tok = Token.query.filter_by(refresh_token=refresh_token).first()
        if tok and tok.user_id:
            tok.user = User.query.get(tok.user_id)
        return tok


@oauth.tokensetter
def save_user_token(token, request, *args, **kwargs):
    expires_in = token.pop('expires_in') + 60 * 60
    expires = datetime.utcnow() + timedelta(seconds=expires_in)

    tok = Token(**token)
    tok.expires = expires
    tok.client_id = request.client.client_id

    if not request.user:
        tok.user_id = current_user.id
    else:
        tok.user_id = request.user.id

    db.session.add(tok)
    db.session.commit()
    return tok


@oauth.usergetter
def get_user(username, password, *args, **kwargs):
    user, authenticated = User.authenticate(username, password)
    if authenticated:
        return user
    return None


@oauth.invalid_response
def invalid_require_oauth(req):
    return jsonify(message=req.error_message), 401
