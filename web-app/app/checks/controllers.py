from app.common.sql import getdb
from app.common.model import Model, UserModel
from flask.ext.login import current_user

class Checks(UserModel):
    table = 'checks'

    def getAll(self, where = None):
        where_admin = None
        if current_user.is_authenticated and current_user.is_admin:
            where_admin = '%s = %s' % ( self.usercol, current_user.get_id() )

        wheres = list()
        for w in [ where, where_admin ]:
            if w:
                wheres.append(w)

        where_sql = 'WHERE %s' % (' AND '.join(wheres)) if len(wheres) > 0 else ''
        
        items = self.db.query_named('''
        SELECT checks.*,check_type.name AS check_type,users.name AS username
        FROM checks
        INNER JOIN check_type ON check_type.id = checks.type
        INNER JOIN users ON users.id = checks.user_id
        %s''' % where_sql)
        return items if items else []


    def getReport(self, user_id, public):
        where = dict(user_id = user_id)
        if public:
            where['user_id'] = user_id
        items = self.filter(**where)
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
