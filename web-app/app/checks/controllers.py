from app.common.sql import getdb
from app.common.model import UserModel

class Checks(UserModel):
    table = 'checks'

    def getAll(self):
        items = self.db.leftJoin((self.table, 'check_type'), ('*', [ 'name AS check_type' ]), ('type', 'id'))
        return items if items else []
