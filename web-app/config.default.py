class Config(object):
    DEBUG = True
    DISABLE_AUTH = True

    HOST = '0.0.0.0'

    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_USER = 'monitor'
    MYSQL_PASSWORD = ''
    MYSQL_DATABASE = 'monitor'

class Development(Config):
    pass

class Production(Config):
    pass
