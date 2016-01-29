from flask import Flask, Blueprint,render_template, request, redirect, url_for
from app.common.sql import getdb
from .forms import CheckForm
from .controllers import Checks
from app.check_type.controllers import CheckType, CheckAttribute
from flask_menu import Menu, register_menu
from flask.ext.login import current_user
import wtforms

from app.auth.utils import user_logged, user_admin
from app.check_type.controllers import CheckType, CheckAttribute


app = Blueprint('checks', __name__, url_prefix = '/checks')
@app.route('/')
@register_menu(app, '.checks.checks_list', 'List', visible_when=user_logged)
@register_menu(app, '.checks', 'Checks', visible_when=user_logged)
def checks_list():
    checks = Checks().getAll()
    return render_template('checks/list.html', items = checks )

@app.route('/edit', methods = [ 'POST', 'GET' ])
@app.route('/edit/<int:id>', methods = [ 'POST', 'GET' ])
@register_menu(app, '.checks.checks_edit', 'Add', visible_when=user_logged)
def checks_edit(id = None):
    class CheckA(CheckForm):
        pass
    if id:
        check = Checks().get(id)
        attrs = CheckAttribute().getAll(checktype_id = check.type)
        for attr in attrs:
            setattr(CheckA, 'attr_%s' % attr.name, wtforms.TextField(attr.name))

    form = CheckA(request.form)
    form.type.choices = CheckType().formList()
    if request.method == 'POST' and form.validate():
        check = Checks().save(id = id, name = form.name.data, type = form.type.data)
        if check:
            return redirect(url_for('.checks_edit', id = check))
    else:
        if id:
            dbcheck = Checks().get(id)
            if dbcheck:
                form.name.data = dbcheck.name
                form.type.default = dbcheck.type
    return render_template('checks/edit.html', form = form)


@app.route('/delete/<int:id>')
def checks_delete(id):
    return redirect(url_for('.checks_list'))

