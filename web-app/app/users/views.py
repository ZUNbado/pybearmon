from flask import Flask, Blueprint,render_template, request, redirect, url_for
from app.common.sql import getdb
from .forms import UserForm
from .controllers import Users
from flask_menu import Menu, register_menu


app = Blueprint('users', __name__, url_prefix = '/users')
@app.route('/')
@register_menu(app, '.users.users_list', 'List')
@register_menu(app, '.users', 'Users')
def users_list():
    users = Users().getAll()
    return render_template('users/list.html', items = users )

@app.route('/edit', methods = [ 'POST', 'GET' ])
@app.route('/edit/<int:id>', methods = [ 'POST', 'GET' ])
@register_menu(app, '.users.users_edit', 'Add')
def users_edit(id = None):
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
        check = Users().save(id = id, name = form.name.data, email = form.email.data, password = form.password.data)
        if check:
            return redirect(url_for('.users_edit', id = check))
    else:
        if id:
            dbcheck = Users().get(id)
            if dbcheck:
                form.name.data = dbcheck.name
                form.email.data = dbcheck.email
                form.password.data = dbcheck.password
    return render_template('users/edit.html', form = form)


@app.route('/delete/<int:id>')
def users_delete(id):
    return redirect(url_for('.users_list'))

