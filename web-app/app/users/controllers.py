from app.common.sql import getdb

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
