from app.common.sql import getdb

class CheckType(object):
    table = 'check_type'
    def __init__(self):
        self.db = getdb()

    def save(self, id = None, name = None):
        if id:
            return self.update(id, name )
        else:
            return self.add(name)

    def update(self, id, name):
        if self.db.update(self.table, dict(name = name), [ 'id = %s' % id ]):
            self.db.commit()
            return id
        return False

    def add(self, name):
        if self.db.insert(self.table, dict( name = name)):
            self.db.commit()
            return self.db.cur.lastrowid
        return False

    def get(self, id):
        item = self.db.getOne(self.table, '*', ( 'id = %s', id ) )
        if item:
            return item
        return False

    def getAll(self):
        items = self.db.getAll(self.table)
        return items if items else []

    def formList(self):
        choices = list()
        for t in self.getAll():
            choices.append( (t.id, t.name) )
        return choices


class CheckAttribute(object):
    table = 'check_attribute'
    def __init__(self):
        self.db = getdb()

    def save(self, id = None, check_type_id = None, name = None, type = None, required = None):
        if id:
            return self.update( id, check_type_id, name, type, required )
        else:
            return self.add( check_type_id, name, type, required )

    def update(self, id, check_type_id, name, type, required):
        if self.db.update(self.table, dict( id_check_type = check_type_id, name = name, type = type, required = required), [ 'id = %s' % id ]):
            self.db.commit()
            return id
        return False

    def add(self, check_type_id, name, type, required):
        if self.db.insert(self.table, dict( id_check_type = check_type_id, name = name, type = type, required = required)):
            self.db.commit()
            return self.db.cur.lastrowid
        return False

    def get(self, id):
        item = self.db.getOne(self.table, '*', ( 'id = %s', id ) )
        if item:
            return item
        return False

    def getAll(self, checktype_id = None):
        where = ( 'id_check_type = %s', checktype_id ) if checktype_id else checktype_id
        items = self.db.getAll(self.table, '*', where)
        return items if items else []
