#!/home/bios/.pyenv/shims/python3

import os
import sys
import requests
import asyncio
import time
import configparser
import pymysql
import warnings
import traceback

def updateSql(sql):

    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)

    cur.close()
    con.close()


def loadNewAsteroids(db_user, db_password, db):

    print("IM IN loadNewAsteroids")
    new_asteroids = getNewAsteroids(db_user, db_password, db)
    for row in new_asteroids:
        asteroid_id = row['asteroid_id']
        crew_id = row['crew_id']
        caller_address = row['caller_address']
        mission_1_insert_sql = ("INSERT INTO colonization_missions_tracking_1 (asteroid_id, req_1_wallet, req_1_crew_id, req_1) VALUES (%s, '%s', %s, %s)" % (asteroid_id, caller_address, crew_id, 1))
        print(mission_1_insert_sql)
        updateSql(mission_1_insert_sql)
        mission_2_insert_sql = ("INSERT INTO colonization_missions_tracking_2 (asteroid_id) VALUES (%s)" % asteroid_id)
        print(mission_2_insert_sql)
        updateSql(mission_2_insert_sql)
        mission_3_insert_sql = ("INSERT INTO colonization_missions_tracking_3 (asteroid_id) VALUES (%s)" % asteroid_id)
        print(mission_3_insert_sql)
        updateSql(mission_3_insert_sql)
        mission_4_insert_sql = ("INSERT INTO colonization_missions_tracking_4 (asteroid_id) VALUES (%s)" % asteroid_id)
        print(mission_4_insert_sql)
        updateSql(mission_4_insert_sql)
        mission_5_insert_sql = ("INSERT INTO colonization_missions_tracking_5 (asteroid_id) VALUES (%s)" % asteroid_id)
        print(mission_5_insert_sql)
        updateSql(mission_5_insert_sql)
        mission_6_insert_sql = ("INSERT INTO colonization_missions_tracking_6 (asteroid_id) VALUES (%s)" % asteroid_id)
        print(mission_6_insert_sql)
        updateSql(mission_6_insert_sql)
        mission_7_insert_sql = ("INSERT INTO colonization_missions_tracking_7 (asteroid_id) VALUES (%s)" % asteroid_id)
        print(mission_7_insert_sql)
        updateSql(mission_7_insert_sql)
        mission_8_insert_sql = ("INSERT INTO colonization_missions_tracking_8 (asteroid_id) VALUES (%s)" % asteroid_id)
        print(mission_8_insert_sql)
        updateSql(mission_8_insert_sql)
        mission_9_insert_sql = ("INSERT INTO colonization_missions_tracking_9 (asteroid_id) VALUES (%s)" % asteroid_id)
        print(mission_9_insert_sql)
        updateSql(mission_9_insert_sql)
        mission_10_insert_sql = ("INSERT INTO colonization_missions_tracking_10 (asteroid_id) VALUES (%s)" % asteroid_id)
        print(mission_10_insert_sql)
        updateSql(mission_10_insert_sql)
        mission_11_insert_sql = ("INSERT INTO colonization_missions_tracking_11 (asteroid_id) VALUES (%s)" % asteroid_id)
        print(mission_11_insert_sql)
        updateSql(mission_11_insert_sql)

        update_asteroid_sql = ("UPDATE asteroids SET colonization_missions_tracking = 1 WHERE asteroid_id = %s" % asteroid_id)
        print(update_asteroid_sql)
        updateSql(update_asteroid_sql)


def getNewAsteroids(db_user, db_password, db):

    asteroids = []
    sql = "SELECT b.asteroid_id, b.caller_crew_id, b.caller_address FROM dispatcher_resource_scan_finished b, asteroids c WHERE b.asteroid_id = c.asteroid_id and c.colonization_missions_tracking = 0"
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()

    if rows == None:
        return asteroids

    for row in rows:
        asteroids.append({"asteroid_id": row[0], "crew_id": row[1], "caller_address": row[2]})

    cur.close()
    con.close()

    return asteroids


