from flask import Flask, render_template
from flask_menu import Menu, register_menu
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

apps = [
        'app.checks',
        'app.auth',
        'app.users',
        'app.check_type',
        'app.contact_type',
        'app.contacts',
        'app.report',
        'app.admin',
        ]

for a in apps:
    try:
        ma = __import__(a, globals(), locals(), [ 'views' ], -1)
        app.register_blueprint(ma.views.app)
    except Exception, e:
        print 'App %s not found' % a
        print e
        ma = False

