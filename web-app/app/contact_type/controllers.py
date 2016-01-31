from app.common.sql import getdb
from app.common.model import Model

class ContactType(Model):
    table = 'contact_type'
    def __init__(self):
        self.db = getdb()

    def formList(self):
        choices = list()
        for t in self.getAll():
            choices.append( (t.id, t.name) )
        return choices

class ContactAttribute(Model):
    table = 'contact_attribute'
    def __init__(self):
        self.db = getdb()
   
    def getAll(self, contacttype_id = None):
        where = [ 'id_contact_type = %s' % contacttype_id ] if contacttype_id else contacttype_id
        items = self.db.getAll(self.table, '*', where)
        return items if items else []
