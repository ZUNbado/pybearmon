from flask import Flask, Blueprint,render_template, request, redirect, url_for
from app.common.sql import getdb
from app.common.forms import getFormForModel
from .forms import CheckForm, AttributeForm
from .controllers import CheckType, CheckAttribute
from flask_menu import Menu, register_menu
from flask.ext.login import fresh_login_required

from app.auth.utils import user_admin


app = Blueprint('checks_type', __name__, url_prefix = '/checks_type')
@app.route('/')
@register_menu(app, '.admin.checkstype.checktype_list', 'List', visible_when=user_admin)
@register_menu(app, '.admin.checkstype.', 'Check Types', visible_when=user_admin)
@fresh_login_required
def checktype_list():
    checks = CheckType().getAll()
    columns = [ 'name' ]
    return render_template('list.html', items = checks, columns = columns, endpoint = 'checktype' )

@app.route('/edit', methods = [ 'POST', 'GET' ])
@app.route('/edit/<int:id>', methods = [ 'POST', 'GET' ])
@register_menu(app, '.admin.checkstype.checktype_edit', 'Add', visible_when=user_admin)
@fresh_login_required
def checktype_edit(id = None):
    form = getFormForModel(CheckForm, CheckType, id)
    if request.method == 'POST' and form.validate():
        check = CheckType().save(id = id, name = form.name.data)
        if check:
            return redirect(url_for('.checktype_edit', id = check))
    if id:
        attrs = CheckAttribute().getAll(checktype_id = id)
    else:
        attrs = list()
    return render_template('checktype/edit.html', form = form, attrs = attrs, id = id)


@app.route('/delete/<int:id>')
@fresh_login_required
def checktype_delete(id):
    CheckType().delete(id)
    return redirect(url_for('.checktype_list'))

@app.route('/delete/<int:checktype_id>/attribute/<int:id>')
@fresh_login_required
def checkattribute_delete(checktype_id, id):
    CheckAttribute().delete(id)
    return redirect(url_for('.checktype_edit', id = checktype_id))

@app.route('/edit/<int:checktype_id>/attribute', methods = [ 'POST', 'GET' ])
@app.route('/edit/<int:checktype_id>/attribute/<int:id>', methods = [ 'POST', 'GET' ])
@fresh_login_required
def checkattribute_edit(checktype_id, id = None):
    form = getFormForModel(AttributeForm, CheckAttribute, id)
    if request.method == 'POST' and form.validate():
        attr = CheckAttribute().save(id = id, id_check_type = checktype_id, name = form.name.data, type = form.type.data, required = form.required.data)
        if attr:
            return redirect(url_for('.checktype_edit', id = checktype_id))
    return render_template('edit.html', form = form)