def getWork(db_user, db_password, db):

    work = []
    sql ="SELECT asteroid_id, req_1_wallet, req_1_crew_id, req_1, req_1_goal, req_2_wallet, req_2_crew_id, req_2, req_2_goal FROM colonization_missions_tracking_1"
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()

    if rows == None:
        return work

    for row in rows:
        asteroid_id=row[0]
        work.append({"asteroid_id": asteroid_id})

    cur.close()
    con.close()

    return work


def getBuilding(db_user, db_password, db, building_type, building_id, asteroid_id):

    caller_address = None
    caller_crew_id = None
    txn_id = None
    name = None
    sql = ("SELECT caller_address, crew_id, finish_txn_id, building_id FROM construction WHERE building_type = %s AND building_id = %s AND asteroid_id = %s" % (building_type, building_id, asteroid_id))
    #print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()
        for row in rows:
            caller_address=row[0]
            caller_crew_id=row[1]
            txn_id=row[2]

    con.close()
    return caller_address, caller_crew_id, txn_id, name


def getAdministrator(db_user, db_password, db, asteroid_id):

    caller_address = None
    caller_crew_id = None
    txn_id = None
    sql = ("SELECT b.crew_id, c.crew_owner FROM asteroids b, crews c WHERE b.asteroid_id = %s AND b.crew_id = c.crew_id" % asteroid_id)
    #print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()
        for row in rows:
            caller_crew_id=row[0]
            caller_address=row[1]

    con.close()
    return caller_address, caller_crew_id


def getPotatoes(db_user, db_password, db, txn_id):

    resource_amount = 0
    sql = ("SELECT resource_amount FROM products_produced WHERE txn_id = '%s' AND resource_id = 92 LIMIT 1" % txn_id)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()
        for row in rows:
            resource_amount=row[0]

    con.close()
    return resource_amount


def getWarehouseStatus(db_user, db_password, db, asteroid_id):

    status = 0
    sql = ("SELECT COUNT(*) FROM colonization_missions_tracking_3 WHERE asteroid_id = %s AND req_2 = 3" % asteroid_id)
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        status=result[0]
        cur.close()

    con.close()
    return status


def processMission1(db_user, db_password, db, work_list):

    print("Processing Mission 1")
    completed_list = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    for work in work_list:
        asteroid_id = work['asteroid_id']
        sql = ("SELECT caller_address, caller_crew_id, block_number, timestamp, txn_id, ship_id FROM dispatcher_ship_docked WHERE asteroid_id = %s ORDER BY BLOCK_NUMBER LIMIT 1" % asteroid_id)
        #print(sql)
        with con:
            cur = con.cursor()
            cur.execute("%s" % sql)
            rows = cur.fetchall()
            cur.close()
        for row in rows:
            caller_address=row[0]
            caller_crew_id=row[1]
            block_number=row[2]
            timestamp=row[3]
            txn_id=row[4]
            ship_id=row[5]

        if len(rows) > 0:
            if int(asteroid_id) not in completed_list:
                update_sql=("UPDATE colonization_missions_tracking_1 SET req_2 = 1, req_2_crew_id = %s, req_2_wallet = '%s', req_2_txn_id = '%s', req_2_timestamp = '%s', req_2_ship_id = %s WHERE asteroid_id = %s" % (caller_crew_id, caller_address, txn_id, timestamp, ship_id, asteroid_id))
                print(update_sql)
                updateSql(update_sql)
                completed_list.append(int(asteroid_id))
            else:
                print("%s already finished mission_1" % asteroid_id)

    con.close()


