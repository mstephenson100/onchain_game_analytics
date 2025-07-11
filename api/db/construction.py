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


def parseConstructionType(building_type):

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


def getConstructionState(con, building_type, parameter1, parameter2, state, start_block, end_block):

    construction = []
    building_type = parseConstructionType(building_type)

    if state == "planned":
        table_name = "dispatcher_construction_planned"
    elif state == "started":
        table_name = "dispatcher_construction_started"
    elif state == "finished":
        table_name = "dispatcher_construction_finished"
    elif state == "deconstructed":
        table_name = "dispatcher_construction_deconstructed"
    elif state == "abandoned":
        table = "dispatcher_construction_abandoned"
    else:
        return construction

    if state == "planned":
        pre_sql = ("SELECT txn_id, block_number, caller_address, caller_crew_id, building_label, building_id, asteroid_id, lot_id, building_type, grace_period_end FROM %s" % table_name)
        if parameter1 == "wallet":
            where_sql = (" WHERE caller_address = '%s' AND building_id = building_id AND building_type = %s AND block_number > %s" % (parameter2, building_type, start_block))
        elif parameter1 == "crew":
            where_sql = (" WHERE caller_crew_id = '%s' AND building_id = building_id AND building_type = %s AND block_number > %s" % (parameter2, building_type, start_block))
    else:
        pre_sql = ("SELECT b.txn_id, b.block_number, b.caller_address, b.caller_crew_id, b.building_label, b.building_id, c.asteroid_id, c.lot_id, c.building_type, c.grace_period_end FROM %s b, dispatcher_construction_planned c" % table_name)
        if parameter1 == "wallet":
            where_sql = (" WHERE b.caller_address = '%s' AND b.building_id = c.building_id AND c.building_type = %s AND b.block_number > %s" % (parameter2, building_type, start_block))
        elif parameter1 == "crew":
            where_sql = (" WHERE b.caller_crew_id = '%s' AND b.building_id = c.building_id AND c.building_type = %s AND b.block_number > %s" % (parameter2, building_type, start_block))

    if end_block > 0:
        finish_sql=(" AND block_number <= %s ORDER BY block_number" % end_block)
    else:
        finish_sql=" ORDER BY block_number"

    sql = pre_sql + where_sql + finish_sql
    print(sql)

    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return construction

    for row in rows:
        txn_id=row[0]
        block_number=row[1]
        caller_address=row[2]
        crew_id=row[3]
        building_label=row[4]
        building_id=row[5]
        asteroid_id=row[6]
        lot_id=row[7]
        building_type=row[8]
        grace_period_end=row[9]
        construction.append({"txn_id": txn_id, "block_number": block_number, "caller_address": caller_address, "crew_id": crew_id, "building_label": building_label, "building_id": building_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "building_type": building_type, "grace_period_end": grace_period_end})

    return construction



def getConstructionPlanned(con, building_type, parameter1, parameter2):

    construction_planned = []
    building_type = parseConstructionType(building_type)

    if parameter1 == 'wallet':
        sql = ("SELECT txn_id, block_number, asteroid_id, lot_id, caller_crew_id, building_id, building_type, grace_period_end, caller_address FROM dispatcher_construction_planned WHERE building_type = %s AND caller_address = '%s'" % (building_type, parameter2))

    if parameter1 == 'crew':
        sql = ("SELECT txn_id, block_number, asteroid_id, lot_id, caller_crew_id, building_id, building_type, grace_period_end, caller_address FROM dispatcher_construction_planned WHERE building_type = %s AND caller_crew_id = %s" % (building_type, parameter2))

    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return construction_planned

    for row in rows:
        txn_id=row[0]
        block_number=row[1]
        asteroid_id=row[2]
        lot_id=row[3]
        crew_id=row[4]
        building_id=row[5]
        building_type=row[6]
        grace_period_end=row[7]
        caller_address=row[8]
        construction_planned.append({"building_id": building_id, "building_type": building_type, "crew_id": crew_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "grace_period_end": grace_period_end, "txn_id": txn_id, "block_number": block_number, "caller_address": caller_address})

    return construction_planned


def getConstructionStarted(con, building_type, parameter1, parameter2):

    construction_started = []
    building_type = parseConstructionType(building_type)

    if parameter1 == 'wallet':
        sql = ("SELECT b.txn_id, b.block_number, b.caller_address, b.building_id, b.caller_crew_id, b.finish_time, c.asteroid_id, c.lot_id, c.building_type FROM dispatcher_construction_started b, dispatcher_construction_planned c WHERE b.building_id = c.building_id AND c.building_type = %s AND b.caller_address = '%s'" %(building_type, parameter2))

    if parameter1 == 'crew':
        sql = ("SELECT b.txn_id, b.block_number, b.caller_address, b.building_id, b.caller_crew_id, b.finish_time, c.asteroid_id, c.lot_id, c.building_type FROM dispatcher_construction_started b, dispatcher_construction_planned c WHERE b.building_id = c.building_id AND c.building_type = %s AND b.caller_crew_id = '%s'" %(building_type, parameter2))

    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return construction_planned

    for row in rows:
        txn_id=row[0]
        block_number=row[1]
        caller_address=row[2]
        building_id=row[3]
        crew_id=row[4]
        finish_time=row[5]
        asteroid_id=row[6]
        lot_id=row[7]
        building_type=row[8]
        construction_started.append({"building_id": building_id, "building_type": building_type, "building_id": building_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "crew_id": crew_id, "finish_time": finish_time, "txn_id": txn_id, "block_number": block_number, "caller_address": caller_address})

    return construction_started


