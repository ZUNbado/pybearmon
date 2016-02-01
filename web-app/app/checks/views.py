from flask import Flask, Blueprint,render_template, request, redirect, url_for
from app.common.sql import getdb
from .forms import CheckForm
from .controllers import Checks
from app.check_type.controllers import CheckType, CheckAttribute
from flask_menu import Menu, register_menu
from flask.ext.login import fresh_login_required
import wtforms
import urllib
import urlparse

from app.auth.utils import user_logged, user_admin
from app.check_type.controllers import CheckType, CheckAttribute

app = Blueprint('checks', __name__, url_prefix = '/checks')
@app.route('/')
@register_menu(app, '.checks.checks_list', 'List', visible_when=user_logged)
@register_menu(app, '.checks', 'Checks', visible_when=user_logged)
@fresh_login_required
def checks_list():
    checks = Checks().getAll()
    return render_template('checks/list.html', items = checks )

@app.route('/edit', methods = [ 'POST', 'GET' ])
@app.route('/edit/<int:id>', methods = [ 'POST', 'GET' ])
@register_menu(app, '.checks.checks_edit', 'Add', visible_when=user_logged)
@fresh_login_required
def checks_edit(id = None):
    class CheckA(CheckForm):
        pass
    if id:
        check = Checks().get(id)
        data = urlparse.parse_qs(check.data)
        attrs = CheckAttribute().getAll(checktype_id = check.type)
        for attr in attrs:
            value = data[attr.name][0] if attr.name in data else ''
            validators = []
            if attr.required: validators.append(wtforms.validators.Required())
            field = getattr(wtforms, attr.type)(attr.name, default = value, validators = validators)
            setattr(CheckA, 'attr_%s' % attr.name, field)


    form = CheckA(request.form)
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
    else:
        if id:
            dbcheck = Checks().get(id)
            if dbcheck:
                form.type.default = dbcheck.type
                form.process()
                form.name.data = dbcheck.name
                form.public.data = dbcheck.public
                form.max_confirmations.data = dbcheck.max_confirmations
    return render_template('checks/edit.html', form = form)


@app.route('/delete/<int:id>')
@fresh_login_required
def checks_delete(id):
    Checks().delete(id)
    return redirect(url_for('.checks_list'))