def processMission2(db_user, db_password, db, work_list):

    print("Processing Mission 2")
    completed_list = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    for work in work_list:
        asteroid_id = work['asteroid_id']
        
        sql = ("SELECT caller_address, caller_crew_id, block_number, timestamp, txn_id, extractor_id, resource_yield FROM dispatcher_resource_extraction_finished WHERE extractor_asteroid_id = %s AND resource_yield >= 2000000 ORDER BY BLOCK_NUMBER LIMIT 1" % asteroid_id)
        #print(sql)
        with con:
            cur = con.cursor()
            cur.execute("%s" % sql)
            rows = cur.fetchall()
            cur.close()
        for row in rows:
            caller_address=row[0]
            caller_crew_id=row[1]
            block_number=row[2]
            timestamp=row[3]
            txn_id=row[4]
            building_id=row[5]
            resource_yield=row[6]

        if len(rows) > 0:
            if int(asteroid_id) not in completed_list:
                building_caller_address, building_caller_crew_id, building_txn_id, building_name = getBuilding(db_user, db_password, db, 2, building_id, asteroid_id)
                update_sql=("UPDATE colonization_missions_tracking_2 SET req_1 = 1, req_1_wallet = '%s', req_1_crew_id = %s, req_1_txn_id = '%s', req_1_building_id = %s, req_2 = 2000000, req_2_crew_id = %s, req_2_wallet = '%s', req_2_txn_id = '%s', req_2_timestamp = '%s', req_2_extractor_id = %s  WHERE asteroid_id = %s" % (building_caller_address, building_caller_crew_id, building_txn_id, building_id, caller_crew_id, caller_address, txn_id, timestamp, building_id, asteroid_id))
                print(update_sql)
                updateSql(update_sql)
                completed_list.append(int(asteroid_id))
            else:
                print("%s already finished mission_2" % asteroid_id)

    con.close()


def processMission3(db_user, db_password, db, work_list):

    print("Processing Mission 3")
    completed_list = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    for work in work_list:
        asteroid_id = work['asteroid_id']
        sql = ("SELECT finish_txn_id, finish_block_number, finish_timestamp, caller_address, crew_id, dest_id, product_id FROM deliveries WHERE dest_asteroid_id = %s AND dest_label = 5 AND dest_type = 1 AND product_id < 23 AND finish_txn_id IS NOT NULL ORDER BY finish_block_number" % asteroid_id)
        #print(sql)
        deliveries = {}
        products = {}
        with con:
            cur = con.cursor()
            cur.execute("%s" % sql)
            rows = cur.fetchall()
            cur.close()
        for row in rows:
            txn_id=row[0]
            block_number=row[1]
            timestamp=row[2]
            caller_address=row[3]
            caller_crew_id=row[4]
            building_id=row[5]
            product_id=row[6]

            if asteroid_id not in completed_list:
                if len(rows) > 0:
                    if building_id in deliveries:
                        deliveries[building_id] += 1
                    else:
                        deliveries[building_id] = 1

                    if building_id in products:
                        print("found %s in %s" % (building_id, products))
                        if product_id not in products[building_id]:
                            products[building_id].append(product_id)
                            print("%s len: %s" % (building_id, len(products[building_id])))
                            if len(products[building_id]) >= 3:
                                print("products for %s: %s" % (asteroid_id, products))
                                #if (len(statuses) == 0):
                                building_caller_address, building_caller_crew_id, building_txn_id, building_name = getBuilding(db_user, db_password, db, 1, building_id, asteroid_id)
                                update_sql=("UPDATE colonization_missions_tracking_3 SET req_1 = 1, req_1_wallet = '%s', req_1_crew_id = %s, req_1_txn_id = '%s', req_1_building_id = %s, req_2 = 3, req_2_wallet = '%s', req_2_crew_id = %s, req_2_txn_id = '%s', req_2_timestamp = '%s', req_2_warehouse_id = %s WHERE asteroid_id = %s" % (building_caller_address, building_caller_crew_id, building_txn_id, building_id, caller_address, caller_crew_id, txn_id, timestamp, building_id, asteroid_id))
                                print(update_sql)
                                updateSql(update_sql)
                                #statuses.append(building_id)
                                completed_list.append(int(asteroid_id))

                    else:
                        products[building_id]=[product_id]
                        print("initializing %s this: %s" % (building_id, products[building_id]))

    con.close()


