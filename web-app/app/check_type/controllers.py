from app.common.sql import getdb
from app.common.model import Model

class CheckType(Model):
    table = 'check_type'
    def __init__(self):
        self.db = getdb()

    def formList(self):
        choices = list()
        for t in self.getAll():
            choices.append( (t.id, t.name) )
        return choices

class CheckAttribute(Model):
    table = 'check_attribute'
    def __init__(self):
        self.db = getdb()
   
    def getAll(self, checktype_id = None):
        where = [ 'id_check_type = %s' % checktype_id ] if checktype_id else checktype_id
        items = self.db.getAll(self.table, '*', where)
        return items if items else []
