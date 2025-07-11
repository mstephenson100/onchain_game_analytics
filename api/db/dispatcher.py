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


def getAsteroidOwner(con, asteroid_id):

    asteroid_owner = {} 
    sql = ("SELECT asteroid_owner, crew_id FROM asteroids WHERE asteroid_id = %s" % asteroid_id)
    print(sql)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        cur.close()
        asteroid_owner=result[0]
        crew_id=result[1]

    asteroid_owner = {"asteroid_id": asteroid_id, "asteroid_owner": asteroid_owner, "crew_id": crew_id}
    return asteroid_owner


def getOwnedAsteroids(con, wallet):

    asteroids=[]
    sql = ("SELECT asteroid_id, asteroid_owner, name, bonuses, radius, spectral_type, scan_status, crew_id, initialized, surface_scan, resource_scan, random_seed FROM asteroids WHERE asteroid_owner = '%s'" % (wallet))
    print(sql)

    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return asteroids

    for row in rows:
        asteroid_id=row[0]
        owner=row[1]
        name=row[2]
        bonuses=row[3]
        radius=row[4]
        spectral_type=row[5]
        scan_status=row[6]
        crew_id=row[7]
        initialized=row[8]
        surface_scan=row[9]
        resource_scan=row[10]
        random_seed=row[11]

        spectral_type = get_types.getSpectralTypes(int(spectral_type))
        scan_status = get_types.getScanStatuses(int(scan_status))

        asteroids.append({"asteroid_id": asteroid_id, "owner": owner, "name": name, "bonuses": bonuses, "radius": radius, "spectral_type": spectral_type, "crew_id": crew_id, "initialized": initialized, "scan_status": scan_status, "random_seed": random_seed})

    return asteroids


def getPoliciesAppliedBy(con, parameter1, parameter2):

    policies=[]
    if parameter1 == 'wallet':
        sql = ("SELECT txn_id, block_number, caller_address, entity_label, entity_id, permission, caller_crew_id FROM public_policies WHERE caller_address = '%s'" % (parameter2))

    if parameter1 == 'crew':
        sql = ("SELECT txn_id, block_number, caller_address, entity_label, entity_id, permission, caller_crew_id FROM public_policies WHERE caller_crew_id = %s" % (parameter2))

    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return policies

    for row in rows:
        txn_id=row[0]
        block_number=row[1]
        wallet=row[2]
        entity_label=row[3]
        entity_id=row[4]
        permission=row[5]
        crew_id=row[6]
        entity_type = get_types.getEntityType(int(entity_label))
        permission_type = get_types.getPermission(int(permission))

        policies.append({"asteroid_id": asteroid_id, "owner": owner, "name": name, "bonuses": bonuses, "radius": radius, "spectral_type": spectral_type, "crew_id": crew_id, "initialized": initialized, "scan_status": scan_status, "random_seed": random_seed, "water": water, "hydrogen": hydrogen, "amonia": amonia, "nitrogen": nitrogen, "sulfur_dioxide": sulfur_dioxide, "carbon_dioxide": carbon_dioxide, "carbon_monoxide": carbon_monoxide, "methane": methane, "apatite": apatite, "bitumen": bitumen, "calcite": calcite, "feldspar": feldspar, "olivine": olivine, "pyroxene": pyroxene, "coffinite": coffinite, "merrillite": merrillite, "xenotime": xenotime, "rhadbdite": rhadbdite, "graphite": graphite, "taenite": taenite, "troilite": troilite, "uranite": uranite})

    return asteroids


def getManagedAsteroids(con, parameter1, parameter2):

    asteroids=[]
    if parameter1 == 'wallet':
        sql = ("SELECT asteroid_id, asteroid_owner, name, bonuses, radius, spectral_type, scan_status, crew_id, initialized, surface_scan, resource_scan, random_seed FROM asteroids WHERE asteroid_owner = '%s' AND crew_id is not NULL" % (parameter2))

    if parameter1 == 'crew':
        sql = ("SELECT asteroid_id, asteroid_owner, name, bonuses, radius, spectral_type, scan_status, crew_id, initialized, surface_scan, resource_scan, random_seed FROM asteroids WHERE crew_id = %s AND crew_id is not NULL" % (parameter2))

    print(sql)

    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return asteroids

    for row in rows:
        asteroid_id=row[0]
        owner=row[1]
        name=row[2]
        bonuses=row[3]
        radius=row[4]
        spectral_type=row[5]
        scan_status=row[6]
        crew_id=row[7]
        initialized=row[8]
        surface_scan=row[9]
        resource_scan=row[10]
        random_seed=row[11]

        spectral_type = get_types.getSpectralTypes(int(spectral_type))
        scan_status = get_types.getScanStatuses(int(scan_status))

        asteroids.append({"asteroid_id": asteroid_id, "owner": owner, "name": name, "bonuses": bonuses, "radius": radius, "spectral_type": spectral_type, "crew_id": crew_id, "initialized": initialized, "scan_status": scan_status, "random_seed": random_seed})

    return asteroids


