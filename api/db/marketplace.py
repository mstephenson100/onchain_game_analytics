import sys
import os
import pymysql
import warnings
import traceback
import configparser
import time
from . import get_types

filename = __file__
config_path = filename.split('/')[3]
config_file = "/home/bios/" + config_path + "/api.conf"

if os.path.exists(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    db_user = config.get('credentials', 'db_user')
    db_password = config.get('credentials', 'db_password')
    db = config.get('credentials', 'db')
else:
    raise Exception(config_file)


def getSellOrders(con, asteroid_id, state, hours):

    orders = []
    if state == 'open':
        tablename = 'sell_orders'
    elif state == 'filled':
        tablename = 'dispatcher_sell_order_filled'

    pre_sql = ("SELECT exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price FROM %s " % tablename)
    if asteroid_id is None:
        from_sql = "WHERE amount > 0 "
    else:
        from_sql = ("WHERE exchange_asteroid_id = %s AND amount > 0 " % asteroid_id)

    if state == 'filled':
        if hours is None:
            finish_sql=" ORDER BY product_name"
        else:
            finish_sql=(" AND timestamp >= (NOW() - INTERVAL %s HOUR) ORDER BY product_name" % hours)
    else:
        finish_sql=" ORDER BY product_name"

    sql = pre_sql + from_sql + finish_sql
    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return orders

    for row in rows:
        exchange_id=row[0]
        asteroid_id=row[1]
        lot_id=row[2]
        product_id=row[3]
        product_name=row[4]
        amount=row[5]
        price=row[6]
        orders.append({"exchange_id": exchange_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "product_id": product_id, "product_name": product_name, "amount": amount, "price": price})

    return orders


def getProductSellOrders(con, asteroid_id, state, hours, product_id):

    orders = []
    if state == 'open':
        tablename = 'sell_orders'
    elif state == 'filled':
        tablename = 'dispatcher_sell_order_filled'

    pre_sql = ("SELECT exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price FROM %s " % tablename)
    if asteroid_id is None:
        from_sql = ("WHERE product_id = %s AND amount > 0 " % product_id)
    else:
        from_sql = ("WHERE product_id = %s AND exchange_asteroid_id = %s AND amount > 0 " % (product_id, asteroid_id))

    if state == 'filled':
        if hours is None:
            finish_sql=" ORDER BY product_name"
        else:
            finish_sql=(" AND timestamp >= (NOW() - INTERVAL %s HOUR) ORDER BY product_name" % hours)
    else:
        finish_sql=" ORDER BY product_name"

    sql = pre_sql + from_sql + finish_sql
    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return orders

    for row in rows:
        exchange_id=row[0]
        asteroid_id=row[1]
        lot_id=row[2]
        product_id=row[3]
        product_name=row[4]
        amount=row[5]
        price=row[6]
        orders.append({"exchange_id": exchange_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "product_id": product_id, "product_name": product_name, "amount": amount, "price": price})

    return orders


def getBuyOrders(con, asteroid_id, state, hours):

    orders = []
    if state == 'open':
        tablename = 'buy_orders'
    elif state == 'filled':
        tablename = 'dispatcher_buy_order_filled'

    pre_sql = ("SELECT exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price FROM %s " % tablename)
    if asteroid_id is None:
        from_sql = "WHERE amount > 0 "
    else:
        from_sql = ("WHERE exchange_asteroid_id = %s AND amount > 0 " % asteroid_id)

    if state == 'filled':
        if hours is None:
            finish_sql=" ORDER BY product_name"
        else:
            finish_sql=(" AND timestamp >= (NOW() - INTERVAL %s HOUR) ORDER BY product_name" % hours)
    else:
        finish_sql=" ORDER BY product_name"

    sql = pre_sql + from_sql + finish_sql
    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return orders

    for row in rows:
        exchange_id=row[0]
        asteroid_id=row[1]
        lot_id=row[2]
        product_id=row[3]
        product_name=row[4]
        amount=row[5]
        price=row[6]
        orders.append({"exchange_id": exchange_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "product_id": product_id, "product_name": product_name, "amount": amount, "price": price})

    return orders


def getProductBuyOrders(con, asteroid_id, state, hours, product_id):

    orders = []
    if state == 'open':
        tablename = 'buy_orders'
    elif state == 'filled':
        tablename = 'dispatcher_buy_order_filled'

    pre_sql = ("SELECT exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price FROM %s " % tablename)
    if asteroid_id is None:
        from_sql = ("WHERE product_id = %s AND amount > 0 " % product_id)
    else:
        from_sql = ("WHERE product_id = %s AND exchange_asteroid_id = %s AND amount > 0 " % (product_id, asteroid_id))

    if state == 'filled':
        if hours is None:
            finish_sql=" ORDER BY product_name"
        else:
            finish_sql=(" AND timestamp >= (NOW() - INTERVAL %s HOUR) ORDER BY product_name" % hours)
    else:
        finish_sql=" ORDER BY product_name"

    sql = pre_sql + from_sql + finish_sql
    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return orders

    for row in rows:
        exchange_id=row[0]
        asteroid_id=row[1]
        lot_id=row[2]
        product_id=row[3]
        product_name=row[4]
        amount=row[5]
        price=row[6]
        orders.append({"exchange_id": exchange_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "product_id": product_id, "product_name": product_name, "amount": amount, "price": price})

    return orders


def sellOrders(asteroid_id, state, hours):

    result = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    result = getSellOrders(con, asteroid_id, state, hours)
    con.close()
    return result


def productSellOrders(asteroid_id, state, hours, product_id):

    result = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    result = getProductSellOrders(con, asteroid_id, state, hours, product_id)
    con.close()
    return result


def buyOrders(asteroid_id, state, hours):

    result = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    result = getBuyOrders(con, asteroid_id, state, hours)
    con.close()
    return result


def productBuyOrders(asteroid_id, state, hours, product_id):

    result = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    result = getProductBuyOrders(con, asteroid_id, state, hours, product_id)
    con.close()
    return result

