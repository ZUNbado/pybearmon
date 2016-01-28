from flask import Flask, render_template
from flask_menu import Menu, register_menu
from common.sql import getdb

app = Flask(__name__)
Menu(app=app)

from app.checks.views import app as checks_view
app.register_blueprint(checks_view)
from app.users.views import app as users_view
app.register_blueprint(users_view)

@app.route('/')
def index():
    db = getdb()
    list_checks = db.getAll('checks')
    return render_template('index.html', checks = list_checks if list_checks else [] )