def processMission4(db_user, db_password, db, work_list):

    print("Processing Mission 4")
    completed_list = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    for work in work_list:
        asteroid_id = work['asteroid_id']
        sql = ("SELECT caller_address, caller_crew_id, block_number, timestamp, txn_id, processor_id FROM dispatcher_material_processing_finished WHERE processor_asteroid_id = %s AND processor_type = 3 ORDER BY BLOCK_NUMBER LIMIT 1" % asteroid_id)
        #print(sql)
        with con:
            cur = con.cursor()
            cur.execute("%s" % sql)
            rows = cur.fetchall()
            cur.close()
        for row in rows:
            caller_address=row[0]
            caller_crew_id=row[1]
            block_number=row[2]
            timestamp=row[3]
            txn_id=row[4]
            building_id=row[5]

        if len(rows) > 0:
            if asteroid_id not in completed_list:
                building_caller_address, building_caller_crew_id, building_txn_id, building_name = getBuilding(db_user, db_password, db, 3, building_id, asteroid_id)
                update_sql=("UPDATE colonization_missions_tracking_4 SET req_1 = 1, req_1_wallet = '%s', req_1_crew_id = %s, req_1_txn_id = '%s', req_1_building_id = %s, req_2 = 1, req_2_crew_id = %s, req_2_wallet = '%s', req_2_txn_id = '%s', req_2_timestamp = '%s', req_2_refinery_id = %s  WHERE asteroid_id = %s" % (building_caller_address, building_caller_crew_id, building_txn_id, building_id, caller_crew_id, caller_address, txn_id, timestamp, building_id, asteroid_id))
                print(update_sql)
                updateSql(update_sql)
                completed_list.append(int(asteroid_id))

    con.close()


def processMission5(db_user, db_password, db, work_list):

    print("Processing Mission 5")
    completed_list = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    for work in work_list:
        asteroid_id = work['asteroid_id']
        sql = ("SELECT caller_address, caller_crew_id, block_number, timestamp, txn_id, processor_id FROM dispatcher_material_processing_finished WHERE processor_asteroid_id = %s AND processor_type = 5 ORDER BY BLOCK_NUMBER LIMIT 1" % asteroid_id)
        #print(sql)
        with con:
            cur = con.cursor()
            cur.execute("%s" % sql)
            rows = cur.fetchall()
            cur.close()
        for row in rows:
            caller_address=row[0]
            caller_crew_id=row[1]
            block_number=row[2]
            timestamp=row[3]
            txn_id=row[4]
            building_id=row[5]

        if len(rows) > 0:
            if asteroid_id not in completed_list:
                building_caller_address, building_caller_crew_id, building_txn_id, building_name = getBuilding(db_user, db_password, db, 5, building_id, asteroid_id)
                update_sql=("UPDATE colonization_missions_tracking_5 SET req_1 = 1, req_1_wallet = '%s', req_1_crew_id = %s, req_1_txn_id = '%s', req_1_building_id = %s, req_2 = 1, req_2_crew_id = %s, req_2_wallet = '%s', req_2_txn_id = '%s', req_2_timestamp = '%s', req_2_factory_id = %s  WHERE asteroid_id = %s" % (building_caller_address, building_caller_crew_id, building_txn_id, building_id, caller_crew_id, caller_address, txn_id, timestamp, building_id, asteroid_id))
                print(update_sql)
                updateSql(update_sql)
                completed_list.append(int(asteroid_id))

    con.close()


def checkMission6(db_user, db_password, db, asteroid_id):

    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    sql=("SELECT req_2 FROM colonization_missions_tracking_6 WHERE asteroid_id = %s LIMIT 1" % asteroid_id)
    #print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()
    for row in rows:
        req_2 = row[0]

    con.close()
    return req_2


