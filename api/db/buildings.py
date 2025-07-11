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


def parseBuildingType(building_type):

    if building_type == 'warehouse':
        building_type = 1

    if building_type == 'extractor':
        building_type = 2

    if building_type == 'refinery':
        building_type = 3

    if building_type == 'bioreactor':
        building_type = 4

    if building_type == 'factory':
        building_type = 5

    if building_type == 'shipyard':
        building_type = 6

    if building_type == 'spaceport':
        building_type = 7

    if building_type == 'marketplace':
        building_type = 8

    if building_type == 'habitat':
        building_type = 9

    return building_type


def getOwnedBuildings(con, building_type, parameter1, parameter2):

    owned_buildings = []
    building_type = parseBuildingType(building_type)

    if parameter1 == 'wallet':
        sql = ("SELECT txn_id, block_number, caller_address, asteroid_id, lot_id, crew_id, building_id, building_type, status FROM buildings WHERE caller_address = '%s' AND building_type = %s AND status = 3" % (parameter2, building_type))
    if parameter1 == 'crew':
        sql = ("SELECT txn_id, block_number, caller_address, asteroid_id, lot_id, crew_id, building_id, building_type, status FROM buildings WHERE crew_id = %s AND building_type = %s AND status = 3" % (parameter2, building_type))

    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return owned_buildings

    for row in rows:
        txn_id=row[0]
        block_number=row[1]
        caller_address=row[2]
        asteroid_id=row[3]
        lot_id=row[4]
        crew_id=row[5]
        building_id=row[6]
        building_type=row[7]
        status=row[8]
        owned_buildings.append({"building_id": building_id, "building_type": building_type, "asteroid_id": asteroid_id, "lot_id": lot_id, "crew_id": crew_id, "status": status, "wallet": caller_address, "txn_id": txn_id, "block_number": block_number})

    return owned_buildings


def getOwnedBuildingsOnAsteroid(con, parameter1, parameter2, asteroid_id):

    owned_buildings = []
    if parameter1 == 'wallet':
        sql = ("SELECT txn_id, block_number, caller_address, asteroid_id, lot_id, crew_id, building_id, building_type, status FROM buildings WHERE caller_address = '%s' AND asteroid_id = %s AND status = 3" % (parameter2, asteroid_id))
    if parameter1 == 'crew':
        sql = ("SELECT txn_id, block_number, caller_address, asteroid_id, lot_id, crew_id, building_id, building_type, status FROM buildings WHERE crew_id = %s AND asteroid_id = %s AND status = 3" % (parameter2, asteroid_id))

    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return owned_buildings

    for row in rows:
        txn_id=row[0]
        block_number=row[1]
        caller_address=row[2]
        asteroid_id=row[3]
        lot_id=row[4]
        crew_id=row[5]
        building_id=row[6]
        building_type=row[7]
        status=row[8]
        owned_buildings.append({"building_id": building_id, "building_type": building_type, "asteroid_id": asteroid_id, "lot_id": lot_id, "crew_id": crew_id, "status": status, "wallet": caller_address, "txn_id": txn_id, "block_number": block_number})

    return owned_buildings


def getOwnedBuildingsOnLot(con, parameter1, parameter2, asteroid_id, lot_id):

    owned_buildings = []
    if parameter1 == 'wallet':
        sql = ("SELECT txn_id, block_number, caller_address, asteroid_id, lot_id, crew_id, building_id, building_type, status FROM buildings WHERE caller_address = '%s' AND asteroid_id = %s AND lot_id = %s AND status = 3" % (parameter2, asteroid_id, lot_id))
    if parameter1 == 'crew':
        sql = ("SELECT txn_id, block_number, caller_address, asteroid_id, lot_id, crew_id, building_id, building_type, status FROM buildings WHERE crew_id = %s AND asteroid_id = %s AND lot_id = %s AND status = 3" % (parameter2, asteroid_id, lot_id))

    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return owned_buildings

    for row in rows:
        txn_id=row[0]
        block_number=row[1]
        caller_address=row[2]
        asteroid_id=row[3]
        lot_id=row[4]
        crew_id=row[5]
        building_id=row[6]
        building_type=row[7]
        status=row[8]
        owned_buildings.append({"building_id": building_id, "building_type": building_type, "asteroid_id": asteroid_id, "lot_id": lot_id, "crew_id": crew_id, "status": status, "wallet": caller_address, "txn_id": txn_id, "block_number": block_number})

    return owned_buildings


def getBuildingState(con, building_id):

    owned_buildings = []
    sql = ("SELECT txn_id, block_number, caller_address, asteroid_id, lot_id, crew_id, building_id, building_type, status FROM buildings WHERE building_id = %s AND status = 3" % (building_id))
    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return owned_buildings

    for row in rows:
        txn_id=row[0]
        block_number=row[1]
        caller_address=row[2]
        asteroid_id=row[3]
        lot_id=row[4]
        crew_id=row[5]
        building_id=row[6]
        building_type=row[7]
        status=row[8]
        owned_buildings.append({"building_id": building_id, "building_type": building_type, "asteroid_id": asteroid_id, "lot_id": lot_id, "crew_id": crew_id, "status": status, "wallet": caller_address, "txn_id": txn_id, "block_number": block_number})

    return owned_buildings


def ownedBuildings(building_type, parameter1, parameter2):

    owned_buildings = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    owned_buildings = getOwnedBuildings(con, building_type, parameter1, parameter2)
    con.close()
    return owned_buildings


def ownedBuildingsOnAsteroid(parameter1, parameter2, asteroid_id):

    owned_buildings = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    owned_buildings = getOwnedBuildingsOnAsteroid(con, parameter1, parameter2, asteroid_id)
    con.close()
    return owned_buildings


def ownedBuildingsOnLot(parameter1, parameter2, asteroid_id, lot_id):

    owned_buildings = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    owned_buildings = getOwnedBuildingsOnLot(con, parameter1, parameter2, asteroid_id, lot_id)
    con.close()
    return owned_buildings


def buildingState(building_id):

    building = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    building = getBuildingState(con, building_id)
    con.close()
    return building
