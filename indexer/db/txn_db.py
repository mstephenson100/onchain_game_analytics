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


def txnCounter(block_number, txns, timestamp, tablename):

    insert_sql = ("INSERT IGNORE INTO %s (block_number, txns, timestamp) VALUES (%s, %s, '%s')" % (tablename, block_number, txns, timestamp))
    print(insert_sql)
    updateSql(insert_sql)


def feeLogger(tx_hash, block_number, fee, timestamp, contract):

    insert_sql = ("INSERT IGNORE INTO influence_txns (txn_id, block_number, contract, fee, timestamp) VALUES ('%s', %s, '%s', %s, '%s')" % (tx_hash, block_number, contract, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)


def checkFee(tx_hash, block_number, contract, description):

    count = 0
    sql=("SELECT COUNT(*) FROM influence_txns WHERE txn_id = '%s' AND block_number = %s AND contract = '%s' AND description = '%s'" % (tx_hash, block_number, contract, description))
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        count=result[0]

    cur.close()
    con.close()

    return count

