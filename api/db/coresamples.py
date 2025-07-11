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

    if building_type == 1:
        building_type = 'warehouse'

    if building_type == 2:
        building_type = 'extractor'

    if building_type == 3:
        building_type = 'refinery'

    if building_type == 4:
        building_type = 'bioreactor'

    if building_type == 5:
        building_type = 'factory'

    if building_type == 6:
        building_type = 'shipyard'

    if building_type == 7:
        building_type = 'spaceport'

    if building_type == 8:
        building_type = 'marketplace'

    if building_type == 9:
        building_type = 'habitat'

    return building_type


def parseShipType(ship_type):

    if ship_type == 1:
        ship_type = 'ESCAPE_MODULE'

    if ship_type == 2:
        ship_type = 'LIGHT_TRANSPORT'

    if ship_type == 3:
        ship_type = 'HEAVY_TRANSPORT'

    if ship_type == 4:
        ship_type = 'SHUTTLE'


def getCoresamplesOwnedAtLot(con, asteroid_id, lot_id, parameter1, parameter2):

    coresamples = []
    if parameter1 == 'wallet':
        sql = ("SELECT txn_id, block_number, caller_address, crew_id, deposit_id, resource_id, resource_name, initial_yield FROM core_samples WHERE caller_address = '%s' AND asteroid_id = %s AND lot_id = %s AND status = 2" % (parameter2, asteroid_id, lot_id))

    if parameter1 == 'crew':
        sql = ("SELECT txn_id, block_number, caller_address, crew_id, deposit_id, resource_id, resource_name, initial_yield FROM core_samples WHERE crew_id = %s AND asteroid_id = %s AND lot_id = %s AND status = 2" % (parameter2, asteroid_id, lot_id))

    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return coresamples

    for row in rows:
        txn_id=row[0]
        block_number=row[1]
        caller_address=row[2]
        crew_id=row[3]
        deposit_id=row[4]
        resource_id=row[5]
        resource_name=row[6]
        initial_yield=row[7]
        coresamples.append({"deposit_id": deposit_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "crew_id": crew_id, "resource_id": resource_id, "resource_name": resource_name, "initial_yield": initial_yield, "txn_id": txn_id, "block_number": block_number, "caller_address": caller_address})

    return coresamples


def getCoresamplesAtLot(con, asteroid_id, lot_id):

    coresamples = []
    sql = ("SELECT txn_id, block_number, caller_address, crew_id, deposit_id, resource_id, resource_name, initial_yield, lot_id, asteroid_id FROM core_samples WHERE asteroid_id = %s AND lot_id = %s AND status = 2" % (asteroid_id, lot_id))
    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return coresamples

    for row in rows:
        txn_id=row[0]
        block_number=row[1]
        caller_address=row[2]
        crew_id=row[3]
        deposit_id=row[4]
        resource_id=row[5]
        resource_name=row[6]
        initial_yield=row[7]
        lot_id=row[8]
        asteroid_id=row[9]
        coresamples.append({"deposit_id": deposit_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "crew_id": crew_id, "resource_id": resource_id, "resource_name": resource_name, "initial_yield": initial_yield, "txn_id": txn_id, "block_number": block_number, "caller_address": caller_address})

    return coresamples


def getCoresamplesOnAsteroid(con, asteroid_id):

    coresamples = []
    sql = ("SELECT txn_id, block_number, caller_address, crew_id, deposit_id, resource_id, resource_name, initial_yield, lot_id, asteroid_id FROM core_samples WHERE asteroid_id = %s AND status > 1" % asteroid_id)
    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return coresamples

    for row in rows:
        txn_id=row[0]
        block_number=row[1]
        caller_address=row[2]
        crew_id=row[3]
        deposit_id=row[4]
        resource_id=row[5]
        resource_name=row[6]
        initial_yield=row[7]
        lot_id=row[8]
        asteroid_id=row[9]
        coresamples.append({"deposit_id": deposit_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "crew_id": crew_id, "resource_id": resource_id, "resource_name": resource_name, "initial_yield": initial_yield, "txn_id": txn_id, "block_number": block_number, "caller_address": caller_address})

    return coresamples


