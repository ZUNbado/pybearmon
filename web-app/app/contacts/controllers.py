from app.common.sql import getdb
from app.common.model import UserModel

class Contacts(UserModel):
    table = 'contacts'

    def getAll(self):
        items = self.db.leftJoin((self.table, 'contact_type'), ('*', [ 'name AS contact_type' ]), ('type', 'id'))
        return items if items else []
