from flask import Flask, Blueprint,render_template, request, redirect, url_for
from app.common.sql import getdb
from .forms import CheckForm
from .controllers import Checks
from flask_menu import Menu, register_menu


app = Blueprint('checks', __name__, url_prefix = '/checks')
@app.route('/')
@register_menu(app, '.checks.checks_list', 'List')
@register_menu(app, '.checks', 'Checks')
def checks_list():
    checks = Checks().getAll()
    return render_template('checks/list.html', items = checks )

@app.route('/edit', methods = [ 'POST', 'GET' ])
@app.route('/edit/<int:id>', methods = [ 'POST', 'GET' ])
@register_menu(app, '.checks.checks_edit', 'Add')
def checks_edit(id = None):
    form = CheckForm(request.form)
    if request.method == 'POST' and form.validate():
        check = Checks().save(id = id, name = form.name.data, type = form.type.data, data = form.data.data)
        if check:
            return redirect(url_for('.checks_edit', id = check))
    else:
        if id:
            dbcheck = Checks().get(id)
            if dbcheck:
                form.name.data = dbcheck.name
                form.type.data = dbcheck.type
                form.data.data = dbcheck.data
    return render_template('checks/edit.html', form = form)


@app.route('/delete/<int:id>')
def checks_delete(id):
    return redirect(url_for('.checks_list'))

