# -*- coding: utf-8 -*-
from sources import lian, db, lm, openid
from flask_login import login_user, logout_user, login_required, current_user
from flask import render_template, flash, redirect, session, url_for, request, g
from sources.forms.auth import LoginForm
from sources.forms.edit_profile import EditProfileForm
from sources.models.users import User, ROLE_USER, ROLE_ADMIN
from datetime import datetime


# All actions before displaying the page
@lian.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


# Path to login page
@lian.route('/login', methods=['GET', 'POST'])
@openid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index.php'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return openid.try_login(form.open_id.data, ask_for=['nickname', 'email'])
    return render_template('/default/login.html',
                           title='Sign In',
                           form=form,
                           providers=lian.config['OPENID_PROVIDERS'])


# Authorization process
@openid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        username = resp.nickname
        if username is None or username == "":
            username = resp.email.split('@')[0]
        username = User.make_unique_username(username).lower()
        user = User(username=username, email=resp.email, role=ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index.php'))


# Load user
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


# Path to index page
@lian.route('/')
@lian.route('/index')
@login_required
def index():
    user = g.user
    posts = [  # список выдуманных постов
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("/default/index.html",
                           title='Home',
                           user=user,
                           posts=posts)


# Logout
@lian.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@lian.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User ' + username + ' not found.')
        return redirect(url_for('index'))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('/default/user.html',
                           user=user,
                           posts=posts,
                           )


@lian.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        g.user.username = form.username.data.lower()
        g.user.about = form.about.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.username.data = g.user.username
        form.about.data = g.user.about
    return render_template('/default/edit_profile.html',
                           form=form)


@lian.errorhandler(404)
def not_found_error(error):
    return render_template('/default/404.html'), 404


@lian.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('/default/500.html'), 500