def getConstructionFinished(con, building_type, parameter1, parameter2):

    construction_finished = []
    building_type = parseConstructionType(building_type)

    if parameter1 == 'wallet':
        sql = ("SELECT b.txn_id, b.block_number, b.caller_address, b.building_id, b.caller_crew_id, c.asteroid_id, c.lot_id, c.building_type FROM dispatcher_construction_finished b, dispatcher_construction_planned c WHERE b.building_id = c.building_id AND c.building_type = %s AND b.caller_address = '%s'" %(building_type, parameter2))

    if parameter1 == 'crew':
        sql = ("SELECT b.txn_id, b.block_number, b.caller_address, b.building_id, b.caller_crew_id, c.asteroid_id, c.lot_id, c.building_type FROM dispatcher_construction_finished b, dispatcher_construction_planned c WHERE b.building_id = c.building_id AND c.building_type = %s AND b.caller_crew_id = %s" %(building_type, parameter2))

    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return construction_finished

    for row in rows:
        txn_id=row[0]
        block_number=row[1]
        caller_address=row[2]
        building_id=row[3]
        crew_id=row[4]
        asteroid_id=row[5]
        lot_id=row[6]
        building_type=row[7]
        construction_finished.append({"building_id": building_id, "building_type": building_type, "crew_id": crew_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "txn_id": txn_id, "block_number": block_number, "caller_address": caller_address})

    return construction_finished


def getConstructionAbandoned(con, building_type, parameter1, parameter2):

    construction_unplanned = []
    building_type = parseConstructionType(building_type)

    if parameter1 == 'wallet':
        sql = ("SELECT b.txn_id, b.block_number, b.caller_address, b.building_id, b.caller_crew_id, b.finish_time, c.asteroid_id, c.lot_id, c.building_type FROM dispatcher_construction_abandoned b, dispatcher_construction_planned c WHERE b.building_id = c.building_id AND c.building_type = %s AND b.caller_address = '%s'" % (building_type, parameter2))

    if parameter1 == 'crew':
        sql = ("SELECT b.txn_id, b.block_number, b.caller_address, b.building_id, b.caller_crew_id, b.finish_time, c.asteroid_id, c.lot_id, c.building_type FROM dispatcher_construction_abandoned b, dispatcher_construction_planned c WHERE b.building_id = c.building_id AND c.building_type = %s AND b.caller_crew_id = %s" % (building_type, parameter2))

    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return construction_unplanned

    for row in rows:
        txn_id=row[0]
        block_number=row[1]
        caller_address=row[2]
        building_id=row[3]
        crew_id=row[4]
        finish_time=row[5]
        asteroid_id=row[6]
        lot_id=row[7]
        building_type=row[8]

        construction_unplanned.append({"building_id": building_id, "building_type": building_type, "finish_time": finish_time, "crew_id": crew_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "txn_id": txn_id, "block_number": block_number, "caller_address": caller_address})

    return construction_unplanned


def getConstructionDeconstructed(con, building_type, parameter1, parameter2):

    construction_deconstructed = []
    building_type = parseConstructionType(building_type)

    if parameter1 == 'wallet':
        sql = ("SELECT b.txn_id, b.block_number, b.caller_address, b.building_id, b.caller_crew_id, c.asteroid_id, c.lot_id, c.building_type FROM dispatcher_construction_deconstructed b, dispatcher_construction_planned c WHERE b.building_id = c.building_id AND c.building_type = %s AND b.caller_address = '%s'" % (building_type, parameter2))

    if parameter1 == 'crew':
        sql = ("SELECT b.txn_id, b.block_number, b.caller_address, b.building_id, b.caller_crew_id, c.asteroid_id, c.lot_id, c.building_type FROM dispatcher_construction_deconstructed b, dispatcher_construction_planned c WHERE b.building_id = c.building_id AND c.building_type = %s AND b.caller_crew_id = %s" % (building_type, parameter2))

    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return construction_deconstructed

    for row in rows:
        txn_id=row[0]
        block_number=row[1]
        caller_address=row[2]
        building_id=row[3]
        crew_id=row[4]
        asteroid_id=row[5]
        lot_id=row[6]
        building_type=row[7]
        construction_deconstructed.append({"building_id": building_id, "building_type": building_type, "crew_id": crew_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "txn_id": txn_id, "block_number": block_number, "caller_address": caller_address})

    return construction_deconstructed


def constructionState(building_type, parameter1, parameter2, state, start_block, end_block):

    construction = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    construction = getConstructionState(con, building_type, parameter1, parameter2, state, start_block, end_block)
    con.close()
    return construction


def constructionPlanned(building_type, parameter1, parameter2):

    construction_planned = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    construction_planned = getConstructionPlanned(con, building_type, parameter1, parameter2)
    con.close()
    return construction_planned


def constructionStarted(building_type, parameter1, parameter2):

    construction_started = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    construction_started = getConstructionStarted(con, building_type, parameter1, parameter2)
    con.close()
    return construction_started


def constructionFinished(building_type, parameter1, parameter2):

    construction_finished = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    construction_finished = getConstructionFinished(con, building_type, parameter1, parameter2)
    con.close()
    return construction_finished


def constructionAbandoned(building_type, parameter1, parameter2):

    construction_abandoned = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    construction_abandoned = getConstructionAbandoned(con, building_type, parameter1, parameter2)
    con.close()
    return construction_abandoned


def constructionDeconstructed(building_type, parameter1, parameter2):

    construction_deconstructed = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    construction_deconstructed = getConstructionDeconstructed(con, building_type, parameter1, parameter2)
    con.close()
    return construction_deconstructed

