import sys
import os
import pymysql
import warnings
import traceback
import configparser
import time

sys.path.insert(0,'../')
import db.get_types as inf

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


def getGlobalCrewsPerAsteroid(con):

    asteroids_list = []
    asteroids = []
    sql = "SELECT b.crew_owner, b.crew_id, b.station_id, b.station_label, c.station_id, c.asteroid_id FROM crews b, stations c WHERE b.station_id = c.station_id AND c.asteroid_id IS NOT NULL GROUP BY b.crew_id"
    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return asteroids_list

    for row in rows:
        crew_owner=row[0]
        crew_id=[1]
        station_id=row[2]
        station_label=row[3]
        station_id=row[4]
        asteroid_id=row[5]

        if asteroid_id not in asteroids_list:
            asteroids_list.append(asteroid_id)
            asteroids.append({"asteroid_id": asteroid_id, "wallets": [crew_owner]})
        else:
            for asteroid_row in asteroids:
                if asteroid_row['asteroid_id'] == asteroid_id:
                    if crew_owner not in asteroid_row['wallets']:
                        asteroid_row['wallets'].append(crew_owner)


    return_list = []
    for row in asteroids:
        asteroid_id = row['asteroid_id']
        wallets = row['wallets']
        wallet_count = len(row['wallets'])
        return_list.append({"asteroid_id": asteroid_id, "wallets": wallet_count})

    sorted_return_list = sorted(return_list, key = lambda i: i['wallets'], reverse=True)
    return sorted_return_list


def getGlobalBuildingsOnAsteroid(con, asteroid_id):

    sql = ("SELECT COUNT(*) FROM buildings WHERE asteroid_id = %s AND status = 3" % asteroid_id)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        count=result[0]

    buildings={"buildings": count}

    return buildings



def getGlobalBuildings(con):

    buildings = []
    warehouse = 0
    extractor = 0
    refinery = 0
    bioreactor = 0
    factory = 0
    shipyard = 0
    spaceport = 0
    marketplace = 0
    habitat = 0
    unknown = 0
    total = 0

    sql = "SELECT building_id, building_type FROM buildings WHERE STATUS = 3"
    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return buildings

    for row in rows:
        building_id=row[0]
        building_type=row[1]

        if building_type == 1:
            warehouse+=1
        elif building_type == 2:
            extractor+=1
        elif building_type == 3:
            refinery+=1
        elif building_type == 4:
            bioreactor+=1
        elif building_type == 5:
            factory+=1
        elif building_type == 6:
            shipyard+=1
        elif building_type == 7:
            spaceport+=1
        elif building_type == 8:
            marketplace+=1
        elif building_type == 9:
            habitat+=1
        elif building_type == 99:
            unknown+=1

        total+=1

    buildings = ({"warehouses": warehouse, "extractors": extractor, "refineries": refinery, "bioreactor": bioreactor, "factories": factory, "shipyards": shipyard, "spaceport": spaceport, "marketplace": marketplace, "habitat": habitat, "unknown": unknown, "total": total})
    return buildings


def getGlobalShipsAssembled(con):

    ships = []
    light_transport = 0
    heavy_transport = 0
    shuttle = 0
    total = 0

    sql = "SELECT ship_id, ship_type FROM ship_assembly WHERE STATUS = 2"
    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return buildings

    for row in rows:
        ship_id=row[0]
        ship_type=row[1]

        if ship_type == 2:
            light_transport+=1
        elif ship_type == 3:
            heavy_transport+=1
        elif ship_type == 4:
            shuttle+=1

        total+=1

    ships = ({"light_transports": light_transport, "heavy_transports": heavy_transport, "shuttles": shuttle, "total": total})
    return ships


def getGlobalTonnesExtracted(con):

    tonnes = []
    amount = 0
    sql = "SELECT resource_yield FROM extractions WHERE status = 2"
    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return tonnes

    for row in rows:
        resource_yield=row[0]
        amount+=resource_yield

    tonnes = {"tonnes": amount}
    return tonnes


def getGlobalPropellant(con):

    tonnes = []
    amount = 0
    sql = "SELECT amount FROM propellant_produced"
    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return tonnes

    for row in rows:
        produced_amount = row[0]
        amount+=produced_amount

    tonnes = {"tonnes": amount}
    return tonnes


def getGlobalFood(con):

    tonnes = []
    amount = 0
    sql = "SELECT amount FROM food_produced"
    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return tonnes

    for row in rows:
        produced_amount = row[0]
        amount+=produced_amount

    tonnes = {"tonnes": amount}
    return tonnes


def getGlobalCrewsComposed(con):

    crews = []
    amount = 0
    sql = "SELECT DISTINCT crew_id FROM crewmates WHERE crew_id IS NOT NULL"
    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return crews 

    for row in rows:
        crew_id=row[0]
        amount+=1

    crews = {"crews": amount}
    return crews


def getGlobalCoreSamples(con):

    deposits = []
    sql = "SELECT COUNT(*) FROM core_samples WHERE status = 2"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        count=result[0]

    deposits={"core_samples": count}

    return deposits


def globalCrewsPerAsteroid():

    result = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    result = getGlobalCrewsPerAsteroid(con)
    con.close()
    return result


def globalBuildings():

    result = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    result = getGlobalBuildings(con)
    con.close()
    return result


def globalShipsAssembled():

    result = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    result = getGlobalShipsAssembled(con)
    con.close()
    return result


def globalTonnesExtracted():

    result = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    result = getGlobalTonnesExtracted(con)
    con.close()
    return result


def globalCrewsComposed():

    result = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    result = getGlobalCrewsComposed(con)
    con.close()
    return result


def globalCoreSamples():

    result = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    result = getGlobalCoreSamples(con)
    con.close()
    return result


def globalPropellant():

    result = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    result = getGlobalPropellant(con)
    con.close()
    return result


def globalFood():

    result = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    result = getGlobalFood(con)
    con.close()
    return result


def globalBuildingsOnAsteroid(asteroid_id):

    result = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    result = getGlobalBuildingsOnAsteroid(con, asteroid_id)
    con.close()
    return result



