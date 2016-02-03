from app.common.sql import getdb
from app.common.model import UserModel
from flask.ext.login import current_user

class Contacts(UserModel):
    table = 'contacts'

    def getAll(self):
        where = None if current_user.is_admin else [ '%s = %s' % ( self.usercol, current_user.get_id() ) ]
        items = self.db.leftJoin((self.table, 'contact_type'), ('*', [ 'name AS contact_type' ]), ('type', 'id'), where)
        return items if items else []
