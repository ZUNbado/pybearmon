from flask import Flask, Blueprint,render_template, request, redirect, url_for, abort
from flask.ext.login import current_user
from app.checks.controllers import Checks
from app.users.controllers import Users

app = Blueprint('report', __name__)

@app.route('/', subdomain='<username>')
@app.route('/report', defaults = dict(username = None))
def public_list(username):
    public = True if username else False
    user = Users().get_by_name(username)

    if not user: return redirect(url_for('index'))

    if current_user.is_active() and current_user.id = user.id:
        public = False

    checks = Checks().getReport(user.id, public)
    return render_template('report/report.html', checks = checks )
