from flask import Flask, render_template
from flask_menu import Menu, register_menu
from common.sql import getdb
from flask.ext.login import LoginManager
from auth.utils import user_admin

app = Flask(__name__)
Menu(app=app)
login_manager = LoginManager(app)
login_manager.login_view = '/auth/login'
@login_manager.user_loader
def load_user(user_id):
    from app.users.controllers import LoginUser
    return LoginUser().get_by_id(user_id)

@app.route('/')
def index():
    db = getdb()
    list_checks = db.getAll('checks', '*', ['public = 1'], limit = [0 ,10])
    return render_template('index.html', checks = list_checks if list_checks else [] )

from app.checks.views import app as checks_view
app.register_blueprint(checks_view)

from app.users.views import app as users_view
app.register_blueprint(users_view)

from app.auth.views import app as auth_view
app.register_blueprint(auth_view)

from app.check_type.views import app as checktype_view
app.register_blueprint(checktype_view)

from app.contact_type.views import app as contacttype_view
app.register_blueprint(contacttype_view)

from app.contacts.views import app as contacts_view
app.register_blueprint(contacts_view)

from app.report.views import app as report_view
app.register_blueprint(report_view)

from app.admin.views import app as admin_view
app.register_blueprint(admin_view)

from app.integrations.telegram.views import app as tg_view
app.register_blueprint(tg_view)
