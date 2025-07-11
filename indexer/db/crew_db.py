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


def checkCrew(crew_id):

    count = 0
    sql=("SELECT COUNT(*) FROM crews WHERE crew_id = %s" % crew_id)
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


def checkTxnRecorder(txn_id, table):

    count = 0
    sql=("SELECT COUNT(*) FROM %s WHERE txn_id = '%s'" % (table, txn_id))
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


def crewTransfer(tx_hash, block_number, from_address, to_address, crew_id, fee, timestamp):

    insert_sql = ("INSERT IGNORE INTO crew_transfers (txn_id, block_number, from_address, to_address, crew_id) VALUES ('%s', %s, '%s', '%s', %s)" % (tx_hash, block_number, from_address, to_address, crew_id))
    print(insert_sql)
    updateSql(insert_sql)
    updateCrew(tx_hash, block_number, to_address, crew_id, timestamp)

    txn_count = checkTxnRecorder(tx_hash, "crew_transfers_txns")
    if txn_count == 0:
        insert_sql2=("INSERT IGNORE INTO crew_transfers_txns (txn_id, block_number, from_address, to_address, crew_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, '%s')" % (tx_hash, block_number, from_address, to_address, crew_id, fee, timestamp))
        print(insert_sql2)
        updateSql(insert_sql2)


def updateCrew(txn_id, block_number, to_address, crew_id, timestamp):

    crew_exists = checkCrew(crew_id)
    if crew_exists == 0:
        sql=("INSERT IGNORE INTO crews (txn_id, block_number, crew_id, crew_owner, delegated_address, timestamp) VALUES ('%s', %s, %s, '%s', '%s', '%s')" % (txn_id, block_number, crew_id, to_address, to_address, timestamp))
        print(sql)
        updateSql(sql)
    else:
        sql=("UPDATE crews SET txn_id = '%s', block_number = %s, crew_id = %s, crew_owner = '%s', delegated_address = '%s' WHERE crew_id = %s" % (txn_id, block_number, crew_id, to_address, to_address, crew_id))
        print(sql)
        updateSql(sql)


