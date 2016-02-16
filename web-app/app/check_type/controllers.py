from app.common.sql import getdb
from app.common.model import Model

class CheckType(Model):
    table = 'check_type'

class CheckAttribute(Model):
    table = 'check_attribute'
   
    def getAll(self, checktype_id = None):
        where =  'id_check_type = %s' % checktype_id if checktype_id else checktype_id
        return super(CheckAttribute, self).getAll(where)
        
