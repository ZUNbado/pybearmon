from flask import Flask, Blueprint,render_template, request, redirect, url_for
from app.common.sql import getdb
from .forms import CheckForm, AttributeForm
from .controllers import CheckType, CheckAttribute
from flask_menu import Menu, register_menu
from flask.ext.login import current_user

from app.auth.utils import user_admin


app = Blueprint('checks_type', __name__, url_prefix = '/checks_type')
@app.route('/')
@register_menu(app, '.checkstype.checktype_list', 'List', visible_when=user_admin)
@register_menu(app, '.checkstype.', 'Check Types', visible_when=user_admin)
def checktype_list():
    checks = CheckType().getAll()
    return render_template('checktype/list.html', items = checks )

@app.route('/edit', methods = [ 'POST', 'GET' ])
@app.route('/edit/<int:id>', methods = [ 'POST', 'GET' ])
@register_menu(app, '.checkstype.checktype_edit', 'Add', visible_when=user_admin)
def checktype_edit(id = None):
    form = CheckForm(request.form)
    if request.method == 'POST' and form.validate():
        check = CheckType().save(id = id, name = form.name.data)
        if check:
            return redirect(url_for('.checks_edit', id = check))
    else:
        if id:
            dbcheck = CheckType().get(id)
            if dbcheck:
                form.name.data = dbcheck.name
    if id:
        attrs = CheckAttribute().getAll(checktype_id = id)
    else:
        attrs = list()
    return render_template('checktype/edit.html', form = form, attrs = attrs, id = id)


@app.route('/delete/<int:id>')
def checktype_delete(id):
    return redirect(url_for('.checktype_list'))


@app.route('/edit/<int:checktype_id>/attribute', methods = [ 'POST', 'GET' ])
@app.route('/edit/<int:checktype_id>/attribute/<int:id>', methods = [ 'POST', 'GET' ])
def checkattribute_edit(checktype_id, id = None):
    form = AttributeForm(request.form)
    if request.method == 'POST' and form.validate():
        pass
    return render_template('checktype/attribute_edit.html', form = form)
