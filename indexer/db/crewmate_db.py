import sys
import os
import pymysql
import warnings
import traceback
import configparser

cwd = os.getcwd()
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


def checkCrewmate(crewmate_id):

    count = 0
    sql=("SELECT COUNT(*) FROM crewmates WHERE crewmate_id = %s" % crewmate_id)
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


def getL1Metadata(crewmate_id):

    l1_metadata = ()
    sql=("SELECT crewmate_id, name, collection, class, title FROM crewmate_metadata_l1 WHERE crewmate_id = %s" % crewmate_id)
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()

    if rows == None:
        return None

    for row in rows:
        l1_metadata = (row[1], row[2], row[3], row[4])

    cur.close()
    con.close()

    return l1_metadata


def updateCrewmate(txn_id, block_id, crewmate_id, crewmate_owner):

    crewmate_exists = checkCrewmate(crewmate_id)
    if crewmate_exists == 0:

        l1_metadata = getL1Metadata(crewmate_id)

        if len(l1_metadata) > 0:
            name = l1_metadata[0]
            collection = l1_metadata[1]
            crewmate_class = l1_metadata[2]
            title = l1_metadata[3]
            sql=("INSERT IGNORE INTO crewmates (txn_id, block_number, crewmate_id, crewmate_owner, name, collection, class, title) VALUES ('%s', %s, %s, '%s', '%s', %s, %s, %s)" % (txn_id, block_id, crewmate_id, crewmate_owner, name, collection, crewmate_class, title))

        else:
            sql=("INSERT IGNORE INTO crewmates (txn_id, block_number, crewmate_id, crewmate_owner) VALUES ('%s', %s, %s, '%s')" % (txn_id, block_id, crewmate_id, crewmate_owner))

        print(sql)
        updateSql(sql)
    else:
        sql=("UPDATE crewmates SET txn_id = '%s', block_number = %s, crewmate_id = %s, crewmate_owner = '%s' WHERE crewmate_id = %s" % (txn_id, block_id, crewmate_id, crewmate_owner, crewmate_id))
        print(sql)
        updateSql(sql)


def crewmatesTransfer(tx_hash, block_number, crewmate_id, from_address, to_address, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO crewmate_transfers (txn_id, block_number, crewmate_id, from_address, to_address) VALUES ('%s', %s, %s, '%s', '%s')" % (tx_hash, block_number, crewmate_id, from_address, to_address))
    print(insert_sql)
    updateSql(insert_sql)
    updateCrewmate(tx_hash, block_number, crewmate_id, to_address)

    txn_count = checkTxnRecorder(tx_hash, "crewmate_transfers_txns")
    if txn_count == 0:
        insert_sql2=("INSERT IGNORE INTO crewmate_transfers_txns (txn_id, block_number, crewmate_id, from_address, to_address, fee, timestamp) VALUES ('%s', %s, %s, '%s', '%s', %s, '%s')" % (tx_hash, block_number, crewmate_id, from_address, to_address, fee, timestamp))
        print(insert_sql2)
        updateSql(insert_sql2)


def bridgedFromL1(tx_hash, block_number, from_address, crewmate_id, to_address, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO crewmate_bridged_from_l1 (txn_id, block_number, crewmate_id, from_address, to_address) VALUES ('%s', %s, %s, '%s', '%s')" % (tx_hash, block_number, crewmate_id, from_address, to_address))
    print(insert_sql)
    updateSql(insert_sql)
    updateCrewmate(tx_hash, block_number, crewmate_id, to_address)

    txn_count = checkTxnRecorder(tx_hash, "crewmate_bridged_from_l1_txns")
    if txn_count == 0:
        insert_sql2=("INSERT IGNORE INTO crewmate_bridged_from_l1_txns (txn_id, block_number, crewmate_id, from_address, to_address, fee, timestamp) VALUES ('%s', %s, %s, '%s', '%s', %s, '%s')" % (tx_hash, block_number, crewmate_id, from_address, to_address, fee, timestamp))
        print(insert_sql2)
        updateSql(insert_sql2)


def bridgedToL1(tx_hash, block_number, from_address, crewmate_id, to_address, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO crewmate_bridged_to_l1 (txn_id, block_number, crewmate_id, from_address, to_address) VALUES ('%s', %s, %s, '%s', '%s')" % (tx_hash, block_number, crewmate_id, from_address, to_address))
    print(insert_sql)
    updateSql(insert_sql)
    updateCrewmate(tx_hash, block_number, crewmate_id, to_address)

    txn_count = checkTxnRecorder(tx_hash, "crewmate_bridged_to_l1_txns")
    if txn_count == 0:
        insert_sql2=("INSERT IGNORE INTO crewmate_bridged_to_l1_txns (txn_id, block_number, crewmate_id, from_address, to_address, fee, timestamp) VALUES ('%s', %s, %s, '%s', '%s', %s, '%s')" % (tx_hash, block_number, crewmate_id, from_address, to_address, fee, timestamp))
        print(insert_sql2)
        updateSql(insert_sql2)


