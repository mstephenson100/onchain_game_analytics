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

    return ship_type


def getExtractionState(con, parameter1, parameter2, state, start_block, end_block):

    extractions = []
    if state == "pending" or state == "finished":
        pre_sql = "SELECT start_txn_id, start_block_number, finish_txn_id, finish_block_number, caller_address, crew_id, deposit_id, resource_id, resource_name, resource_yield, extractor_id, extractor_slot, extractor_type, extractor_asteroid_id, extractor_lot_id, destination_label, destination_id, destination_slot, destination_type, destination_asteroid_id, destination_lot_id, finish_time FROM extractions"
        if state == "pending":
            status = 1
        else:
            status = 2
        if parameter1 == "wallet":
            where_sql = (" WHERE caller_address = '%s' AND status = %s AND start_block_number > %s" % (parameter2, status, start_block))
        elif parameter1 == "crew":
            where_sql = (" WHERE crew_id = %s AND status = %s AND start_block_number > %s" % (parameter2, status, start_block))
        if end_block > 0:
            finish_sql=(" AND finish_block_number <= %s ORDER BY start_block_number" % end_block)
        else:
            finish_sql=" ORDER BY start_block_number"
    else:
        pre_sql = "SELECT txn_id, block_number, NULL, NULL, caller_address, caller_crew_id, deposit_id, resource_id, resource_name, resource_yield, extractor_id, extractor_slot, extractor_type, extractor_asteroid_id, extractor_lot_id, destination_label, destination_id, destination_slot, destination_type, destination_asteroid_id, destination_lot_id, finish_time FROM dispatcher_resource_extraction_started"
        if parameter1 == "wallet":
            where_sql = (" WHERE caller_address = '%s' AND block_number > %s" % (parameter2, start_block))
        elif parameter1 == "crew":
            where_sql = (" WHERE caller_crew_id = %s AND block_number > %s" % (parameter2, start_block))
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
        return extractions

    for row in rows:
        start_txn_id=row[0]
        start_block_number=row[1]
        finish_txn_id=row[2]
        finish_block_number=row[3]
        caller_address=row[4]
        crew_id=row[5]
        deposit_id=row[6]
        resource_id=row[7]
        resource_name=row[8]
        resource_yield=row[9]
        extractor_id=row[10]
        extractor_slot=row[11]
        extractor_type=row[12]
        extractor_asteroid_id=row[13]
        extractor_lot_id=row[14]
        destination_label=row[15]
        destination_id=row[16]
        destination_slot=row[17]
        destination_type=row[18]
        destination_asteroid_id=row[19]
        destination_lot_id=row[20]
        finish_time=row[21]
        extractions.append({"start_txn_id": start_txn_id, "start_block_number": start_block_number, "finish_txn_id": finish_txn_id, "finish_block_number": finish_block_number, "caller_address": caller_address, "crew_id": crew_id, "deposit_id": deposit_id, "resource_id": resource_id, "resource_name": resource_name, "resource_yield": resource_yield, "extractor_id": extractor_id, "extractor_slot": extractor_slot, "extractor_type": extractor_type, "extractor_asteroid_id": extractor_asteroid_id, "extractor_lot_id": extractor_lot_id, "destination_label": destination_label, "destination_id": destination_id, "destination_slot": destination_slot, "destination_type": destination_type, "destination_asteroid_id": destination_asteroid_id, "destination_lot_id": destination_lot_id, "finish_time": finish_time})

    return extractions