def getCoresamplesOwnedOnAsteroid(con, asteroid_id, parameter1, parameter2):

    coresamples = []
    if parameter1 == 'wallet':
        sql = ("SELECT txn_id, block_number, caller_address, crew_id, deposit_id, lot_id, asteroid_id, resource_id, resource_name, initial_yield, origin_id, origin_slot FROM core_samples WHERE caller_address = '%s' AND asteroid_id = %s AND status = 2" % (parameter2, asteroid_id))

    if parameter1 == 'crew':
        sql = ("SELECT txn_id, block_number, caller_address, crew_id, deposit_id, lot_id, asteroid_id, resource_id, resource_name, initial_yield, origin_id, origin_slot FROM core_samples WHERE crew_id = %s AND asteroid_id = %s AND status = 2" % (parameter2, asteroid_id))

    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return coresamples

    for row in rows:
        txn_id=row[0]
        block_number=row[1]
        caller_address=row[2]
        crew_id=row[3]
        deposit_id=row[4]
        lot_id=row[5]
        asteroid_id=row[6]
        resource_id=row[7]
        resource_name=row[8]
        initial_yield=row[9]
        origin_id=row[10]
        origin_slot=row[11]
        coresamples.append({"deposit_id": deposit_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "crew_id": crew_id, "resource_id": resource_id, "resource_name": resource_name, "initial_yield": initial_yield, "origin_id": origin_id, "origin_slot": origin_slot, "txn_id": txn_id, "block_number": block_number, "caller_address": caller_address})

    return coresamples


def getOwnedCoresamples(con, parameter1, parameter2):

    coresamples = []
    if parameter1 == 'wallet':
        sql = ("SELECT txn_id, block_number, caller_address, crew_id, deposit_id, lot_id, asteroid_id, resource_id, resource_name, initial_yield, origin_id, origin_slot, status FROM core_samples WHERE caller_address = '%s' AND status = 2" % parameter2)

    if parameter1 == 'crew':
        sql = ("SELECT txn_id, block_number, caller_address, crew_id, deposit_id, lot_id, asteroid_id, resource_id, resource_name, initial_yield, origin_id, origin_slot, status FROM core_samples WHERE crew_id = %s AND status = 2" % parameter2)

    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return coresamples

    for row in rows:
        txn_id=row[0]
        block_number=row[1]
        caller_address=row[2]
        crew_id=row[3]
        deposit_id=row[4]
        lot_id=row[5]
        asteroid_id=row[6]
        resource_id=row[7]
        resource_name=row[8]
        initial_yield=row[9]
        origin_id=row[10]
        origin_slot=row[11]
        coresamples.append({"deposit_id": deposit_id, "crew_id": crew_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "resource_id": resource_id, "resource_name": resource_name, "initial_yield": initial_yield, "origin_id": origin_id, "origin_slot": origin_slot, "txn_id": txn_id, "block_number": block_number, "caller_address": caller_address})

    return coresamples


def getCoresamplesState(con, state, parameter1, parameter2, start_block, end_block):

    coresamples=[]
    if state == "pending":
        status = 1
    if state == "finished":
        status = 2

    if state == "pending" or state == "finished":
        pre_sql="SELECT start_txn_id, start_block_number, finish_txn_id, finish_block_number, caller_address, crew_id, deposit_id, asteroid_id, lot_id, resource_id, resource_name, improving, finish_time, initial_yield, origin_id, origin_slot FROM core_samples "
        if parameter1 == "wallet":
            from_sql = ("WHERE status = %s AND caller_address = '%s' AND start_block_number > %s" % (status, parameter2, start_block))
        elif parameter1 == "crew":
            from_sql = ("WHERE status = %s AND crew_id = %s AND start_block_number > %s" % (status, parameter2, start_block))
        if end_block > 0:
            finish_sql=(" AND finish_block_number <= %s ORDER BY start_block_number" % end_block)
        else:
            finish_sql=" ORDER BY start_block_number"

    if state == "started":
        pre_sql="SELECT txn_id, block_number, NULL, NULL, caller_address, caller_crew_id, deposit_id, asteroid_id, lot_id, resource_id, resource_name, improving, finish_time, NULL, origin_id, origin_slot FROM dispatcher_sampling_deposit_started_v1 "
        if parameter1 == "wallet":
            from_sql = ("WHERE caller_address = '%s' AND block_number > %s" % (parameter2, start_block))
        elif parameter1 == "crew":
            from_sql = ("WHERE caller_crew_id = %s AND block_number > %s" % (parameter2, start_block))
        if end_block > 0:
            finish_sql=(" AND block_number <= %s ORDER BY block_number" % end_block)
        else:
            finish_sql=" ORDER BY block_number"

    sql = pre_sql + from_sql + finish_sql
    print(sql)

    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return coresamples

    for row in rows:
        start_txn_id=row[0]
        start_block_number=row[1]
        finish_txn_id=row[2]
        finish_block_number=row[3]
        caller_address=row[4]
        crew_id=row[5]
        deposit_id=row[6]
        asteroid_id=row[7]
        lot_id=row[8]
        resource_id=row[9]
        resource_name=row[10]
        improving=row[11]
        finish_time=row[12]
        initial_yield=row[13]
        origin_id=row[14]
        origin_slot=row[15]
        coresamples.append({"start_txn_id": start_txn_id, "start_block_number": start_block_number, "finish_txn_id": finish_txn_id, "finish_block_number": finish_block_number, "caller_address": caller_address, "crew_id": crew_id, "deposit_id": deposit_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "resource_id": resource_id, "resource_name": resource_name, "improving": improving, "finish_time": finish_time, "initial_yield": initial_yield, "origin_id": origin_id, "origin_slot": origin_slot})

    return coresamples


