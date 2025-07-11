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


def verifyDB(db_user, db_password, db):

    sql = ("SELECT mission_id, mission_name, mission_required FROM community_missions_summary")
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()

    mission_count = 0
    for row in rows:
        mission_count+=1

    if mission_count != 8:
        print("truncate and load the db")
        truncate_sql = ("TRUNCATE community_missions_summary")
        print(truncate_sql)
        updateSql(truncate_sql)

        sql1="INSERT INTO community_missions_summary (mission_id, mission_name, mission_required, mission_description) VALUES (1, 'Romulus, Remus, and the Rest', 7000, 'Construct a building on Adalia Prime')"
        sql2="INSERT INTO community_missions_summary (mission_id, mission_name, mission_required, mission_description) VALUES (2, 'Learn by Doing', 6000, 'Construct a warehouse or an extractor anywhere in the Belt')"
        sql3="INSERT INTO community_missions_summary (mission_id, mission_name, mission_required, mission_description) VALUES (3, 'Four Pillars', 3000, 'Construct a refinery, bioreactor, factory, or shipyard anywhere in the Belt')"
        sql4="INSERT INTO community_missions_summary (mission_id, mission_name, mission_required, mission_description) VALUES (4, 'Together, We Can Rise', 400, 'Construct a spaceport, marketplace, or habitat anywhere in the Belt')"
        sql5="INSERT INTO community_missions_summary (mission_id, mission_name, mission_required, mission_description) VALUES (5, 'The Fleet', 300, 'Construct a ship')"
        sql6="INSERT INTO community_missions_summary (mission_id, mission_name, mission_required, mission_description) VALUES (6, 'Rock Breaker', 12000000, 'Mine one tonne of material')"
        sql7="INSERT INTO community_missions_summary (mission_id, mission_name, mission_required, mission_description) VALUES (7, 'Prospecting Pays Off', 15000, 'Take one core sample')"
        sql8="INSERT INTO community_missions_summary (mission_id, mission_name, mission_required, mission_description) VALUES (8, 'Potluck', 20000, 'Manufacture 5 tonnes of food')"
        updateSql(sql1)
        updateSql(sql2)
        updateSql(sql3)
        updateSql(sql4)
        updateSql(sql5)
        updateSql(sql6)
        updateSql(sql7)
        updateSql(sql8)


def updateSummary(mission_id, actual, crews):

    sql=("UPDATE community_missions_summary SET mission_actual = %s, mission_crews = %s WHERE mission_id = %s" % (actual, crews, mission_id))
    print(sql)
    updateSql(sql)


def loadNewCrews(db_user, db_password, db):

    new_crews = getNewCrews(db_user, db_password, db)
    for row in new_crews:
        crew_id = row['crew_id']
        wallet = row['wallet']
        new_insert_sql = ("INSERT INTO community_missions_tracking (crew_id, wallet) VALUES (%s, '%s')" % (crew_id, wallet))
        print(new_insert_sql)
        updateSql(new_insert_sql)

        update_crew_sql = ("UPDATE crews SET community_missions_tracking = 1 WHERE crew_id = %s" % crew_id)
        print(update_crew_sql)
        updateSql(update_crew_sql)


