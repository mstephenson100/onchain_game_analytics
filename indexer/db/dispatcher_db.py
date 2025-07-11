import sys
import os
import pymysql
import warnings
import traceback
import configparser
import sdk.sdk as sdk
import sdk.components as component

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


def cleanBadCharacters(string):

    bad_chars = [';', ':', '!', "*", "'", '-', '(', ')', '’']
    string = ''.join(i for i in string if not i in bad_chars)
    return string


def assignImpactful(impactful_traits):

    if len(impactful_traits) == 6:
        impactful_1 = impactful_traits[0]
        impactful_2 = impactful_traits[1]
        impactful_3 = impactful_traits[2]
        impactful_4 = impactful_traits[3]
        impactful_5 = impactful_traits[4]
        impactful_6 = impactful_traits[5]
    elif len(impactful_traits) == 5:
        impactful_1 = impactful_traits[0]
        impactful_2 = impactful_traits[1]
        impactful_3 = impactful_traits[2]
        impactful_4 = impactful_traits[3]
        impactful_5 = impactful_traits[4]
        impactful_6 = "NULL"
    elif len(impactful_traits) == 4:
        impactful_1 = impactful_traits[0]
        impactful_2 = impactful_traits[1]
        impactful_3 = impactful_traits[2]
        impactful_4 = impactful_traits[3]
        impactful_5 = "NULL"
        impactful_6 = "NULL"
    elif len(impactful_traits) == 3:
        impactful_1 = impactful_traits[0]
        impactful_2 = impactful_traits[1]
        impactful_3 = impactful_traits[2]
        impactful_4 = "NULL"
        impactful_5 = "NULL"
        impactful_6 = "NULL"
    elif len(impactful_traits) == 2:
        impactful_1 = impactful_traits[0]
        impactful_2 = impactful_traits[1]
        impactful_3 = "NULL"
        impactful_4 = "NULL"
        impactful_5 = "NULL"
        impactful_6 = "NULL"
    elif len(impactful_traits) == 1:
        impactful_1 = impactful_traits[0]
        impactful_2 = "NULL"
        impactful_3 = "NULL"
        impactful_4 = "NULL"
        impactful_5 = "NULL"
        impactful_6 = "NULL"

    return impactful_1, impactful_2, impactful_3, impactful_4, impactful_5, impactful_6


def assignCrewmates(composition):

    if len(composition) == 5:
        crewmate_1 = composition[0]
        crewmate_2 = composition[1]
        crewmate_3 = composition[2]
        crewmate_4 = composition[3]
        crewmate_5 = composition[4]
    elif len(composition) == 4:
        crewmate_1 = composition[0]
        crewmate_2 = composition[1]
        crewmate_3 = composition[2]
        crewmate_4 = composition[3]
        crewmate_5 = "NULL"
    elif len(composition) == 3:
        crewmate_1 = composition[0]
        crewmate_2 = composition[1]
        crewmate_3 = composition[2]
        crewmate_4 = "NULL"
        crewmate_5 = "NULL"
    elif len(composition) == 2:
        crewmate_1 = composition[0]
        crewmate_2 = composition[1]
        crewmate_3 = "NULL"
        crewmate_4 = "NULL"
        crewmate_5 = "NULL"
    elif len(composition) == 1:
        crewmate_1 = composition[0]
        crewmate_2 = "NULL"
        crewmate_3 = "NULL"
        crewmate_4 = "NULL"
        crewmate_5 = "NULL"
    else:
        crewmate_1 = "NULL"
        crewmate_2 = "NULL"
        crewmate_3 = "NULL"
        crewmate_4 = "NULL"
        crewmate_5 = "NULL"

    return crewmate_1, crewmate_2, crewmate_3, crewmate_4, crewmate_5


def deleteOldSystemRegistered(name):

    update_sql = ("DELETE FROM systems_registered WHERE name = '%s'" % name)
    print(update_sql)
    updateSql(update_sql)


