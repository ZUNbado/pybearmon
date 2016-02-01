from app.common.sql import getdb
from app.common.model import Model
from flask.ext.login import UserMixin

class Users(Model):
    table = 'users'

    def __init__(self):
        self.db = getdb()

    def login(self, email, password):
        user = self.db.getOne(self.table, '*', ( 'email = %s AND password = %s', [ email, password ]))
        if user:
            return user
        return False

class LoginUser(UserMixin):
    def __init__(self, email=None, password=None, active=True, id=None):
        self.email = email
        self.password = password
        self.active = active
        self.id = None

    def get_by_id(self, user_id):
        user = Users().get(user_id)
        if user:
            return LoginUser(user.email, user.password, id = user.id)
        return False

    def is_authenticated(self):
        user = Users().login(self.email, self.password)
        if user:
            self.user = user
            return True
        return False

    def is_active(self):
        if self.is_authenticated():
            if self.user.is_active:
                return True
        return False

    def is_admin(self):
        if self.is_active():
            if self.user.is_admin:
                return True
        return False

    def get_id(self):
        if self.is_active():
            return unicode(self.user.id)
