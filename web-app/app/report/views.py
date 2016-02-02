from flask import Flask, Blueprint,render_template, request, redirect, url_for, abort
from flask.ext.login import current_user
from app.checks.controllers import Checks
from app.users.controllers import Users

app = Blueprint('report', __name__)

@app.route('/', subdomain='<username>')
@app.route('/report', defaults = dict(username = None))
def public_list(username):
    public = True if username else False
    if not username and current_user.is_active():
        user = current_user.user
    else:
        user = Users().get_by_name(username)
    if not user: return redirect(url_for('index'))
    checks = Checks().getReport(user.id, public)
    return render_template('report/report.html', checks = checks )
