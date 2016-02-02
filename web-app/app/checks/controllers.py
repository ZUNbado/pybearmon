from app.common.sql import getdb
from app.common.model import UserModel

class Checks(UserModel):
    table = 'checks'

    def getAll(self):
        # add user_id to where
        items = self.db.leftJoin((self.table, 'check_type'), ('*', [ 'name AS check_type' ]), ('type', 'id'))
        return items if items else []

    def getReport(self, user_id, public):
        if public:
            where = [ 'user_id = %s AND public = 1' % user_id ]
        else:
            where = [ 'user_id = %s' % user_id ]
        items = self.db.leftJoin((self.table, 'check_type'), ('*', [ 'name AS check_type' ]), ('type', 'id'), where)
        return items if items else []
