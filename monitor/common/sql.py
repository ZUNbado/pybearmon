from .simplemysql import SimpleMysql
from config import config

def getdb():
    try:
        return SimpleMysql(
                host=config['db_host'],
                port=3306,
                user=config['db_username'],
                passwd=config['db_password'],
                db=config['db_name'],
                )
    except Exception, e:
        print 'Error conecting to %s: %s' % (config['db_host'], e)
        return False
