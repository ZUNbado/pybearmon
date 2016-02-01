from flask import Flask, Blueprint,render_template, request, redirect, url_for
from app.common.sql import getdb
from app.common.forms import getFormForModelAttr
from .forms import CheckForm
from .controllers import Checks
from app.check_type.controllers import CheckType, CheckAttribute
from flask_menu import Menu, register_menu
from flask.ext.login import fresh_login_required
import urllib

from app.auth.utils import user_logged, user_admin
from app.check_type.controllers import CheckType, CheckAttribute

app = Blueprint('checks', __name__, url_prefix = '/checks')
@app.route('/')
@register_menu(app, '.checks.checks_list', 'List', visible_when=user_logged)
@register_menu(app, '.checks', 'Checks', visible_when=user_logged)
@fresh_login_required
def checks_list():
    checks = Checks().getAll()
    columns = [ 'name', 'check_type', 'status', 'last_checked', 'confirmations' ]
    return render_template('list.html', items = checks, columns = columns, endpoint = 'checks' )

@app.route('/edit', methods = [ 'POST', 'GET' ])
@app.route('/edit/<int:id>', methods = [ 'POST', 'GET' ])
@register_menu(app, '.checks.checks_edit', 'Add', visible_when=user_logged)
@fresh_login_required
def checks_edit(id = None):
    form = getFormForModelAttr(CheckForm, Checks, CheckAttribute, id, 'checktype_id')
    form.type.choices = CheckType().formList()
    if request.method == 'POST' and form.validate_on_submit():
        data = dict()
        for field in form:
            if field.id[:5] == 'attr_':
                data[field.id[5:]] = field.data
        data = urllib.urlencode(data)
        check = Checks().save(id = id, name = form.name.data, type = form.type.data, data = data, public = form.public.data, max_confirmations = form.max_confirmations.data)
        if check:
            return redirect(url_for('.checks_edit', id = check))
    return render_template('edit.html', form = form)


@app.route('/delete/<int:id>')
@fresh_login_required
def checks_delete(id):
    Checks().delete(id)
    return redirect(url_for('.checks_list'))
