from app.common.sql import getdb

class Checks(object):
    def __init__(self):
        self.db = getdb()

    def save(self, id = None, name = None, type = None, data = None, user_id = None):
        if id:
            return self.update(id, name, type, data )
        else:
            return self.add(name, type, data, user_id)

    def update(self, id, name, type, data):
        if self.db.update('checks', dict(name = name, type = type, data = data), [ 'id = %s' % id ]):
            self.db.commit()
            return id
        return False

    def add(self, name, type, data, user_id):
        if self.db.insert('checks', dict( name = name, type = type, data = data, user_id = user_id)):
            self.db.commit()
            return self.db.cur.lastrowid
        return False

    def get(self, id):
        check = self.db.getOne('checks', '*', ( 'id = %s', id ) )
        if check:
            return check
        return False

    def getAll(self, user_id = None):
        where = ( 'user_id = %s', user_id ) if user_id else user_id
        checks = self.db.getAll('checks', '*', where)
        return checks if checks else []