def updateDelagatedCrews(db_user, db_password, db):

    crew_sql = "SELECT crew_id, delegated_address FROM crews WHERE community_missions_tracking = 1"
    print(crew_sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with con:
        cur = con.cursor()
        cur.execute("%s" % crew_sql)
        rows = cur.fetchall()

    for row in rows:
        crew_id = row[0]
        wallet = row[1]
        update_sql = ("UPDATE community_missions_tracking SET wallet = '%s' WHERE crew_id = %s" % (wallet, crew_id))
        print(update_sql)
        updateSql(update_sql)

    cur.close()
    con.close()



def getNewCrews(db_user, db_password, db):

    crews = []
    sql = "SELECT crew_id, delegated_address FROM crews WHERE community_missions_tracking = 0"
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()

    if rows == None:
        return crews

    for row in rows:
        crews.append({"crew_id": row[0], "wallet": row[1]})

    cur.close()
    con.close()

    return crews


def processResults(db_user, db_password, db, mission_results, col_1, col_2):

    print(mission_results)
    for row in mission_results:
        crew_id = row['crew_id']
        value = row['value']
        update_sql=("UPDATE community_missions_tracking SET %s = %s, %s = 1 WHERE crew_id = %s" % (col_1, value, col_2, crew_id))
        print(update_sql)
        updateSql(update_sql)


def getGlobal1(user, db_password, db):

    mission_1 = []
    count = 0
    sql = "SELECT COUNT(*) FROM construction WHERE asteroid_id = 1 AND status = 2"
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        count=result[0]

    return count


def getGlobal2(user, db_password, db):

    mission_2 = []
    count = 0
    sql = "SELECT COUNT(*) FROM construction WHERE building_type in (1, 2) AND status = 2"
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        count=result[0]

    return count


def getGlobal3(user, db_password, db):

    mission_3 = []
    count = 0
    sql = "SELECT COUNT(*) FROM construction WHERE building_type in (3, 4, 5, 6) AND status = 2"
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        count=result[0]

    return count


def getGlobal4(user, db_password, db):

    mission_4 = []
    count = 0
    sql = "SELECT COUNT(*) FROM construction WHERE building_type in (7, 8, 9) AND status = 2"
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        count=result[0]

    return count


def getGlobal5(user, db_password, db):

    mission_5 = []
    count = 0
    sql = "SELECT COUNT(*) FROM ship_assembly WHERE STATUS = 2"
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        count=result[0]

    return count


def getGlobal6(user, db_password, db):

    mission_6 = []
    count = 0
    sql = "SELECT SUM(resource_yield) FROM extractions WHERE status = 2"
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        count=result[0]

    if count is None:
        count = 0

    return count


def getGlobal7(user, db_password, db):

    mission_7 = []
    count = 0
    sql = "SELECT COUNT(*) FROM core_samples WHERE status = 2"
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        count=result[0]

    return count


def getGlobal8(user, db_password, db):

    mission_8 = []
    count = 0
    sql = "SELECT SUM(amount) FROM food_produced"
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        count=result[0]

    if count is None:
        count = 0

    return count


def getGlobalWallets1(db_user, db_password, db):

    print("IM IN getGlobalWallets1")
    mission_1 = []
    crews = []
    sql = "SELECT COUNT(*), crew_id, caller_address FROM construction WHERE asteroid_id = 1 AND status = 2 GROUP BY crew_id"
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()

    for row in rows:
        building_count = row[0]
        crew_id = row[1]
        wallet = row[2]
        if crew_id not in crews:
            mission_1.append({"crew_id": crew_id, "value": building_count, "wallet": wallet})
            crews.append(crew_id)

    print(mission_1)
    return mission_1


def getGlobalWallets2(db_user, db_password, db):

    print("IM IN getGlobalWallets2")
    mission_2 = []
    crews = []
    sql = "SELECT COUNT(*), crew_id, caller_address FROM construction WHERE building_type in (1, 2) AND status = 2 GROUP BY crew_id"
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()

    for row in rows:
        building_count = row[0]
        crew_id = row[1]
        wallet = row[2]
        if crew_id not in crews:
            mission_2.append({"crew_id": crew_id, "value": building_count, "wallet": wallet})
            crews.append(crew_id)

    print(mission_2)
    return mission_2


def getGlobalWallets3(db_user, db_password, db):

    print("IM IN getGlobalWallets3")
    mission_3 = []
    crews = []
    sql = "SELECT COUNT(*), crew_id, caller_address FROM construction WHERE building_type in (3, 4, 5, 6) AND status = 2 GROUP BY crew_id"
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()

    for row in rows:
        building_count = row[0]
        crew_id = row[1]
        wallet = row[2]
        if crew_id not in crews:
            mission_3.append({"crew_id": crew_id, "value": building_count, "wallet": wallet})
            crews.append(crew_id)

    print(mission_3)
    return mission_3


def getGlobalWallets4(db_user, db_password, db):

    print("IM IN getGlobalWallets4")
    mission_4 = []
    crews = []
    sql = "SELECT COUNT(*), crew_id, caller_address FROM construction WHERE building_type in (7, 8, 9) AND status = 2 GROUP BY crew_id"
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()

    for row in rows:
        building_count = row[0]
        crew_id = row[1]
        wallet = row[2]
        if crew_id not in crews:
            mission_4.append({"crew_id": crew_id, "value": building_count, "wallet": wallet})
            crews.append(crew_id)

    print(mission_4)
    return mission_4


def getGlobalWallets5(db_user, db_password, db):

    print("IM IN getGlobalWallets5")
    mission_5 = []
    crews = []
    sql = "SELECT COUNT(*), crew_id, caller_address FROM ship_assembly WHERE STATUS = 2 GROUP BY crew_id"
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()

    for row in rows:
        ships = row[0]
        crew_id = row[1]
        wallet = row[2]
        if crew_id not in crews:
            mission_5.append({"crew_id": crew_id, "value": ships, "wallet": wallet})
            crews.append(crew_id)

    print(mission_5)
    return mission_5


def getGlobalWallets6(db_user, db_password, db):

    print("IM IN getGlobalWallets6")
    mission_6 = []
    crews = []
    sql = "SELECT SUM(resource_yield), caller_crew_id, caller_address FROM dispatcher_resource_extraction_finished GROUP BY caller_crew_id"
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()

    for row in rows:
        resource_yield = row[0]
        crew_id = row[1]
        wallet = row[2]
        if resource_yield >= 1000:
            if crew_id not in crews:
                mission_6.append({"crew_id": crew_id, "value": resource_yield, "wallet": wallet})
                crews.append(crew_id)

    print(mission_6)
    return mission_6


def getGlobalWallets7(db_user, db_password, db):

    print("IM IN getGlobalWallets7")
    mission_7 = []
    crews = []
    sql = "SELECT COUNT(*), crew_id, caller_address FROM core_samples WHERE status = 2 GROUP BY crew_id"
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()

    for row in rows:
        core_samples = row[0]
        crew_id = row[1]
        wallet = row[2]
        if crew_id not in crews:
            mission_7.append({"crew_id": crew_id, "value": core_samples, "wallet": wallet})
            crews.append(crew_id)

    print(mission_7)
    return mission_7


def getGlobalWallets8(db_user, db_password, db):

    print("IM IN getGlobalWallets8")
    mission_8 = []
    crews = []
    sql = "SELECT SUM(amount), crew_id, caller_address FROM food_produced GROUP BY crew_id"
    print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()

    for row in rows:
        food = row[0]
        crew_id = row[1]
        wallet = row[2]
        if food > 5000:
            if crew_id not in crews:
                mission_8.append({"crew_id": crew_id, "value": food, "wallet": wallet})
                crews.append(crew_id)

    print(mission_8)
    return mission_8


async def log_loop(poll_interval, db_user, db_password, db, phase):

    while True:

        updateDelagatedCrews(db_user, db_password, db)
        loadNewCrews(db_user, db_password, db)

        # Romulus, Remus, and the Rest
        # Construct a building on AP
        # Must Reach: 7000 buildings
        global_1_min_required = 1
        global_1_actual = getGlobal1(db_user, db_password, db)
        if global_1_actual >= global_1_min_required:
            print("global_1_required: %s" % global_1_min_required)
            print("global_1_actual: %s" % global_1_actual)
            mission_1_results = getGlobalWallets1(db_user, db_password, db)
            updateSummary(1, global_1_actual, len(mission_1_results))
            processResults(db_user, db_password, db, mission_1_results, "mission_1_wallet_amount", "mission_1_wallet_status")

        # Learn by Doing
        # Construct a Warehouse or an Extractor anywhere in the Belt
        # Must Reach: 6000 buildings
        global_2_min_required = 1
        global_2_actual = getGlobal2(db_user, db_password, db)
        if global_2_actual >= global_2_min_required:
            print("global_2_required: %s" % global_2_min_required)
            print("global_2_actual: %s" % global_2_actual)
            mission_2_results = getGlobalWallets2(db_user, db_password, db)
            updateSummary(2, global_2_actual, len(mission_2_results))
            processResults(db_user, db_password, db, mission_2_results, "mission_2_wallet_amount", "mission_2_wallet_status")

        # Four Pillars
        # Construct a Refinery, Bioreactor, Factory, or Shipyard anywhere in the Belt
        # Must Reach: 3000 buildings
        global_3_min_required = 1
        global_3_actual = getGlobal3(db_user, db_password, db)
        if global_3_actual >= global_3_min_required:
            print("global_3_required: %s" % global_3_min_required)
            print("global_3_actual: %s" % global_3_actual)
            mission_3_results = getGlobalWallets3(db_user, db_password, db)
            updateSummary(3, global_3_actual, len(mission_3_results))
            processResults(db_user, db_password, db, mission_3_results, "mission_3_wallet_amount", "mission_3_wallet_status")

        # Together, We Can Rise
        # Construct a Spaceport, Marketplace, or Habitat anywhere in the Belt
        # Must Reach: 400 buildings
        global_4_min_required = 1
        global_4_actual = getGlobal4(db_user, db_password, db)
        if global_4_actual >= global_4_min_required:
            print("global_4_required: %s" % global_4_min_required)
            print("global_4_actual: %s" % global_4_actual)
            mission_4_results = getGlobalWallets4(db_user, db_password, db)
            updateSummary(4, global_4_actual, len(mission_4_results))
            processResults(db_user, db_password, db, mission_4_results, "mission_4_wallet_amount", "mission_4_wallet_status")

        # The Fleet
        # Construct a ship
        # Must Reach: 300 ships
        global_5_min_required = 1
        global_5_actual = getGlobal5(db_user, db_password, db)
        if global_5_actual >= global_5_min_required:
            print("global_5_required: %s" % global_5_min_required)
            print("global_5_actual: %s" % global_5_actual)
            mission_5_results = getGlobalWallets5(db_user, db_password, db)
            updateSummary(5, global_5_actual, len(mission_5_results))
            processResults(db_user, db_password, db, mission_5_results, "mission_5_wallet_amount", "mission_5_wallet_status")

        # Rock Breaker 
        # Mine one tonne of material
        # Must Reach: 12k tonnes
        global_6_min_required = 1
        global_6_actual = getGlobal6(db_user, db_password, db)
        global_6_actual = round(global_6_actual / 1000)
        if global_6_actual >= global_6_min_required:
            print("global_6_required: %s" % global_6_min_required)
            print("global_6_actual: %s" % global_6_actual)
            mission_6_results = getGlobalWallets6(db_user, db_password, db)
            updateSummary(6, global_6_actual, len(mission_6_results))
            processResults(db_user, db_password, db, mission_6_results, "mission_6_wallet_amount", "mission_6_wallet_status")

        # Prospecting Pays Off
        # Take one core sample
        # Must Reach: 15k core samples
        global_7_min_required = 1
        global_7_actual = getGlobal7(db_user, db_password, db)
        if global_7_actual >= global_7_min_required:
            print("global_7_required: %s" % global_7_min_required)
            print("global_7_actual: %s" % global_7_actual)
            mission_7_results = getGlobalWallets7(db_user, db_password, db)
            updateSummary(7, global_7_actual, len(mission_7_results))
            processResults(db_user, db_password, db, mission_7_results, "mission_7_wallet_amount", "mission_7_wallet_status")

        # Potluck 
        # Manufacture 5 tonnes of food
        # Must Reach: 20k tonnes
        global_8_min_required = 1
        global_8_actual = getGlobal8(db_user, db_password, db)
        global_8_actual = round(global_8_actual / 1000)
        if global_8_actual >= global_8_min_required:
            print("global_8_required: %s" % global_8_min_required)
            print("global_8_actual: %s" % global_8_actual)
            mission_8_results = getGlobalWallets8(db_user, db_password, db)
            updateSummary(8, global_8_actual, len(mission_8_results))
            processResults(db_user, db_password, db, mission_8_results, "mission_8_wallet_amount", "mission_8_wallet_status")

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

    verifyDB(db_user, db_password, db)

    poll_interval=120
    loop = asyncio.get_event_loop()
    try:
        print("*** Starting community missions aggregator")
        loop.run_until_complete(
            asyncio.gather(
                log_loop(poll_interval, db_user, db_password, db, phase)))
    finally:
        loop.close()


if __name__ == "__main__" : main()

