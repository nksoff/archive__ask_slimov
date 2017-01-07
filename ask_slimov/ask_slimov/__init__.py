try:
    import MySQLdb
except:
    import pymysql

    pymysql.install_as_MySQLdb()

default_app_config = 'ask_slimov.apps.AskSlimovConfig'