def getExtractionOnAsteroid(con, parameter1, parameter2, state, asteroid_id, start_block, end_block):

    extractions = []
    if state == "pending" or state == "finished":
        pre_sql = "SELECT start_txn_id, start_block_number, finish_txn_id, finish_block_number, caller_address, crew_id, deposit_id, resource_id, resource_name, resource_yield, extractor_id, extractor_slot, extractor_type, extractor_asteroid_id, extractor_lot_id, destination_label, destination_id, destination_slot, destination_type, destination_asteroid_id, destination_lot_id, finish_time FROM extractions"
        if state == "pending":
            status = 1
        else:
            status = 2
        if parameter1 == "wallet":
            where_sql = (" WHERE extractor_asteroid_id = %s AND caller_address = '%s' AND status = %s AND start_block_number > %s" % (asteroid_id, parameter2, status, start_block))
        elif parameter1 == "crew":
            where_sql = (" WHERE extractor_asteroid_id = %s AND crew_id = %s AND status = %s AND start_block_number > %s" % (asteroid_id, parameter2, status, start_block))
        if end_block > 0:
            finish_sql=(" AND finish_block_number <= %s ORDER BY start_block_number" % end_block)
        else:
            finish_sql=" ORDER BY start_block_number"
    else:
        pre_sql = "SELECT txn_id, block_number, NULL, NULL, caller_address, caller_crew_id, deposit_id, resource_id, resource_name, resource_yield, extractor_id, extractor_slot, extractor_type, extractor_asteroid_id, extractor_lot_id, destination_label, destination_id, destination_slot, destination_type, destination_asteroid_id, destination_lot_id, finish_time FROM dispatcher_resource_extraction_started"
        if parameter1 == "wallet":
            where_sql = (" WHERE extractor_asteroid_id = %s AND caller_address = '%s' AND block_number > %s" % (asteroid_id, parameter2, start_block))
        elif parameter1 == "crew":
            where_sql = (" WHERE extractor_asteroid_id = %s AND caller_crew_id = %s AND block_number > %s" % (asteroid_id, parameter2, start_block))
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
        return extractions

    for row in rows:
        start_txn_id=row[0]
        start_block_number=row[1]
        finish_txn_id=row[2]
        finish_block_number=row[3]
        caller_address=row[4]
        crew_id=row[5]
        deposit_id=row[6]
        resource_id=row[7]
        resource_name=row[8]
        resource_yield=row[9]
        extractor_id=row[10]
        extractor_slot=row[11]
        extractor_type=row[12]
        extractor_asteroid_id=row[13]
        extractor_lot_id=row[14]
        destination_label=row[15]
        destination_id=row[16]
        destination_slot=row[17]
        destination_type=row[18]
        destination_asteroid_id=row[19]
        destination_lot_id=row[20]
        finish_time=row[21]
        extractions.append({"start_txn_id": start_txn_id, "start_block_number": start_block_number, "finish_txn_id": finish_txn_id, "finish_block_number": finish_block_number, "caller_address": caller_address, "crew_id": crew_id, "deposit_id": deposit_id, "resource_id": resource_id, "resource_name": resource_name, "resource_yield": resource_yield, "extractor_id": extractor_id, "extractor_slot": extractor_slot, "extractor_type": extractor_type, "extractor_asteroid_id": extractor_asteroid_id, "extractor_lot_id": extractor_lot_id, "destination_label": destination_label, "destination_id": destination_id, "destination_slot": destination_slot, "destination_type": destination_type, "destination_asteroid_id": destination_asteroid_id, "destination_lot_id": destination_lot_id, "finish_time": finish_time})

    return extractions


