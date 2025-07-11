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


def checkShip(ship_id):

    count = 0
    sql=("SELECT COUNT(*) FROM ships WHERE ship_id = %s" % ship_id)
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


def updateShip(txn_id, block_number, to_address, ship_id):

    ship_exists = checkShip(ship_id)
    if ship_exists == 0:
        sql=("INSERT IGNORE INTO ships (txn_id, block_number, ship_id, ship_owner) VALUES ('%s', %s, %s, '%s')" % (txn_id, block_number, ship_id, to_address))
        print(sql)
        updateSql(sql)
    else:
        sql=("UPDATE ships SET ship_owner = '%s' WHERE ship_id = %s" % (to_address, ship_id))
        print(sql)
        updateSql(sql)


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


def shipTransfer(tx_hash, block_number, from_address, to_address, ship_id, fee, timestamp):

    insert_sql = ("INSERT IGNORE INTO ship_transfers (txn_id, block_number, from_address, to_address, ship_id) VALUES ('%s', %s, '%s', '%s', %s)" % (tx_hash, block_number, from_address, to_address, ship_id))
    print(insert_sql)
    updateSql(insert_sql)
    updateShip(tx_hash, block_number, to_address, ship_id)

    txn_count = checkTxnRecorder(tx_hash, "ship_transfers_txns")
    if txn_count == 0:
        insert_sql2=("INSERT IGNORE INTO ship_transfers_txns (txn_id, block_number, from_address, to_address, ship_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, '%s')" % (tx_hash, block_number, from_address, to_address, ship_id, fee, timestamp))
        print(insert_sql2)
        updateSql(insert_sql2)


def bridgedFromL1(tx_hash, block_number, from_address, ship_id, to_address, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO ship_bridged_from_l1 (txn_id, block_number, ship_id, from_address, to_address) VALUES ('%s', %s, %s, '%s', '%s')" % (tx_hash, block_number, ship_id, from_address, to_address))
    print(insert_sql)
    updateSql(insert_sql)
    updateShip(tx_hash, block_number, ship_id, to_address)

    txn_count = checkTxnRecorder(tx_hash, "ship_bridged_from_l1_txns")
    if txn_count == 0:
        insert_sql2=("INSERT IGNORE INTO ship_bridged_from_l1_txns (txn_id, block_number, ship_id, from_address, to_address, fee, timestamp) VALUES ('%s', %s, %s, '%s', '%s', %s, '%s')" % (tx_hash, block_number, ship_id, from_address, to_address, fee, timestamp))
        print(insert_sql2)
        updateSql(insert_sql2)


def bridgedToL1(tx_hash, block_number, from_address, ship_id, to_address, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO ship_bridged_to_l1 (txn_id, block_number, ship_id, from_address, to_address) VALUES ('%s', %s, %s, '%s', '%s')" % (tx_hash, block_number, ship_id, from_address, to_address))
    print(insert_sql)
    updateSql(insert_sql)
    updateShip(tx_hash, block_number, ship_id, to_address)

    txn_count = checkTxnRecorder(tx_hash, "ship_bridged_to_l1_txns")
    if txn_count == 0:
        insert_sql2=("INSERT IGNORE INTO ship_bridged_to_l1_txns (txn_id, block_number, ship_id, from_address, to_address, fee, timestamp) VALUES ('%s', %s, %s, '%s', '%s', %s, '%s')" % (tx_hash, block_number, ship_id, from_address, to_address, fee, timestamp))
        print(insert_sql2)
        updateSql(insert_sql2)


def sellOrderSet(tx_hash, block_number, from_address, ship_id, price, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO ship_sell_order_set (txn_id, block_number, from_address, ship_id, price, fee, timestamp) VALUES ('%s', %s, '%s', %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, ship_id, price, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    ship_type, asteroid_id, lot_id = getShipData(ship_id)
    state = getShipState(ship_id)
    if state > 0:
        update_sql=("UPDATE ships_for_sale SET txn_id = '%s', block_number = %s, seller_address = '%s', price = %s, asteroid_id = %s, lot_id = %s WHERE ship_id = %s" % (tx_hash, block_number, from_address, price, asteroid_id, lot_id, ship_id))
        print(update_sql)
        updateSql(update_sql)
    else:
        insert_sql2=("INSERT INTO ships_for_sale (txn_id, block_number, seller_address, ship_id, ship_type, asteroid_id, lot_id, price) VALUES ('%s', %s, '%s', %s, %s, %s, %s, %s)" % (tx_hash, block_number, from_address, ship_id, ship_type, asteroid_id, lot_id, price))
        print(insert_sql2)
        updateSql(insert_sql2)


def sellOrderFilled(tx_hash, block_number, from_address, ship_id, price, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO ship_sell_order_filled (txn_id, block_number, from_address, ship_id, price, fee, timestamp) VALUES ('%s', %s, '%s', %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, ship_id, price, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    seller_address = getShipSeller(ship_id)
    ship_type, asteroid_id, lot_id = getShipData(ship_id)
    insert_sql2=("INSERT IGNORE INTO ships_sold (txn_id, block_number, buyer_address, seller_address, ship_id, ship_type, asteroid_id, lot_id, price) VALUES ('%s', %s, '%s', %s, %s, %s, %s, %s, %s)" % (tx_hash, block_number, from_address, seller_address, ship_id, ship_type, asteroid_id, lot_id, price))
    print(insert_sql2)
    updateSql(insert_sql2)

    delete_sql=("DELETE FROM ships_for_sale WHERE ship_id = %s" % ship_id)
    print(delete_sql)
    updateSql(delete_sql)


def getShipData(ship_id):

    sql=("SELECT b.ship_id, b.dock_asteroid_id, b.dock_lot_id, c.ship_type FROM ships_docked b, ships c WHERE b.ship_id = %s AND b.ship_id = c.ship_id" % ship_id)
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        if result is None:
            ship_type = None
            asteroid_id = None
            lot_id = None
        else:
            ship_id=result[0]
            asteroid_id=result[1]
            lot_id=result[2]
            ship_type=result[3]

    cur.close()
    con.close()

    if ship_type is None:
        ship_type = 0

    if asteroid_id is None:
        asteroid_id = 'NULL'

    if lot_id is None:
        lot_id = 'NULL'

    print("ship_type: %s" % ship_type)
    print("asteroid_id: %s" % asteroid_id)
    print("lot_id: %s" % lot_id)
    return ship_type, asteroid_id, lot_id


def getShipState(ship_id):

    state = 0
    sql=("SELECT COUNT(*) FROM ships_for_sale WHERE ship_id = %s" % ship_id)
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        state=result[0]

    cur.close()
    con.close()

    return state


def getShipSeller(ship_id):

    seller_address = 0
    sql=("SELECT seller_address FROM ships_for_sale WHERE ship_id = %s" % ship_id)
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        state=result[0]

    cur.close()
    con.close()

    return seller_address

