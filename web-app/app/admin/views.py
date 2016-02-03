from flask import Flask, Blueprint,render_template, request, redirect, url_for
from flask_menu import Menu, register_menu
from flask.ext.login import fresh_login_required
from app.auth.utils import user_admin

from app.users.controllers import Users
from app.checks.controllers import Checks
from app.check_type.controllers import CheckType
from app.contact_type.controllers import ContactType


app = Blueprint('admin', __name__, url_prefix = '/admin')
@app.route('/')
@register_menu(app, '.admin', 'Admin', visible_when=user_admin)
@fresh_login_required
def admin_dash():
    return render_template('admin.html', users = Users().count(), checks = Checks().count(), contact_types = ContactType().count(), check_types = CheckType().count())
