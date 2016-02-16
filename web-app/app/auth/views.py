from flask import Flask, flash, Blueprint, request, redirect, url_for, render_template
from flask.ext.login import login_required, login_user, current_user, logout_user
from app.users.controllers import Users, LoginUser
from .forms import LoginForm, RegisterForm

app = Blueprint('auth', __name__, url_prefix = '/auth')

@app.route('/login', methods = [ 'POST', 'GET' ])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = LoginUser(email = form.email.data, password = form.password.data)
        if user.is_authenticated:
            login_user(user)
            flash('Logged in successfully', 'success')
            return redirect(url_for('report.index'))
        else:
            flash('Credentials not valid', 'danger')
    return render_template('form.html', form = form)

@app.route('/register', methods = [ 'POST', 'GET' ])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        if Users().save(name = form.name.data, email = form.email.data, password = form.password.data, is_active = 1):
            user = LoginUser(email = form.email.data, password = form.password.data)
            if user.is_authenticated:
                login_user(user)
                return redirect(url_for('report.index'))
    return render_template('form.html', form = form)

@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('report.index'))