def systemRegistered(tx_hash, block_number, from_address, class_hash, name, fee, timestamp):

    deleteOldSystemRegistered(name)
    insert_sql = ("INSERT IGNORE INTO dispatcher_system_registered (txn_id, block_number, from_address, class_hash, name, fee, timestamp) VALUES ('%s', %s, '%s', '%s', '%s', %s, '%s')" % (tx_hash, block_number, from_address, class_hash, name, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)
    insert_sql2 = ("INSERT IGNORE INTO systems_registered (txn_id, block_number, from_address, class_hash, name) VALUES ('%s', %s, '%s', '%s', '%s')" % (tx_hash, block_number, from_address, class_hash, name))
    updateSql(insert_sql2)


def surfaceScanStarted(tx_hash, block_number, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id, finish_time, fee, timestamp):

    scan_status = 1
    insert_sql = ("INSERT IGNORE INTO dispatcher_surface_scan_started (txn_id, block_number, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id, finish_time, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id, finish_time, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)
    updateAsteroid(tx_hash, block_number, asteroid_id)
    update_sql = ("UPDATE asteroids SET scan_status = 1 WHERE asteroid_id = %s" % asteroid_id)
    print(update_sql)
    updateSql(update_sql)

    crew_asteroid_id = asteroid_id
    crew_lot_id = None
    crew_ship_id = None
    action = "SurfaceScanStarted"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def surfaceScanFinished(tx_hash, block_number, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id, bonuses, fee, timestamp):

    scan_status = 2
    insert_sql = ("INSERT IGNORE INTO dispatcher_surface_scan_finished (txn_id, block_number, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id, bonuses, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id, bonuses, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)
    updateAsteroid(tx_hash, block_number, asteroid_id)
    update_sql = ("UPDATE asteroids SET bonuses = %s, scan_status = %s, surface_scan = %s WHERE asteroid_id = %s" % (bonuses, scan_status, scan_status, asteroid_id))
    print(update_sql)
    updateSql(update_sql)
    queueGrab(tx_hash, block_number, 1, asteroid_id)

    crew_asteroid_id = asteroid_id
    crew_lot_id = None
    crew_ship_id = None
    action = "SurfaceScanFinished"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def crewmateRecruitedV1(tx_hash, block_number, from_address, caller_address, caller_crew_id, caller_crew_label, crewmate_label, crewmate_id, collection, class_name, title, impactful_traits, name, station_label, station_id, fee, timestamp):

    impactful_1, impactful_2, impactful_3, impactful_4, impactful_5, impactful_6 = assignImpactful(impactful_traits)
    insert_sql = ("INSERT IGNORE INTO dispatcher_crewmate_recruited_v1 (txn_id, block_number, from_address, caller_address, caller_crew_id, caller_crew_label, crewmate_label, crewmate_id, collection, class, title, impactful_1, impactful_2, impactful_3, impactful_4, impactful_5, impactful_6, name, station_label, station_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s', %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_id, caller_crew_label, crewmate_label, crewmate_id, collection, class_name, title, impactful_1, impactful_2, impactful_3, impactful_4, impactful_5, impactful_6, name, station_label, station_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    entity_type, asteroid_id, lot_id = getBuildingData(station_id)
    updateCrewmate(tx_hash, block_number, crewmate_id)
    update_sql = ("UPDATE crewmates SET name = '%s', impactful_1 = %s, impactful_2 = %s, impactful_3 = %s, impactful_4 = %s, impactful_5 = %s, impactful_6 = %s, collection = %s, class = %s, title = %s, crew_id = %s, station_label = %s, station_id = %s, origin_asteroid_id = %s WHERE crewmate_id = %s" % (name, impactful_1, impactful_2, impactful_3, impactful_4, impactful_5, impactful_6, collection, class_name, title, caller_crew_id, station_label, station_id, asteroid_id, crewmate_id))
    print(update_sql)
    updateSql(update_sql)

    origin_asteroid_id = getOriginAsteroidId(caller_crew_id)
    if origin_asteroid_id == asteroid_id:
        origin_asteroid_id = asteroid_id
    else:
        if origin_asteroid_id is None:
            origin_asteroid_id = asteroid_id

    if caller_crew_id == 1:
        origin_asteroid_id = 1

    updateCrew(tx_hash, block_number, caller_crew_id, timestamp)
    update_crew_sql = ("UPDATE crews SET station_id = %s, station_label = %s, origin_asteroid_id = %s WHERE crew_id = %s" % (station_id, station_label, origin_asteroid_id, caller_crew_id))
    print(update_crew_sql)
    updateSql(update_crew_sql)
    queueGrab(tx_hash, block_number, 2, crewmate_id)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def crewmateRecruited(tx_hash, block_number, from_address, caller_address, caller_crew_id, caller_crew_label, crewmate_label, crewmate_id, collection, class_name, title, impactful_traits, station_label, station_id, fee, timestamp):

    impactful_1, impactful_2, impactful_3, impactful_4, impactful_5, impactful_6 = assignImpactful(impactful_traits)
    insert_sql = ("INSERT IGNORE INTO dispatcher_crewmate_recruited (txn_id, block_number, from_address, caller_address, caller_crew_id, caller_crew_label, crewmate_label, crewmate_id, collection, class, title, impactful_1, impactful_2, impactful_3, impactful_4, impactful_5, impactful_6, station_label, station_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,  %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_id, caller_crew_label, crewmate_label, crewmate_id, collection, class_name, title, impactful_1, impactful_2, impactful_3, impactful_4, impactful_5, impactful_6, station_label, station_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    entity_type, asteroid_id, lot_id = getBuildingData(station_id)
    updateCrewmate(tx_hash, block_number, crewmate_id)
    update_sql = ("UPDATE crewmates SET impactful_1 = %s, impactful_2 = %s, impactful_3 = %s, impactful_4 = %s, impactful_5 = %s, impactful_6 = %s, collection = %s, class = %s, title = %s, crew_id = %s, origin_asteroid_id = %s WHERE crewmate_id = %s" % (impactful_1, impactful_2, impactful_3, impactful_4, impactful_5, impactful_6, collection, class_name, title, caller_crew_id, asteroid_id, crewmate_id))
    print(update_sql)
    updateSql(update_sql)

    updateCrew(tx_hash, block_number, caller_crew_id, timestamp)

    origin_asteroid_id = getOriginAsteroidId(caller_crew_id)
    if origin_asteroid_id == asteroid_id:
        origin_asteroid_id = asteroid_id


    update_crew_sql = ("UPDATE crews SET station_id = %s, origin_asteroid_id = %s WHERE crew_id = %s" % (station_id, origin_asteroid_id, caller_crew_id))
    print(update_crew_sql)
    updateSql(update_crew_sql)
    queueGrab(tx_hash, block_number, 2, crewmate_id)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def asteroidInitialized(tx_hash, block_number, from_address, asteroid_label, asteroid_id, fee, timestamp):

    insert_sql = ("INSERT IGNORE INTO dispatcher_asteroid_initialized (txn_id, block_number, from_address, asteroid_label, asteroid_id, fee, timestamp) VALUES ('%s', %s, '%s', %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, asteroid_label, asteroid_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)
    updateAsteroid(tx_hash, block_number, asteroid_id)
    update_sql = ("UPDATE asteroids SET initialized = 1 WHERE asteroid_id = %s" % asteroid_id)
    print(update_sql)
    updateSql(update_sql)


def asteroidManaged(tx_hash, block_number, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id, fee, timestamp):

    insert_sql = ("INSERT IGNORE INTO dispatcher_asteroid_managed (txn_id, block_number, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)
    updateAsteroid(tx_hash, block_number, asteroid_id)
    update_sql = ("UPDATE asteroids SET crew_id = %s WHERE asteroid_id = %s" % (caller_crew_id, asteroid_id))
    print(update_sql)
    updateSql(update_sql)

    crew_asteroid_id = asteroid_id
    crew_lot_id = None
    crew_ship_id = None
    action = "AsteroidManaged"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def asteroidPurchased(tx_hash, block_number, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id, fee, timestamp):

    insert_sql = ("INSERT IGNORE INTO dispatcher_asteroid_purchased (txn_id, block_number, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)
    updateAsteroid(tx_hash, block_number, asteroid_id)
    update_sql = ("UPDATE asteroids SET crew_id = %s WHERE asteroid_id = %s" % (caller_crew_id, asteroid_id))
    print(update_sql)
    updateSql(update_sql)
    queueGrab(tx_hash, block_number, 1, asteroid_id)

    crew_asteroid_id = asteroid_id
    crew_lot_id = None
    crew_ship_id = None
    action = "AsteroidPurchased"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)



def crewmatePurchased(tx_hash, block_number, from_address, caller_address, crewmate_label, crewmate_id, fee, timestamp):

    collection = 4
    insert_sql = ("INSERT IGNORE INTO dispatcher_crewmate_purchased (txn_id, block_number, from_address, caller_address, crewmate_label, crewmate_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, crewmate_label, crewmate_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)


def updateCrewComposition(tx_hash, block_number, from_address, caller_address, composition, crew_id):

    delete_sql = ("DELETE FROM crew_composition WHERE crew_id = %s" % crew_id)
    print(delete_sql)
    updateSql(delete_sql)

    for crewmate_id in composition:

        insert_sql = ("INSERT IGNORE INTO crew_composition (txn_id, block_number, from_address, caller_address, crew_id, crewmate_id) VALUES ('%s', %s, '%s', '%s', %s, %s)" % (tx_hash, block_number, from_address, caller_address, crew_id, crewmate_id))
        print(insert_sql)
        updateSql(insert_sql)

        updateCrewmate(tx_hash, block_number, crewmate_id)
        update_sql = ("UPDATE crewmates SET crew_id = %s WHERE crewmate_id = %s" % (crew_id, crewmate_id))
        print(update_sql)
        updateSql(update_sql)


def crewmatesArrangedV1(tx_hash, block_number, from_address, caller_address, composition_old, composition_new, caller_crew_label, caller_crew_id, fee, timestamp):

    old_crewmate_1, old_crewmate_2, old_crewmate_3, old_crewmate_4, old_crewmate_5 = assignCrewmates(composition_old)
    new_crewmate_1, new_crewmate_2, new_crewmate_3, new_crewmate_4, new_crewmate_5 = assignCrewmates(composition_new)
    insert_sql = ("INSERT IGNORE INTO dispatcher_crewmates_arranged_v1 (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, old_crewmate_1, old_crewmate_2, old_crewmate_3, old_crewmate_4, old_crewmate_5, new_crewmate_1, new_crewmate_2, new_crewmate_3, new_crewmate_4, new_crewmate_5, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, old_crewmate_1, old_crewmate_2, old_crewmate_3, old_crewmate_4, old_crewmate_5, new_crewmate_1, new_crewmate_2, new_crewmate_3, new_crewmate_4, new_crewmate_5, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)
    updateCrewComposition(tx_hash, block_number, from_address, caller_address, composition_new, caller_crew_id)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def crewmatesExchanged(tx_hash, block_number, from_address, caller_address, crew1_label, crew1_id, crew1_composition_old, crew1_composition_new, crew2_label, crew2_id, crew2_composition_old, crew2_composition_new, fee, timestamp):

    crew1_old_crewmate_1, crew1_old_crewmate_2, crew1_old_crewmate_3, crew1_old_crewmate_4, crew1_old_crewmate_5 = assignCrewmates(crew1_composition_old)
    crew1_new_crewmate_1, crew1_new_crewmate_2, crew1_new_crewmate_3, crew1_new_crewmate_4, crew1_new_crewmate_5 = assignCrewmates(crew1_composition_new)
    crew2_old_crewmate_1, crew2_old_crewmate_2, crew2_old_crewmate_3, crew2_old_crewmate_4, crew2_old_crewmate_5 = assignCrewmates(crew2_composition_old)
    crew2_new_crewmate_1, crew2_new_crewmate_2, crew2_new_crewmate_3, crew2_new_crewmate_4, crew2_new_crewmate_5 = assignCrewmates(crew2_composition_new)

    insert_sql = ("INSERT IGNORE INTO dispatcher_crewmates_exchanged (txn_id, block_number, from_address, caller_address, crew1_label, crew1_id, crew2_label, crew2_id, crew1_old_crewmate_1, crew1_old_crewmate_2, crew1_old_crewmate_3, crew1_old_crewmate_4, crew1_old_crewmate_5, crew1_new_crewmate_1, crew1_new_crewmate_2, crew1_new_crewmate_3, crew1_new_crewmate_4, crew1_new_crewmate_5, crew2_old_crewmate_1, crew2_old_crewmate_2, crew2_old_crewmate_3, crew2_old_crewmate_4, crew2_old_crewmate_5, crew2_new_crewmate_1, crew2_new_crewmate_2, crew2_new_crewmate_3, crew2_new_crewmate_4, crew2_new_crewmate_5, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, crew1_label, crew1_id, crew2_label, crew2_id, crew1_old_crewmate_1, crew1_old_crewmate_2, crew1_old_crewmate_3, crew1_old_crewmate_4, crew1_old_crewmate_5, crew1_new_crewmate_1, crew1_new_crewmate_2, crew1_new_crewmate_3, crew1_new_crewmate_4, crew1_new_crewmate_5, crew2_old_crewmate_1, crew2_old_crewmate_2, crew2_old_crewmate_3, crew2_old_crewmate_4, crew2_old_crewmate_5, crew2_new_crewmate_1, crew2_new_crewmate_2, crew2_new_crewmate_3, crew2_new_crewmate_4, crew2_new_crewmate_5, fee, timestamp))

    print(insert_sql)
    updateSql(insert_sql)

    updateCrewComposition(tx_hash, block_number, from_address, caller_address, crew1_composition_old, crew1_id)
    updateCrewComposition(tx_hash, block_number, from_address, caller_address, crew2_composition_old, crew2_id)
    updateCrewComposition(tx_hash, block_number, from_address, caller_address, crew1_composition_new, crew1_id)
    updateCrewComposition(tx_hash, block_number, from_address, caller_address, crew2_composition_new, crew2_id)


    crew1_origin_id = getOriginAsteroidId(crew1_id)
    crew2_origin_id = getOriginAsteroidId(crew2_id)
    asteroid_id = None

    crew_state = checkCrew(crew2_id)
    station_label, station_id = getStation(crew1_id)
    if station_label is not None or station_id is not None:
        asteroid_id, lot_id = getStationLocation(station_label, station_id)
        if asteroid_id == 'NULL':
            asteroid_id = getOriginAsteroidId(crew1_id)
            if asteroid_id is None:
                asteroid_id = 'NULL'

    if asteroid_id == 'NULL':
        station_label, station_id = getStation(crew2_id)
        if station_label is None or station_id is None:
            station_label = 'NULL'
            station_id = 'NULL'
            asteroid_id = 'NULL'
        else:
            asteroid_id, lot_id = getStationLocation(station_label, station_id)

    if crew_state < 1:
        updateCrew(tx_hash, block_number, crew2_id, timestamp)

    if crew2_origin_id is None or crew2_origin_id == 'NULL':
        asteroid_id = asteroid_id
    else:
        asteroid_id = crew2_origin_id

    if asteroid_id is None:
        asteroid_id = 'NULL'
        station_label = 'NULL'
        station_id = 'NULL'

    if station_label is None:
        station_label = 'NULL'
    
    if station_id is None:
        station_id = 'NULL'

    update_sql=("UPDATE crews SET delegated_address = '%s', station_label = %s, station_id = %s, origin_asteroid_id = %s WHERE crew_id = %s" % (caller_address, station_label, station_id, asteroid_id, crew2_id))
    print(update_sql)
    updateSql(update_sql)


def crewFormed(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, composition, fee, timestamp):

    crewmate_1, crewmate_2, crewmate_3, crewmate_4, crewmate_5 = assignCrewmates(composition)
    insert_sql = ("INSERT IGNORE INTO dispatcher_crew_formed (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, crewmate_1, crewmate_2, crewmate_3, crewmate_4, crewmate_5, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, crewmate_1, crewmate_2, crewmate_3, crewmate_4, crewmate_5, fee, timestamp))
    updateSql(insert_sql)

    updateCrewComposition(tx_hash, block_number, from_address, caller_address, composition, caller_crew_id)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def deleteOldConstant(name):

    update_sql = ("DELETE FROM constants WHERE name = '%s'" % name)
    print(update_sql)
    updateSql(update_sql)


def constantRegistered(tx_hash, block_number, from_address, name, value, fee, timestamp):

    deleteOldConstant(name)

    insert_sql = ("INSERT IGNORE INTO dispatcher_constant_registered (txn_id, block_number, from_address, name, value, fee, timestamp) VALUES ('%s', %s, '%s', '%s', '%s', %s, '%s')" % (tx_hash, block_number, from_address, name, value, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)
    insert_sql2 = ("INSERT IGNORE INTO constants (txn_id, block_number, from_address, name, value) VALUES ('%s', %s, '%s', '%s', '%s')" % (tx_hash, block_number, from_address, name, value))
    updateSql(insert_sql2)


def deleteOldContract(name):

    update_sql = ("DELETE FROM contracts WHERE name = '%s'" % name)
    print(update_sql)
    updateSql(update_sql)


def contractRegistered(tx_hash, block_number, from_address, name, contract, fee, timestamp):

    deleteOldContract(name)

    insert_sql = ("INSERT IGNORE INTO dispatcher_contract_registered (txn_id, block_number, from_address, name, contract, fee, timestamp) VALUES ('%s', %s, '%s', '%s', '%s', %s, '%s')" % (tx_hash, block_number, from_address, name, contract, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)
    insert_sql2 = ("INSERT IGNORE INTO contracts (txn_id, block_number, from_address, name, contract) VALUES ('%s', %s, '%s', '%s', '%s')" % (tx_hash, block_number, from_address, name, contract))
    updateSql(insert_sql2)


def deleteOldPublicPolicy(entity_label, entity_id, caller_crew_label, caller_crew_id):

    update_sql = ("DELETE FROM public_policies WHERE entity_label = %s AND entity_id = %s AND crew_id = %s" % (entity_label, entity_id, caller_crew_id))
    print(update_sql)
    updateSql(update_sql)

    if entity_label == 5:
        entity_type, asteroid_id, lot_id = getBuildingData(entity_id)
        crew_ship_id = None
    elif entity_label == 6:
        entity_type, asteroid_id, lot_id = getShipData(entity_id)
        crew_ship_id = entity_id

    crew_asteroid_id = asteroid_id
    crew_lot_id = lot_id

    action = "DeletePublicPolicy"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def publicPolicyAssigned(tx_hash, event, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, entity_name, fee, timestamp):

    insert_sql = ("INSERT IGNORE INTO dispatcher_public_policy_assigned (txn_id, block_number, from_address, caller_address, entity_label, entity_id, permission, caller_crew_label, caller_crew_id, entity_name, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, '%s', %s, '%s')" % (tx_hash, block_number, from_address, caller_address, entity_label, entity_id, permission, caller_crew_label, caller_crew_id, entity_name, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    if entity_label == 5:
        entity_type, asteroid_id, lot_id = getBuildingData(entity_id)
        crew_ship_id = None
    elif entity_label == 6:
        entity_type, asteroid_id, lot_id = getShipData(entity_id)
        crew_ship_id = entity_id

    policy_count = checkPublicPolicy(entity_label, entity_id, permission)
    if policy_count == 1:
        update_sql = ("UPDATE public_policies SET permission = %s, txn_id = '%s', block_number = %s, from_address = '%s', caller_address = '%s', crew_id = %s, entity_type = %s WHERE entity_label = %s AND entity_id = %s" % (permission, tx_hash, block_number, from_address, caller_address, caller_crew_id, entity_type, entity_label, entity_id))
        print(update_sql)
        updateSql(update_sql)
    else:
        if entity_label == 5:
            insert_sql2 = ("INSERT IGNORE INTO public_policies (txn_id, block_number, from_address, caller_address, crew_id, entity_label, entity_id, entity_type, asteroid_id, lot_id, permission) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s)" % (tx_hash, block_number, from_address, caller_address, caller_crew_id, entity_label, entity_id, entity_type, asteroid_id, lot_id, permission))
        elif entity_label == 6:
            insert_sql2 = ("INSERT IGNORE INTO public_policies (txn_id, block_number, from_address, caller_address, crew_id, entity_label, entity_id, entity_type, permission) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s)" % (tx_hash, block_number, from_address, caller_address, caller_crew_id, entity_label, entity_id, entity_type, permission))
        print(insert_sql2)
        updateSql(insert_sql2)

    crew_asteroid_id = asteroid_id
    crew_lot_id = lot_id
    action = "PublicPolicyAssigned"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def setPublicPolicy(tx_hash, block_number, from_address, caller_address, crew_id, entity_id, entity_type, asteroid_id, lot_id, permission):

    insert_sql = ("INSERT IGNORE INTO public_policies (txn_id, block_number, from_address, caller_address, crew_id, entity_label, entity_id, entity_type, asteroid_id, lot_id, permission) VALUES ('%s', %s, '%s', '%s', %s, 5, %s, %s, %s, %s, %s)" % (tx_hash, block_number, from_address, caller_address, crew_id, entity_id, entity_type, asteroid_id, lot_id, permission))
    print(insert_sql)
    updateSql(insert_sql)


def constructionPlanned(tx_hash, block_number, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id, building_label, building_id, building_type, lot_label, lot_id, packed_lot_id, grace_period_end, fee, timestamp):

    insert_sql = ("INSERT IGNORE INTO dispatcher_construction_planned (txn_id, block_number, from_address, caller_address, building_label, building_id, caller_crew_label, caller_crew_id, building_type, lot_label, lot_id, packed_lot_id, asteroid_label, asteroid_id, grace_period_end, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, building_label, building_id, caller_crew_label, caller_crew_id, building_type, lot_label, lot_id, packed_lot_id, asteroid_label, asteroid_id, grace_period_end, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    updateAsteroid(tx_hash, block_number, asteroid_id)
    updateCrew(tx_hash, block_number, caller_crew_id, timestamp)
    insert_sql2=("INSERT IGNORE INTO buildings (txn_id, block_number, from_address, caller_address, building_label, building_id, crew_id, building_type, lot_id, asteroid_id, grace_period_end, status) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, 1)" % (tx_hash, block_number, from_address, caller_address, building_label, building_id, caller_crew_id, building_type, lot_id, asteroid_id, grace_period_end))
    print(insert_sql2)
    updateSql(insert_sql2)

    crew_asteroid_id = asteroid_id
    crew_lot_id = lot_id
    crew_ship_id = None

    action = "ConstructionPlanned"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def constructionStarted(tx_hash, block_number, from_address, caller_address, building_label, building_id, finish_time, caller_crew_label, caller_crew_id, fee, timestamp):

    insert_sql = ("INSERT IGNORE INTO dispatcher_construction_started (txn_id, block_number, from_address, caller_address, building_label, building_id, finish_time, caller_crew_label, caller_crew_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, building_label, building_id, finish_time, caller_crew_label, caller_crew_id, fee, timestamp))
    updateSql(insert_sql)
    print(insert_sql)

    updateCrew(tx_hash, block_number, caller_crew_id, timestamp)
    update_sql = ("UPDATE buildings SET status=2, finish_time = %s WHERE building_label = %s AND building_id = %s" % (finish_time, building_label, building_id))
    print(update_sql)
    updateSql(update_sql)

    delete_sql = ("DELETE FROM inventories WHERE inventory_label = 5 AND inventory_id = %s" % building_id)
    print(delete_sql)
    updateSql(delete_sql)

    building_type, asteroid_id, lot_id = getBuildingData(building_id)

    insert_sql2=("INSERT IGNORE INTO construction (start_txn_id, start_block_number, start_timestamp, from_address, caller_address, crew_id, building_label, building_id, building_type, lot_id, asteroid_id, finish_time, status) VALUES ('%s', %s, '%s', '%s', '%s', %s, %s, %s, %s, %s, %s, %s, 1)" % (tx_hash, block_number, timestamp, from_address, caller_address, caller_crew_id, building_label, building_id, building_type, lot_id, asteroid_id, finish_time))
    print(insert_sql2)
    updateSql(insert_sql2)

    materials_to_burn = getToBurn(asteroid_id, lot_id)
    if materials_to_burn is not None:
        origin_type = 4
        for material in materials_to_burn:
            product_id_to_burn = material['product_id']
            product_name_to_burn = material['product_name']
            product_amount_to_burn = material['product_amount']
            insert_sql3=("INSERT IGNORE INTO products_consumed (txn_id, block_number, caller_address, crew_id, origin_type, asteroid_id, lot_id, resource_id, resource_name, resource_amount, timestamp) VALUES ('%s', %s, '%s', %s, %s, %s, %s, %s, '%s', %s, '%s')" % (tx_hash, block_number, caller_address, caller_crew_id, origin_type, asteroid_id, lot_id, product_id_to_burn, product_name_to_burn, product_amount_to_burn, timestamp))
            print(insert_sql3)
            updateSql(insert_sql3)

    update_sql2 = ("UPDATE deliveries SET burned_inventory = 1 WHERE dest_asteroid_id = %s AND dest_lot_id = %s AND burned_inventory = 0" % (asteroid_id, lot_id))
    print(update_sql2)
    updateSql(update_sql2)

    crew_asteroid_id = asteroid_id
    crew_lot_id = lot_id
    crew_ship_id = None
    action = "ConstructionStarted"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def constructionFinished(tx_hash, block_number, from_address, caller_address, building_label, building_id, caller_crew_label, caller_crew_id, start_inventory, fee, timestamp):

    insert_sql = ("INSERT IGNORE INTO dispatcher_construction_finished (txn_id, block_number, from_address, caller_address, building_label, building_id, caller_crew_label, caller_crew_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, building_label, building_id, caller_crew_label, caller_crew_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    updateCrew(tx_hash, block_number, caller_crew_id, timestamp)
    building_count = checkBuilding(building_id)
    if building_count > 0:
        update_sql = ("UPDATE buildings SET status = 3 WHERE building_label = %s AND building_id = %s" % (building_label, building_id))
        print(update_sql)
        updateSql(update_sql)
    else:
        insert_sql2 = ("INSERT IGNORE INTO buildings (txn_id, block_number, from_address, caller_address, building_label, building_id, crew_id, status) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, 3)" % (tx_hash, block_number, from_address, caller_address, building_label, building_id, caller_crew_id))
        print(insert_sql2)
        updateSql(insert_sql2)

        started_status=checkStartStatus(building_id)
        building_type = 99
        if started_status == 0:
            update_sql2 = ("UPDATE buildings SET building_type = %s, asteroid_id = 1, status = 3 WHERE building_id = %s" % (building_type, building_id))
            print(update_sql2)
            updateSql(update_sql2)

    building_type, building_asteroid_id, building_lot_id = getBuildingData(building_id)
    if building_type == 9:
        station_sql=("INSERT IGNORE INTO stations (txn_id, block_number, from_address, caller_address, crew_id, station_id, station_label, asteroid_id, lot_id) VALUES ('%s', %s, '%s', '%s', %s , %s, %s, %s, %s)" % (tx_hash, block_number, from_address, caller_address, caller_crew_id, building_id, building_label, building_asteroid_id, building_lot_id))
        print(station_sql)
        updateSql(station_sql)

    update_sql3 = ("UPDATE construction SET finish_txn_id = '%s', finish_block_number = %s, finish_timestamp = '%s', status = 2 WHERE building_id = %s" % (tx_hash, block_number, timestamp, building_id))
    print(update_sql3)
    updateSql(update_sql3)

    for inventory in start_inventory:
        inv_resource_id = inventory['resource_id']
        inv_resource_name = inventory['resource_name']
        inv_resource_amount = inventory['resource_amount']
        insert_sql2=("INSERT INTO inventories (inventory_label, inventory_id, inventory_slot, inventory_type, resource_id, inventory_amount) VALUES (%s, %s, %s, %s, %s, %s)" % (building_label, building_id, 2, building_type, inv_resource_id, inv_resource_amount))
        print(insert_sql2)
        updateSql(insert_sql2)


    crew_asteroid_id = building_asteroid_id
    crew_lot_id = building_lot_id
    crew_ship_id = None
    action = "ConstructionFinished"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def constructionDeconstructed(tx_hash, block_number, from_address, caller_address, building_label, building_id, caller_crew_label, caller_crew_id, fee, timestamp):

    insert_sql = ("INSERT IGNORE INTO dispatcher_construction_deconstructed (txn_id, block_number, from_address, caller_address, building_label, building_id, caller_crew_label, caller_crew_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, building_label, building_id, caller_crew_label, caller_crew_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    delete_sql = ("UPDATE buildings SET status = 4 WHERE building_id = %s" % building_id)
    print(delete_sql)
    updateSql(delete_sql)

    delete_sql2 = ("DELETE FROM inventories WHERE inventory_id = %s" % building_id)
    print(delete_sql2)
    updateSql(delete_sql2)

    building_type, asteroid_id, lot_id = getBuildingData(building_id)
    crew_asteroid_id = asteroid_id
    crew_lot_id = lot_id
    crew_ship_id = None
    action = "ConstructionDeconstructed"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def constructionAbandoned(tx_hash, block_number, from_address, caller_address, building_label, building_id, caller_crew_label, caller_crew_id, fee, timestamp):

    insert_sql = ("INSERT IGNORE INTO dispatcher_construction_abandoned (txn_id, block_number, from_address, caller_address, building_label, building_id, caller_crew_label, caller_crew_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, building_label, building_id, caller_crew_label, caller_crew_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    delete_sql = ("DELETE FROM buildings WHERE building_label = %s AND building_id = %s" % (building_label, building_id))
    print(delete_sql)
    updateSql(delete_sql)

    building_type, asteroid_id, lot_id = getBuildingData(building_id)

    crew_asteroid_id = asteroid_id
    crew_lot_id = lot_id
    crew_ship_id = None
    action = "ConstructionAbandoned"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def samplingDepositStarted(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, lot_label, lot_id, packed_lot_id, resource_id, resource_name, finish_time, asteroid_id, fee, timestamp):

    insert_sql = ("INSERT IGNORE INTO dispatcher_sampling_deposit_started (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, lot_label, lot_id, packed_lot_id, resource_id, resource_name, finish_time, asteroid_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, '%s', %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, lot_label, lot_id, packed_lot_id, resource_id, resource_name, finish_time, asteroid_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    insert_sql2 = ("INSERT IGNORE INTO core_samples (start_txn_id, start_block_number, start_timestamp, from_address, caller_address, crew_id, deposit_id, lot_id, packed_lot_id, resource_id, resource_name, finish_time, asteroid_id, status) VALUES ('%s', %s, '%s', '%s', '%s', %s, %s, %s, %s, %s, '%s', %s, %s, 1)" % (tx_hash, block_number, timestamp, from_address, caller_address, caller_crew_id, deposit_id, lot_id, packed_lot_id, resource_id, resource_name, finish_time, asteroid_id))
    print(insert_sql2)
    updateSql(insert_sql2)

    crew_asteroid_id = asteroid_id
    crew_lot_id = lot_id
    crew_ship_id = None
    action = "SamplingDepositStarted"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def samplingDepositStartedV1(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, lot_label, lot_id, packed_lot_id, resource_id, resource_name, improving, origin_label, origin_id, origin_slot, finish_time, asteroid_id, origin_inventory, fee, timestamp):


    insert_sql = ("INSERT IGNORE INTO dispatcher_sampling_deposit_started_v1 (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, lot_label, lot_id, packed_lot_id, resource_id, resource_name, finish_time, improving, origin_label, origin_id, origin_slot, asteroid_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, '%s', %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, lot_label, lot_id, packed_lot_id, resource_id, resource_name, finish_time, improving, origin_label, origin_id, origin_slot, asteroid_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    if improving == 1:
        insert_sql2 = ("UPDATE core_samples SET status = 3 WHERE deposit_id = %s AND lot_id = %s" % (deposit_id, packed_lot_id))
    else:
        insert_sql2 = ("INSERT IGNORE INTO core_samples (start_txn_id, start_block_number, start_timestamp, from_address, caller_address, crew_id, deposit_id, lot_id, packed_lot_id, resource_id, resource_name, finish_time, asteroid_id, improving, origin_label, origin_id, origin_slot, status) VALUES ('%s', %s, '%s', '%s', '%s', %s, %s, %s, %s, %s, '%s', %s, %s, %s, %s, %s, %s, 1)" % (tx_hash, block_number, timestamp, from_address, caller_address, caller_crew_id, deposit_id, lot_id, packed_lot_id, resource_id, resource_name, finish_time, asteroid_id, improving, origin_label, origin_id, origin_slot))

    print(insert_sql2)
    updateSql(insert_sql2)

    if origin_label == 5:
        origin_type, origin_asteroid_id, origin_lot_id = getBuildingData(origin_id)
        crew_ship_id = None
    elif origin_label == 6:
        origin_type, origin_asteroid_id, origin_lot_id = getShipData(origin_id)
        crew_ship_id = origin_id


    if len(origin_inventory) == 0:
        delete_sql = ("DELETE FROM inventories WHERE inventory_label = %s AND inventory_id = %s AND inventory_slot = %s AND inventory_type = %s" % (origin_label, origin_id, origin_slot, origin_type))
        print(delete_sql)
        updateSql(delete_sql)
    else:
        for inventory in origin_inventory:
            inv_resource_id = inventory['resource_id']
            inv_resource_name = inventory['resource_name']
            inv_resource_amount = inventory['resource_amount']
            state = getInventoryState(origin_label, origin_id, origin_slot, inv_resource_id)
            if state > 0:
                update_sql2=("UPDATE inventories SET inventory_amount = %s WHERE inventory_label = %s AND inventory_id = %s AND inventory_slot = %s AND inventory_type = %s AND resource_id = %s" % (inv_resource_amount, origin_label, origin_id, origin_slot, origin_type, inv_resource_id))
                print(update_sql2)
                updateSql(update_sql2)
            else:
                insert_sql2=("INSERT INTO inventories (inventory_label, inventory_id, inventory_slot, inventory_type, resource_id, inventory_amount) VALUES (%s, %s, %s, %s, %s, %s)" % (origin_label, origin_id, origin_slot, origin_type, inv_resource_id, inv_resource_amount))
                print(insert_sql2)
                updateSql(insert_sql2)

    crew_asteroid_id = asteroid_id
    crew_lot_id = lot_id
    action = "SamplingDepositStarted"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def samplingDepositFinished(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, initial_yield, fee, timestamp):

    insert_sql = ("INSERT IGNORE INTO dispatcher_sampling_deposit_finished (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, initial_yield, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, initial_yield, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    previous_initial_yield = getCoreSample(deposit_id)
    new_initial_yield = (previous_initial_yield + initial_yield)

    update_sql = ("UPDATE core_samples SET finish_txn_id = '%s', finish_block_number = %s, finish_timestamp = '%s', initial_yield = %s, status = 2 WHERE deposit_id = %s" % (tx_hash, block_number, timestamp, new_initial_yield, deposit_id))
    print(update_sql)
    updateSql(update_sql)
    asteroid_id, lot_id = getCoreSampleData(deposit_id)

    crew_asteroid_id = asteroid_id
    crew_lot_id = lot_id
    crew_ship_id = None
    action = "SamplingDepositFinished"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def resourceExtractionStarted(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, resource_id, resource_name, resource_yield, extractor_label, extractor_id, extractor_slot, destination_label, destination_id, destination_slot, finish_time, fee, timestamp):

    extractor_type, extractor_asteroid_id, extractor_lot_id = getBuildingData(extractor_id)
    if destination_label == 5:
        destination_type, destination_asteroid_id, destination_lot_id = getBuildingData(destination_id)
    if destination_label == 6:
        destination_type, destination_asteroid_id, destination_lot_id = getShipData(destination_id)

    insert_sql = ("INSERT IGNORE INTO dispatcher_resource_extraction_started (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, resource_id, resource_name, resource_yield, extractor_label, extractor_id, extractor_slot, extractor_type, extractor_asteroid_id, extractor_lot_id,  destination_label, destination_id, destination_slot, destination_type, destination_asteroid_id, destination_lot_id,  finish_time, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, resource_id, resource_name, resource_yield, extractor_label, extractor_id, extractor_slot, extractor_type, extractor_asteroid_id, extractor_lot_id, destination_label, destination_id, destination_slot, destination_type, destination_asteroid_id, destination_lot_id, finish_time, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    insert_sql2=("INSERT IGNORE INTO extractions (start_txn_id, start_block_number, start_timestamp, from_address, caller_address, crew_id, deposit_id, resource_id, resource_name, resource_yield, extractor_id, extractor_slot, extractor_type, extractor_asteroid_id, extractor_lot_id, destination_label, destination_id, destination_slot, destination_type, destination_asteroid_id, destination_lot_id, finish_time, status) VALUES ('%s', %s, '%s', '%s', '%s', %s, %s, %s, '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % (tx_hash, block_number, timestamp, from_address, caller_address, caller_crew_id, deposit_id, resource_id, resource_name, resource_yield, extractor_id, extractor_slot, extractor_type, extractor_asteroid_id, extractor_lot_id, destination_label, destination_id, destination_slot, destination_type, destination_asteroid_id, destination_lot_id, finish_time, 1))
    print(insert_sql2)
    updateSql(insert_sql2)

    initial_yield = getCoreSample(deposit_id)
    new_initial_yield = (initial_yield - resource_yield)
    update_sql=("UPDATE core_samples SET initial_yield = %s WHERE deposit_id = %s AND resource_id = %s" % (new_initial_yield, deposit_id, resource_id))
    print(update_sql)
    updateSql(update_sql)

    if new_initial_yield == 0:
        lot_id, asteroid_id = getLotForDeposit(deposit_id)
        insert_sql3=("INSERT IGNORE INTO core_samples_depleted (txn_id, block_number, caller_address, crew_id, deposit_id, resource_id, resource_name, current_yield, destination_label, destination_id, destination_slot, finish_time, lot_id, asteroid_id) VALUES ('%s', %s, '%s', %s, %s, %s, '%s', %s, %s, %s, %s, %s, %s, %s)" % (tx_hash, block_number, caller_address, caller_crew_id, deposit_id, resource_id, resource_name, new_initial_yield, destination_label, destination_id, destination_slot, finish_time, lot_id, asteroid_id))
        print(insert_sql3)
        updateSql(insert_sql3)

    crew_asteroid_id = extractor_asteroid_id
    crew_lot_id = extractor_lot_id
    crew_ship_id = None
    action = "ResourceExtractionStarted"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def resourceExtractionFinished(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, extractor_label, extractor_id, extractor_slot, resource_id, resource_name, resource_yield, destination_label, destination_id, destination_slot, destination_inventory, fee, timestamp):

    extractor_type, extractor_asteroid_id, extractor_lot_id = getBuildingData(extractor_id)
    if destination_label == 5:
        destination_type, destination_asteroid_id, destination_lot_id = getBuildingData(destination_id)
    if destination_label == 6:
        destination_type, destination_asteroid_id, destination_lot_id = getShipData(destination_id)

    insert_sql = ("INSERT IGNORE INTO dispatcher_resource_extraction_finished (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, extractor_label, extractor_id, extractor_slot, extractor_type, extractor_asteroid_id, extractor_lot_id, resource_id, resource_name, resource_yield, destination_label, destination_id, destination_slot, destination_type, destination_asteroid_id, destination_lot_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s', %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, extractor_label, extractor_id, extractor_slot, extractor_type, extractor_asteroid_id, extractor_lot_id, resource_id, resource_name, resource_yield, destination_label, destination_id, destination_slot, destination_type, destination_asteroid_id, destination_lot_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    update_sql=("UPDATE extractions SET status = 2, finish_txn_id = '%s', finish_block_number = %s, finish_timestamp = '%s'  WHERE extractor_id = %s AND resource_id = %s AND status = 1" % (tx_hash, block_number, timestamp, extractor_id, resource_id))
    print(update_sql)
    updateSql(update_sql)

    for inventory in destination_inventory:
        inv_resource_id = inventory['resource_id']
        inv_resource_name = inventory['resource_name']
        inv_resource_amount = inventory['resource_amount']
        state = getInventoryState(destination_label, destination_id, destination_slot, inv_resource_id)
        if state > 0:
            update_sql2=("UPDATE inventories SET inventory_amount = %s WHERE inventory_label = %s AND inventory_id = %s AND inventory_slot = %s AND inventory_type = %s AND resource_id = %s" % (inv_resource_amount, destination_label, destination_id, destination_slot, destination_type, inv_resource_id))
            print(update_sql2)
            updateSql(update_sql2)
        else:
            insert_sql2=("INSERT INTO inventories (inventory_label, inventory_id, inventory_slot, inventory_type, resource_id, inventory_amount) VALUES (%s, %s, %s, %s, %s, %s)" % (destination_label, destination_id, destination_slot, destination_type, inv_resource_id, inv_resource_amount))
            print(insert_sql2)
            updateSql(insert_sql2)

    crew_asteroid_id = extractor_asteroid_id
    crew_lot_id = extractor_lot_id
    crew_ship_id = None
    action = "ResourceExtractionFinished"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def nameChanged(tx_hash, block_number, from_address, caller_address, entity_label, entity_id, entity_name, caller_crew_label, caller_crew_id, fee, timestamp):

    entity_name = cleanBadCharacters(entity_name)

    insert_sql = ("INSERT IGNORE INTO dispatcher_name_changed (txn_id, block_number, from_address, caller_address, entity_label, entity_id, entity_name, caller_crew_label, caller_crew_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, '%s', %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, entity_label, entity_id, entity_name, caller_crew_label, caller_crew_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    if int(entity_label) == 1:
        updateCrew(tx_hash, block_number, entity_id, timestamp)
        crew_sql = ("UPDATE crews SET name = '%s' WHERE crew_id = %s" % (entity_name, entity_id))
        print(crew_sql)
        updateSql(crew_sql)
    elif int(entity_label) == 3:
        updateAsteroid(tx_hash, block_number, entity_id)
        asteroid_sql = ("UPDATE asteroids SET name = '%s' WHERE asteroid_id = %s" % (entity_name, entity_id))
        print(asteroid_sql)
        updateSql(asteroid_sql)
    elif int(entity_label) == 5:
        updateAsteroid(tx_hash, block_number, entity_id)
        building_sql = ("UPDATE buildings SET name = '%s' WHERE building_id = %s" % (entity_name, entity_id))
        print(building_sql)
        updateSql(building_sql)
    elif int(entity_label) == 6:
        updateShip(tx_hash, block_number, entity_id)
        ship_sql = ("UPDATE ships SET name = '%s' WHERE ship_id = %s" % (entity_name, entity_id))
        print(ship_sql)
        updateSql(ship_sql)

    crew_asteroid_id = None
    crew_lot_id = None
    crew_ship_id = None
    action = "NameChanged"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def resourceScanStarted(tx_hash, block_number, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id, finish_time, fee, timestamp):

    insert_sql = ("INSERT IGNORE INTO dispatcher_resource_scan_started (txn_id, block_number, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id, finish_time, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id, finish_time, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    updateCrew(tx_hash, block_number, caller_crew_id, timestamp)
    updateAsteroid(tx_hash, block_number, asteroid_id)
    update_sql = ("UPDATE asteroids SET scan_status = 3 WHERE asteroid_id = %s" % asteroid_id)
    print(update_sql)
    updateSql(update_sql)

    crew_asteroid_id = asteroid_id
    crew_lot_id = None
    crew_ship_id = None
    action = "ResourceScanStarted"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def resourceScanFinished(block_number, event_type, tx_hash, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id, water, hydrogen, amonia, nitrogen, sulfur_dioxide, carbon_dioxide, carbon_monoxide, methane, apatite, bitumen, calcite, feldspar, olivine, pyroxene, coffinite, merrillite, xenotime, rhadbdite, graphite, taenite, troilite, uranite, fee, timestamp):

    insert_sql = ("INSERT IGNORE INTO dispatcher_resource_scan_finished (txn_id, block_number, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id, water, hydrogen, amonia, nitrogen, sulfur_dioxide, carbon_dioxide, carbon_monoxide, methane, apatite, bitumen, calcite, feldspar, olivine, pyroxene, coffinite, merrillite, xenotime, rhadbdite, graphite, taenite, troilite, uranite, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id, water, hydrogen, amonia, nitrogen, sulfur_dioxide, carbon_dioxide, carbon_monoxide, methane, apatite, bitumen, calcite, feldspar, olivine, pyroxene, coffinite, merrillite, xenotime, rhadbdite, graphite, taenite, troilite, uranite, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    updateAsteroid(tx_hash, block_number, asteroid_id)
    update_sql = ("UPDATE asteroids SET water = %s, hydrogen = %s, amonia = %s, nitrogen = %s, sulfur_dioxide = %s, carbon_dioxide = %s, carbon_monoxide = %s, methane = %s, apatite = %s, bitumen =%s, calcite = %s, feldspar = %s, olivine = %s, pyroxene = %s, coffinite = %s, merrillite = %s, xenotime = %s, rhadbdite = %s, graphite = %s, taenite = %s, troilite = %s, uranite = %s, scan_status = 4 WHERE asteroid_id = %s" % (water, hydrogen, amonia, nitrogen, sulfur_dioxide, carbon_dioxide, carbon_monoxide, methane, apatite, bitumen, calcite, feldspar, olivine, pyroxene, coffinite, merrillite, xenotime, rhadbdite, graphite, taenite, troilite, uranite, asteroid_id))
    print(update_sql)
    updateSql(update_sql)

    crew_asteroid_id = asteroid_id
    crew_lot_id = None
    crew_ship_id = None
    action = "ResourceScanFinished"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def deliveryStarted(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_slot, dest_label, dest_id, dest_slot, delivery_label, delivery_id, finish_time, products, origin_inventory, fee, timestamp):

    origin_asteroid_id = 'NULL'
    origin_lot_id = 'NULL'
    dest_asteroid_id = 'NULL'
    dest_lot_id = 'NULL'

    if origin_label == 5:
        origin_type, origin_asteroid_id, origin_lot_id = getBuildingData(origin_id)

    if dest_label == 5:
        dest_type, dest_asteroid_id, dest_lot_id = getBuildingData(dest_id)

    if origin_label == 6:
        origin_type, origin_asteroid_id, origin_lot_id = getShipData(origin_id)

    if dest_label == 6:
        dest_type, dest_asteroid_id, dest_lot_id = getShipData(dest_id)

    for row in products:
        state = None
        old_inventory_amount = 0
        new_inventory_amount = 0
        print(row)
        # ORIGIN LABEL WILL PROBABLY CHANGE BASED ON INVENTORY TYPE
        insert_sql = ("INSERT IGNORE INTO dispatcher_delivery_started (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_type, origin_slot, origin_asteroid_id, origin_lot_id, dest_label, dest_id, dest_type, dest_slot, dest_asteroid_id, dest_lot_id, delivery_label, delivery_id, finish_time, product_name, product_id, product_amount, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s', %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_type, origin_slot, origin_asteroid_id, origin_lot_id,  dest_label, dest_id, dest_type, dest_slot, dest_asteroid_id, dest_asteroid_id, delivery_label, delivery_id, finish_time, row['name'], row['id'], row['amount'], fee, timestamp))
        print(insert_sql)
        updateSql(insert_sql)

        insert_sql2 = ("INSERT IGNORE INTO deliveries (start_txn_id, start_block_number, start_timestamp, from_address, caller_address, crew_id, origin_label, origin_id, origin_type, origin_slot, origin_asteroid_id, origin_lot_id, dest_label, dest_id, dest_type, dest_slot, dest_asteroid_id, dest_lot_id, delivery_id, finish_time, product_name, product_id, product_amount, status) VALUES ('%s', %s, '%s', '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s', %s, %s, 1)" % (tx_hash, block_number, timestamp, from_address, caller_address, caller_crew_id, origin_label, origin_id, origin_type, origin_slot, origin_asteroid_id, origin_lot_id, dest_label, dest_id, dest_type, dest_slot, dest_asteroid_id, dest_lot_id, delivery_id, finish_time, row['name'], row['id'], row['amount']))
        print(insert_sql2)
        updateSql(insert_sql2)

        insert_sql3 = ("INSERT IGNORE INTO deliveries_pending (txn_id, block_number, from_address, caller_address, crew_id, origin_label, origin_id, origin_type, origin_slot, origin_asteroid_id, origin_lot_id, dest_label, dest_id, dest_type, dest_slot, dest_asteroid_id, dest_lot_id, delivery_id, finish_time, product_name, product_id, product_amount) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s', %s, %s)" % (tx_hash, block_number, from_address, caller_address, caller_crew_id, origin_label, origin_id, origin_type, origin_slot, origin_asteroid_id, origin_lot_id, dest_label, dest_id, dest_type, dest_slot, dest_asteroid_id, dest_lot_id, delivery_id, finish_time, row['name'], row['id'], row['amount']))
        print(insert_sql3)
        updateSql(insert_sql3)

        if origin_label == 5:
            origin_type, origin_asteroid_id, origin_lot_id = getBuildingData(origin_id)
            crew_ship_id = None
        elif origin_label == 6:
            origin_type, origin_asteroid_id, origin_lot_id = getShipData(origin_id)
            crew_ship_id = origin_id

    for inventory in origin_inventory:
        inv_resource_id = inventory['resource_id']
        inv_resource_name = inventory['resource_name']
        inv_resource_amount = inventory['resource_amount']
        state = getInventoryState(origin_label, origin_id, origin_slot, inv_resource_id)
        if state > 0:
            update_sql=("UPDATE inventories SET inventory_amount = %s WHERE inventory_label = %s AND inventory_id = %s AND inventory_slot = %s AND inventory_type = %s AND resource_id = %s" % (inv_resource_amount, origin_label, origin_id, origin_slot, origin_type, inv_resource_id))
            print(update_sql)
            updateSql(update_sql)
        else:
            insert_sql4=("INSERT INTO inventories (inventory_label, inventory_id, inventory_slot, inventory_type, resource_id, inventory_amount) VALUES (%s, %s, %s, %s, %s, %s)" % (origin_label, origin_id, origin_slot, origin_type, inv_resource_id, inv_resource_amount))
            print(insert_sql4)
            updateSql(insert_sql4)

    crew_asteroid_id = origin_asteroid_id
    crew_lot_id = origin_lot_id
    action = "DeliveryStarted"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def deliveryFinished(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, delivery_label, delivery_id, destination_inventory, fee, timestamp):

    insert_sql = ("INSERT IGNORE INTO dispatcher_delivery_finished (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, delivery_label, delivery_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, delivery_label, delivery_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    update_sql = ("UPDATE deliveries SET finish_txn_id = '%s', finish_block_number = %s, finish_timestamp = '%s', status = 2 WHERE delivery_id = %s" % (tx_hash, block_number, timestamp, delivery_id))
    print(update_sql)
    updateSql(update_sql)

    destination_label, destination_id, destination_slot = getDeliveryDestination(delivery_id)
    if destination_label == 5:
        destination_type, destination_asteroid_id, destination_lot_id = getBuildingData(destination_id)
        crew_ship_id = None
    elif destination_label == 6:
        destination_type, destination_asteroid_id, destination_lot_id = getShipData(destination_id)
        crew_ship_id = destination_id

    for inventory in destination_inventory:
        inv_resource_id = inventory['resource_id']
        inv_resource_name = inventory['resource_name']
        inv_resource_amount = inventory['resource_amount']
        print("destination_label: %s" % destination_label)
        print("destination_id: %s" % destination_id)
        print("destination_slot: %s" % destination_slot)
        print("inv_resource_id: %s" % inv_resource_id)
        state = getInventoryState(destination_label, destination_id, destination_slot, inv_resource_id)
        if state > 0:
            update_sql2=("UPDATE inventories SET inventory_amount = %s WHERE inventory_label = %s AND inventory_id = %s AND inventory_slot = %s AND inventory_type = %s AND resource_id = %s" % (inv_resource_amount, destination_label, destination_id, destination_slot, destination_type, inv_resource_id))
            print(update_sql2)
            updateSql(update_sql2)
        else:
            insert_sql2=("INSERT INTO inventories (inventory_label, inventory_id, inventory_slot, inventory_type, resource_id, inventory_amount) VALUES (%s, %s, %s, %s, %s, %s)" % (destination_label, destination_id, destination_slot, destination_type, inv_resource_id, inv_resource_amount))
            print(insert_sql2)
            updateSql(insert_sql2)

    delete_sql = ("DELETE FROM deliveries_pending WHERE delivery_id = %s" % delivery_id)
    print(delete_sql)
    updateSql(delete_sql)

    crew_asteroid_id = destination_asteroid_id
    crew_lot_id = destination_lot_id
    action = "DeliveryFinished"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def deliveryFinishedV1(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_slot, dest_label, dest_id, dest_slot, delivery_label, delivery_id, products, destination_inventory, fee, timestamp):

    origin_asteroid_id = 'NULL'
    origin_lot_id = 'NULL'
    dest_asteroid_id = 'NULL'
    dest_lot_id = 'NULL'

    if origin_label == 5:
        origin_type, origin_asteroid_id, origin_lot_id = getBuildingData(origin_id)

    if dest_label == 5:
        dest_type, dest_asteroid_id, dest_lot_id = getBuildingData(dest_id)
        crew_ship_id = 'NULL'

    if origin_label == 6:
        origin_type, origin_asteroid_id, origin_lot_id = getShipData(origin_id)

    if dest_label == 6:
        dest_type, dest_asteroid_id, dest_lot_id = getShipData(dest_id)
        crew_ship_id = dest_id

    for row in products:
        old_inventory_amount = 0
        new_inventory_amount = 0
        state = None
        print(row)
        # ORIGIN LABEL WILL PROBABLY CHANGE BASED ON INVENTORY TYPE
        insert_sql = ("INSERT IGNORE INTO dispatcher_delivery_finished_v1 (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_type, origin_slot, dest_label, dest_id, dest_type, dest_slot, delivery_label, delivery_id, product_name, product_id, product_amount, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s', %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_type, origin_slot, dest_label, dest_id, dest_type, dest_slot, delivery_label, delivery_id, row['name'], row['id'], row['amount'], fee, timestamp))
        print(insert_sql)
        updateSql(insert_sql)

        old_inventory_amount, state = getInventory(dest_label, dest_id, dest_slot, row['id'])
        new_inventory_amount=(old_inventory_amount + row['amount'])

        if dest_label == 5:
            dest_type, dest_asteroid_id, dest_lot_id = getBuildingData(dest_id)
            crew_ship_id = None
        elif dest_label == 6:
            dest_type, dest_asteroid_id, dest_lot_id = getShipData(dest_id)
            crew_ship_id = dest_id

    for inventory in destination_inventory:
        inv_resource_id = inventory['resource_id']
        inv_resource_name = inventory['resource_name']
        inv_resource_amount = inventory['resource_amount']
        state = getInventoryState(dest_label, dest_id, dest_slot, inv_resource_id)
        if state > 0:
            update_sql=("UPDATE inventories SET inventory_amount = %s WHERE inventory_label = %s AND inventory_id = %s AND inventory_slot = %s AND inventory_type = %s AND resource_id = %s" % (inv_resource_amount, dest_label, dest_id, dest_slot, dest_type, inv_resource_id))
            print(update_sql)
            updateSql(update_sql)
        else:
            insert_sql2=("INSERT INTO inventories (inventory_label, inventory_id, inventory_slot, inventory_type, resource_id, inventory_amount) VALUES (%s, %s, %s, %s, %s, %s)" % (dest_label, dest_id, dest_slot, dest_type, inv_resource_id, inv_resource_amount))
            print(insert_sql2)
            updateSql(insert_sql2)

    update_sql2 = ("UPDATE deliveries SET status = 2, finish_txn_id = '%s', finish_block_number = %s, finish_timestamp = '%s' WHERE delivery_id = %s" % (tx_hash, block_number, timestamp, delivery_id))
    print(update_sql2)
    updateSql(update_sql2)

    delete_sql = ("DELETE FROM deliveries_pending WHERE delivery_id = %s" % delivery_id)
    print(delete_sql)
    updateSql(delete_sql)

    crew_asteroid_id = dest_asteroid_id
    crew_lot_id = dest_lot_id
    action = "DeliveryFinished"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def deliverySent(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_slot, dest_label, dest_id, dest_slot, delivery_label, delivery_id, finish_time, products, destination_inventory, origin_inventory, delivery_manifest, fee, timestamp):

    origin_asteroid_id = 'NULL'
    origin_lot_id = 'NULL'
    dest_asteroid_id = 'NULL'
    dest_lot_id = 'NULL'

    if origin_label == 5:
        origin_type, origin_asteroid_id, origin_lot_id = getBuildingData(origin_id)
        crew_ship_id = None

    if dest_label == 5:
        dest_type, dest_asteroid_id, dest_lot_id = getBuildingData(dest_id)
        crew_ship_id = None

    if origin_label == 6:
        origin_type, origin_asteroid_id, origin_lot_id = getShipData(origin_id)
        crew_ship_id = origin_id

    if dest_label == 6:
        dest_type, dest_asteroid_id, dest_lot_id = getShipData(dest_id)
        crew_ship_id = dest_id

    for row in products:
        state = None
        old_inventory_amount = 0
        new_inventory_amount = 0
        print(row)
        # ORIGIN LABEL WILL PROBABLY CHANGE BASED ON INVENTORY TYPE
        insert_sql = ("INSERT IGNORE INTO dispatcher_delivery_sent (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_type, origin_slot, origin_asteroid_id, origin_lot_id, dest_label, dest_id, dest_type, dest_slot, dest_asteroid_id, dest_lot_id, delivery_label, delivery_id, finish_time, product_name, product_id, product_amount, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s', %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_type, origin_slot, origin_asteroid_id, origin_lot_id,  dest_label, dest_id, dest_type, dest_slot, dest_asteroid_id, dest_asteroid_id, delivery_label, delivery_id, finish_time, row['name'], row['id'], row['amount'], fee, timestamp))
        print(insert_sql)
        updateSql(insert_sql)

        insert_sql2 = ("INSERT IGNORE INTO deliveries (start_txn_id, start_block_number, start_timestamp, from_address, caller_address, crew_id, origin_label, origin_id, origin_type, origin_slot, origin_asteroid_id, origin_lot_id, dest_label, dest_id, dest_type, dest_slot, dest_asteroid_id, dest_lot_id, delivery_id, finish_time, product_name, product_id, product_amount, status) VALUES ('%s', %s, '%s', '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s', %s, %s, 1)" % (tx_hash, block_number, timestamp, from_address, caller_address, caller_crew_id, origin_label, origin_id, origin_type, origin_slot, origin_asteroid_id, origin_lot_id, dest_label, dest_id, dest_type, dest_slot, dest_asteroid_id, dest_lot_id, delivery_id, finish_time, row['name'], row['id'], row['amount']))
        print(insert_sql2)
        updateSql(insert_sql2)

        insert_sql3 = ("INSERT IGNORE INTO deliveries_pending (txn_id, block_number, from_address, caller_address, crew_id, origin_label, origin_id, origin_type, origin_slot, origin_asteroid_id, origin_lot_id, dest_label, dest_id, dest_type, dest_slot, dest_asteroid_id, dest_lot_id, delivery_id, finish_time, product_name, product_id, product_amount) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s', %s, %s)" % (tx_hash, block_number, from_address, caller_address, caller_crew_id, origin_label, origin_id, origin_type, origin_slot, origin_asteroid_id, origin_lot_id, dest_label, dest_id, dest_type, dest_slot, dest_asteroid_id, dest_lot_id, delivery_id, finish_time, row['name'], row['id'], row['amount']))
        print(insert_sql3)
        updateSql(insert_sql3)

    if origin_inventory is not None:
        if origin_label == 5:
            origin_type, origin_asteroid_id, origin_lot_id = getBuildingData(origin_id)
        elif origin_label == 6:
            origin_type, origin_asteroid_id, origin_lot_id = getShipData(origin_id)

        if len(origin_inventory) == 0:
            delete_sql = ("DELETE FROM inventories WHERE inventory_label = %s AND inventory_id = %s AND inventory_slot = %s AND inventory_type = %s" % (origin_label, origin_id, origin_slot, origin_type))
            print(delete_sql)
            updateSql(delete_sql)
        else:
            for inventory in origin_inventory:
                inv_resource_id = inventory['resource_id']
                inv_resource_name = inventory['resource_name']
                inv_resource_amount = inventory['resource_amount']
                state = getInventoryState(origin_label, origin_id, origin_slot, inv_resource_id)
                if state > 0:
                    update_sql=("UPDATE inventories SET inventory_amount = %s WHERE inventory_label = %s AND inventory_id = %s AND inventory_slot = %s AND inventory_type = %s AND resource_id = %s" % (inv_resource_amount, origin_label, origin_id, origin_slot, origin_type, inv_resource_id))
                    print(update_sql)
                    updateSql(update_sql)
                else:
                    insert_sql4=("INSERT INTO inventories (inventory_label, inventory_id, inventory_slot, inventory_type, resource_id, inventory_amount) VALUES (%s, %s, %s, %s, %s, %s)" % (origin_label, origin_id, origin_slot, origin_type, inv_resource_id, inv_resource_amount))
                    print(insert_sql4)
                    updateSql(insert_sql4)

    if dest_label == 5:
        dest_type, dest_asteroid_id, dest_lot_id = getBuildingData(dest_id)
    elif dest_label == 6:
        dest_type, dest_asteroid_id, dest_lot_id = getShipData(dest_id)

    if len(destination_inventory) == 0:
        delete_sql2 = ("DELETE FROM inventories WHERE inventory_label = %s AND inventory_id = %s AND inventory_slot = %s AND inventory_type = %s" % (dest_label, dest_id, dest_slot, dest_type))
        print(delete_sql2)
        updateSql(delete_sql2)
    else:
        for inventory in destination_inventory:
            inv_resource_id = inventory['resource_id']
            inv_resource_name = inventory['resource_name']
            inv_resource_amount = inventory['resource_amount']
            state = getInventoryState(dest_label, dest_id, dest_slot, inv_resource_id)
            if state > 0:
                update_sql2=("UPDATE inventories SET inventory_amount = %s WHERE inventory_label = %s AND inventory_id = %s AND inventory_slot = %s AND inventory_type = %s AND resource_id = %s" % (inv_resource_amount, dest_label, dest_id, dest_slot, dest_type, inv_resource_id))
                print(update_sql2)
                updateSql(update_sql2)
            else:
                insert_sql5=("INSERT INTO inventories (inventory_label, inventory_id, inventory_slot, inventory_type, resource_id, inventory_amount) VALUES (%s, %s, %s, %s, %s, %s)" % (dest_label, dest_id, dest_slot, dest_type, inv_resource_id, inv_resource_amount))
                print(insert_sql5)
                updateSql(insert_sql5)

    crew_asteroid_id = origin_asteroid_id
    crew_lot_id = origin_lot_id
    action = "DeliverySent"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def deliveryReceived(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_slot, dest_label, dest_id, dest_slot, delivery_label, delivery_id, products, destination_inventory, delivery_manifest, fee, timestamp):

    origin_asteroid_id = 'NULL'
    origin_lot_id = 'NULL'
    dest_asteroid_id = 'NULL'
    dest_lot_id = 'NULL'

    if origin_label == 5:
        origin_type, origin_asteroid_id, origin_lot_id = getBuildingData(origin_id)

    if dest_label == 5:
        dest_type, dest_asteroid_id, dest_lot_id = getBuildingData(dest_id)

    if origin_label == 6:
        origin_type, origin_asteroid_id, origin_lot_id = getShipData(origin_id)

    if dest_label == 6:
        dest_type, dest_asteroid_id, dest_lot_id = getShipData(dest_id)

    for row in products:
        old_inventory_amount = 0
        new_inventory_amount = 0
        state = None
        print(row)
        # ORIGIN LABEL WILL PROBABLY CHANGE BASED ON INVENTORY TYPE
        insert_sql = ("INSERT IGNORE INTO dispatcher_delivery_received (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_type, origin_slot, dest_label, dest_id, dest_type, dest_slot, delivery_label, delivery_id, product_name, product_id, product_amount, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s', %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_type, origin_slot, dest_label, dest_id, dest_type, dest_slot, delivery_label, delivery_id, row['name'], row['id'], row['amount'], fee, timestamp))
        print(insert_sql)
        updateSql(insert_sql)

        old_inventory_amount, state = getInventory(dest_label, dest_id, dest_slot, row['id'])
        new_inventory_amount=(old_inventory_amount + row['amount'])

        if dest_label == 5:
            dest_type, dest_asteroid_id, dest_lot_id = getBuildingData(dest_id)
            crew_ship_id = None
        elif dest_label == 6:
            dest_type, dest_asteroid_id, dest_lot_id = getShipData(dest_id)
            crew_ship_id = dest_id

    update_sql2 = ("UPDATE deliveries SET status = 2, finish_txn_id = '%s', finish_block_number = %s, finish_timestamp = '%s' WHERE delivery_id = %s" % (tx_hash, block_number, timestamp, delivery_id))
    print(update_sql2)
    updateSql(update_sql2)

    delete_sql = ("DELETE FROM deliveries_pending WHERE delivery_id = %s" % delivery_id)
    print(delete_sql)
    updateSql(delete_sql)

    for inventory in destination_inventory:
        inv_resource_id = inventory['resource_id']
        inv_resource_name = inventory['resource_name']
        inv_resource_amount = inventory['resource_amount']
        state = getInventoryState(dest_label, dest_id, dest_slot, inv_resource_id)
        if state > 0:
            update_sql3=("UPDATE inventories SET inventory_amount = %s WHERE inventory_label = %s AND inventory_id = %s AND inventory_slot = %s AND inventory_type = %s AND resource_id = %s" % (inv_resource_amount, dest_label, dest_id, dest_slot, dest_type, inv_resource_id))
            print(update_sql3)
            updateSql(update_sql3)
        else:
            insert_sql2=("INSERT INTO inventories (inventory_label, inventory_id, inventory_slot, inventory_type, resource_id, inventory_amount) VALUES (%s, %s, %s, %s, %s, %s)" % (dest_label, dest_id, dest_slot, dest_type, inv_resource_id, inv_resource_amount))
            print(insert_sql2)
            updateSql(insert_sql2)

    crew_asteroid_id = dest_asteroid_id
    crew_lot_id = dest_lot_id
    action = "DeliveryReceived"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def deliveryCancelled(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_slot, dest_label, dest_id, dest_slot, delivery_label, delivery_id, products, origin_inventory, fee, timestamp):

    origin_asteroid_id = 'NULL'
    origin_lot_id = 'NULL'
    dest_asteroid_id = 'NULL'
    dest_lot_id = 'NULL'

    if origin_label == 5:
        origin_type, origin_asteroid_id, origin_lot_id = getBuildingData(origin_id)
        crew_ship_id = None

    if dest_label == 5:
        dest_type, dest_asteroid_id, dest_lot_id = getBuildingData(dest_id)

    if origin_label == 6:
        origin_type, origin_asteroid_id, origin_lot_id = getShipData(origin_id)
        crew_ship_id = origin_id

    if dest_label == 6:
        dest_type, dest_asteroid_id, dest_lot_id = getShipData(dest_id)

    for row in products:
        old_inventory_amount = 0
        new_inventory_amount = 0
        state = None   
        print(row)
        # ORIGIN LABEL WILL PROBABLY CHANGE BASED ON INVENTORY TYPE
        insert_sql = ("INSERT IGNORE INTO dispatcher_delivery_cancelled (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_type, origin_slot, dest_label, dest_id, dest_type, dest_slot, delivery_label, delivery_id, product_name, product_id, product_amount, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s', %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_type, origin_slot, dest_label, dest_id, dest_type, dest_slot, delivery_label, delivery_id, row['name'], row['id'], row['amount'], fee, timestamp))
        print(insert_sql)
        updateSql(insert_sql)
        update_sql = ("UPDATE deliveries SET status = 4, cancelled_txn_id = '%s', cancelled_block_number = %s, cancelled_timestamp = '%s' WHERE delivery_id = %s" % (tx_hash, block_number, timestamp, delivery_id))
        print(update_sql)
        updateSql(update_sql)

    delete_sql = ("DELETE FROM deliveries_pending WHERE delivery_id = %s" % delivery_id)
    print(delete_sql)
    updateSql(delete_sql)

    for inventory in origin_inventory:
        inv_resource_id = inventory['resource_id']
        inv_resource_name = inventory['resource_name']
        inv_resource_amount = inventory['resource_amount']
        state = getInventoryState(origin_label, origin_id, origin_slot, inv_resource_id)
        if state > 0:
            update_sql2=("UPDATE inventories SET inventory_amount = %s WHERE inventory_label = %s AND inventory_id = %s AND inventory_slot = %s AND inventory_type = %s AND resource_id = %s" % (inv_resource_amount, origin_label, origin_id, origin_slot, origin_type, inv_resource_id))
            print(update_sql2)
            updateSql(update_sql2)
        else:
            insert_sql2=("INSERT INTO inventories (inventory_label, inventory_id, inventory_slot, inventory_type, resource_id, inventory_amount) VALUES (%s, %s, %s, %s, %s, %s)" % (origin_label, origin_id, origin_slot, origin_type, inv_resource_id, inv_resource_amount))
            print(insert_sql2)
            updateSql(insert_sql2)

    crew_asteroid_id = dest_asteroid_id
    crew_lot_id = dest_lot_id
    action = "DeliveryCancelled"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def deliveryPackaged(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_slot, dest_label, dest_id, dest_slot, price, delivery_label, delivery_id, products, origin_inventory, fee, timestamp):

    origin_asteroid_id = 'NULL'
    origin_lot_id = 'NULL'
    dest_asteroid_id = 'NULL'
    dest_lot_id = 'NULL'

    if origin_label == 5:
        origin_type, origin_asteroid_id, origin_lot_id = getBuildingData(origin_id)

    if dest_label == 5:
        dest_type, dest_asteroid_id, dest_lot_id = getBuildingData(dest_id)

    if origin_label == 6:
        origin_type, origin_asteroid_id, origin_lot_id = getShipData(origin_id)

    if dest_label == 6:
        dest_type, dest_asteroid_id, dest_lot_id = getShipData(dest_id)

    insert_sql = ("INSERT IGNORE INTO dispatcher_delivery_packaged (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_type, origin_slot, dest_label, dest_id, dest_type, dest_slot, delivery_label, delivery_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_type, origin_slot, dest_label, dest_id, dest_type, dest_slot, delivery_label, delivery_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    for row in products:
        old_inventory_amount = 0
        new_inventory_amount = 0
        state = None
        print(row)
        insert_sql2 = ("INSERT IGNORE INTO packaged_deliveries (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_type, origin_slot, dest_label, dest_id, dest_type, dest_slot, delivery_label, delivery_id, product_name, product_id, product_amount, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s', %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_type, origin_slot, dest_label, dest_id, dest_type, dest_slot, delivery_label, delivery_id, row['name'], row['id'], row['amount'], fee, timestamp))
        print(insert_sql2)
        updateSql(insert_sql2)

        insert_sql3 = ("INSERT IGNORE INTO deliveries (packaged_txn_id, packaged_block_number, packaged_timestamp, from_address, caller_address, crew_id, origin_label, origin_id, origin_type, origin_slot, origin_asteroid_id, origin_lot_id, dest_label, dest_id, dest_type, dest_slot, dest_asteroid_id, dest_lot_id, delivery_id, product_name, product_id, product_amount, status) VALUES ('%s', %s, '%s', '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s', %s, %s, 3)" % (tx_hash, block_number, timestamp, from_address, caller_address, caller_crew_id, origin_label, origin_id, origin_type, origin_slot, origin_asteroid_id, origin_lot_id, dest_label, dest_id, dest_type, dest_slot, dest_asteroid_id, dest_lot_id, delivery_id, row['name'], row['id'], row['amount']))
        print(insert_sql3)
        updateSql(insert_sql3)

        old_inventory_amount, state = getInventory(origin_label, origin_id, origin_slot, row['id'])
        new_inventory_amount=(old_inventory_amount - row['amount'])

    if origin_label == 5:
        origin_type, origin_asteroid_id, origin_lot_id = getBuildingData(origin_id)
        crew_ship_id = None
    elif origin_label == 6:
        origin_type, origin_asteroid_id, origin_lot_id = getShipData(origin_id)
        crew_ship_id = origin_id

    if len(origin_inventory) == 0:
        delete_sql = ("DELETE FROM inventories WHERE inventory_label = %s AND inventory_id = %s AND inventory_slot = %s AND inventory_type = %s" % (origin_label, origin_id, origin_slot, origin_type))
        print(delete_sql)
        updateSql(delete_sql)
    else:
        for inventory in origin_inventory:
            inv_resource_id = inventory['resource_id']
            inv_resource_name = inventory['resource_name']
            inv_resource_amount = inventory['resource_amount']
            state = getInventoryState(origin_label, origin_id, origin_slot, inv_resource_id)
            if state > 0:
                update_sql=("UPDATE inventories SET inventory_amount = %s WHERE inventory_label = %s AND inventory_id = %s AND inventory_slot = %s AND inventory_type = %s AND resource_id = %s" % (inv_resource_amount, origin_label, origin_id, origin_slot, origin_type, inv_resource_id))
                print(update_sql)
                updateSql(update_sql)
            else:
                insert_sql4=("INSERT INTO inventories (inventory_label, inventory_id, inventory_slot, inventory_type, resource_id, inventory_amount) VALUES (%s, %s, %s, %s, %s, %s)" % (origin_label, origin_id, origin_slot, origin_type, inv_resource_id, inv_resource_amount))
                print(insert_sql4)
                updateSql(insert_sql4)

    crew_asteroid_id = origin_asteroid_id
    crew_lot_id = origin_lot_id
    action = "DeliveryPackaged"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def materialProcessingStartedV1(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, processor_label, processor_id, processor_slot, process_id, process_name, inputs, origin_label, origin_id, origin_slot, outputs, destination_label, destination_id, destination_slot, finish_time, origin_inventory, fee, timestamp):

    if processor_label == 5:
        processor_type, processor_asteroid_id, processor_lot_id = getBuildingData(processor_id)
    else:
        print("WTF")
        sys.exit(1)

    if origin_label == 5:
        origin_type, origin_asteroid_id, origin_lot_id = getBuildingData(origin_id)
    elif origin_label == 6:
        origin_type, origin_asteroid_id, origin_lot_id = getShipData(origin_id)

    if destination_label == 5:
        destination_type, destination_asteroid_id, destination_lot_id = getBuildingData(destination_id)
    elif destination_label == 6:
        destination_type, destination_asteroid_id, destination_lot_id = getShipData(destination_id)

    insert_sql=("INSERT IGNORE INTO dispatcher_material_processing_started_v1 (txn_id, block_number, from_address, caller_address, caller_crew_id, caller_crew_label, processor_label, processor_id, processor_slot, processor_type, processor_asteroid_id, processor_lot_id, process_id, process_name, origin_label, origin_id, origin_slot, origin_type, origin_asteroid_id, origin_lot_id, destination_label, destination_id, destination_slot, destination_type, destination_asteroid_id, destination_lot_id, finish_time, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_id, caller_crew_label, processor_label, processor_id, processor_slot, processor_type, processor_asteroid_id, processor_lot_id, process_id, process_name, origin_label, origin_id, origin_slot, origin_type, origin_asteroid_id, origin_lot_id, destination_label, destination_id, destination_slot, destination_type, destination_asteroid_id, destination_lot_id, finish_time, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    for row in inputs:
        print("row: %s" % row)
        input_id=row['id']
        input_amount=row['amount']
        input_name=row['name']
        input_sql=("INSERT IGNORE INTO dispatcher_material_processing_started_inputs (txn_id, block_number, caller_address, crew_id, process_id, process_name, resource_name, resource_id, resource_amount) VALUES ('%s', %s, '%s', %s, %s, '%s', '%s', %s, %s)" % (tx_hash, block_number, caller_address, caller_crew_id, process_id, process_name, input_name, input_id, input_amount))
        print(input_sql)
        updateSql(input_sql)

        insert_sql2=("INSERT IGNORE INTO products_consumed (txn_id, block_number, caller_address, crew_id, origin_label, origin_id, origin_type, asteroid_id, lot_id, resource_id, resource_name, resource_amount, timestamp) VALUES ('%s', %s, '%s', %s, %s, %s, %s, %s, %s, %s, '%s', %s, '%s')" % (tx_hash, block_number, caller_address, caller_crew_id, origin_label, origin_id, origin_type, origin_asteroid_id, origin_lot_id, input_id, input_name, input_amount, timestamp))
        print(insert_sql2)
        updateSql(insert_sql2)

        if input_id == 129:
            insert_sql3=("INSERT IGNORE INTO food_burned (txn_id, block_number, caller_address, crew_id, station_label, station_id, asteroid_id, lot_id, food, timestamp) VALUES ('%s', %s, '%s', %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, caller_address, caller_crew_id, origin_label, origin_id, origin_asteroid_id, origin_lot_id, input_amount, timestamp))
            print(insert_sql3)
            updateSql(insert_sql3)

    for row in outputs:
        output_id=row['id']
        output_amount=row['amount']
        output_name=row['name']
        output_sql=("INSERT IGNORE INTO dispatcher_material_processing_started_outputs (txn_id, block_number, caller_address, crew_id, process_id, process_name, resource_name, resource_id, resource_amount) VALUES ('%s', %s, '%s', %s, %s, '%s', '%s', %s, %s)" % (tx_hash, block_number, caller_address, caller_crew_id, process_id, process_name, output_name, output_id, output_amount))
        print(output_sql)
        updateSql(output_sql)

    insert_sql4=("INSERT IGNORE INTO processing_actions (start_txn_id, start_block_number, start_timestamp, from_address, caller_address, crew_id, process_id, process_name, finish_time, processor_id, processor_type, processor_asteroid_id, processor_lot_id, processor_slot, processor_label, origin_id, origin_type, origin_asteroid_id, origin_lot_id, origin_slot, origin_label, destination_id, destination_type, destination_asteroid_id, destination_lot_id, destination_slot, destination_label, status) VALUES ('%s', %s, '%s', '%s', '%s', %s, %s, '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)" % (tx_hash, block_number, timestamp, from_address, caller_address, caller_crew_id, process_id, process_name, finish_time, processor_id, processor_type, processor_asteroid_id, processor_lot_id, processor_slot, processor_label, origin_id, origin_type, origin_asteroid_id, origin_lot_id, origin_slot, origin_label, destination_id, destination_type, destination_asteroid_id, destination_lot_id, destination_slot, destination_label))
    print(insert_sql4)
    updateSql(insert_sql4)

    if len(origin_inventory) == 0:
        delete_sql = ("DELETE FROM inventories WHERE inventory_label = %s AND inventory_id = %s AND inventory_slot = %s AND inventory_type = %s" % (origin_label, origin_id, origin_slot, origin_type))
        print(delete_sql)
        updateSql(delete_sql)
    else:
        for inventory in origin_inventory:
            inv_resource_id = inventory['resource_id']
            inv_resource_name = inventory['resource_name']
            inv_resource_amount = inventory['resource_amount']
            state = getInventoryState(origin_label, origin_id, origin_slot, inv_resource_id)
            if state > 0:
                update_sql2=("UPDATE inventories SET inventory_amount = %s WHERE inventory_label = %s AND inventory_id = %s AND inventory_slot = %s AND inventory_type = %s AND resource_id = %s" % (inv_resource_amount, origin_label, origin_id, origin_slot, origin_type, inv_resource_id))
                print(update_sql2)
                updateSql(update_sql2)
            else:
                insert_sql2=("INSERT IGNORE INTO inventories (inventory_label, inventory_id, inventory_slot, inventory_type, resource_id, inventory_amount) VALUES (%s, %s, %s, %s, %s, %s)" % (origin_label, origin_id, origin_slot, origin_type, inv_resource_id, inv_resource_amount))
                print(insert_sql2)
                updateSql(insert_sql2)

    crew_asteroid_id = origin_asteroid_id
    crew_lot_id = origin_lot_id
    crew_ship_id = None
    action = "ProcessingStarted"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def materialProcessingFinished(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, processor_label, processor_id, processor_slot, destination_inventory, fee, timestamp):

    if processor_label == 5:
        processor_type, processor_asteroid_id, processor_lot_id = getBuildingData(processor_id)
    else:
        print("WTF")
        sys.exit(1)

    insert_sql=("INSERT IGNORE INTO dispatcher_material_processing_finished (txn_id, block_number, from_address, caller_address, caller_crew_id, caller_crew_label, processor_label, processor_id, processor_slot, processor_type, processor_asteroid_id, processor_lot_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_id, caller_crew_label, processor_label, processor_id, processor_slot, processor_type, processor_asteroid_id, processor_lot_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    update_sql=("UPDATE processing_actions SET finish_txn_id = '%s', finish_block_number = %s, finish_timestamp = '%s', status = 2 WHERE processor_id = %s AND status = 1" % (tx_hash, block_number, timestamp, processor_id))
    print(update_sql)
    updateSql(update_sql)

    outputs_data=getMaterialProcessingOutputs(tx_hash, processor_id, processor_slot)
    destination_id = outputs_data['destination_id']
    destination_type = outputs_data['destination_type']
    destination_label = outputs_data['destination_label']
    destination_slot = outputs_data['destination_slot']
    products = outputs_data['products']

    if destination_label == 5:
        destination_type, destination_asteroid_id, destination_lot_id = getBuildingData(destination_id)
        crew_ship_id = None
    elif destination_label == 6:
        destination_type, destination_asteroid_id, destination_lot_id = getShipData(destination_id)
        crew_ship_id = destination_id

    for inventory in destination_inventory:
        inv_resource_id = inventory['resource_id']
        inv_resource_name = inventory['resource_name']
        inv_resource_amount = inventory['resource_amount']
        state = getInventoryState(destination_label, destination_id, destination_slot, inv_resource_id)
        if state > 0:
            update_sql2=("UPDATE inventories SET inventory_amount = %s WHERE inventory_label = %s AND inventory_id = %s AND inventory_slot = %s AND inventory_type = %s AND resource_id = %s" % (inv_resource_amount, destination_label, destination_id, destination_slot, destination_type, inv_resource_id))
            print(update_sql2)
            updateSql(update_sql2)
        else:
            insert_sql2=("INSERT INTO inventories (inventory_label, inventory_id, inventory_slot, inventory_type, resource_id, inventory_amount) VALUES (%s, %s, %s, %s, %s, %s)" % (destination_label, destination_id, destination_slot, destination_type, inv_resource_id, inv_resource_amount))
            print(insert_sql2)
            updateSql(insert_sql2)

    for row in products:
        output_id=row['output_id']
        output_amount=row['output_amount']
        output_name=row['output_name']
        old_inventory_amount, state = getInventory(destination_label, destination_id, destination_slot, output_id)
        new_inventory_amount=(old_inventory_amount + output_amount)

        insert_sql3=("INSERT IGNORE INTO products_produced (txn_id, block_number, caller_address, crew_id, destination_label, destination_id, destination_type, asteroid_id, lot_id, resource_id, resource_name, resource_amount, timestamp) VALUES ('%s', %s, '%s', %s, %s, %s, %s, %s, %s, %s, '%s', %s, '%s')" % (tx_hash, block_number, caller_address, caller_crew_id, destination_label, destination_id, destination_type, destination_asteroid_id, destination_lot_id, output_id, output_name, output_amount, timestamp))
        print(insert_sql3)
        updateSql(insert_sql3)

        if output_id == 170:
            insert_sql4=("INSERT IGNORE INTO propellant_produced (txn_id, block_number, caller_address, crew_id, destination_label, destination_id, destination_type, asteroid_id, lot_id, amount, method, timestamp) VALUES ('%s', %s, '%s', %s, %s, %s, %s, %s, %s, %s, '%s', '%s')" % (tx_hash, block_number, caller_address, caller_crew_id, destination_label, destination_id, destination_type, destination_asteroid_id, destination_lot_id, output_amount, "factory", timestamp))
            print(insert_sql4)
            updateSql(insert_sql4)

        elif output_id == 129:
            insert_sql5=("INSERT IGNORE INTO food_produced (txn_id, block_number, caller_address, crew_id, destination_label, destination_id, destination_type, asteroid_id, lot_id, amount, timestamp) VALUES ('%s', %s, '%s', %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, caller_address, caller_crew_id, destination_label, destination_id, destination_type, destination_asteroid_id, destination_lot_id, output_amount, timestamp))
            print(insert_sql5)
            updateSql(insert_sql5)

    crew_asteroid_id = destination_asteroid_id
    crew_lot_id = destination_lot_id
    action = "ProcessingFinished"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def foodSupplied(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, food, last_fed, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_food_supplied (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, food, last_fed, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, food, last_fed, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    insert_sql2=("INSERT IGNORE INTO food_supplied_actions (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, food, last_fed, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, food, last_fed, fee, timestamp))
    print(insert_sql2)
    updateSql(insert_sql2)

    station_label, station_id = getStation(caller_crew_id)
    asteroid_id, lot_id = getStationLocation(station_label, station_id)
    insert_sql3=("INSERT IGNORE INTO food_burned (txn_id, block_number, caller_address, crew_id, station_label, station_id, asteroid_id, lot_id, food, timestamp) VALUES ('%s', %s, '%s', %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, caller_address, caller_crew_id, station_label, station_id, asteroid_id, lot_id, food, timestamp))
    print(insert_sql3)
    updateSql(insert_sql3)

    crew_asteroid_id = asteroid_id
    crew_lot_id = lot_id
    crew_ship_id = None
    action = "FoodSupplied"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def foodSuppliedV1(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, food, last_fed, origin_label, origin_id, origin_slot, origin_inventory, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_food_supplied_v1 (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, food, last_fed, origin_label, origin_id, origin_slot, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, food, last_fed, origin_label, origin_id, origin_slot, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    if origin_label == 5:
        origin_type, origin_asteroid_id, origin_lot_id = getBuildingData(origin_id)
        crew_ship_id = None
    elif origin_label == 6:
        origin_type, origin_asteroid_id, origin_lot_id = getShipData(origin_id)
        crew_ship_id = origin_id

    insert_sql2=("INSERT IGNORE INTO food_supplied_actions (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, food, last_fed, origin_label, origin_id, origin_slot, origin_type, origin_asteroid_id, origin_lot_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, food, last_fed, origin_label, origin_id, origin_slot, origin_type, origin_asteroid_id, origin_lot_id, fee, timestamp))
    print(insert_sql2)
    updateSql(insert_sql2)

    if len(origin_inventory) == 0:
        delete_sql = ("DELETE FROM inventories WHERE inventory_label = %s AND inventory_id = %s AND inventory_slot = %s AND inventory_type = %s" % (origin_label, origin_id, origin_slot, origin_type))
        print(delete_sql)
        updateSql(delete_sql)
    else:
        for inventory in origin_inventory:
            inv_resource_id = inventory['resource_id']
            inv_resource_name = inventory['resource_name']
            inv_resource_amount = inventory['resource_amount']
            state = getInventoryState(origin_label, origin_id, origin_slot, inv_resource_id)
            if state > 0:
                update_sql2=("UPDATE inventories SET inventory_amount = %s WHERE inventory_label = %s AND inventory_id = %s AND inventory_slot = %s AND inventory_type = %s AND resource_id = %s" % (inv_resource_amount, origin_label, origin_id, origin_slot, origin_type, inv_resource_id))
                print(update_sql2)
                updateSql(update_sql2)
            else:
                insert_sql2=("INSERT INTO inventories (inventory_label, inventory_id, inventory_slot, inventory_type, resource_id, inventory_amount) VALUES (%s, %s, %s, %s, %s, %s)" % (origin_label, origin_id, origin_slot, origin_type, inv_resource_id, inv_resource_amount))
                print(insert_sql2)
                updateSql(insert_sql2)

    station_label, station_id = getStation(caller_crew_id)
    asteroid_id, lot_id = getStationLocation(station_label, station_id)

    insert_sql4=("INSERT IGNORE INTO food_burned (txn_id, block_number, caller_address, crew_id, station_label, station_id, asteroid_id, lot_id, food, timestamp) VALUES ('%s', %s, '%s', %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, caller_address, caller_crew_id, station_label, station_id, asteroid_id, lot_id, food, timestamp))
    print(insert_sql4)
    updateSql(insert_sql4)

    crew_asteroid_id = origin_asteroid_id
    crew_lot_id = origin_lot_id
    action = "FoodSupplied"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def shipUndocked(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, dock_label, dock_id, asteroid_id, lot_id, fee, timestamp, new_fuel):

    insert_sql=("INSERT IGNORE INTO dispatcher_ship_undocked (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, dock_label, dock_id, asteroid_id, lot_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, dock_label, dock_id, asteroid_id, lot_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    if dock_label == 4:
        dock_type = 4
        dock_asteroid_id = asteroid_id
        dock_lot_id = lot_id
    else:
        dock_type, dock_asteroid_id, dock_lot_id = getBuildingData(dock_id)

    delete_sql=("DELETE FROM ships_docked WHERE ship_id = %s" % ship_id)
    print(delete_sql)
    updateSql(delete_sql)

    update_sql=("UPDATE stations SET asteroid_id = NULL, lot_id = NULL WHERE station_label = 6 AND station_id = %s" % ship_id)
    print(update_sql)
    updateSql(update_sql)

    if new_fuel is not None:
        old_inventory_amount, state = getInventory(ship_label, ship_id, 1, 170)
        inventory_diff = (old_inventory_amount - new_fuel)
        new_inventory_amount = new_fuel
        burn_type = 'Undocked'
        update_sql2 = ("INSERT IGNORE INTO propellant_burned (txn_id, block_number, caller_address, crew_id, ship_label, ship_id, asteroid_id, lot_id, burn_type, fuel_burned, previous_fuel, new_fuel, timestamp) VALUES ('%s', %s, '%s', %s, %s, %s, %s, %s, '%s', %s, %s, %s, '%s')" % (tx_hash, block_number, caller_address, caller_crew_id, ship_label, ship_id, dock_asteroid_id, dock_lot_id, burn_type, inventory_diff, old_inventory_amount, new_inventory_amount, timestamp))
        print(update_sql2)
        updateSql(update_sql2)

        update_sql3=("UPDATE inventories SET inventory_amount = %s WHERE inventory_label = %s AND inventory_id = %s AND inventory_slot = 1 AND resource_id = 170" % (new_fuel, ship_label, ship_id))
        print(update_sql3)
        updateSql(update_sql3)

    crew_asteroid_id = asteroid_id
    crew_lot_id = lot_id
    crew_ship_id = ship_id
    action = "ShipUndocked"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def shipDocked(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, dock_label, dock_id, asteroid_id, lot_id, fee, timestamp, new_fuel):

    insert_sql=("INSERT IGNORE INTO dispatcher_ship_docked (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, dock_label, dock_id, asteroid_id, lot_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, dock_label, dock_id, asteroid_id, lot_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    if dock_label == 4:
        dock_type = 4
        dock_asteroid_id = asteroid_id
        dock_lot_id = lot_id
    else:
        dock_type, dock_asteroid_id, dock_lot_id = getBuildingData(dock_id)

    ship_docked = checkShipDock(ship_id)
    if ship_docked == 0:
        insert_sql2=("INSERT IGNORE INTO ships_docked (txn_id, block_number, caller_address, crew_id, ship_label, ship_id, dock_label, dock_id, dock_type, dock_asteroid_id, dock_lot_id, status) VALUES ('%s', %s, '%s', %s, %s, %s, %s, %s, %s, %s, %s, 1)" % (tx_hash, block_number, caller_address, caller_crew_id, ship_label, ship_id, dock_label, dock_id, dock_type, dock_asteroid_id, dock_lot_id))
        print(insert_sql2)
        updateSql(insert_sql2)

    else:
        update_sql=("UPDATE ships_docked SET txn_id = '%s', block_number = %s, caller_address = '%s', crew_id = %s, dock_label = %s, dock_id = %s, dock_type = %s, dock_asteroid_id = %s, dock_lot_id = %s, status = 1 WHERE ship_id = %s" % (tx_hash, block_number, caller_address, caller_crew_id, dock_label, dock_id, dock_type, dock_asteroid_id, dock_lot_id, ship_id))
        print(update_sql)
        updateSql(update_sql)

    update_sql2=("UPDATE stations SET asteroid_id = %s, lot_id = %s WHERE station_label = 6 AND station_id = %s" % (dock_asteroid_id, dock_lot_id, ship_id))
    print(update_sql2)
    updateSql(update_sql2)

    if new_fuel is not None:
        old_inventory_amount, state = getInventory(ship_label, ship_id, 1, 170)
        inventory_diff = (old_inventory_amount - new_fuel)
        new_inventory_amount = new_fuel
        burn_type = 'Docked'
        update_sql3 = ("INSERT IGNORE INTO propellant_burned (txn_id, block_number, caller_address, crew_id, ship_label, ship_id, asteroid_id, lot_id, burn_type, fuel_burned, previous_fuel, new_fuel, timestamp) VALUES ('%s', %s, '%s', %s, %s, %s, %s, %s, '%s', %s, %s, %s, '%s')" % (tx_hash, block_number, caller_address, caller_crew_id, ship_label, ship_id, asteroid_id, lot_id, burn_type, inventory_diff, old_inventory_amount, new_inventory_amount, timestamp))
        print(update_sql3)
        updateSql(update_sql3)

        update_sql4=("UPDATE inventories SET inventory_amount = %s WHERE inventory_label = %s AND inventory_id = %s AND inventory_slot = 1 AND resource_id = 170" % (new_fuel, ship_label, ship_id))
        print(update_sql4)
        updateSql(update_sql4)

    crew_asteroid_id = asteroid_id
    crew_lot_id = lot_id
    crew_ship_id = ship_id
    action = "ShipDocked"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def shipCommandeered(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_ship_commandeered (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)
    updateShip(tx_hash, block_number, ship_id)
    update_sql = ("UPDATE ships SET crew_id = %s WHERE ship_id = %s" % (caller_crew_id, ship_id))
    print(update_sql)
    updateSql(update_sql)

    update_sql2 = ("UPDATE ships_docked SET crew_id = %s WHERE ship_id = %s" % (caller_crew_id, ship_id))
    print(update_sql2)
    updateSql(update_sql2)

    asteroid_id, lot_id = getStationLocation(ship_label, ship_id)
    update_sql3 = ("UPDATE crews SET station_id = %s, station_label = %s WHERE crew_id = %s" % (ship_id, ship_label, caller_crew_id))
    print(update_sql3)
    updateSql(update_sql3)

    update_sql4=("UPDATE crewmates SET station_label = %s, station_id = %s WHERE crew_id = %s" % (ship_label, ship_id, caller_crew_id))
    print(update_sql4)
    updateSql(update_sql4)

    crew_asteroid_id = None
    crew_lot_id = None
    crew_ship_id = ship_id
    action = "ShipCommandeered"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def lotReclaimed(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, lot_label, lot_id, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_lot_reclaimed (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, lot_label, lot_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, lot_label, lot_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    crew_asteroid_id = None
    crew_lot_id = lot_id
    crew_ship_id = None
    action = "LotReclaimed"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def buildingRepossessed(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, building_label, building_id, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_building_repossessed (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, building_label, building_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, building_label, building_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    update_sql=("UPDATE buildings SET txn_id = '%s', block_number = %s, from_address = '%s', caller_address = '%s', crew_id = %s WHERE building_id = %s" % (tx_hash, block_number, from_address, caller_address, caller_crew_id, building_id))
    print(update_sql)
    updateSql(update_sql)

    building_type, asteroid_id, lot_id = getBuildingData(building_id)
    crew_asteroid_id = asteroid_id
    crew_lot_id = lot_id
    crew_ship_id = None
    action = "BuildingRepossessed"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def randomEventResolved(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, random_event, choice, action_type, action_target_label, action_target_id, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_random_event_resolved (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, random_event, choice, action_type, action_target_label, action_target_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, random_event, choice, action_type, action_target_label, action_target_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)


def crewDelegated(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, delegated_to, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_crew_delegated (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, delegated_to, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, '%s', %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, delegated_to, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    update_sql=("UPDATE crews SET delegated_address = '%s' WHERE crew_id = %s" % (delegated_to, caller_crew_id))
    print(update_sql)
    updateSql(update_sql)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def crewEjected(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ejected_crew_label, ejected_crew_id, finish_time, station_label, station_id, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_crew_ejected (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ejected_crew_label, ejected_crew_id, finish_time, station_label, station_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ejected_crew_label, ejected_crew_id, finish_time, station_label, station_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    update_sql=("UPDATE crews SET station_label = NULL, station_id = NULL WHERE crew_id = %s" % ejected_crew_id)
    print(update_sql)
    updateSql(update_sql)

    update_sql2=("UPDATE crewmates SET station_label = NULL, station_id = NULL WHERE crew_id = %s" % ejected_crew_id)
    print(update_sql2)
    updateSql(update_sql2)

    crew_asteroid_id = None
    crew_lot_id = None
    crew_ship_id = None
    action = "CrewEjected"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def depositListedForSale(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, price, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_deposit_listed_for_sale (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, price, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, price, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    update_sql=("UPDATE core_samples SET for_sale = 1, price = %s WHERE deposit_id = %s" % (price, deposit_id))
    print(update_sql)
    updateSql(update_sql)

    asteroid_id, lot_id = getCoreSampleData(deposit_id)
    crew_asteroid_id = asteroid_id
    crew_lot_id = lot_id
    crew_ship_id = None
    action = "DepositListedForSale"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def depositPurchased(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, price, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_deposit_purchased (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, price, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, price, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    update_sql=("UPDATE core_samples SET for_sale = 2, price = %s, buyer_address = '%s', buyer_crew_id = %s WHERE deposit_id = %s" % (price, caller_address, caller_crew_id, deposit_id))
    print(update_sql)
    updateSql(update_sql)

    asteroid_id, lot_id = getCoreSampleData(deposit_id)
    crew_asteroid_id = asteroid_id
    crew_lot_id = lot_id
    crew_ship_id = None
    action = "DepositPurchased"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def depositPurchasedV1(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, seller_crew_label, seller_crew_id, price, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_deposit_purchased_v1 (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, seller_crew_label, seller_crew_id, price, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, seller_crew_label, seller_crew_id, price, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)
    
    update_sql=("UPDATE core_samples SET for_sale = 2, price = %s, buyer_address = '%s', buyer_crew_id = %s WHERE deposit_id = %s" % (price, caller_address, caller_crew_id, deposit_id))
    print(update_sql)
    updateSql(update_sql)
    
    asteroid_id, lot_id = getCoreSampleData(deposit_id)
    crew_asteroid_id = asteroid_id
    crew_lot_id = lot_id
    crew_ship_id = None
    action = "DepositPurchased"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)
    
    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def depositUnlistedForSale(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_deposit_unlisted_for_sale (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    update_sql=("UPDATE core_samples SET for_sale = 0, price = NULL, buyer_address = NULL, buyer_crew_id = NULL WHERE deposit_id = %s" % deposit_id)
    print(update_sql)
    updateSql(update_sql)

    asteroid_id, lot_id = getCoreSampleData(deposit_id)
    crew_asteroid_id = asteroid_id
    crew_lot_id = lot_id
    crew_ship_id = None
    action = "DepositUnlistedForSale"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def sellOrderCreated(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, exchange_label, exchange_id, product_id, product_name, amount, price, storage_label, storage_id, storage_slot, valid_time, maker_fee, fee, timestamp):

    exchange_type, exchange_asteroid_id, exchange_lot_id = getBuildingData(exchange_id)
    if storage_label == 5:
        storage_type, storage_asteroid_id, storage_lot_id = getBuildingData(storage_id)
    elif storage_label == 6:
        storage_type, storage_asteroid_id, storage_lot_id = getShipData(storage_id)

    insert_sql=("INSERT IGNORE INTO dispatcher_sell_order_created (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, exchange_label, exchange_id, exchange_type, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price, storage_label, storage_id, storage_slot, storage_type, storage_asteroid_id, storage_lot_id, valid_time, maker_fee, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, exchange_label, exchange_id, exchange_type, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price, storage_label, storage_id, storage_slot, storage_type, storage_asteroid_id, storage_lot_id, valid_time, maker_fee, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    old_inventory_amount, old_maker_fee, state = getSellOrderInventory(exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price)
    if state is True:
        new_inventory_amount = (old_inventory_amount + amount)
        update_sql=("UPDATE sell_orders SET amount = %s, maker_fee = %s WHERE exchange_label = %s AND exchange_id = %s AND exchange_asteroid_id = %s AND exchange_lot_id = %s AND product_id = %s AND price = %s" % (new_inventory_amount, maker_fee, exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price))
        print(update_sql)
        updateSql(update_sql)
    else:
        insert_sql2=("INSERT INTO sell_orders (exchange_label, exchange_id, exchange_type, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price, valid_time, maker_fee) VALUES (%s, %s, %s, %s, %s, %s, '%s', %s, %s, %s, %s)" % (exchange_label, exchange_id, exchange_type, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price, valid_time, maker_fee))
        print(insert_sql2)
        updateSql(insert_sql2)

    state = None
    old_order_amount, old_maker_fee, state = getSellOrderInventoryWallet(caller_address, exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price)
    if state is True:
        new_order_amount = (old_order_amount + amount)
        update_wallet_sql=("UPDATE wallet_sell_orders SET amount = %s, maker_fee = %s WHERE exchange_label = %s AND exchange_id = %s AND exchange_asteroid_id = %s AND exchange_lot_id = %s AND product_id = %s AND price = %s AND caller_address = '%s'" % (new_order_amount, maker_fee, exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price, caller_address))
        print(update_wallet_sql)
        updateSql(update_wallet_sql)
    else:
        insert_wallet_sql=("INSERT INTO wallet_sell_orders (exchange_label, exchange_id, exchange_type, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price, valid_time, maker_fee, caller_address) VALUES (%s, %s, %s, %s, %s, %s, '%s', %s, %s, %s, %s, '%s')" % (exchange_label, exchange_id, exchange_type, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price, valid_time, maker_fee, caller_address))
        print(insert_wallet_sql)
        updateSql(insert_wallet_sql)

    crew_asteroid_id = exchange_asteroid_id
    crew_lot_id = exchange_lot_id
    crew_ship_id = None
    action = "SellOrderCreated"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def sellOrderFilled(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, seller_crew_label, seller_crew_id, exchange_label, exchange_id, product_id, product_name, amount, price, storage_label, storage_id, storage_slot, destination_label, destination_id, destination_slot, fill_count, fee, timestamp):

    exchange_type, exchange_asteroid_id, exchange_lot_id = getBuildingData(exchange_id)
    if storage_label == 5:
        storage_type, storage_asteroid_id, storage_lot_id = getBuildingData(storage_id)
    elif storage_label == 6:
        storage_type, storage_asteroid_id, storage_lot_id = getShipData(storage_id)

    if destination_label == 5:
        destination_type, destination_asteroid_id, destination_lot_id = getBuildingData(destination_id)
    elif destination_label == 6:
        destination_type, destination_asteroid_id, destination_lot_id = getShipData(destination_id)
    elif destination_label == 1:
        destination_type = 0
        destination_asteroid_id = storage_asteroid_id
        destination_lot_id = 0

    market_order = 1
    limit_order = 0

    insert_sql=("INSERT IGNORE INTO dispatcher_sell_order_filled (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, seller_crew_label, seller_crew_id, exchange_label, exchange_id, exchange_type, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price, storage_label, storage_id, storage_slot, storage_type, storage_asteroid_id, storage_lot_id, destination_label, destination_id, destination_slot, destination_type, destination_asteroid_id, destination_lot_id, market_order, limit_order, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, seller_crew_label, seller_crew_id, exchange_label, exchange_id, exchange_type, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price, storage_label, storage_id, storage_slot, storage_type, storage_asteroid_id, storage_lot_id, destination_label, destination_id, destination_slot, destination_type, destination_asteroid_id, destination_lot_id, market_order, limit_order, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    old_inventory_amount, maker_fee, state = getSellOrderInventory(exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price)
    new_inventory_amount = (old_inventory_amount - amount)

    update_sql=("UPDATE sell_orders SET amount = %s WHERE exchange_label = %s AND exchange_id = %s AND exchange_asteroid_id = %s AND exchange_lot_id = %s AND product_id = %s AND price = %s" % (new_inventory_amount, exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price))
    print(update_sql)
    updateSql(update_sql)

    seller_address = getCrewDelegate(seller_crew_id)

    update_wallet_sql=("UPDATE wallet_sell_orders SET amount = %s WHERE exchange_label = %s AND exchange_id = %s AND exchange_asteroid_id = %s AND exchange_lot_id = %s AND product_id = %s AND price = %s AND caller_address = '%s'" % (new_inventory_amount, exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price, seller_address))
    print(update_wallet_sql)
    updateSql(update_wallet_sql)

    order_type = "sell"
    insert_sql2=("INSERT IGNORE INTO products_sold (txn_id, block_number, from_address, buyer_address, buyer_crew_id, seller_address, seller_crew_id, exchange_label, exchange_id, exchange_type, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price, storage_label, storage_id, storage_slot, storage_type, storage_asteroid_id, storage_lot_id, destination_label, destination_id, destination_slot, destination_type, destination_asteroid_id, destination_lot_id, maker_fee, order_type, market_order, limit_order, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, '%s', %s, %s, %s, %s, %s, %s, %s, '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s', %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_id, seller_address, seller_crew_id, exchange_label, exchange_id, exchange_type, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price, storage_label, storage_id, storage_slot, storage_type, storage_asteroid_id, storage_lot_id, destination_label, destination_id, destination_slot, destination_type, destination_asteroid_id, destination_lot_id, maker_fee, order_type, market_order, limit_order, fee, timestamp))
    print(insert_sql2)
    updateSql(insert_sql2)

    crew_asteroid_id = exchange_asteroid_id
    crew_lot_id = exchange_lot_id
    crew_ship_id = None
    action = "SellOrderFilled"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def sellOrderCancelled(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, seller_crew_label, seller_crew_id, exchange_label, exchange_id, product_id, product_name, price, storage_label, storage_id, storage_slot, products, fee, timestamp):

    exchange_type, exchange_asteroid_id, exchange_lot_id = getBuildingData(exchange_id)
    if storage_label == 5:
        storage_type, storage_asteroid_id, storage_lot_id = getBuildingData(storage_id)
    elif storage_label == 6:
        storage_type, storage_asteroid_id, storage_lot_id = getShipData(storage_id)

    for product_row in products:
        amount = product_row['amount']

    insert_sql=("INSERT IGNORE INTO dispatcher_sell_order_cancelled (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, exchange_label, exchange_id, exchange_type, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price, storage_label, storage_id, storage_slot, storage_type, storage_asteroid_id, storage_lot_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, exchange_label, exchange_id, exchange_type, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price, storage_label, storage_id, storage_slot, storage_type, storage_asteroid_id, storage_lot_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    old_inventory_amount, old_maker_fee, state = getSellOrderInventory(exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price)
    if state is True:
        new_inventory_amount = (old_inventory_amount - amount)
        if new_inventory_amount > 0:
            update_sql=("UPDATE sell_orders SET amount = %s WHERE exchange_label = %s AND exchange_id = %s AND exchange_asteroid_id = %s AND exchange_lot_id = %s AND product_id = %s AND price = %s" % (new_inventory_amount, exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price))
        else:
            update_sql=("DELETE FROM sell_orders WHERE exchange_label = %s AND exchange_id = %s AND exchange_asteroid_id = %s AND exchange_lot_id = %s AND product_id = %s AND price = %s" % (exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price))
        print(update_sql)
        updateSql(update_sql)

    state = None
    old_order_amount, old_maker_fee, state = getSellOrderInventoryWallet(caller_address, exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price)
    if state is True:
        new_order_amount = (old_order_amount - amount)
        if new_order_amount > 0:
            update_wallet_sql=("UPDATE wallet_sell_orders SET amount = %s WHERE exchange_label = %s AND exchange_id = %s AND exchange_asteroid_id = %s AND exchange_lot_id = %s AND product_id = %s AND price = %s AND caller_address = '%s'" % (new_order_amount, exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price, caller_address))
        else:
            update_wallet_sql=("DELETE FROM wallet_sell_orders WHERE exchange_label = %s AND exchange_id = %s AND exchange_asteroid_id = %s AND exchange_lot_id = %s AND product_id = %s AND price = %s AND caller_address = '%s'" % (exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price, caller_address))
        print(update_wallet_sql)
        updateSql(update_wallet_sql)

    crew_asteroid_id = exchange_asteroid_id
    crew_lot_id = exchange_lot_id
    crew_ship_id = None
    action = "SellOrderCancelled"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def buyOrderCreated(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, exchange_label, exchange_id, product_id, product_name, amount, price, storage_label, storage_id, storage_slot, valid_time, maker_fee, fee, timestamp):

    exchange_type, exchange_asteroid_id, exchange_lot_id = getBuildingData(exchange_id)
    if storage_label == 5:
        storage_type, storage_asteroid_id, storage_lot_id = getBuildingData(storage_id)
    elif storage_label == 6:
        storage_type, storage_asteroid_id, storage_lot_id = getShipData(storage_id)

    insert_sql=("INSERT IGNORE INTO dispatcher_buy_order_created (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, exchange_label, exchange_id, exchange_type, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price, storage_label, storage_id, storage_slot, storage_type, storage_asteroid_id, storage_lot_id, valid_time, maker_fee, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, exchange_label, exchange_id, exchange_type, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price, storage_label, storage_id, storage_slot, storage_type, storage_asteroid_id, storage_lot_id, valid_time, maker_fee, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    old_inventory_amount, old_maker_fee, state = getBuyOrderInventory(exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price)
    if state is True:
        new_inventory_amount = (old_inventory_amount + amount)
        update_sql=("UPDATE buy_orders SET amount = %s, maker_fee = %s WHERE exchange_label = %s AND exchange_id = %s AND exchange_asteroid_id = %s AND exchange_lot_id = %s AND product_id = %s AND price = %s" % (new_inventory_amount, maker_fee, exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price))
        print(update_sql)
        updateSql(update_sql)
    else:
        insert_sql2=("INSERT INTO buy_orders (exchange_label, exchange_id, exchange_type, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price, valid_time, maker_fee) VALUES (%s, %s, %s, %s, %s, %s, '%s', %s, %s, %s, %s)" % (exchange_label, exchange_id, exchange_type, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price, valid_time, maker_fee))
        print(insert_sql2)
        updateSql(insert_sql2)

    state = None
    old_order_amount, old_maker_fee, state = getBuyOrderInventoryWallet(caller_address, exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price)
    if state is True:
        new_order_amount = (old_order_amount + amount)
        update_wallet_sql=("UPDATE wallet_buy_orders SET amount = %s, maker_fee = %s WHERE exchange_label = %s AND exchange_id = %s AND exchange_asteroid_id = %s AND exchange_lot_id = %s AND product_id = %s AND price = %s AND caller_address = '%s'" % (new_order_amount, maker_fee, exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price, caller_address))
        print(update_wallet_sql)
        updateSql(update_wallet_sql)
    else:
        insert_wallet_sql=("INSERT INTO wallet_buy_orders (exchange_label, exchange_id, exchange_type, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price, valid_time, maker_fee, caller_address) VALUES (%s, %s, %s, %s, %s, %s, '%s', %s, %s, %s, %s, '%s')" % (exchange_label, exchange_id, exchange_type, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price, valid_time, maker_fee, caller_address))
        print(insert_wallet_sql)
        updateSql(insert_wallet_sql)

    crew_asteroid_id = exchange_asteroid_id
    crew_lot_id = exchange_lot_id
    crew_ship_id = None
    action = "BuyOrderCreated"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def buyOrderFilled(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, buyer_crew_label, buyer_crew_id, exchange_label, exchange_id, product_id, product_name, amount, price, storage_label, storage_id, storage_slot, origin_label, origin_id, origin_slot, fill_count, fee, timestamp):

    exchange_type, exchange_asteroid_id, exchange_lot_id = getBuildingData(exchange_id)
    if storage_label == 5:
        storage_type, storage_asteroid_id, storage_lot_id = getBuildingData(storage_id)
    elif storage_label == 6:
        storage_type, storage_asteroid_id, storage_lot_id = getShipData(storage_id)

    if origin_label == 5:
        origin_type, origin_asteroid_id, origin_lot_id = getBuildingData(origin_id)
    elif origin_label == 6:
        origin_type, origin_asteroid_id, origin_lot_id = getShipData(origin_id)

    market_order = 1
    limit_order = 0

    insert_sql=("INSERT IGNORE INTO dispatcher_buy_order_filled (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, buyer_crew_label, buyer_crew_id, exchange_label, exchange_id, exchange_type, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price, storage_label, storage_id, storage_slot, storage_type, storage_asteroid_id, storage_lot_id, origin_label, origin_id, origin_slot, origin_type, origin_asteroid_id, origin_lot_id, market_order, limit_order, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, buyer_crew_label, buyer_crew_id, exchange_label, exchange_id, exchange_type, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price, storage_label, storage_id, storage_slot, storage_type, storage_asteroid_id, storage_lot_id, origin_label, origin_id, origin_slot, origin_type, origin_asteroid_id, origin_lot_id, market_order, limit_order, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    old_inventory_amount, maker_fee, state = getBuyOrderInventory(exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price)
    new_inventory_amount = (old_inventory_amount - amount)

    update_sql=("UPDATE buy_orders SET amount = %s WHERE exchange_label = %s AND exchange_id = %s AND exchange_asteroid_id = %s AND exchange_lot_id = %s AND product_id = %s AND price = %s" % (new_inventory_amount, exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price))
    print(update_sql)
    updateSql(update_sql)

    buyer_address = getCrewDelegate(buyer_crew_id)
    old_order_amount, old_maker_fee, state = getBuyOrderInventoryWallet(buyer_address, exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price)
    new_order_amount = (old_order_amount - amount)
    update_wallet_sql=("UPDATE wallet_buy_orders SET amount = %s WHERE exchange_label = %s AND exchange_id = %s AND exchange_asteroid_id = %s AND exchange_lot_id = %s AND product_id = %s AND price = %s AND caller_address = '%s'" % (new_order_amount, exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price, buyer_address))
    print(update_wallet_sql)
    updateSql(update_wallet_sql)

    order_type = "buy"
    insert_sql2=("INSERT IGNORE INTO products_sold (txn_id, block_number, from_address, buyer_address, buyer_crew_id, seller_address, seller_crew_id, exchange_label, exchange_id, exchange_type, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price, storage_label, storage_id, storage_slot, storage_type, storage_asteroid_id, storage_lot_id, origin_label, origin_id, origin_slot, origin_type, origin_asteroid_id, origin_lot_id, maker_fee, order_type, market_order, limit_order, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, '%s', %s, %s, %s, %s, %s, %s, %s, '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s', %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, buyer_address, buyer_crew_id, caller_address, caller_crew_id, exchange_label, exchange_id, exchange_type, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price, storage_label, storage_id, storage_slot, storage_type, storage_asteroid_id, storage_lot_id, origin_label, origin_id, origin_slot, origin_type, origin_asteroid_id, origin_lot_id, maker_fee, order_type, market_order, limit_order, fee, timestamp))
    print(insert_sql2)
    updateSql(insert_sql2)

    crew_asteroid_id = exchange_asteroid_id
    crew_lot_id = exchange_lot_id
    crew_ship_id = None
    action = "BuyOrderFilled"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def buyOrderCancelled(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, buyer_crew_label, buyer_crew_id, exchange_label, exchange_id, product_id, product_name, amount, price, storage_label, storage_id, storage_slot, fee, timestamp):

    exchange_type, exchange_asteroid_id, exchange_lot_id = getBuildingData(exchange_id)
    if storage_label == 5:
        storage_type, storage_asteroid_id, storage_lot_id = getBuildingData(storage_id)
    elif storage_label == 6:
        storage_type, storage_asteroid_id, storage_lot_id = getShipData(storage_id)

    insert_sql=("INSERT IGNORE INTO dispatcher_buy_order_cancelled (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, exchange_label, exchange_id, exchange_type, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price, storage_label, storage_id, storage_slot, storage_type, storage_asteroid_id, storage_lot_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, exchange_label, exchange_id, exchange_type, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price, storage_label, storage_id, storage_slot, storage_type, storage_asteroid_id, storage_lot_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    old_inventory_amount, old_maker_fee, state = getBuyOrderInventory(exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price)
    if state is True:
        new_inventory_amount = (old_inventory_amount - amount)
        update_sql=("UPDATE buy_orders SET amount = %s WHERE exchange_label = %s AND exchange_id = %s AND exchange_asteroid_id = %s AND exchange_lot_id = %s AND product_id = %s AND price = %s" % (new_inventory_amount, exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price))
        print(update_sql)
        updateSql(update_sql)

    state = None
    old_order_amount, old_maker_fee, state = getBuyOrderInventoryWallet(caller_address, exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price)
    if state is True:
        new_order_amount = (old_order_amount - amount)
        wallet_update_sql=("UPDATE wallet_buy_orders SET amount = %s WHERE exchange_label = %s AND exchange_id = %s AND exchange_asteroid_id = %s AND exchange_lot_id = %s AND product_id = %s AND price = %s AND caller_address = '%s'" % (new_order_amount, exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price, caller_address))
        print(wallet_update_sql)
        updateSql(wallet_update_sql)

    crew_asteroid_id = exchange_asteroid_id
    crew_lot_id = exchange_lot_id
    crew_ship_id = None
    action = "BuyOrderCancelled"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def contractPolicyAssigned(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, contract, entity_name, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_contract_policy_assigned (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, contract, entity_name, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, '%s', '%s', %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, contract, entity_name, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    insert_sql2=("INSERT IGNORE INTO contract_policies (txn_id, block_number, from_address, caller_address, crew_id, entity_label, entity_id, permission, contract, entity_name) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, '%s', '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_id, entity_label, entity_id, permission, contract, entity_name))
    print(insert_sql2)
    updateSql(insert_sql2)

    crew_asteroid_id = None
    crew_lot_id = None
    crew_ship_id = None
    action = "ContractPolicyAssigned"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def contractPolicyRemoved(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, entity_name, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_contract_policy_removed (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, entity_name, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, '%s', %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, entity_name, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    delete_sql=("DELETE FROM contract_policies WHERE entity_label = %s AND entity_id = %s AND permission = %s" % (entity_label, entity_id, permission))
    print(delete_sql)
    updateSql(delete_sql)

    crew_asteroid_id = None
    crew_lot_id = None
    crew_ship_id = None
    action = "ContractPolicyRemoved"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def prepaidPolicyAssigned(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, rate, initial_term, notice_period, entity_name, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_prepaid_policy_assigned (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, rate, initial_term, notice_period, entity_name, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, '%s', %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, rate, initial_term, notice_period, entity_name, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    insert_sql2=("INSERT IGNORE INTO prepaid_policies (txn_id, block_number, from_address, caller_address, crew_id, entity_label, entity_id, permission, rate, initial_term, notice_period, entity_name) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_id, entity_label, entity_id, permission, rate, initial_term, notice_period, entity_name))
    print(insert_sql2)
    updateSql(insert_sql2)

    crew_asteroid_id = None
    crew_lot_id = None
    crew_ship_id = None
    action = "PrepaidPolicyAssigned"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def prepaidAgreementAccepted(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permission, permitted_label, permitted_id, term, rate, initial_term, notice_period, asteroid_id, lot_id, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_prepaid_agreement_accepted (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permission, permitted_label, permitted_id, term, rate, initial_term, notice_period, asteroid_id, lot_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permission, permitted_label, permitted_id, term, rate, initial_term, notice_period, asteroid_id, lot_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    insert_sql2=("INSERT IGNORE INTO prepaid_agreements (txn_id, block_number, caller_address, crew_id, target_label, target_id, permission, permitted_label, permitted_id, term, rate, initial_term, notice_period, asteroid_id, lot_id) VALUES ('%s', %s, '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % (tx_hash, block_number, caller_address, caller_crew_id, target_label, target_id, permission, permitted_label, permitted_id, term, rate, initial_term, notice_period, asteroid_id, lot_id))
    print(insert_sql2)
    updateSql(insert_sql2)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def prepaidAgreementExtended(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permission, permitted_label, permitted_id, term, rate, initial_term, notice_period, asteroid_id, lot_id, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_prepaid_agreement_extended (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permission, permitted_label, permitted_id, term, rate, initial_term, notice_period, asteroid_id, lot_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permission, permitted_label, permitted_id, term, rate, initial_term, notice_period, asteroid_id, lot_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    update_sql=("UPDATE prepaid_agreements SET txn_id = '%s', block_number = %s, initial_term = %s, notice_period = %s WHERE crew_id = %s AND target_label = %s AND target_id = %s AND permission = %s AND permitted_label = %s AND permitted_id = %s AND rate = %s AND asteroid_id = %s AND lot_id = %s" % (tx_hash, block_number, initial_term, notice_period, caller_crew_id, target_label, target_id, permission, permitted_label, permitted_id, rate, asteroid_id, lot_id))
    print(update_sql)
    updateSql(update_sql)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def prepaidAgreementCancelled(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permission, permitted_label, permitted_id, eviction_time, asteroid_id, lot_id, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_prepaid_agreement_cancelled (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permission, permitted_label, permitted_id, eviction_time, asteroid_id, lot_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permission, permitted_label, permitted_id, eviction_time, asteroid_id, lot_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    update_sql=("UPDATE prepaid_agreements SET cancelled_txn_id = '%s', cancelled_block_number = %s, status = 2, eviction_time = %s WHERE target_label = %s AND target_id = %s AND permission = %s AND permitted_label = %s AND permitted_id = %s AND asteroid_id = %s AND lot_id = %s" % (tx_hash, block_number, eviction_time, target_label, target_id, permission, permitted_label, permitted_id, asteroid_id, lot_id))
    print(update_sql)
    updateSql(update_sql)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def contractAgreementAccepted(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permission, permitted_label, permitted_id, contract_address, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_contract_agreement_accepted (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permission, permitted_label, permitted_id, contract_address, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, '%s', %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permission, permitted_label, permitted_id, contract_address, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    insert_sql2=("INSERT IGNORE INTO contract_agreements (txn_id, block_number, caller_address, crew_id, target_label, target_id, permission, permitted_label, permitted_id, contract_address) VALUES ('%s', %s, '%s', %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, caller_address, caller_crew_id, target_label, target_id, permission, permitted_label, permitted_id, contract_address))
    print(insert_sql2)
    updateSql(insert_sql2)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def addedToWhitelist(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, target_label, target_id, permission, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_added_to_whitelist (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, target_label, target_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, target_label, target_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    whitelist_count = checkWhitelist(entity_label, entity_id, target_label, target_id, permission)
    if whitelist_count == 0:
        insert_sql2 = ("INSERT IGNORE INTO whitelist (txn_id, block_number, caller_address, crew_id, entity_label, entity_id, target_label, target_id, permission) VALUES ('%s', %s, '%s', %s, %s, %s, %s, %s, %s)" % (tx_hash, block_number, caller_address, caller_crew_id, entity_label, entity_id, target_label, target_id, permission))
        print(insert_sql2)
        updateSql(insert_sql2)

    crew_asteroid_id = None
    crew_lot_id = None
    crew_ship_id = None
    action = "AddedToWhitelist"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def addedToWhitelistV1(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permission, permitted_label, permitted_id, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_added_to_whitelist_v1 (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permission, permitted_label, permitted_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permission, permitted_label, permitted_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    whitelist_count = checkWhitelistV1(target_label, target_id, permitted_label, permitted_id, permission)
    if whitelist_count == 0:
        insert_sql2 = ("INSERT IGNORE INTO whitelist_v1 (txn_id, block_number, caller_address, crew_id, target_label, target_id, permitted_label, permitted_id, permission) VALUES ('%s', %s, '%s', %s, %s, %s, %s, %s, %s)" % (tx_hash, block_number, caller_address, caller_crew_id, target_label, target_id, permitted_label, permitted_id, permission))
        print(insert_sql2)
        updateSql(insert_sql2)

    crew_asteroid_id = None
    crew_lot_id = None
    crew_ship_id = None
    action = "AddedToWhitelist"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def addedAccountToWhitelist(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permission, permitted, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_added_account_to_whitelist (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permission, permitted, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, '%s', %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permission, permitted, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)
    
    whitelist_count = checkAccountWhitelist(target_label, target_id, permitted, permission)
    if whitelist_count == 0:
        insert_sql2 = ("INSERT IGNORE INTO account_whitelist (txn_id, block_number, caller_address, crew_id, target_label, target_id, permitted, permission) VALUES ('%s', %s, '%s', %s, %s, %s, '%s', %s)" % (tx_hash, block_number, caller_address, caller_crew_id, target_label, target_id, permitted, permission))
        print(insert_sql2)
        updateSql(insert_sql2)
    
    crew_asteroid_id = None
    crew_lot_id = None
    crew_ship_id = None
    action = "AddedAccountToWhitelist"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)
        
    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def removedFromWhitelist(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, target_label, target_id, permission, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_removed_from_whitelist (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, target_label, target_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, target_label, target_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    delete_sql = ("DELETE FROM whitelist WHERE entity_label = %s AND entity_id = %s AND permission = %s AND target_label = %s AND target_id = %s" % (entity_label, entity_id, permission, target_label, target_id))
    print(delete_sql)
    updateSql(delete_sql)

    crew_asteroid_id = None
    crew_lot_id = None
    crew_ship_id = None
    action = "RemovedFromWhitelist"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def removedFromWhitelistV1(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permitted_label, permitted_id, permission, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_removed_from_whitelist_v1 (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permitted_label, permitted_id, permission, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permitted_label, permitted_id, permission, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    delete_sql = ("DELETE FROM whitelist_v1 WHERE target_label = %s AND target_id = %s AND permission = %s AND permitted_label = %s AND permitted_id = %s" % (target_label, target_id, permission, permitted_label, permitted_id))
    print(delete_sql)
    updateSql(delete_sql)

    crew_asteroid_id = None
    crew_lot_id = None
    crew_ship_id = None
    action = "RemovedFromWhitelistV1"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def prepaidPolicyRemoved(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, entity_name, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_prepaid_policy_removed (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, entity_name, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, '%s', %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, entity_name, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    delete_sql=("DELETE FROM prepaid_policies WHERE entity_label = %s AND entity_id = %s AND permission = %s" % (entity_label, entity_id, permission))
    print(delete_sql)
    updateSql(delete_sql)

    crew_asteroid_id = None
    crew_lot_id = None
    crew_ship_id = None
    action = "PrepaidPolicyRemoved"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def prepaidMerklePolicyRemoved(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, entity_name, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_prepaid_merkle_policy_removed (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, entity_name, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, '%s', %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, entity_name, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    delete_sql=("DELETE FROM prepaid_merkle_policies WHERE entity_label = %s AND entity_id = %s AND permission = %s" % (entity_label, entity_id, permission))
    print(delete_sql)
    updateSql(delete_sql)

    crew_asteroid_id = None
    crew_lot_id = None
    crew_ship_id = None
    action = "PrepaidMerklePolicyRemoved"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def publicPolicyRemoved(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, entity_name, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_public_policy_removed (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, entity_name, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, '%s', %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, entity_name, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    delete_sql=("DELETE FROM public_policies WHERE entity_label = %s AND entity_id = %s AND permission = %s" % (entity_label, entity_id, permission))
    print(delete_sql)
    updateSql(delete_sql)

    crew_asteroid_id = None
    crew_lot_id = None
    crew_ship_id = None
    action = "PublicPolicyRemoved"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def transitStarted(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, origin_label, origin_id, destination_label, destination_id, departure, arrival, finish_time, fee, timestamp, new_fuel):

    ship_type = getShipType(ship_id)
    if ship_type is None:
        ship_type = 0
    insert_sql=("INSERT IGNORE INTO dispatcher_transit_started (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, ship_type, origin_label, origin_id, destination_label, destination_id, departure, arrival, finish_time, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, ship_type, origin_label, origin_id, destination_label, destination_id, departure, arrival, finish_time, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    cargo = getCargo(ship_id)
    c_type_cargo = getRawCargo(ship_id, 'C')
    m_type_cargo = getRawCargo(ship_id, 'M')
    s_type_cargo = getRawCargo(ship_id, 'S')
    i_type_cargo = getRawCargo(ship_id, 'I')
    print("C_TYPE_CARGO: %s" % c_type_cargo)
    print("M_TYPE_CARGO: %s" % m_type_cargo)
    print("S_TYPE_CARGO: %s" % s_type_cargo)
    print("I_TYPE_CARGO: %s" % i_type_cargo)

    insert_sql2=("INSERT IGNORE INTO transit (start_txn_id, start_block_number, start_timestamp, from_address, caller_address, crew_id, ship_label, ship_id, ship_type, origin_label, origin_id, destination_label, destination_id, departure, arrival, finish_time, status, cargo, c_cargo, m_cargo, s_cargo, i_cargo, fuel) VALUES ('%s', %s, '%s', '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1, %s, %s, %s, %s, %s, %s)" % (tx_hash, block_number, timestamp, from_address, caller_address, caller_crew_id, ship_label, ship_id, ship_type, origin_label, origin_id, destination_label, destination_id, departure, arrival, finish_time, cargo, c_type_cargo, m_type_cargo, s_type_cargo, i_type_cargo, new_fuel))
    print(insert_sql2)
    updateSql(insert_sql2)

    delete_sql=("DELETE FROM ships_docked WHERE ship_id = %s" % ship_id)
    print(delete_sql)
    updateSql(delete_sql)

    old_inventory_amount, state = getInventory(ship_label, ship_id, 1, 170)
    inventory_diff = (old_inventory_amount - new_fuel)
    new_inventory_amount = new_fuel
    burn_type = 'TransitStarted'
    update_sql = ("INSERT IGNORE INTO propellant_burned (txn_id, block_number, caller_address, crew_id, ship_label, ship_id, burn_type, fuel_burned, previous_fuel, new_fuel, timestamp) VALUES ('%s', %s, '%s', %s, %s, %s, '%s', %s, %s, %s, '%s')" % (tx_hash, block_number, caller_address, caller_crew_id, ship_label, ship_id, burn_type, inventory_diff, old_inventory_amount, new_inventory_amount, timestamp))
    print(update_sql)
    updateSql(update_sql)

    update_sql2=("UPDATE inventories SET inventory_amount = %s WHERE inventory_label = %s AND inventory_id = %s AND inventory_slot = 1 AND resource_id = 170" % (new_fuel, ship_label, ship_id))
    print(update_sql2)
    updateSql(update_sql2)

    crew_asteroid_id = origin_id
    crew_lot_id = None
    crew_ship_id = ship_id
    action = "TransitStarted"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def transitFinished(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, origin_label, origin_id, destination_label, destination_id, departure, arrival, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_transit_finished (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, origin_label, origin_id, destination_label, destination_id, departure, arrival, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, origin_label, origin_id, destination_label, destination_id, departure, arrival, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    update_sql=("UPDATE transit SET finish_txn_id = '%s', finish_block_number = %s, finish_timestamp = '%s', status = 2 WHERE ship_id = %s AND origin_id = %s AND destination_id = %s AND status = 1" % (tx_hash, block_number, timestamp, ship_id, origin_id, destination_id))
    print(update_sql)
    updateSql(update_sql)

    crew_asteroid_id = destination_id
    crew_lot_id = None
    crew_ship_id = ship_id
    action = "TransitFinished"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def prepareForLaunchRewardClaimed(tx_hash, block_number, from_address, caller_address, asteroid_label, asteroid_id, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_prepare_for_launch_reward_claim (txn_id, block_number, from_address, caller_address, asteroid_label, asteroid_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, asteroid_label, asteroid_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    insert_sql2=("INSERT IGNORE INTO prepare_for_launch_rewards (txn_id, block_number, caller_address, asteroid_id, redeemed) VALUES ('%s', %s, '%s', %s, 1)" % (tx_hash, block_number, caller_address, asteroid_id))
    print(insert_sql2)
    updateSql(insert_sql2)


def arrivalRewardClaimed(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, asteroid_label, asteroid_id, ships, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_arrival_reward_claim (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, asteroid_label, asteroid_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, asteroid_label, asteroid_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    insert_sql2=("INSERT IGNORE INTO arrival_rewards (txn_id, block_number, caller_address, crew_id, asteroid_id, redeemed) VALUES ('%s', %s, '%s', %s, %s, 1)" % (tx_hash, block_number, caller_address, caller_crew_id, asteroid_id))
    print(insert_sql2)
    updateSql(insert_sql2)

    for ship in ships:
        ship_label = 6
        propellant_slot = 1
        inventory_slot = 2
        ship_id = ship['ship_id']
        ship_type = ship['ship_type']
        ship_owner = caller_address
        ship_type_name = ship['ship_type_name']
        propellant = ship['propellant']
        products = ship['products']

        ship_exists = checkShipExists(ship_id)
        if ship_exists == 0:
            insert_sql3=("INSERT IGNORE INTO ships (txn_id, block_number, caller_address, ship_owner, crew_id, ship_id, ship_type, ship_type_name) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, '%s')" % (tx_hash, block_number, caller_address, caller_address, caller_crew_id, ship_id, ship_type, ship_type_name))
            print(insert_sql3)
            updateSql(insert_sql3)

        else:
            update_sql=("UPDATE ships SET txn_id = '%s', block_number = %s, caller_address = '%s', ship_owner = '%s', crew_id = %s, ship_type = %s, ship_type_name = '%s' WHERE ship_id = %s" % (tx_hash, block_number, caller_address, caller_address, caller_crew_id, ship_type, ship_type_name, ship_id))
            print(update_sql)
            updateSql(update_sql)

        insert_sql4=("INSERT IGNORE INTO stations (txn_id, block_number, from_address, caller_address, crew_id, station_id, station_label) VALUES ('%s', %s, '%s', '%s', %s ,%s, %s)" % (tx_hash, block_number, from_address, caller_address, caller_crew_id, ship_id, ship_label))
        print(insert_sql4)
        updateSql(insert_sql4)
        
        for product in products:
            product_id = product['product_id']
            product_name = product['product_name']
            product_amount = product['product_amount']
            insert_sql5=("INSERT INTO inventories (inventory_label, inventory_id, inventory_slot, inventory_type, resource_id, inventory_amount) VALUES (%s, %s, %s, %s, %s, %s)" % (ship_label, ship_id, inventory_slot, ship_type, product_id, product_amount))
            print(insert_sql5)
            updateSql(insert_sql5)

            insert_sql6=("INSERT IGNORE INTO products_produced (txn_id, block_number, caller_address, crew_id, destination_label, destination_id, destination_type, resource_id, resource_name, resource_amount, timestamp) VALUES ('%s', %s, '%s', %s, %s, %s, %s, %s, '%s', %s, '%s')" % (tx_hash, block_number, caller_address, caller_crew_id, ship_label, ship_id, ship_type, product_id, product_name, product_amount, timestamp))
            print(insert_sql6)
            updateSql(insert_sql6)

        insert_sql7=("INSERT INTO inventories (inventory_label, inventory_id, inventory_slot, inventory_type, resource_id, inventory_amount) VALUES (%s, %s, %s, %s, %s, %s)" % (ship_label, ship_id, propellant_slot, ship_type, 170, propellant))
        print(insert_sql7)
        updateSql(insert_sql7)

        insert_sql8=("INSERT IGNORE INTO propellant_produced (txn_id, block_number, caller_address, crew_id, destination_label, destination_id, destination_type, amount, method, timestamp) VALUES ('%s', %s, '%s', %s, %s, %s, %s, %s, '%s', '%s')" % (tx_hash, block_number, caller_address, caller_crew_id, ship_label, ship_id, ship_type, propellant, 'arrival', timestamp))
        print(insert_sql8)
        updateSql(insert_sql8)

        for_sale=checkForSale(ship_id)
        if for_sale > 0:
            update_sql2=("UPDATE ships_for_sale SET ship_type = %s WHERE ship_id = %s" % (ship_type, ship_id))
            print(update_sql2)
            updateSql(update_sql2)

        ship_sold=checkShipSold(ship_id)
        if ship_sold > 0:
            update_sql3=("UPDATE ships_sold SET ship_type = %s WHERE ship_id = %s" % (ship_type, ship_id))
            print(update_sql3)
            updateSql(update_sql3)

        crew_asteroid_id = asteroid_id
        crew_lot_id = None
        crew_ship_id = ship_id
        action = "ArrivalRewardClaimed"
        crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def shipAssemblyStartedV1(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, ship_type, ship_type_name, dry_dock_label, dry_dock_id, dry_dock_slot, origin_label, origin_id, origin_slot, finish_time, origin_inventory, fee, timestamp):

    dry_dock_type, dry_dock_asteroid_id, dry_dock_lot_id = getBuildingData(dry_dock_id)
    if origin_label == 5:
        origin_type, origin_asteroid_id, origin_lot_id = getBuildingData(origin_id)
    elif origin_label == 6:
        origin_type, origin_asteroid_id, origin_lot_id = getShipData(origin_id)

    insert_sql=("INSERT IGNORE INTO dispatcher_ship_assembly_started_v1 (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, ship_type, ship_type_name, dry_dock_label, dry_dock_id, dry_dock_slot, dry_dock_type, dry_dock_asteroid_id, dry_dock_lot_id, origin_label, origin_id, origin_slot, origin_type, origin_asteroid_id, origin_lot_id, finish_time, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, ship_type, ship_type_name, dry_dock_label, dry_dock_id, dry_dock_slot, dry_dock_type, dry_dock_asteroid_id, dry_dock_lot_id, origin_label, origin_id, origin_slot, origin_type, origin_asteroid_id, origin_lot_id, finish_time, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    insert_sql2=("INSERT IGNORE INTO ship_assembly (start_txn_id, start_block_number, start_timestamp, caller_address, crew_id, ship_id, ship_type, ship_type_name, dry_dock_label, dry_dock_id, dry_dock_slot, dry_dock_type, dry_dock_asteroid_id, dry_dock_lot_id, origin_label, origin_id, origin_slot, origin_type, origin_asteroid_id, origin_lot_id, finish_time, status) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)" % (tx_hash, block_number, timestamp, caller_address, caller_crew_id, ship_id, ship_type, ship_type_name, dry_dock_label, dry_dock_id, dry_dock_slot, dry_dock_type, dry_dock_asteroid_id, dry_dock_lot_id, origin_label, origin_id, origin_slot, origin_type, origin_asteroid_id, origin_lot_id, finish_time))
    print(insert_sql2)
    updateSql(insert_sql2)

    ship_exists = checkShipExists(ship_id)
    if ship_exists == 0:
        insert_sql3=("INSERT IGNORE INTO ships (txn_id, block_number, caller_address, ship_owner, crew_id, ship_id, ship_type, ship_type_name) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, '%s')" % (tx_hash, block_number, caller_address, caller_address, caller_crew_id, ship_id, ship_type, ship_type_name))
        print(insert_sql3)
        updateSql(insert_sql3)
    else:
        update_sql=("UPDATE ships SET txn_id = '%s', block_number = %s, caller_address = '%s', ship_owner = '%s', crew_id = %s, ship_type = %s, ship_type_name = '%s' WHERE ship_id = %s" % (tx_hash, block_number, caller_address, caller_address, caller_crew_id, ship_type, ship_type_name, ship_id))
        print(update_sql)
        updateSql(update_sql)

    dry_dock_type, dry_dock_asteroid_id, dry_dock_lot_id = getBuildingData(dry_dock_id)
    ship_docked = checkShipDock(ship_id)
    if ship_docked == 0:
        insert_sql4=("INSERT IGNORE INTO ships_docked (txn_id, block_number, caller_address, crew_id, ship_label, ship_id, dock_label, dock_id, dock_type, dock_asteroid_id, dock_lot_id, status) VALUES ('%s', %s, '%s', %s, %s, %s, %s, %s, %s, %s, %s, 1)" % (tx_hash, block_number, caller_address, caller_crew_id, ship_label, ship_id, dry_dock_label, dry_dock_id, dry_dock_type, dry_dock_asteroid_id, dry_dock_lot_id))
        print(insert_sql4)
        updateSql(insert_sql4)

    else:
        update_sql2=("UPDATE ships_docked SET txn_id = '%s', block_number = %s, caller_address = '%s', crew_id = %s, dock_label = %s, dock_id = %s, dock_type = %s, dock_asteroid_id = %s, dock_lot_id = %s, status = 0  WHERE ship_id = %s" % (tx_hash, block_number, caller_address, caller_crew_id, dry_dock_label, dry_dock_id, dry_dock_type, dry_dock_asteroid_id, dry_dock_lot_id, ship_id))
        print(update_sql2)
        updateSql(update_sql2)

    if ship_type_name == 'LIGHT_TRANSPORT':
        components = component.getLightTransport()
    elif ship_type_name == 'HEAVY_TRANSPORT':
        components = component.getHeavyTransport()
    elif ship_type_name == 'SHUTTLE':
        components = component.getShuttle()

    if len(origin_inventory) == 0:
        delete_sql = ("DELETE FROM inventories WHERE inventory_label = %s AND inventory_id = %s AND inventory_slot = %s AND inventory_type = %s" % (origin_label, origin_id, origin_slot, origin_type))
        print(delete_sql)
        updateSql(delete_sql)
    else:
        for inventory in origin_inventory:
            inv_resource_id = inventory['resource_id']
            inv_resource_name = inventory['resource_name']
            inv_resource_amount = inventory['resource_amount']
            state = getInventoryState(origin_label, origin_id, origin_slot, inv_resource_id)
            if state > 0:
                update_sql2=("UPDATE inventories SET inventory_amount = %s WHERE inventory_label = %s AND inventory_id = %s AND inventory_slot = %s AND inventory_type = %s AND resource_id = %s" % (inv_resource_amount, origin_label, origin_id, origin_slot, origin_type, inv_resource_id))
                print(update_sql2)
                updateSql(update_sql2)
            else:
                insert_sql2=("INSERT INTO inventories (inventory_label, inventory_id, inventory_slot, inventory_type, resource_id, inventory_amount) VALUES (%s, %s, %s, %s, %s, %s)" % (origin_label, origin_id, origin_slot, origin_type, inv_resource_id, inv_resource_amount))
                print(insert_sql2)
                updateSql(insert_sql2)

    for input_dict in components:
        print("input_dict: %s" % input_dict)
        input_id = int(input_dict['id'])
        input_name = input_dict['name']
        input_amount = int(input_dict['amount'])
        insert_sql6=("INSERT IGNORE INTO products_consumed (txn_id, block_number, caller_address, crew_id, origin_label, origin_id, origin_type, asteroid_id, lot_id, resource_id, resource_name, resource_amount, timestamp) VALUES ('%s', %s, '%s', %s, %s, %s, %s, %s, %s, %s, '%s', %s, '%s')" % (tx_hash, block_number, caller_address, caller_crew_id, origin_label, origin_id, origin_type, origin_asteroid_id, origin_lot_id, input_id, input_name, input_amount, timestamp))
        print(insert_sql6)
        updateSql(insert_sql6)

    crew_asteroid_id = origin_asteroid_id
    crew_lot_id = origin_lot_id
    crew_ship_id = ship_id
    action = "ShipAssemblyStarted"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def shipAssemblyFinished(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, dry_dock_label, dry_dock_id, dry_dock_slot, destination_label, destination_id, finish_time, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_ship_assembly_finished (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, dry_dock_label, dry_dock_id, dry_dock_slot, destination_label, destination_id, finish_time, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, dry_dock_label, dry_dock_id, dry_dock_slot, destination_label, destination_id, finish_time, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    if destination_label == 4:
        entity = sdk.unpackLot(destination_id)
        destination_lot_id = entity['lotIndex']
        destination_asteroid_id = entity['asteroidId']
        destination_type = 4
    else:
        destination_type, destination_asteroid_id, destination_lot_id = getBuildingData(destination_id)

    dry_dock_type, dry_dock_asteroid_id, dry_dock_lot_id = getBuildingData(dry_dock_id)

    update_sql=("UPDATE ship_assembly SET finish_txn_id = '%s', finish_block_number = %s, finish_timestamp = '%s', destination_label = %s, destination_id = %s, destination_type = %s, destination_asteroid_id = %s, destination_lot_id = %s, finish_time = %s, status = 2 WHERE ship_id = %s" % (tx_hash, block_number, timestamp, destination_label, destination_id, destination_type, destination_asteroid_id, destination_lot_id, finish_time, ship_id)) 
    print(update_sql)
    updateSql(update_sql)

    ship_docked = checkShipDock(ship_id)
    if ship_docked == 0:
        insert_sql2=("INSERT IGNORE INTO ships_docked (txn_id, block_number, caller_address, crew_id, ship_label, ship_id, dock_label, dock_id, dock_type, dock_asteroid_id, dock_lot_id, status) VALUES ('%s', %s, '%s', %s, %s, %s, %s, %s, %s, %s, %s, 1)" % (tx_hash, block_number, caller_address, caller_crew_id, ship_label, ship_id, destination_label, destination_id, destination_type, destination_asteroid_id, destination_lot_id))
        print(insert_sql2)
        updateSql(insert_sql2)

    else:
        update_sql2=("UPDATE ships_docked SET txn_id = '%s', block_number = %s, caller_address = '%s', crew_id = %s, dock_label = %s, dock_id = %s, dock_type = %s, dock_asteroid_id = %s, dock_lot_id = %s, status = 1 WHERE ship_id = %s" % (tx_hash, block_number, caller_address, caller_crew_id, destination_label, destination_id, destination_type, destination_asteroid_id, destination_lot_id, ship_id))
        print(update_sql2)
        updateSql(update_sql2)

    insert_sql3=("INSERT IGNORE INTO stations (txn_id, block_number, from_address, caller_address, crew_id, station_id, station_label, asteroid_id, lot_id) VALUES ('%s', %s, '%s', '%s', %s ,%s, %s, %s, %s)" % (tx_hash, block_number, from_address, caller_address, caller_crew_id, ship_id, ship_label, destination_asteroid_id, destination_lot_id))
    print(insert_sql3)
    updateSql(insert_sql3)

    ship_type, ignore_asteroid_id, ignore_lot_id = getShipData(ship_id)
    for_sale=checkForSale(ship_id)
    if for_sale > 0:
        update_sql3=("UPDATE ships_for_sale SET ship_type = %s WHERE ship_id = %s" % (ship_type, ship_id))
        print(update_sql3)
        updateSql(update_sql3)

    ship_sold=checkShipSold(ship_id)
    if ship_sold > 0:
        update_sql4=("UPDATE ships_sold SET ship_type = %s WHERE ship_id = %s" % (ship_type, ship_id))
        print(update_sql4)
        updateSql(update_sql4)

    crew_asteroid_id = destination_asteroid_id
    crew_lot_id = destination_lot_id
    crew_ship_id = ship_id
    action = "ShipAssemblyFinished"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def crewStationed(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, station_label, station_id, finish_time, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_crew_stationed (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, station_label, station_id, finish_time, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, station_label, station_id, finish_time, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    update_sql=("UPDATE crews SET station_label = %s, station_id = %s WHERE crew_id = %s" % (station_label, station_id, caller_crew_id))
    print(update_sql)
    updateSql(update_sql)

    update_sql2=("UPDATE crewmates SET station_label = %s, station_id = %s WHERE crew_id = %s" % (station_label, station_id, caller_crew_id))
    print(update_sql2)
    updateSql(update_sql2)

    asteroid_id, lot_id = getStationLocation(station_label, station_id)
    crew_asteroid_id = asteroid_id
    crew_lot_id = lot_id
    if station_label == 5:
        crew_ship_id = None
    else:
        crew_ship_id = station_id

    action = "CrewStationed"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def crewStationedV1(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, origin_station_label, origin_station_id, destination_station_label, destination_station_id, finish_time, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_crew_stationed_v1 (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, origin_station_label, origin_station_id, destination_station_label, destination_station_id, finish_time, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, origin_station_label, origin_station_id, destination_station_label, destination_station_id, finish_time, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)
    
    update_sql=("UPDATE crews SET station_label = %s, station_id = %s WHERE crew_id = %s" % (destination_station_label, destination_station_id, caller_crew_id))
    print(update_sql)
    updateSql(update_sql)
    
    update_sql2=("UPDATE crewmates SET station_label = %s, station_id = %s WHERE crew_id = %s" % (destination_station_label, destination_station_id, caller_crew_id))
    print(update_sql2)
    updateSql(update_sql2)
    
    asteroid_id, lot_id = getStationLocation(destination_station_label, destination_station_id)
    crew_asteroid_id = asteroid_id
    crew_lot_id = lot_id
    if destination_station_label == 5:
        crew_ship_id = None
    else:
        crew_ship_id = destination_station_id
        
    action = "CrewStationedV1"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)
    
    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def emergencyActivated(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_emergency_activated (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    ship_type, ship_asteroid_id, ship_lot_id = getShipData(ship_id)
    insert_sql2=("INSERT IGNORE INTO ship_emergency (start_txn_id, start_block_number, start_timestamp, caller_address, crew_id, ship_label, ship_id, ship_type, status) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, 1)" % (tx_hash, block_number, timestamp, caller_address, caller_crew_id, ship_label, ship_id, ship_type))
    print(insert_sql2)
    updateSql(insert_sql2)

    update_sql=("UPDATE ships SET emergency = 1 WHERE ship_id = %s" % ship_id)
    print(update_sql)
    updateSql(update_sql)

    update_sql2=("DELETE from inventories WHERE inventory_label = %s AND inventory_id = %s AND inventory_slot = 2" % (ship_label, ship_id))
    print(update_sql2)
    updateSql(update_sql2)

    crew_asteroid_id = None
    crew_lot_id = None
    crew_ship_id = ship_id
    action = "EmergencyActivated"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def emergencyDeactivated(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, fee, timestamp, new_fuel):

    insert_sql=("INSERT IGNORE INTO dispatcher_emergency_deactivated (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    ship_type, ship_asteroid_id, ship_lot_id = getShipData(ship_id)
    update_sql=("UPDATE ship_emergency SET finish_txn_id = '%s', finish_block_number = %s, finish_timestamp = '%s', status = 2 WHERE ship_id = %s" % (tx_hash, block_number, timestamp, ship_id))
    print(update_sql)
    updateSql(update_sql)

    update_sql2=("UPDATE ships SET emergency = 0 WHERE ship_id = %s" % ship_id)
    print(update_sql2)
    updateSql(update_sql2)

    if new_fuel is not None:
        old_inventory_amount, state = getInventory(ship_label, ship_id, 1, 170)
        inventory_diff = (old_inventory_amount - new_fuel)
        new_inventory_amount = new_fuel
        burn_type = 'EmergencyDeactivated'
        update_sql3 = ("INSERT IGNORE INTO propellant_burned (txn_id, block_number, caller_address, crew_id, ship_label, ship_id, burn_type, fuel_burned, previous_fuel, new_fuel, timestamp) VALUES ('%s', %s, '%s', %s, %s, %s, '%s', %s, %s, %s, '%s')" % (tx_hash, block_number, caller_address, caller_crew_id, ship_label, ship_id, burn_type, inventory_diff, old_inventory_amount, new_inventory_amount, timestamp))
        print(update_sql3)
        updateSql(update_sql3)

        update_sql4=("UPDATE inventories SET inventory_amount = %s WHERE inventory_label = %s AND inventory_id = %s AND inventory_slot = 1 AND resource_id = 170" % (new_fuel, ship_label, ship_id))
        print(update_sql4)
        updateSql(update_sql4)

    crew_asteroid_id = None
    crew_lot_id = None
    crew_ship_id = ship_id
    action = "EmergencyDeactivated"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def emergencyPropellantCollected(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, amount, fee, timestamp, new_fuel):

    insert_sql=("INSERT IGNORE INTO dispatcher_emergency_propellant_collected (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, amount, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, amount, fee, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    update_sql=("UPDATE ship_emergency SET amount = %s WHERE ship_id = %s" % (amount, ship_id))
    print(update_sql)
    updateSql(update_sql)

    inventory_slot = 1
    resource_id = 170

    inventory_type, dock_asteroid_id, dock_lot_id = getShipData(ship_id)

    if new_fuel is not None:

        update_sql2=("UPDATE inventories SET inventory_amount = %s WHERE inventory_label = %s AND inventory_id = %s AND inventory_slot = 1 AND resource_id = 170" % (new_fuel, ship_label, ship_id))
        print(update_sql2)
        updateSql(update_sql2)

    insert_sql2=("INSERT IGNORE INTO propellant_produced (txn_id, block_number, caller_address, crew_id, destination_label, destination_id, destination_type, amount, method, timestamp) VALUES ('%s', %s, '%s', %s, %s, %s, %s, %s, '%s', '%s')" % (tx_hash, block_number, caller_address, caller_crew_id, ship_label, ship_id, inventory_type, amount, "emergency", timestamp))
    print(insert_sql2)
    updateSql(insert_sql2)

    crew_asteroid_id = None
    crew_lot_id = None
    crew_ship_id = ship_id
    action = "EmergencyPropellantCollected"
    crewAction(tx_hash, block_number, caller_address, caller_crew_id, action, crew_asteroid_id, crew_lot_id, crew_ship_id, timestamp)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def exchangeConfigured(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, exchange_label, exchange_id, fee, timestamp):

    insert_sql=("INSERT IGNORE INTO dispatcher_exchange_configured (txn_id, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, exchange_label, exchange_id, fee, timestamp) VALUES ('%s', %s, '%s', '%s', %s, %s, %s, %s, %s, '%s')" % (tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, exchange_label, exchange_id, fee, timestamp))
    updateSql(insert_sql)

    if exchange_label == 5:
        exchange_type, asteroid_id, lot_id = getBuildingData(exchange_id)
    elif exchange_label == 6:
        exchange_type, asteroid_id, lot_id = getShipData(exchange_id)

    exchange_exists = checkExchangeConfigured(exchange_label, exchange_id)
    if exchange_exists == 0:
        insert_sql2=("INSERT IGNORE INTO configured_exchanges (txn_id, block_number, caller_address, crew_id, exchange_label, exchange_id, exchange_type, asteroid_id, lot_id) VALUES ('%s', %s, '%s', %s, %s, %s, %s, %s, %s)" % (tx_hash, block_number, caller_address, caller_crew_id, exchange_label, exchange_id, exchange_type, asteroid_id, lot_id))
        print(insert_sql2)
        updateSql(insert_sql2)
    else:
        update_sql=("UPDATE configured_exchanges SET txn_id = '%s', block_number = %s, caller_address = '%s', crew_id = %s, exchange_label = %s, exchange_id = %s, exchange_type = %s, asteroid_id = %s, lot_id = %s WHERE exchange_label = %s AND exchange_id = %s" % (tx_hash, block_number, caller_address, caller_crew_id, exchange_label, exchange_id, exchange_type, asteroid_id, lot_id, exchange_label, exchange_id))
        updateSql(update_sql)

    txn_sql=("UPDATE influence_txns SET crew_id = %s, wallet = '%s' WHERE txn_id = '%s'" % (caller_crew_id, caller_address, tx_hash))
    print(txn_sql)
    updateSql(txn_sql)


def checkExchangeConfigured(exchange_label, exchange_id):

    count = 0
    sql=("SELECT COUNT(*) FROM configured_exchanges WHERE exchange_label = %s AND exchange_id = %s" % (exchange_label, exchange_id))
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


def checkStartStatus(building_id):

    count = 0
    sql=("SELECT COUNT(*) FROM dispatcher_construction_started WHERE building_id = %s" % building_id)
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


def updateAsteroid(tx_hash, block_number, asteroid_id):

    asteroid_exists = checkAsteroid(asteroid_id)
    if asteroid_exists == 0:

        l1_metadata = getL1MetadataAsteroid(asteroid_id)
        print(l1_metadata)

        if l1_metadata is not None:
            name = l1_metadata[0]
            radius = l1_metadata[1]
            spectral_type = l1_metadata[2]
            bonuses = l1_metadata[3]
            surface_scan = l1_metadata[4]
            sql=("INSERT IGNORE INTO asteroids (txn_id, block_number, asteroid_id, name, radius, spectral_type, bonuses, surface_scan) VALUES ('%s', %s, %s, '%s', %s, %s, %s, %s)" % (tx_hash, block_number, asteroid_id, name, radius, spectral_type, bonuses, surface_scan))
        else:
            sql=("INSERT IGNORE INTO asteroids (txn_id, block_number, asteroid_id) VALUES ('%s', %s, %s)" % (tx_hash, block_number, asteroid_id))

        print(sql)
        updateSql(sql)


def updateShip(tx_hash, block_number, ship_id):

    ship_exists = checkShipExists(ship_id)
    if ship_exists == 0:
        sql=("INSERT IGNORE INTO ships (txn_id, block_number, ship_id, crew_id) VALUES ('%s', %s, %s, %s)" % (tx_hash, block_number, ship_id, crew_id))

        print(sql)
        updateSql(sql)


def getL1MetadataAsteroid(asteroid_id):

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


def checkBuilding(building_id):

    count = 0
    sql=("SELECT COUNT(*) FROM buildings WHERE building_id = %s" % building_id)
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


def checkPublicPolicy(entity_label, entity_id, permission):

    count = 0
    sql=("SELECT COUNT(*) FROM public_policies WHERE entity_label = %s AND entity_id = %s AND permission = %s" % (entity_label, entity_id, permission))
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


def checkWhitelist(entity_label, entity_id, target_label, target_id, permission):

    count = 0
    sql=("SELECT COUNT(*) FROM whitelist WHERE entity_label = %s AND entity_id = %s AND target_label = %s AND target_id = %s AND permission = %s" % (entity_label, entity_id, target_label, target_id, permission))
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


def checkWhitelistV1(target_label, target_id, permitted_label, permitted_id, permission):

    count = 0
    sql=("SELECT COUNT(*) FROM whitelist_v1 WHERE target_label = %s AND target_id = %s AND permitted_label = %s AND permitted_id = %s AND permission = %s" % (target_label, target_id, permitted_label, permitted_id, permission))
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


def checkAccountWhitelist(target_label, target_id, permitted, permission):

    count = 0
    sql=("SELECT COUNT(*) FROM account_whitelist WHERE target_label = %s AND target_id = %s AND permitted = '%s' AND permission = %s" % (target_label, target_id, permitted, permission))
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


def getCrewLocation(crew_id):
    
    station_id = None
    sql=("SELECT station_id FROM crews WHERE crew_id = %s" % crew_id)
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        station_id=result[0]

    cur.close()
    con.close()

    if station_id == 1:
        asteroid_id = 1
    else:
        asteroid_id, lot_id = getStationLocation(station_id)

    return asteroid_id


def getCrewDelegate(crew_id):

    delegate_address = None
    sql=("SELECT delegated_address FROM crews WHERE crew_id = %s" % crew_id)
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        if result is None:
            delegate_address = None
        else:
            delegate_address=result[0]

    cur.close()
    con.close()

    return delegate_address


def getStationLocation(station_label, station_id):

    sql=("SELECT asteroid_id, lot_id FROM stations WHERE station_label = %s AND station_id = %s" % (station_label, station_id))
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        if result is None:
            asteroid_id = 'NULL'
            lot_id = 'NULL'
        else:
            asteroid_id=result[0]
            lot_id=result[1]

    cur.close()
    con.close()

    if lot_id is None:
        lot_id = 'NULL'
    if asteroid_id is None:
        asteroid_id = 'NULL'

    return asteroid_id, lot_id


def getMaterialProcessingOutputs(tx_hash, processor_id, processor_slot):

    outputs = ()
    products = []
    sql=("SELECT start_txn_id, destination_id, destination_type, destination_label, destination_slot FROM processing_actions WHERE  processor_id = %s AND processor_slot = %s AND finish_txn_id = '%s'" % (processor_id, processor_slot, tx_hash))
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        if result is None:
            start_txn_id = None
            destination_id = None
            destination_type = None
            destination_label = None
            destination_slot = None
        else:
            start_txn_id=result[0]
            destination_id=result[1]
            destination_type=result[2]
            destination_label=result[3]
            destination_slot=result[4]

    cur.close()
    con.close()

    if start_txn_id is not None:
        sql2=("SELECT resource_name, resource_id, resource_amount FROM dispatcher_material_processing_started_outputs WHERE txn_id = '%s'" % start_txn_id)
        print(sql2)
        con = pymysql.connect("127.0.0.1", db_user, db_password, db)
        with con:
            cur = con.cursor()
            cur.execute("%s" % sql2)
            rows = cur.fetchall()
        cur.close()
        cur.close()

        if rows == None:
            products = []

        for row in rows:
            products.append({"output_name": row[0], "output_id": row[1], "output_amount": row[2]})

    outputs = {"destination_id": destination_id, "destination_type": destination_type, "destination_label": destination_label, "destination_slot": destination_slot, "products": products}
    return outputs


def getBuildingData(building_id):

    sql=("SELECT building_type, asteroid_id, lot_id FROM buildings WHERE building_id = %s" % building_id)
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        if result is None:
            building_type = None
            asteroid_id = None
            lot_id = None
        else:
            building_type=result[0]
            asteroid_id=result[1]
            lot_id=result[2]

    cur.close()
    con.close()

    if building_type is None:
        building_type = 0

    if asteroid_id is None:
        asteroid_id = 'NULL'

    if lot_id is None:
        lot_id = 'NULL'

    return building_type, asteroid_id, lot_id


def getCoreSampleData(deposit_id):

    sql=("SELECT asteroid_id, lot_id FROM core_samples WHERE deposit_id = %s" % deposit_id)
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        asteroid_id=result[0]
        lot_id=result[1]

    cur.close()
    con.close()

    return asteroid_id, lot_id


def getStation(crew_id):

    sql=("SELECT station_label, station_id FROM crews WHERE crew_id = %s" % crew_id)
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        if result is None:
            station_label = 'NULL'
            station_id = 'NULL'
        else:
            station_label=result[0]
            station_id=result[1]

    cur.close()
    con.close()

    return station_label, station_id


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

    return ship_type, asteroid_id, lot_id


def getCoreSample(deposit_id):

    sql=("SELECT initial_yield FROM core_samples WHERE deposit_id = %s" % deposit_id)
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        initial_yield=result[0]

    cur.close()
    con.close()

    if initial_yield is None:
        initial_yield = 0

    print("initial_yield: %s" % initial_yield)
    return initial_yield


def getInventory(inventory_label, inventory_id, inventory_slot, resource_id):

    state = False
    inventory_amount = 0
    sql=("SELECT inventory_amount FROM inventories WHERE inventory_label = %s AND inventory_id = %s AND inventory_slot = %s AND resource_id = %s" % (inventory_label, inventory_id, inventory_slot, resource_id))
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        if result is None:
            inventory_amount = 0
        else:
            inventory_amount=result[0]
            state = True

    cur.close()
    con.close()

    return inventory_amount, state


def getInventoryState(inventory_label, inventory_id, inventory_slot, resource_id):

    state = 0
    sql=("SELECT COUNT(*) FROM inventories WHERE inventory_label = %s AND inventory_id = %s AND inventory_slot = %s AND resource_id = %s" % (inventory_label, inventory_id, inventory_slot, resource_id))
    #print(sql)
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


def getSellOrderInventory(exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price):

    state = False
    sell_amount = 0

    sql=("SELECT amount, maker_fee FROM sell_orders WHERE exchange_label = %s AND exchange_id = %s AND exchange_asteroid_id = %s AND exchange_lot_id = %s AND product_id = %s AND price = %s" % (exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price))
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        if result is None:
            sell_amount = 0
            maker_fee = 0
            crew_id = None
        else:
            sell_amount=result[0]
            maker_fee=result[1]
            state = True

    cur.close()
    con.close()

    return sell_amount, maker_fee, state


def getSellOrderInventoryWallet(caller_address, exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price):

    state = False
    sell_amount = 0

    sql=("SELECT amount, maker_fee FROM wallet_sell_orders WHERE exchange_label = %s AND exchange_id = %s AND exchange_asteroid_id = %s AND exchange_lot_id = %s AND product_id = %s AND price = %s AND caller_address = '%s'" % (exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price, caller_address))
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        if result is None:
            sell_amount = 0
            maker_fee = 0
            crew_id = None
        else:
            sell_amount=result[0]
            maker_fee=result[1]
            state = True

    cur.close()
    con.close()

    return sell_amount, maker_fee, state


def getBuyOrderInventory(exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price):

    state = False
    buy_amount = 0

    sql=("SELECT amount, maker_fee FROM buy_orders WHERE exchange_label = %s AND exchange_id = %s AND exchange_asteroid_id = %s AND exchange_lot_id = %s AND product_id = %s AND price = %s" % (exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price))
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        if result is None:
            buy_amount = 0
            maker_fee = 0
            crew_id = None
        else:
            buy_amount=result[0]
            maker_fee=result[1]
            state = True

    cur.close()
    con.close()

    return buy_amount, maker_fee, state


def getBuyOrderInventoryWallet(caller_address, exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price):

    state = False
    buy_amount = 0

    sql=("SELECT amount, maker_fee FROM wallet_buy_orders WHERE exchange_label = %s AND exchange_id = %s AND exchange_asteroid_id = %s AND exchange_lot_id = %s AND product_id = %s AND price = %s AND caller_address = '%s'" % (exchange_label, exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, price, caller_address))
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        if result is None:
            buy_amount = 0
            maker_fee = 0
            crew_id = None
        else:
            buy_amount=result[0]
            maker_fee=result[1]
            state = True

    cur.close()
    con.close()

    return buy_amount, maker_fee, state


def getLotForDeposit(deposit_id):

    sql=("SELECT lot_id, asteroid_id FROM core_samples WHERE deposit_id = %s" % deposit_id)
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        if result is None:
            lot_id = None
            asteroid_id = None
        else:
            lot_id=result[0]
            asteroid_id=result[1]

    cur.close()
    con.close()

    return lot_id, asteroid_id


def getDeliveryDestination(delivery_id):

    destination_label = None
    destination_id = None
    destination_slot = None

    sql=("SELECT dest_label, dest_id, dest_slot FROM deliveries_pending where delivery_id = %s LIMIT 1" % delivery_id)
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()

    if rows == None:
        destination_label = None
        destination_id = None
        destination_slot = None

    else:
        for row in rows:
            destination_label = row[0]
            destination_id = row[1]
            destination_slot = row[2]

    return destination_label, destination_id, destination_slot


def getPendingDeliveries(delivery_id):

    deliveries=[]
    sql=("SELECT dest_label, dest_id, dest_slot, product_id, product_amount FROM deliveries_pending where delivery_id = %s" % delivery_id)
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()

    if rows == None:
        return None

    for row in rows:
        deliveries.append({"dest_label": row[0], "dest_id": row[1], "dest_slot": row[2], "resource_id": row[3], "resource_amount": row[4]})

    cur.close()
    con.close()

    return deliveries


def getShipType(ship_id):

    ship_type = None
    sql=("SELECT ship_type FROM ships WHERE ship_id = %s" % ship_id)
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
        else:
            ship_type=result[0]

    cur.close()
    con.close()

    return ship_type


def getCargo(ship_id):

    cargo_amount = 0
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    sql2=("SELECT resource_id, inventory_amount FROM inventories WHERE inventory_label = 6 AND inventory_amount > 0 AND inventory_id = %s AND inventory_slot = 2" % ship_id)
    print(sql2)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql2)
        rows = cur.fetchall()

    for row in rows:
        resource_id=row[0]
        resource_amount=row[1]
        mass_per_unit=component.getMass(resource_id)
        resource_mass=(resource_amount * mass_per_unit)
        cargo_amount+=resource_amount

    cur.close()
    con.close()

    return cargo_amount


def getRawCargo(ship_id, spectral_type):

    cargo_amount = 0
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    sql2=("SELECT resource_id, inventory_amount FROM inventories WHERE inventory_label = 6 AND inventory_amount > 0 AND inventory_id = %s AND inventory_slot = 2" % ship_id)
    print(sql2)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql2)
        rows = cur.fetchall()

    for row in rows:
        resource_id=row[0]
        resource_amount=row[1]
        if resource_id <= 22:
            print("checking resource %s for spectral type %s" % (resource_id, spectral_type))
            mass_per_unit = component.getRawMaterial(resource_id, spectral_type)
            if mass_per_unit is not None:
                resource_mass=(resource_amount * mass_per_unit)
                cargo_amount+=resource_amount

    cur.close()
    con.close()

    return cargo_amount

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


def checkShipDock(ship_id):

    count = 0
    sql=("SELECT COUNT(*) FROM ships_docked WHERE ship_id = %s" % ship_id)
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


def checkShipExists(ship_id):

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


def checkShipExistsTxn(txn_id):

    ship_exists = 0
    ship_id = None
    sql=("SELECT ship_id FROM ships WHERE txn_id = '%s'" % txn_id)
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()

    print(rows)
    if rows is not None:
        for row in rows:
            ship_id = row[0]

    cur.close()
    con.close()

    if ship_id is not None:
        ship_exists = 1

    return ship_exists, ship_id


def getL1MetadataCrewmate(crewmate_id):

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


def updateCrewmate(tx_hash, block_number, crewmate_id):

    crewmate_exists = checkCrewmate(crewmate_id)
    if crewmate_exists == 0:

        l1_metadata = getL1MetadataCrewmate(crewmate_id)

        if len(l1_metadata) > 0:
            name = l1_metadata[0]
            collection = l1_metadata[1]
            crewmate_class = l1_metadata[2]
            title = l1_metadata[3]
            sql=("INSERT IGNORE INTO crewmates (txn_id, block_number, crewmate_id, name, collection, class, title) VALUES ('%s', %s, %s, '%s', %s, %s, %s)" % (tx_hash, block_number, crewmate_id, name, collection, crewmate_class, title))

        else:
            sql=("INSERT IGNORE INTO crewmates (txn_id, block_number, crewmate_id) VALUES ('%s', %s, %s)" % (tx_hash, block_number, crewmate_id))

        print(sql)
        updateSql(sql)


def queueGrab(tx_hash, block_number, asset_type, asset_id):

    insert_sql = ("INSERT IGNORE INTO art_grabs (txn_id, block_number, asset_type, asset_id, status) VALUES ('%s', %s, %s, %s, 1)" % (tx_hash, block_number, asset_type, asset_id))
    print(insert_sql)
    updateSql(insert_sql)


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


def checkForSale(ship_id):

    count = 0
    sql=("SELECT COUNT(*) FROM ships_for_sale WHERE ship_id = %s" % ship_id)
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


def checkShipSold(ship_id):

    count = 0
    sql=("SELECT COUNT(*) FROM ships_sold WHERE ship_id = %s" % ship_id)
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


def getOriginAsteroidId(caller_crew_id):

    origin_asteroid_id = None
    sql=("SELECT origin_asteroid_id FROM crews WHERE crew_id = %s" % caller_crew_id)
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        if len(result) == 0:
            origin_asteroid_id = None
        else:
            origin_asteroid_id=result[0]

    cur.close()
    con.close()

    return origin_asteroid_id


def updateCrew(tx_hash, block_number, crew_id, timestamp):

    crew_exists = checkCrew(crew_id)
    if crew_exists == 0:
        sql=("INSERT IGNORE INTO crews (txn_id, block_number, crew_id, timestamp) VALUES ('%s', %s, %s, '%s')" % (tx_hash, block_number, crew_id, timestamp))
        print(sql)
        updateSql(sql)


def getToBurn(asteroid_id, lot_id):

    materials = []
    sql=("SELECT product_id, product_name, product_amount FROM deliveries WHERE dest_asteroid_id = %s AND dest_lot_id = %s AND burned_inventory = 0" % (asteroid_id, lot_id))
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()

    if rows == None:
        return None

    for row in rows:
        product_id = row[0]
        product_name = row[1]
        product_amount = row[2]

        materials.append({"product_id": product_id, "product_name": product_name, "product_amount": product_amount})

    cur.close()
    con.close()

    return materials


def crewAction(tx_hash, block_number, caller_address, crew_id, action, asteroid_id, lot_id, ship_id, timestamp):

    pass

    if asteroid_id is None:
        asteroid_id = 'NULL'
    
    if lot_id is None:
        lot_id = 'NULL'

    if ship_id is None:
        ship_id = 'NULL'

    insert_sql=("INSERT IGNORE INTO crew_actions (txn_id, block_number, caller_address, crew_id, action, asteroid_id, lot_id, ship_id, timestamp) VALUES ('%s', %s, '%s', %s, '%s', %s, %s, %s, '%s')" % (tx_hash, block_number, caller_address, crew_id, action, asteroid_id, lot_id, ship_id, timestamp))
    print(insert_sql)
    updateSql(insert_sql)

    crewmates = getCrewComposition(crew_id)
    for crewmate_id in crewmates:
        insert_sql2=("INSERT IGNORE INTO crewmate_actions (txn_id, block_number, caller_address, crew_id, crewmate_id, action, asteroid_id, lot_id, ship_id, timestamp) VALUES ('%s', %s, '%s', %s, %s, '%s', %s, %s, %s, '%s')" % (tx_hash, block_number, caller_address, crew_id, crewmate_id, action, asteroid_id, lot_id, ship_id, timestamp))
        print(insert_sql2)
        updateSql(insert_sql2)


def getCrewComposition(crew_id):

    crewmates = []
    sql = ("SELECT crewmate_id FROM crewmates WHERE crew_id = %s" % (crew_id))
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return crewmates

    for row in rows:
        crewmate_id=row[0]
        crewmates.append(crewmate_id)

    cur.close()
    con.close()

    return crewmates

