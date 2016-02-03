from app.common.sql import getdb
from app.common.model import UserModel
from flask.ext.login import current_user

class Checks(UserModel):
    table = 'checks'

    def getAll(self):
        where = None if current_user.is_admin else [ '%s = %s' % ( self.usercol, current_user.get_id() ) ]
        items = self.db.leftJoin((self.table, 'check_type'), ('*', [ 'name AS check_type' ]), ('type', 'id'), where)
        return items if items else []

    def getReport(self, user_id, public):
        if public:
            where = [ 'user_id = %s AND public = 1' % user_id ]
        else:
            where = [ 'user_id = %s' % user_id ]
        items = self.db.leftJoin((self.table, 'check_type'), ('*', [ 'name AS check_type' ]), ('type', 'id'), where)
        return items if items else []
