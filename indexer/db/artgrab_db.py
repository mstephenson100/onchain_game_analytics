import sys
import os
import pymysql
import warnings
import traceback
import configparser
import time

filename = __file__
config_path = filename.split('/')[3]
config_file = "/home/bios/" + config_path + "/indexer.conf"

if os.path.exists(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    db_user = config.get('credentials', 'db_user')
    db_password = config.get('credentials', 'db_password')
    db = config.get('credentials', 'db')
else:
    raise Exception(config_file)


def updateSql(sql):

    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)

    cur.close()
    con.close()


def getToGrab(asset_type):

    assets=[]
    sql=("SELECT asset_id FROM art_grabs WHERE asset_type = %s AND status = 1 AND date < (SELECT NOW() - INTERVAL 60 MINUTE) LIMIT 10" % asset_type)
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    cur = con.cursor()
    cur.execute("%s" % sql)
    rows = cur.fetchall()
    for row in rows:
        assets.append(row[0])

    cur.close()
    con.close()

    return assets


def markDone(asset_type, asset_id):

    update_sql = ("UPDATE art_grabs SET status = 2 WHERE asset_type = %s AND asset_id = %s" % (asset_type, asset_id))
    print(update_sql)
    updateSql(update_sql)

