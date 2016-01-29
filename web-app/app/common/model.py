from app.common.sql import getdb
from flask.ext.login import current_user

class Model(object):
    table = None
    primary_key = 'id'

    def __init__(self):
        self.db = getdb()

    def save(self, id = None, **kwargs):
        if id:
            return self.update(id, **kwargs)
        else:
            return self.add(**kwargs)

    def update(self, id, **kwargs):
        if self.db.update(self.table, kwargs, [ '%s = %s' % (self.primary_key, id) ]):
            self.db.commit()
            return id
        return False

    def add(self, **kwargs):
        if self.db.insert(self.table, kwargs):
            self.db.commit()
            return self.db.cur.lastrowid
        return False

    def get(self, key):
        check = self.db.getOne(self.table, '*', [ '%s = %s' % (self.primary_key, key) ] )
        if check:
            return check
        return False

    def getAll(self):
        items = self.db.getAll(self.table)
        return items if items else []

class UserModel(Model):
    usercol = 'user_id'

    def save(self, id, **kwargs):
        kwargs['user_id'] = current_user.get_id()
        print kwargs
        super(UserModel, self).save(id, **kwargs)

    def getAll(self):
        items = self.db.getAll(self.table, '*', [ '%s = %s' % ( self.usercol, current_user.get_id() ) ])
        return items if items else []
