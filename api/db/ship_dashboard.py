import sys
import os
import pymysql
import warnings
import traceback
import configparser
import time

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


def getShipsForSale(con):

    ships = []
    sql = "SELECT ship_id, ship_type, price, asteroid_id, lot_id FROM ships_for_sale WHERE price > 0"
    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return ships

    for row in rows:
        ship_id=row[0]
        ship_type=row[1]
        price=row[2]
        asteroid_id=row[3]
        lot_id=row[4]
        transit = getShipTransitState(con, ship_id)
        orbit_asteroid_id = getShipOrbit(con, ship_id)
        ships.append({"ship_id": ship_id, "ship_type": ship_type, "price": price, "asteroid_id": asteroid_id, "lot_id": lot_id, "transit_state": transit, "orbiting": orbit_asteroid_id})

    return ships


def getShipsSold(con):

    ships = []
    sql = "SELECT ship_id, ship_type, price, asteroid_id, lot_id, txn_id FROM ships_sold"
    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return ships

    for row in rows:
        ship_id=row[0]
        ship_type=row[1]
        price=row[2]
        asteroid_id=row[3]
        lot_id=row[4]
        txn_id=row[5]
        ships.append({"ship_id": ship_id, "ship_type": ship_type, "price": price, "asteroid_id": asteroid_id, "lot_id": lot_id, "txn_id": txn_id})

    return ships


def getShipTransitState(con, ship_id):

    transit_sql = ("SELECT origin_id, destination_id, finish_time FROM transit WHERE status = 1 AND ship_id = %s" % ship_id)
    transit = []
    with con:
        cur = con.cursor()
        cur.execute("%s" % transit_sql)
        rows = cur.fetchall()
        cur.close()

    if len(rows) == 0:
        transit = []

    for row in rows:
        origin_id=row[0]
        destination_id=row[1]
        finish_time=row[2]
        transit.append({"origin_id": origin_id, "destination_id": destination_id, "finish_time": finish_time})

    return transit


def getShipOrbit(con, ship_id):

    transit_sql = ("SELECT destination_id FROM transit WHERE status = 2 AND ship_id = %s ORDER BY finish_time DESC LIMIT 1" % ship_id)
    with con:
        cur = con.cursor()
        cur.execute("%s" % transit_sql)
        rows = cur.fetchall()
        cur.close()

    if len(rows) == 0:
        orbit_asteroid_id = 0

    for row in rows:
        orbit_asteroid_id=row[0]

    return orbit_asteroid_id


def getShipDashboard(con):

    ships = []
    ships_for_sale = getShipsForSale(con)
    ships_sold = getShipsSold(con)
    ships.append({"for_sale": ships_for_sale, "sold": ships_sold})
    return ships


def shipDashboard():

    ships = None
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    ships = getShipDashboard(con)
    con.close()
    return ships