def processMission6(db_user, db_password, db, work_list):

    print("Processing Mission 6")
    completed_list = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    for work in work_list:
        asteroid_id = work['asteroid_id']
        result = checkMission6(db_user, db_password, db, asteroid_id)
        if result < 75600:
            sql = ("SELECT caller_address, crew_id, finish_block_number, finish_timestamp, finish_txn_id, processor_id FROM processing_actions WHERE processor_asteroid_id = %s AND processor_type = 4 AND process_id = 98 AND finish_txn_id IS NOT NULL ORDER BY finish_block_number" % asteroid_id)
            #print(sql)
            with con:
                cur = con.cursor()
                cur.execute("%s" % sql)
                rows = cur.fetchall()
                cur.close()
            for row in rows:
                caller_address=row[0]
                caller_crew_id=row[1]
                block_number=row[2]
                timestamp=row[3]
                txn_id=row[4]
                building_id=row[5]

            if len(rows) > 0:
                building_caller_address, building_caller_crew_id, building_txn_id, building_name = getBuilding(db_user, db_password, db, 4, building_id, asteroid_id)
                resource_amount = getPotatoes(db_user, db_password, db, txn_id)
                if resource_amount >= 75600:
                    if asteroid_id not in completed_list:
                        update_sql=("UPDATE colonization_missions_tracking_6 SET req_1 = 1, req_1_wallet = '%s', req_1_crew_id = %s, req_1_txn_id = '%s', req_1_building_id = %s, req_2 = 1, req_2_crew_id = %s, req_2_wallet = '%s', req_2_txn_id = '%s', req_2_timestamp = '%s', req_2_bioreactor_id = %s  WHERE asteroid_id = %s" % (building_caller_address, building_caller_crew_id, building_txn_id, building_id, caller_crew_id, caller_address, txn_id, timestamp, building_id, asteroid_id))
                        print(update_sql)
                        updateSql(update_sql)
                        completed_list.append(int(asteroid_id))

    con.close()


def processMission7(db_user, db_password, db, work_list):

    print("Processing Mission 7")
    completed_list = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    for work in work_list:
        asteroid_id = work['asteroid_id']
        sql = ("SELECT caller_address, crew_id, finish_block_number, finish_timestamp, finish_txn_id, dry_dock_id, ship_id FROM ship_assembly WHERE origin_asteroid_id = %s AND finish_txn_id IS NOT NULL ORDER BY finish_block_number LIMIT 1" % asteroid_id)
        #print(sql)
        with con:
            cur = con.cursor()
            cur.execute("%s" % sql)
            rows = cur.fetchall()
            cur.close()
        for row in rows:
            caller_address=row[0]
            caller_crew_id=row[1]
            block_number=row[2]
            timestamp=row[3]
            txn_id=row[4]
            building_id=row[5]
            ship_id=row[6]

        if len(rows) > 0:
            if asteroid_id not in completed_list:
                building_caller_address, building_caller_crew_id, building_txn_id, building_name = getBuilding(db_user, db_password, db, 6, building_id, asteroid_id)
                update_sql=("UPDATE colonization_missions_tracking_7 SET req_1 = 1, req_1_wallet = '%s', req_1_crew_id = %s, req_1_txn_id = '%s', req_1_building_id = %s, req_2 = 1, req_2_crew_id = %s, req_2_wallet = '%s', req_2_txn_id = '%s', req_2_timestamp = '%s', req_2_shipyard_id = %s, req_2_ship_id = %s WHERE asteroid_id = %s" % (building_caller_address, building_caller_crew_id, building_txn_id, building_id, caller_crew_id, caller_address, txn_id, timestamp, building_id, ship_id, asteroid_id))
                print(update_sql)
                updateSql(update_sql)
                completed_list.append(int(asteroid_id))

    con.close()


def processMission8(db_user, db_password, db, work_list):

    print("Processing Mission 8")
    completed_list = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    for work in work_list:
        asteroid_id = work['asteroid_id']
        sql = ("SELECT b.caller_address, b.crew_id, b.txn_id, b.block_number, b.dock_id, b.ship_id, c.timestamp FROM ships_docked b, dispatcher_ship_docked c WHERE b.dock_asteroid_id = %s AND b.dock_type = 7 AND b.txn_id = c.txn_id ORDER BY b.block_number LIMIT 1" % asteroid_id)
        #print(sql)
        with con:
            cur = con.cursor()
            cur.execute("%s" % sql)
            rows = cur.fetchall()
            cur.close()
        for row in rows:
            caller_address=row[0]
            crew_id=row[1]
            txn_id=row[2]
            block_number=row[3]
            building_id=row[4]
            ship_id=row[5]
            timestamp=row[6]

        if len(rows) > 0:
            if asteroid_id not in completed_list:
                building_caller_address, building_caller_crew_id, building_txn_id, building_name = getBuilding(db_user, db_password, db, 7, building_id, asteroid_id)
                update_sql=("UPDATE colonization_missions_tracking_8 SET req_1 = 1, req_1_wallet = '%s', req_1_crew_id = %s, req_1_txn_id = '%s', req_1_building_id = %s, req_2 = 1, req_2_crew_id = %s, req_2_wallet = '%s', req_2_txn_id = '%s', req_2_timestamp = '%s', req_2_spaceport_id = %s, req_2_ship_id = %s WHERE asteroid_id = %s" % (building_caller_address, building_caller_crew_id, building_txn_id, building_id, crew_id, caller_address, txn_id, timestamp, building_id, ship_id, asteroid_id))
                print(update_sql)
                updateSql(update_sql)
                completed_list.append(asteroid_id)

    con.close()