def getExtractionOnLot(con, parameter1, parameter2, state, asteroid_id, lot_id, start_block, end_block):

    extractions = []
    if state == "pending" or state == "finished":
        pre_sql = "SELECT start_txn_id, start_block_number, finish_txn_id, finish_block_number, caller_address, crew_id, deposit_id, resource_id, resource_name, resource_yield, extractor_id, extractor_slot, extractor_type, extractor_asteroid_id, extractor_lot_id, destination_label, destination_id, destination_slot, destination_type, destination_asteroid_id, destination_lot_id, finish_time FROM extractions"
        if state == "pending":
            status = 1
        else:
            status = 2
        if parameter1 == "wallet":
            where_sql = (" WHERE extractor_asteroid_id = %s AND extractor_lot_id = %s AND caller_address = '%s' AND status = %s AND start_block_number > %s" % (asteroid_id, lot_id, parameter2, status, start_block))
        elif parameter1 == "crew":
            where_sql = (" WHERE extractor_asteroid_id = %s AND extractor_lot_id = %s AND crew_id = %s AND status = %s AND start_block_number > %s" % (asteroid_id, lot_id, parameter2, status, start_block))
        if end_block > 0:
            finish_sql=(" AND finish_block_number <= %s ORDER BY start_block_number" % end_block)
        else:
            finish_sql=" ORDER BY start_block_number"
    else:
        pre_sql = "SELECT txn_id, block_number, NULL, NULL, caller_address, caller_crew_id, deposit_id, resource_id, resource_name, resource_yield, extractor_id, extractor_slot, extractor_type, extractor_asteroid_id, extractor_lot_id, destination_label, destination_id, destination_slot, destination_type, destination_asteroid_id, destination_lot_id, finish_time FROM dispatcher_resource_extraction_started"
        if parameter1 == "wallet":
            where_sql = (" WHERE extractor_asteroid_id = %s AND extractor_lot_id = %s AND caller_address = '%s' AND block_number > %s" % (asteroid_id, lot_id, parameter2, start_block))
        elif parameter1 == "crew":
            where_sql = (" WHERE extractor_asteroid_id = %s AND extractor_lot_id = %s AND caller_crew_id = %s AND block_number > %s" % (asteroid_id, lot_id, parameter2, start_block))
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
        return extractions

    for row in rows:
        start_txn_id=row[0]
        start_block_number=row[1]
        finish_txn_id=row[2]
        finish_block_number=row[3]
        caller_address=row[4]
        crew_id=row[5]
        deposit_id=row[6]
        resource_id=row[7]
        resource_name=row[8]
        resource_yield=row[9]
        extractor_id=row[10]
        extractor_slot=row[11]
        extractor_type=row[12]
        extractor_asteroid_id=row[13]
        extractor_lot_id=row[14]
        destination_label=row[15]
        destination_id=row[16]
        destination_slot=row[17]
        destination_type=row[18]
        destination_asteroid_id=row[19]
        destination_lot_id=row[20]
        finish_time=row[21]
        extractions.append({"start_txn_id": start_txn_id, "start_block_number": start_block_number, "finish_txn_id": finish_txn_id, "finish_block_number": finish_block_number, "caller_address": caller_address, "crew_id": crew_id, "deposit_id": deposit_id, "resource_id": resource_id, "resource_name": resource_name, "resource_yield": resource_yield, "extractor_id": extractor_id, "extractor_slot": extractor_slot, "extractor_type": extractor_type, "extractor_asteroid_id": extractor_asteroid_id, "extractor_lot_id": extractor_lot_id, "destination_label": destination_label, "destination_id": destination_id, "destination_slot": destination_slot, "destination_type": destination_type, "destination_asteroid_id": destination_asteroid_id, "destination_lot_id": destination_lot_id, "finish_time": finish_time})

    return extractions


