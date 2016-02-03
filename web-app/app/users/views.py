from flask import Flask, Blueprint,render_template, request, redirect, url_for
from app.common.sql import getdb
from app.common.forms import getFormForModel
from .forms import UserForm
from .controllers import Users
from flask_menu import Menu, register_menu

from app.auth.utils import user_admin


app = Blueprint('users', __name__, url_prefix = '/users')
@app.route('/')
@register_menu(app, '.admin.users.users_list', 'List', visible_when=user_admin)
@register_menu(app, '.admin.users', 'Users', visible_when=user_admin)
def users_list():
    users = Users().getAll()
    columns = [ 'name', 'email', 'is_active', 'is_admin' ]
    return render_template('list.html', items = users, columns = columns, endpoint = 'users' )

@app.route('/edit', methods = [ 'POST', 'GET' ])
@app.route('/edit/<int:id>', methods = [ 'POST', 'GET' ])
@register_menu(app, '.admin.users.users_edit', 'Add', visible_when=user_admin)
def users_edit(id = None):
    form = getFormForModel(UserForm, Users, id)
    if request.method == 'POST' and form.validate():
        user = dict(id = id, name = form.name.data, email = form.email.data)
        if form.password.data: user['password'] = form.password.data
        item = Users().save(**user)
        if item:
            return redirect(url_for('.users_edit', id = item))
    return render_template('edit.html', form = form)


@app.route('/delete/<int:id>')
def users_delete(id):
    Users().delete(id)
    return redirect(url_for('.users_list'))