def processMission9(db_user, db_password, db, work_list):

    print("Processing Mission 9")
    completed_list = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    for work in work_list:
        asteroid_id = work['asteroid_id']
        sql = ("SELECT txn_id, block_number, timestamp, exchange_id, caller_address, caller_crew_id FROM dispatcher_sell_order_filled WHERE exchange_asteroid_id = %s ORDER BY block_number" % asteroid_id)
        #print(sql)
        sell_orders = {}
        with con:
            cur = con.cursor()
            cur.execute("%s" % sql)
            rows = cur.fetchall()
            cur.close()
        for row in rows:
            txn_id=row[0]
            block_number=row[1]
            timestamp=row[2]
            building_id=row[3]
            caller_address=row[4]
            caller_crew_id=row[5]

            if len(rows) > 0:
                if building_id in sell_orders:
                    sell_orders[building_id] += 1
                else:
                    sell_orders[building_id] = 1

                if sell_orders[building_id] == 10:
                    #if (len(statuses) == 0):
                    if asteroid_id not in completed_list:
                        building_caller_address, building_caller_crew_id, building_txn_id, building_name = getBuilding(db_user, db_password, db, 8, building_id, asteroid_id)
                        update_sql=("UPDATE colonization_missions_tracking_9 SET req_1 = 1, req_1_wallet = '%s', req_1_crew_id = %s, req_1_txn_id = '%s', req_1_building_id = %s, req_2 = 10, req_2_wallet = '%s', req_2_crew_id = %s, req_2_txn_id = '%s', req_2_timestamp = '%s', req_2_exchange_id = %s WHERE asteroid_id = %s" % (building_caller_address, building_caller_crew_id, building_txn_id, building_id, caller_address, caller_crew_id, txn_id, timestamp, building_id, asteroid_id))
                        print(update_sql)
                        updateSql(update_sql)
                        completed_list.append(asteroid_id)

    con.close()


def processMission10(db_user, db_password, db, work_list):

    print("Processing Mission 10")
    completed_list = []
    recruits = {}
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    for work in work_list:
        asteroid_id = work['asteroid_id']
        sql = ("SELECT b.txn_id, b.block_number, b.crewmate_owner, b.station_id, b.crew_id, c.timestamp FROM crewmates b, dispatcher_crewmate_recruited_v1 c WHERE b.origin_asteroid_id = %s AND b.station_label = 5 AND b.crewmate_id = c.crewmate_id ORDER BY b.block_number" % asteroid_id)
        with con:
            cur = con.cursor()
            cur.execute("%s" % sql)
            rows = cur.fetchall()
            cur.close()
        for row in rows:
            txn_id=row[0]
            block_number=row[1]
            caller_address=row[2]
            building_id=row[3]
            crew_id=row[4]
            timestamp=row[5]
            
            if len(rows) > 0:
                if building_id in recruits:
                    recruits[building_id] += 1
                else:
                    recruits[building_id] = 1

                if recruits[building_id] == 5:
                    #if (len(statuses) == 0):
                    if asteroid_id not in completed_list:
                        building_caller_address, building_caller_crew_id, building_txn_id, building_name = getBuilding(db_user, db_password, db, 9, building_id, asteroid_id)
                        update_sql=("UPDATE colonization_missions_tracking_10 SET req_1 = 1, req_1_wallet = '%s', req_1_crew_id = %s, req_1_txn_id = '%s', req_1_building_id = %s, req_2 = 5, req_2_wallet = '%s', req_2_crew_id = %s, req_2_txn_id = '%s', req_2_timestamp = '%s', req_2_habitat_id = %s WHERE asteroid_id = %s" % (building_caller_address, building_caller_crew_id, building_txn_id, building_id, caller_address, crew_id, txn_id, timestamp, building_id, asteroid_id))
                        print(update_sql)
                        updateSql(update_sql)
                        completed_list.append(int(asteroid_id))

    con.close()


