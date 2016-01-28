from app.common.sql import getdb

class Checks(object):
    def __init__(self):
        self.db = getdb()

    def save(self, id = None, name = None, type = None, data = None):
        if id:
            return self.update(id, name, type, data)
        else:
            return self.add(name, type, data)

    def update(self, id, name, type, data):
        if self.db.update('checks', dict(name = name, type = type, data = data), [ 'id = %s' % id ]):
            self.db.commit()
            return id
        return False

    def add(self, name, type, data):
        if self.db.insert('checks', dict( name = name, type = type, data = data)):
            self.db.commit()
            return self.db.cur.lastrowid
        return False

    def get(self, id):
        check = self.db.getOne('checks', '*', ( 'id = %s', id ) )
        if check:
            return check
        return False

    def getAll(self):
        checks = self.db.getAll('checks')
        return checks if checks else []
