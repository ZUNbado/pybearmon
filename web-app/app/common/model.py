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
        return check if check else False

    def delete(self, key):
        if self.db.delete(self.table, [ '%s = %s' % (self.primary_key, key) ]):
            self.db.commit()
            return True
        return False

    def getAll(self, where = None):
        items = self.db.getAll(self.table, '*', where)
        return items if items else []

    def filter(self, **kwargs):
        wheres = list()
        for param, value in kwargs.items():
            wheres.append('%s = %s' % ( param, value ))
        return self.getAll(' AND '.join(wheres))

    def count(self):
        item = self.db.getOne(self.table, [ 'COUNT(*) AS count' ])
        return item.count

class UserModel(Model):
    usercol = 'user_id'

    def save(self, id, **kwargs):
        if not current_user.is_admin:
            kwargs['user_id'] = current_user.get_id()
        return super(UserModel, self).save(id, **kwargs)

    def getAll(self):
        where = None if current_user.is_admin else [ '%s = %s' % ( self.usercol, current_user.get_id() ) ]
        items = self.db.getAll(self.table, '*',  where)
        return items if items else []
