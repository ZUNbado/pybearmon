from flask import Flask, flash, Blueprint, request, redirect, url_for, render_template
from flask.ext.menu import Menu, register_menu
from flask.ext.login import login_required, login_user, current_user, logout_user

from .utils import user_logged, user_anonymous

from app.users.controllers import Users, LoginUser
from .forms import LoginForm, RegisterForm


app = Blueprint('auth', __name__, url_prefix = '/auth')


@app.route('/login', methods = [ 'POST', 'GET' ])
@register_menu(app, '.login', 'Login', visible_when=user_anonymous)
def login():
    if current_user.is_active: return redirect(url_for('index'))

    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = LoginUser(email = form.email.data, password = form.password.data)
        if user.is_authenticated:
            login_user(user)
            flash('Logged in successfully')
            return redirect(url_for('index'))
        else:
            flash('Credentials not valid')
    return render_template('auth/login.html', form = form)

@app.route('/register', methods = [ 'POST', 'GET' ])
@register_menu(app, '.register', 'Register', visible_when=user_anonymous)
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        if Users().save(name = form.name.data, email = form.email.data, password = form.password.data, is_active = 1):
            user = LoginUser(email = form.email.data, password = form.password.data)
            if user.is_authenticated:
                login_user(user)
                return redirect(url_for('index'))
    return render_template('edit.html', form = form)

@app.route('/logout')
@register_menu(app, '.logout', 'Logout', visible_when=user_logged)
def logout():
    logout_user()
    return redirect(url_for('index'))
