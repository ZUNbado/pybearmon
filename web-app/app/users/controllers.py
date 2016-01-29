from app.common.sql import getdb
from flask.ext.login import UserMixin

class Users(object):
    def __init__(self):
        self.db = getdb()

    def save(self, id = None, name = None, email = None, password = None):
        if id:
            return self.update(id, name, email, password)
        else:
            return self.add(name, email, password)

    def update(self, id, name, email, password):
        if self.db.update('users', dict(name = name, email = email, password = password), [ 'id = %s' % id ]):
            self.db.commit()
            return id
        return False

    def add(self, name, email, password):
        if self.db.insert('users', dict( name = name, email = email, password = password)):
            self.db.commit()
            return self.db.cur.lastrowid
        return False

    def get(self, id):
        check = self.db.getOne('users', '*', ( 'id = %s', id ) )
        if check:
            return check
        return False

    def getAll(self):
        users = self.db.getAll('users')
        return users if users else []

    def login(self, email, password):
        user = self.db.getOne('users', '*', ( 'email = %s AND password = %s', [ email, password ]))
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

    @property
    def is_authenticated(self):
        user = Users().login(self.email, self.password)
        if user:
            self.user = user
            return True
        return False

    @property
    def is_active(self):
        if self.is_authenticated:
            self.active = self.user.is_active
            if self.active:
                return True
        return False

    @property
    def is_admin(self):
        if self.is_active:
            if self.user.is_admin:
                return True
        return False

    def get_id(self):
        if self.is_active:
            return unicode(self.user.id)
