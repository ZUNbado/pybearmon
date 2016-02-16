from app.common.sql import getdb
from flask.ext.login import current_user

class Model(object):
    table = None
    fields = '*'
    primary_key = 'id'
    foreign_keys = list()

    def __init__(self):
        self.db = getdb()

    def save(self, id = None, **kwargs):
        if id:
            return self.update(id, **kwargs)
        return self.add(**kwargs)

    def update(self, id, **kwargs):
        if self.db.update(self.table, kwargs, [ '%s = %s' % (self.primary_key, id) ]):
            self.db.commit()
            return id
        return False

    def add(self, **kwargs):
        if self.db.insert(self.table, kwargs):
            self.db.commit()
            return self.db.cur.lastrowid
        return False

    def get(self, key):
        check = self.db.getOne(self.table, '*', [ '%s = %s' % (self.primary_key, key) ] )
        return check if check else False

    def delete(self, key):
        if self.db.delete(self.table, [ '%s = %s' % (self.primary_key, key) ]):
            self.db.commit()
            return True
        return False

    def parse_fields(self, fields, table):
        if type(fields) == str:
            fields = fields.split(',')

        fields_str = ''
        for field in fields:
            fields_str += '%s.%s' % (table, field)
        return fields_str 

    def getAll(self, where = None):
        if where:
            where = 'WHERE %s' % where
        else:
            where = ''
                
        select = list()
        select.append( self.parse_fields(self.fields, self.table) )
        
        joins = list()
        for foreign in self.foreign_keys:
            fields = foreign.get('fields', None)
            table = foreign.get('table', None)
            join = foreign.get('join', 'LEFT')
            on = foreign.get('on', None)
            
            if table:
                if fields:
                    select.append( self.parse_fields(fields, table))
                    
                join = '%s JOIN %s' % (join, table)
                if on: 
                    join += ' ON %s' % on
                joins.append(join)


        query = 'SELECT %s FROM %s %s %s' % (','.join(select), self.table, '\n'.join(joins), where)

        items = self.db.query_named(query)
        return items if items else []

    def filter(self, **kwargs):
        wheres = list()
        for param, value in kwargs.items():
            wheres.append('%s = %s' % ( param, value ))
        return self.getAll(' AND '.join(wheres))

    def count(self):
        item = self.db.getOne(self.table, [ 'COUNT(*) AS count' ])
        return item.count

    def formList(self, index = 'id', description = 'name'):
        choices = list()
        for t in self.getAll():
            choices.append( ( getattr(t, index), getattr(t,description) ) )
        return choices

class UserModel(Model):
    usercol = 'user_id'

    def save(self, id, **kwargs):
        if not current_user.is_admin:
            kwargs['user_id'] = current_user.get_id()
        return super(UserModel, self).save(id, **kwargs)

    def getAll(self, where = ''):
        where_admin = None 
        if current_user.is_authenticated and current_user.is_admin:
            where_admin = '%s = %s' % ( self.usercol, current_user.get_id() )
        
        wheres = list()
        for w in [ where, where_admin ]:
            if w:
                wheres.append(w)
        
        where_sql = '%s' % (' AND '.join(wheres)) if len(wheres) > 0 else ''
        return super(UserModel, self).getAll(where_sql)