def getUnmanagedAsteroids(con, wallet):

    asteroids=[]
    sql = ("SELECT asteroid_id, asteroid_owner, name, bonuses, radius, spectral_type, scan_status, crew_id, initialized, surface_scan, resource_scan, random_seed FROM asteroids WHERE asteroid_owner = '%s' AND crew_id is NULL" % (wallet))
    print(sql)

    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return asteroids

    for row in rows:
        asteroid_id=row[0]
        owner=row[1]
        name=row[2]
        bonuses=row[3]
        radius=row[4]
        spectral_type=row[5]
        scan_status=row[6]
        crew_id=row[7]
        initialized=row[8]
        surface_scan=row[9]
        resource_scan=row[10]
        random_seed=row[11]

        spectral_type = get_types.getSpectralTypes(int(spectral_type))
        scan_status = get_types.getScanStatuses(int(scan_status))

        asteroids.append({"asteroid_id": asteroid_id, "owner": owner, "name": name, "bonuses": bonuses, "radius": radius, "spectral_type": spectral_type, "crew_id": crew_id, "initialized": initialized, "scan_status": scan_status, "random_seed": random_seed})

    return asteroids


def getAsteroid(con, asteroid_id):

    asteroid = {}
    sql = ("SELECT asteroid_id, asteroid_owner, name, bonuses, radius, spectral_type, scan_status, crew_id, initialized, surface_scan, resource_scan, random_seed, water, hydrogen, amonia, nitrogen, sulfur_dioxide, carbon_dioxide, carbon_monoxide, methane, apatite, bitumen, calcite, feldspar, olivine, pyroxene, coffinite, merrillite, xenotime, rhadbdite, graphite, taenite, troilite, uranite FROM asteroids WHERE asteroid_id = %s" % (asteroid_id))
    print(sql)

    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return asteroid

    for row in rows:
        print(row)
        asteroid_id=row[0]
        asteroid_owner=row[1]
        asteroid_name=row[2]
        bonuses=row[3]
        radius=row[4]
        spectral_type=row[5]
        scan_status=row[6]
        crew_id=row[7]
        initialized=row[8]
        surface_scan=row[9]
        resource_scan=row[10]
        random_seed=row[11]
        water=row[12]
        hydrogen=row[13]
        amonia=row[14]
        nitrogen=row[15]
        sulfur_dioxide=row[16]
        carbon_dioxide=row[17]
        carbon_monoxide=row[18]
        methane=row[19]
        apatite=row[20]
        bitumen=row[21]
        calcite=row[22]
        feldspar=row[23]
        olivine=row[24]
        pyroxene=row[25]
        coffinite=row[26]
        merrillite=row[27]
        xenotime=row[28]
        rhadbdite=row[29]
        graphite=row[30]
        taenite=row[31]
        troilite=row[32]
        uranite=row[33]
        spectral_type = get_types.getSpectralTypes(int(spectral_type))
        scan_status = get_types.getScanStatuses(int(scan_status))

        asteroid = {"asteroid_id": asteroid_id, "owner": asteroid_owner, "name": asteroid_name, "bonuses": bonuses, "radius": radius, "spectral_type": spectral_type, "crew_id": crew_id, "initialized": initialized, "scan_status": scan_status, "random_seed": random_seed, "water": water, "hydrogen": hydrogen, "amonia": amonia, "nitrogen": nitrogen, "sulfur_dioxide": sulfur_dioxide, "carbon_dioxide": carbon_dioxide, "carbon_monoxide": carbon_monoxide, "methane": methane, "apatite": apatite, "bitumen": bitumen, "calcite": calcite, "feldspar": feldspar, "olivine": olivine, "pyroxene": pyroxene, "coffinite": coffinite, "merrillite": merrillite, "xenotime": xenotime, "rhadbdite": rhadbdite, "graphite": graphite, "taenite": taenite, "troilite": troilite, "uranite": uranite}

    return asteroid


def asteroidOwner(asteroid_id):

    asteroid_owner = None
    asteroid_owner = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    asteroid_owner = getAsteroidOwner(con, asteroid_id)
    con.close()
    return asteroid_owner


def asteroid(asteroid_id):

    asteroid = {}
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    asteroid = getAsteroid(con, asteroid_id)
    con.close()
    return asteroid


def ownedAsteroids(wallet):

    owned_asteroids = None
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    owned_asteroids = getOwnedAsteroids(con, wallet)
    con.close()
    return owned_asteroids


def policiesAppliedBy(parameter1, parameter2):

    policies = None
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    policies = getPoliciesAppliedBy(con, parameter1, parameter2)
    con.close()
    return policies

def unmanagedAsteroids(wallet):

    unmanaged_asteroids = None
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    unmanaged_asteroids = getUnmanagedAsteroids(con, wallet)
    con.close()
    return unmanaged_asteroids


def scannedAsteroids(parameter1, parameter2):

    scanned_asteroids = None
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    scanned_asteroids = getScannedAsteroids(con, parameter1, parameter2)
    con.close()
    return scanned_asteroids