def getDepletedCoresamples(con, parameter1, parameter2):

    coresamples=[]
    if parameter1 == 'wallet':
        sql = ("SELECT txn_id, block_number, crew_id, deposit_id, asteroid_id, lot_id, resource_id, resource_name, current_yield, destination_label, destination_id, destination_slot, finish_time, caller_address FROM core_samples_depleted WHERE caller_address = '%s'" % parameter2)

    if parameter1 == 'crew':
        sql = ("SELECT txn_id, block_number, crew_id, deposit_id, asteroid_id, lot_id, resource_id, resource_name, current_yield, destination_label, destination_id, destination_slot, finish_time, caller_address FROM core_samples_depleted WHERE crew_id = %s" % parameter2)

    print(sql)

    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return coresamples

    for row in rows:
        txn_id=row[0]
        block_number=row[1]
        crew_id=row[2]
        deposit_id=row[3]
        asteroid_id=row[4]
        lot_id=row[5]
        resource_id=row[6]
        resource_name=row[7]
        current_yield=row[8]
        destination_label=row[9]
        destination_id=row[10]
        destination_slot=row[11]
        finish_time=row[12]
        caller_address=row[13]

        coresamples.append({"deposit_id": deposit_id, "crew_id": crew_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "resource_id": resource_id, "resource_name": resource_name, "current_yield": current_yield, "destination_label": destination_label, "destination_id": destination_id, "destination_slot": destination_slot, "txn_id": txn_id, "block_number": block_number, "caller_address": caller_address})

    return coresamples


