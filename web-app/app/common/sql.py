from .simplemysql import SimpleMysql
from sshtunnel import SSHTunnelForwarder
from flask import current_app

def getdb():
    if 'SSH_TUNNEL' in current_app.config and current_app.config['SSH_TUNNEL']:
        host ='127.0.0.1'
        port = sshtunnel()
    else:
        host=current_app.config['MYSQL_HOST']
        port=current_app.config['MYSQL_PORT']
    try:
        return SimpleMysql(
                host=host,
                port=port,
                user=current_app.config['MYSQL_USER'],
                passwd=current_app.config['MYSQL_PASSWORD'],
                db=current_app.config['MYSQL_DATABASE'],
                )
    except Exception, e:
        print 'Error conecting to %s: %s' % (current_app.config['MYSQL_HOST'], e)
        return False

def sshtunnel():
    server = SSHTunnelForwarder(
            (current_app.config['SSH_HOST'],current_app.config['SSH_PORT']),
            ssh_username=current_app.config['SSH_USER'],
            ssh_password=current_app.config['SSH_PASSWORD'],
            remote_bind_address=(current_app.config['SSH_REMOTE_HOST'], current_app.config['SSH_REMOTE_PORT'])
            )
    server.start()

    return server.local_bind_port

