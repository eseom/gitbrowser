import hashlib
import logging
import time

from flask import render_template, redirect, request, url_for, Blueprint, flash
from flask.ext.mail import Message
from flask_login import login_user, logout_user, current_user
from .forms import LoginForm, JoinForm
from ..models import db, User

auth = Blueprint('auth', __name__)

app = None
mail = None


@auth.record
def set_app(setup_state):
    global app, mail
    app = setup_state.app
    mail = app.extensions['mail']


@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('main.app'))
    form = LoginForm(request.form)
    error = None
    if request.method == 'POST':  # and form.validate():
        # return redirect(request.args.get("next") or url_for("main.app"))
        # username = form.username.data.lower().strip()
        # password = form.password.data
        username = request.form.get('email')
        password = request.form.get('password')

        user, authenticated = User.authenticate(username, password)
        if authenticated:
            login_user(user)
            return redirect(request.args.get("next") or url_for("main.app"))
        else:
            flash('Incorrect username or password. Try again.')
            return redirect(url_for('auth.signin'))

    return render_template('auth/signin.html', form=form, title='Sign in',
                           error=error)


@auth.route('/signout')
def signout():
    logout_user()
    return redirect(url_for('auth.signin'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    # if current_user.is_authenticated():
    #     return redirect(url_for('main.index'))

    form = JoinForm(request.form)
    if request.method == 'POST':  # and form.validate():
        email = form.email.data.lower().strip()

        # TODO validate email

        user = User.query.filter(User.username == email).first()
        if not user:
            user = User()
        user.username = email
        user.validation_code = hashlib.md5(
            str(int(round(time.time() * 1000))).encode('utf-8')).hexdigest()

        url = 'http://%s%s?code=%s' % (
            request.host, url_for('.signup_confirm'), user.validation_code)
        msg = Message('Flamengo confirmation instructions',
                      sender='flamengo@customdomain.com',
                      recipients=[email])
        msg.body = 'Welcome! You can confirm your account through the link: %s' % (
            url,)
        msg.html = ('<p>Welcome!</p>'
                    '<p>You can confirm your account through the link below:<br><a href="%s">%s</a></p>' % (
                        url, url,))
        try:
            mail.send(msg)
        except ConnectionRefusedError:
            logging.error('SMTP not respond')
            pass

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('auth.signup_introduction'))

    return render_template('auth/signup.html', form=form, title='Sign up')


@auth.route('/signup/introduction', methods=['GET'])
def signup_introduction():
    return render_template('auth/signup_introduction.html',
                           title='Confirmation instructions')


@auth.route('/signup/confirm', methods=['GET', 'POST'])
def signup_confirm():
    # @TODO validation
    code = request.args.get('code')
    user = User.query.filter(User.validation_code == code).first()
    if request.method == 'POST':
        user.password = request.form.get('password1')
        user.name = request.form.get('name')
        user.validation_code = ''
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.signup_done'))
    return render_template('auth/signup_confirm.html', email=user.username,
                           title='Confirm signup request')


@auth.route('/signup/done', methods=['GET'])
def signup_done():
    return render_template('auth/signup_done.html', title='Welcome')
