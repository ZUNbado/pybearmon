from app.common.sql import getdb
from app.common.model import UserModel
from flask.ext.login import current_user

class Contacts(UserModel):
    table = 'contacts'
    fields = '*'
    foreign_keys = [
            dict(fields = ['name AS contact_type'], table = 'contact_type', join = 'INNER', on = 'contact_type.id = contacts.type'),
            dict(fields = ['name AS username'], table = 'users', join = 'INNER', on = 'users.id = contacts.user_id'),
            ]
