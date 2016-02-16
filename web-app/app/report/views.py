from flask import Flask, Blueprint,render_template, request, redirect, url_for, abort
from flask.ext.login import current_user
from flask.ext.menu import register_menu
from app.checks.controllers import Checks
from app.users.controllers import Users
from app.auth.utils import user_logged

app = Blueprint('report', __name__)

@app.route('/', subdomain='<username>')
@app.route('/report', defaults = dict(username = None))
@register_menu(app, '.report', 'Reports', visible_when=user_logged)
def public_list(username):
    public = True if username else False
    user = Users().get_by_name(username)

    if current_user.is_authenticated:
        if not username:
            user = current_user.user
        if int(current_user.get_id()) == int(user.id):
            public = False
            user = current_user.user
        else:
            public = True

    if not user: return redirect(url_for('index'))

    checks = Checks().getReport(user.id, public)
    return render_template('report/report.html', checks = checks )


@app.route('/')
def index():
    list_checks = Checks().filter(public = 1, user_id = 1)
    return render_template('index.html', checks = list_checks if list_checks else [] )