def getCoresampleDetails(con, deposit_id):

    coresample=[]
    coresample_state=()

    sql = ("SELECT txn_id, block_number, caller_address, crew_id, deposit_id, asteroid_id, lot_id, resource_id, resource_name, finish_time, improving, initial_yield, origin_id, origin_slot, status FROM core_samples WHERE deposit_id = %s" % deposit_id)
    print(sql)

    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return coresample

    for row in rows:
        txn_id=row[0]
        block_number=row[1]
        caller_address=row[2]
        crew_id=row[3]
        deposit_id=row[4]
        asteroid_id=row[5]
        lot_id=row[6]
        resource_id=row[7]
        resource_name=row[8]
        finish_time=row[9]
        improving=row[10]
        current_yield=row[11]
        origin_id=row[12]
        origin_slot=row[13]
        status=row[14]

    if status == 1:
        status_desc = 'drilling_started'
    if status == 2:
        status_desc = 'drilling_finished'

    coresample_state = {"deposit_id": deposit_id, "crew_id": crew_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "resource_id": resource_id, "resource_name": resource_name, "current_yield": current_yield, "finish_time": finish_time, "improving": improving, "origin_id": origin_id, "origin_slot": origin_slot, "status": status, "status_desc": status_desc, "txn_id": txn_id, "block_number": block_number, "caller_address": caller_address}

    extraction_started=[]
    sql2 = ("SELECT b.txn_id, b.block_number, b.caller_address, b.caller_crew_id, b.deposit_id, b.resource_id, b.resource_name, b.resource_yield, b.extractor_id, b.extractor_slot, b.destination_label, b.destination_id, b.destination_slot, b.finish_time, c.lot_id, c.asteroid_id FROM dispatcher_resource_extraction_started b, buildings c WHERE b.extractor_id = c.building_id AND b.deposit_id = %s" % deposit_id)
    print(sql2)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql2)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        coresample={"state": coresample_state, "extractions": {}}
        return coresample

    for row in rows:
        s_txn_id=row[0]
        s_block_number=row[1]
        s_caller_address=row[2]
        s_crew_id=row[3]
        s_deposit_id=row[4]
        s_resource_id=row[5]
        s_resource_name=row[6]
        s_resource_yield=row[7]
        s_extractor_id=row[8]
        s_extractor_slot=row[9]
        s_destination_label=row[10]
        s_destination_id=row[11]
        s_destination_slot=row[12]
        s_finish_time=row[13]
        s_lot_id=row[14]
        s_asteroid_id=row[15]

        if s_destination_label == 5:
            s_dest_sql = ("SELECT lot_id, asteroid_id, building_type FROM buildings WHERE building_id = %s" % s_destination_id)
        elif s_destination_label == 6:
            s_dest_sql = ("SELECT lot_id, asteroid_id, ship_type FROM ships WHERE ship_id = %s" % s_destination_id)

        print(s_dest_sql)
        with con:
            cur = con.cursor()
            cur.execute("%s" % s_dest_sql)
            s_dest_rows = cur.fetchall()
            cur.close()

        if s_dest_rows == None:
            s_dest_lot_id = None
            s_dest_asteroid_id = None
            s_dest_type = None

        for s_dest_row in s_dest_rows:
            s_dest_lot_id=s_dest_row[0]
            s_dest_asteroid_id=s_dest_row[1]
            s_dest_type=s_dest_row[2]

        if s_destination_label == 5:
            s_dest_type_description = parseBuildingType(s_dest_type)

        if s_destination_label == 6:
            s_dest_type_description = parseShipType(s_dest_type)

        extraction_started.append({"asteroid_id": s_asteroid_id, "lot_id": s_lot_id, "crew_id": s_crew_id, "deposit_id": s_deposit_id, "resource_id": s_resource_id, "resource_name": s_resource_name, "resource_yield": s_resource_yield, "extractor_id": s_extractor_id, "extractor_slot": s_extractor_slot, "destination_id": s_destination_id, "destination_label": s_destination_label, "destination_slot": s_destination_slot, "destination_type_id": s_dest_type, "destination_type": s_dest_type_description, "destination_asteroid_id": s_dest_asteroid_id, "destination_lot_id": s_dest_lot_id, "finish_time": s_finish_time, "txn_id": s_txn_id, "block_number": s_block_number, "caller_address": s_caller_address})

    coresample={"state": coresample_state, "extractions": extraction_started}

    return coresample


def coresamplesOwnedAtLot(asteroid_id, lot_id, parameter1, parameter2):

    coresamples=[]
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    coresamples = getCoresamplesOwnedAtLot(con, asteroid_id, lot_id, parameter1, parameter2)
    con.close()
    return coresamples


def coresamplesOwnedOnAsteroid(asteroid_id, parameter1, parameter2):

    coresamples=[]
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    coresamples = getCoresamplesOwnedOnAsteroid(con, asteroid_id, parameter1, parameter2)
    con.close()
    return coresamples


def coresamplesAtLot(asteroid_id, lot_id):

    coresamples=[]
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    coresamples = getCoresamplesAtLot(con, asteroid_id, lot_id)
    con.close()
    return coresamples


def coresamplesOnAsteroid(asteroid_id):

    coresamples=[]
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    coresamples = getCoresamplesOnAsteroid(con, asteroid_id)
    con.close()
    return coresamples


def coresamplesOwned(parameter1, parameter2):

    coresamples=[]
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    coresamples = getOwnedCoresamples(con, parameter1, parameter2)
    con.close()
    return coresamples


def coresamplesState(state, parameter1, parameter2, start_block, end_block):

    coresamples=[]
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    coresamples = getCoresamplesState(con, state, parameter1, parameter2, start_block, end_block)
    con.close()
    return coresamples


def depletedCoresamples(parameter1, parameter2):

    coresamples=[]
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    coresamples = getDepletedCoresamples(con, parameter1, parameter2)
    con.close()
    return coresamples


def coresampleDetails(deposit_id):

    coresample=[]
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    coresample = getCoresampleDetails(con, deposit_id)
    con.close()
    return coresample

