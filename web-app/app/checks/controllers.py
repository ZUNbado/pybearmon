from app.common.sql import getdb
from app.common.model import Model, UserModel
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

    def getAlerts(self, check_id):
        if check_id:
            return Alerts().getByCheck(check_id)
        return list()

class Alerts(Model):
    table = 'alerts'

    def deleteByCheck(self, check_id):
        self.db.delete(self.table, ['check_id = %s' % check_id])
        self.db.commit()

    def getByCheck(self, check_id):
        items = self.db.getAll(self.table, '*', ['check_id = %s' % check_id])
        return items if items else []