def processMission11(db_user, db_password, db, work_list):

    print("Processing Mission 11")
    completed_list = []
    for work in work_list:
        asteroid_id = work['asteroid_id']
        con = pymysql.connect("127.0.0.1", db_user, db_password, db)
        if asteroid_id not in completed_list:
            sql = ("SELECT caller_address, crew_id, finish_txn_id, finish_timestamp, building_id, building_type FROM construction WHERE asteroid_id = %s AND status = 2 AND building_type <= 10" % asteroid_id)
            #print(sql)
            buildings = []
            with con:
                cur = con.cursor()
                cur.execute("%s" % sql)
                rows = cur.fetchall()
                cur.close()
            for row in rows:
                caller_address=row[0]
                crew_id=row[1]
                txn_id=row[2]
                timestamp=row[3]
                building_id=row[4]
                building_type=row[5]
                if building_type not in buildings:
                    buildings.append(building_type)
                        
            buildings_len = len(buildings)
            if (buildings_len >= 10):
                print("buildings: %s" % buildings)
                administrator_address, administrator_crew_id = getAdministrator(db_user, db_password, db, asteroid_id)
                update_sql=("UPDATE colonization_missions_tracking_11 SET req_1 = 10, req_1_wallet = '%s', req_1_crew_id = %s, req_1_txn_id = '%s', req_1_timestamp = '%s' WHERE asteroid_id = %s" % (administrator_address, administrator_crew_id, txn_id, timestamp, asteroid_id))
                print(update_sql)
                updateSql(update_sql)
                completed_list.append(int(asteroid_id))

        con.close()


async def log_loop(poll_interval, db_user, db_password, db, phase):

    while True:

        loadNewAsteroids(db_user, db_password, db)
        work = getWork(db_user, db_password, db)
        # Touchdown
        processMission1(db_user, db_password, db, work)
        # Below the Surface
        processMission2(db_user, db_password, db, work)
        # Pack it Up
        processMission3(db_user, db_password, db, work)
        # Refined Taste
        processMission4(db_user, db_password, db, work)
        # Industrial Revolution
        processMission5(db_user, db_password, db, work)
        # PoTAYto / PoTAHto
        processMission6(db_user, db_password, db, work)
        # Expansion and Exploration
        processMission7(db_user, db_password, db, work)
        # Port City
        processMission8(db_user, db_password, db, work)
        # Open for Business
        processMission9(db_user, db_password, db, work)
        # Homesteading
        processMission10(db_user, db_password, db, work)
        # We Built this City
        processMission11(db_user, db_password, db, work)

        await asyncio.sleep(poll_interval)


def main():

    global db_user
    global db_password
    global db

    filename = __file__
    config_path = filename.split('/')[3]
    phase = config_path.split('_')[1]
    config_file = "/home/bios/" + config_path + "/indexer.conf"

    if os.path.exists(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        db_user = config.get('credentials', 'db_user')
        db_password = config.get('credentials', 'db_password')
        db = config.get('credentials', 'db')

    else:
        raise Exception(config_file)

    poll_interval=120
    loop = asyncio.get_event_loop()
    try:
        print("*** Starting solo missions aggregator")
        loop.run_until_complete(
            asyncio.gather(
                log_loop(poll_interval, db_user, db_password, db, phase)))
    finally:
        loop.close()


if __name__ == "__main__" : main()

