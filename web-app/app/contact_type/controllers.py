from app.common.sql import getdb
from app.common.model import Model

class ContactType(Model):
    table = 'contact_type'

class ContactAttribute(Model):
    table = 'contact_attribute'
   
    def getAll(self, contacttype_id = None):
        where = 'id_contact_type = %s' % contacttype_id if contacttype_id else contacttype_id
        return super(ContactAttribute, self).getAll(where)
