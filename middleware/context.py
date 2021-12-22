import os
import pymysql

def email_keygen():
    return 'c784699b774e4bcc89ef39708249263f'

def google_auth_keygen():
    return '891041318318-ocp6i17mcevembkehugg0j0s0f9ni40u.apps.googleusercontent.com', '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'

def get_db_info():

    db_host = os.environ.get("DBHOST", None)
    db_user = os.environ.get("DBUSER", None)
    db_password = os.environ.get("DBPASSWORD", None)
    db_host = None
    if db_host is not None:
        db_info = {
            "host": db_host,
            "user": db_user,
            "password": db_password,
            "cursorclass": pymysql.cursors.DictCursor
        }
    else:
        db_info = {
            'host': 'charitystoredb.cchzjvmkb07e.us-east-1.rds.amazonaws.com',
            'port':3306,
            "user":'admin',
            'password':'buckets1',
            "cursorclass": pymysql.cursors.DictCursor
        }

    return db_info