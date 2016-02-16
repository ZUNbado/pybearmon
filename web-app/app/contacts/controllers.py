from app.common.sql import getdb
from app.common.model import UserModel
from flask.ext.login import current_user

class Contacts(UserModel):
    table = 'contacts'

    def getAll(self):
        where = '' if current_user.is_admin else [ 'WHERE %s = %s' % ( self.usercol, current_user.get_id() ) ]
        items = self.db.query_named('''
        SELECT contacts.*,contact_type.name AS contact_type,users.name AS username
        FROM contacts
        INNER JOIN contact_type ON contact_type.id = contacts.type
        INNER JOIN users ON users.id = contacts.user_id
        %s''' % where)
        return items if items else []


    def formList(self):
        choices = list()
        for t in self.getAll():
            choices.append( (t.id, t.name) )
        return choices

