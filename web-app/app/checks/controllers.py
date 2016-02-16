from app.common.sql import getdb
from app.common.model import Model, UserModel
from flask.ext.login import current_user

class Checks(UserModel):
    table = 'checks'
    fields = '*'
    foreign_keys = [
            dict(fields = ['name AS check_type'], table = 'check_type', join = 'INNER', on = 'check_type.id = checks.type'),
            dict(fields = ['name AS username'], table = 'users', join = 'INNER', on = 'users.id = checks.user_id'),
            ]

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