def getExtractedByResource(con, resource_id, parameter1, parameter2):

    extracted_resources = []
    if parameter1 == 'wallet':
        sql = ("SELECT start_txn_id, start_block_number, finish_txn_id, finish_block_number, caller_address, resource_id, resource_name, resource_yield, crew_id, deposit_id, extractor_id, destination_label, destination_id, finish_time FROM extractions WHERE resource_id = %s AND caller_address = '%s' AND status = 2" % (resource_id, parameter2))

    if parameter1 == 'crew':
        sql = ("SELECT start_txn_id, start_block_number, finish_txn_id, finish_block_number, caller_address, resource_id, resource_name, resource_yield, crew_id, deposit_id, extractor_id, destination_label, destination_id, finish_time FROM extractions WHERE resource_id = %s AND crew_id = %s AND status = 2" % (resource_id, parameter2))

    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return extracted_resources

    for row in rows:
        start_txn_id=row[0]
        start_block_number=row[1]
        finish_txn_id=row[2]
        finish_block_number=row[3]
        caller_address=row[4]
        resource_id=row[5]
        resource_name=row[6]
        resource_yield=row[7]
        crew_id=row[8]
        deposit_id=row[9]
        extractor_id=row[10]
        destination_label=row[11]
        destination_id=row[12]
        finish_time=row[13]

        extracted_resources.append({"start_txn_id": start_txn_id, "start_block_number": start_block_number, "finish_txn_id": finish_txn_id, "finish_block_number": finish_block_number, "caller_address": caller_address, "resource_id": resource_id, "resource_name": resource_name, "resource_yield": resource_yield, "crew_id": crew_id, "deposit_id": deposit_id, "extractor_id": extractor_id, "destination_label": destination_label, "destination_id": destination_id, "finish_time": finish_time})

    return extracted_resources


def getExtractedResourcesAll(con, parameter1, parameter2):

    extracted_resources = []
    if parameter1 == 'wallet':
        sql = ("SELECT start_txn_id, start_block_number, finish_txn_id, finish_block_number, caller_address, resource_id, resource_name, resource_yield, crew_id, deposit_id, extractor_id, destination_label, destination_id, finish_time FROM extractions WHERE caller_address = '%s' AND status = 2" % parameter2)

    if parameter1 == 'crew':
        sql = ("SELECT start_txn_id, start_block_number, finish_txn_id, finish_block_number, caller_address, resource_id, resource_name, resource_yield, crew_id, deposit_id, extractor_id, destination_label, destination_id, finish_time FROM extractions WHERE crew_id = %s AND status = 2" % parameter2)

    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return extracted_resources

    for row in rows:
        start_txn_id=row[0]
        start_block_number=row[1]
        finish_txn_id=row[2]
        finish_block_number=row[3]
        caller_address=row[4]
        resource_id=row[5]
        resource_name=row[6]
        resource_yield=row[7]
        crew_id=row[8]
        deposit_id=row[9]
        extractor_id=row[10]
        destination_label=row[11]
        destination_id=row[12]
        finish_time=row[13]

        extracted_resources.append({"start_txn_id": start_txn_id, "start_block_number": start_block_number, "finish_txn_id": finish_txn_id, "finish_block_number": finish_block_number, "caller_address": caller_address, "resource_id": resource_id, "resource_name": resource_name, "resource_yield": resource_yield, "crew_id": crew_id, "deposit_id": deposit_id, "extractor_id": extractor_id, "destination_label": destination_label, "destination_id": destination_id, "finish_time": finish_time})

    return extracted_resources


def extractedResourcesAll(parameter1, parameter2):

    extracted_resources = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    extracted_resources = getExtractedResourcesAll(con, parameter1, parameter2)
    con.close()
    return extracted_resources


def extractedByResource(resource_id, parameter1, parameter2):

    extracted_resources = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    extracted_resources = getExtractedByResource(con, resource_id, parameter1, parameter2)
    con.close()
    return extracted_resources


def extractionState(parameter1, parameter2, state, start_block, end_block):

    extractions = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    extractions = getExtractionState(con, parameter1, parameter2, state, start_block, end_block)
    con.close()
    return extractions


def extractionOnAsteroid(parameter1, parameter2, state, asteroid_id, start_block, end_block):

    extractions = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    extractions = getExtractionOnAsteroid(con, parameter1, parameter2, state, asteroid_id, start_block, end_block)
    con.close()
    return extractions


def extractionOnLot(parameter1, parameter2, state, asteroid_id, lot_id, start_block, end_block):

    extraction = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    extractions = getExtractionOnLot(con, parameter1, parameter2, state, asteroid_id, lot_id, start_block, end_block)
    con.close()
    return extractions

