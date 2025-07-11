import sys
import os
import pymysql
import warnings
import traceback
import configparser

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


def checkAsteroid(asteroid_id):

    count = 0
    sql=("SELECT COUNT(*) FROM asteroids WHERE asteroid_id = %s" % asteroid_id)
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


def getL1Metadata(asteroid_id):

    l1_metadata = ()
    sql=("SELECT asteroid_id, name, radius, spectral_type, bonuses, scan_status FROM asteroid_metadata_l1 WHERE asteroid_id = %s" % asteroid_id)
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()

    if rows == None:
        return None

    for row in rows:
        l1_metadata = (row[1], row[2], row[3], row[4], row[5])

    cur.close()
    con.close()

    return l1_metadata


def updateAsteroid(txn_id, block_id, asteroid_id, asteroid_owner):

    asteroid_exists = checkAsteroid(asteroid_id)
    if asteroid_exists == 0:

        l1_metadata = getL1Metadata(asteroid_id)
        print(l1_metadata)

        if l1_metadata is not None:
            name = l1_metadata[0]
            radius = l1_metadata[1]
            spectral_type = l1_metadata[2]
            bonuses = l1_metadata[3]
            surface_scan = l1_metadata[4]
            sql=("INSERT IGNORE INTO asteroids (txn_id, block_number, asteroid_id, asteroid_owner, name, radius, spectral_type, bonuses, surface_scan, scan_status) VALUES ('%s', %s, %s, '%s', '%s', %s, %s, %s, %s, %s)" % (txn_id, block_id, asteroid_id, asteroid_owner, name, radius, spectral_type, bonuses, surface_scan, surface_scan))
        else:
            sql=("INSERT IGNORE INTO asteroids (txn_id, block_number, asteroid_id, asteroid_owner) VALUES ('%s', %s, %s, '%s')" % (txn_id, block_id, asteroid_id, asteroid_owner))

    else:
        sql=("UPDATE asteroids SET txn_id = '%s', block_number = %s, asteroid_id = %s, asteroid_owner = '%s' WHERE asteroid_id = %s" % (txn_id, block_id, asteroid_id, asteroid_owner, asteroid_id))

    print(sql)
    updateSql(sql)


def asteroidTransfer(tx_hash, block_number, asteroid_id, from_address, to_address, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO asteroid_transfers (txn_id, block_number, asteroid_id, from_address, to_address) VALUES ('%s', %s, %s, '%s', '%s')" % (tx_hash, block_number, asteroid_id, from_address, to_address))
    print(insert_sql)
    updateSql(insert_sql)
    updateAsteroid(tx_hash, block_number, asteroid_id, to_address)

    txn_count = checkTxnRecorder(tx_hash, "asteroid_transfers_txns")
    if txn_count == 0:
        insert_sql2=("INSERT IGNORE INTO asteroid_transfers_txns (txn_id, block_number, asteroid_id, from_address, to_address, fee, timestamp) VALUES ('%s', %s, %s, '%s', '%s', %s, '%s')" % (tx_hash, block_number, asteroid_id, from_address, to_address, fee, timestamp))
        print(insert_sql2)
        updateSql(insert_sql2)


def bridgedFromL1(tx_hash, block_number, from_address, asteroid_id, to_address, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO asteroid_bridged_from_l1 (txn_id, block_number, asteroid_id, from_address, to_address) VALUES ('%s', %s, %s, '%s', '%s')" % (tx_hash, block_number, asteroid_id, from_address, to_address))
    print(insert_sql)
    updateSql(insert_sql)
    updateAsteroid(tx_hash, block_number, asteroid_id, to_address)

    txn_count = checkTxnRecorder(tx_hash, "asteroid_bridged_from_l1_txns")
    if txn_count == 0:
        insert_sql2=("INSERT IGNORE INTO asteroid_bridged_from_l1_txns (txn_id, block_number, asteroid_id, from_address, to_address, fee, timestamp) VALUES ('%s', %s, %s, '%s', '%s', %s, '%s')" % (tx_hash, block_number, asteroid_id, from_address, to_address, fee, timestamp))
        print(insert_sql2)
        updateSql(insert_sql2)


def bridgedToL1(tx_hash, block_number, from_address, asteroid_id, to_address, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO asteroid_bridged_to_l1 (txn_id, block_number, asteroid_id, from_address, to_address) VALUES ('%s', %s, %s, '%s', '%s')" % (tx_hash, block_number, asteroid_id, from_address, to_address))
    print(insert_sql)
    updateSql(insert_sql)
    updateAsteroid(tx_hash, block_number, asteroid_id, to_address)

    txn_count = checkTxnRecorder(tx_hash, "asteroid_bridged_to_l1_txns")
    if txn_count == 0:
        insert_sql2=("INSERT IGNORE INTO asteroid_bridged_to_l1_txns (txn_id, block_number, asteroid_id, from_address, to_address, fee, timestamp) VALUES ('%s', %s, %s, '%s', '%s', %s, '%s')" % (tx_hash, block_number, asteroid_id, from_address, to_address, fee, timestamp))
        print(insert_sql2)
        updateSql(insert_sql2)


