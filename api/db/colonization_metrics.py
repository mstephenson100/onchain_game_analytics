import sys
import os
import pymysql
import warnings
import traceback
import configparser
import time

sys.path.insert(0,'../')
import db.get_types as inf
import db.fix_address as fix_address

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


def getAsteroidStatus(con, asteroid_id):

    missions = []
    mission_1_sql = ("SELECT name, asteroid_id, req_1_wallet, req_1_crew_id, req_2_timestamp, req_2 FROM colonization_missions_tracking_1 WHERE asteroid_id = %s" % asteroid_id)
    mission_2_sql = ("SELECT name, asteroid_id, req_1_wallet, req_1_crew_id, req_2_timestamp, req_2 FROM colonization_missions_tracking_2 WHERE asteroid_id = %s" % asteroid_id)
    mission_3_sql = ("SELECT name, asteroid_id, req_1_wallet, req_1_crew_id, req_2_timestamp, req_2 FROM colonization_missions_tracking_3 WHERE asteroid_id = %s" % asteroid_id)
    mission_4_sql = ("SELECT name, asteroid_id, req_1_wallet, req_1_crew_id, req_2_timestamp, req_2 FROM colonization_missions_tracking_4 WHERE asteroid_id = %s" % asteroid_id)
    mission_5_sql = ("SELECT name, asteroid_id, req_1_wallet, req_1_crew_id, req_2_timestamp, req_2 FROM colonization_missions_tracking_5 WHERE asteroid_id = %s" % asteroid_id)
    mission_6_sql = ("SELECT name, asteroid_id, req_1_wallet, req_1_crew_id, req_2_timestamp, req_2 FROM colonization_missions_tracking_6 WHERE asteroid_id = %s" % asteroid_id)
    mission_7_sql = ("SELECT name, asteroid_id, req_1_wallet, req_1_crew_id, req_2_timestamp, req_2 FROM colonization_missions_tracking_7 WHERE asteroid_id = %s" % asteroid_id)
    mission_8_sql = ("SELECT name, asteroid_id, req_1_wallet, req_1_crew_id, req_2_timestamp, req_2 FROM colonization_missions_tracking_8 WHERE asteroid_id = %s" % asteroid_id)
    mission_9_sql = ("SELECT name, asteroid_id, req_1_wallet, req_1_crew_id, req_2_timestamp, req_2 FROM colonization_missions_tracking_9 WHERE asteroid_id = %s" % asteroid_id)
    mission_10_sql = ("SELECT name, asteroid_id, req_1_wallet, req_1_crew_id, req_2_timestamp, req_2 FROM colonization_missions_tracking_10 WHERE asteroid_id = %s" % asteroid_id)
    mission_11_sql = ("SELECT name, asteroid_id, req_1_wallet, req_1_crew_id, req_1_timestamp, req_1 FROM colonization_missions_tracking_11 WHERE asteroid_id = %s" % asteroid_id)

    with con:
        cur = con.cursor()
        cur.execute("%s" % mission_1_sql)
        mission_1_rows = cur.fetchall()
        cur.execute("%s" % mission_2_sql)
        mission_2_rows = cur.fetchall()
        cur.execute("%s" % mission_3_sql)
        mission_3_rows = cur.fetchall()
        cur.execute("%s" % mission_4_sql)
        mission_4_rows = cur.fetchall()
        cur.execute("%s" % mission_5_sql)
        mission_5_rows = cur.fetchall()
        cur.execute("%s" % mission_6_sql)
        mission_6_rows = cur.fetchall()
        cur.execute("%s" % mission_7_sql)
        mission_7_rows = cur.fetchall()
        cur.execute("%s" % mission_8_sql)
        mission_8_rows = cur.fetchall()
        cur.execute("%s" % mission_9_sql)
        mission_9_rows = cur.fetchall()
        cur.execute("%s" % mission_10_sql)
        mission_10_rows = cur.fetchall()
        cur.execute("%s" % mission_11_sql)
        mission_11_rows = cur.fetchall()
        cur.close()

        if len(mission_1_rows) > 0:
            mission_1_summary = parseAsteroidMission(mission_1_rows, "mission_1")
            mission_2_summary = parseAsteroidMission(mission_2_rows, "mission_2")
            mission_3_summary = parseAsteroidMission(mission_3_rows, "mission_3")
            mission_4_summary = parseAsteroidMission(mission_4_rows, "mission_4")
            mission_5_summary = parseAsteroidMission(mission_5_rows, "mission_5")
            mission_6_summary = parseAsteroidMission(mission_6_rows, "mission_6")
            mission_7_summary = parseAsteroidMission(mission_7_rows, "mission_7")
            mission_8_summary = parseAsteroidMission(mission_8_rows, "mission_8")
            mission_9_summary = parseAsteroidMission(mission_9_rows, "mission_9")
            mission_10_summary = parseAsteroidMission(mission_10_rows, "mission_10")
            mission_11_summary = parseAsteroidMission(mission_11_rows, "mission_11")
            missions = {asteroid_id: [mission_1_summary, mission_2_summary, mission_3_summary, mission_4_summary, mission_5_summary, mission_6_summary, mission_7_summary, mission_8_summary, mission_9_summary, mission_10_summary, mission_11_summary]}

        else:
            missions = {asteroid_id: []}

    return missions


def parseAsteroidMission(mission_results, label):

    summary = {}
    mission_name = None
    mission_wallet = None
    mission_crew_id = None
    mission_timestamp = None

    for row in mission_results:
        mission_name = row[0]
        mission_wallet = row[2]
        mission_crew_id = row[3]
        mission_timestamp = str(row[4])
        mission_req = row[5]

    if mission_req == 0:
        mission_wallet = None
        mission_crew_id = None
        mission_timestamp = None

    summary={label: {"name": mission_name, "wallet": mission_wallet, "crew_id": mission_crew_id, "timestamp": mission_timestamp}}
    return summary


def getGlobalReport(con):

    missions = []
    asteroids = getAsteroids(con, None)

    mission_1_sql = "SELECT name, asteroid_id, req_1_wallet, req_1_crew_id, req_2_timestamp, req_2 FROM colonization_missions_tracking_1"
    mission_2_sql = "SELECT name, asteroid_id, req_1_wallet, req_1_crew_id, req_2_timestamp, req_2 FROM colonization_missions_tracking_2"
    mission_3_sql = "SELECT name, asteroid_id, req_1_wallet, req_1_crew_id, req_2_timestamp, req_2 FROM colonization_missions_tracking_3"
    mission_4_sql = "SELECT name, asteroid_id, req_1_wallet, req_1_crew_id, req_2_timestamp, req_2 FROM colonization_missions_tracking_4"
    mission_5_sql = "SELECT name, asteroid_id, req_1_wallet, req_1_crew_id, req_2_timestamp, req_2 FROM colonization_missions_tracking_5"
    mission_6_sql = "SELECT name, asteroid_id, req_1_wallet, req_1_crew_id, req_2_timestamp, req_2 FROM colonization_missions_tracking_6"
    mission_7_sql = "SELECT name, asteroid_id, req_1_wallet, req_1_crew_id, req_2_timestamp, req_2 FROM colonization_missions_tracking_7"
    mission_8_sql = "SELECT name, asteroid_id, req_1_wallet, req_1_crew_id, req_2_timestamp, req_2 FROM colonization_missions_tracking_8"
    mission_9_sql = "SELECT name, asteroid_id, req_1_wallet, req_1_crew_id, req_2_timestamp, req_2 FROM colonization_missions_tracking_9"
    mission_10_sql = "SELECT name, asteroid_id, req_1_wallet, req_1_crew_id, req_2_timestamp, req_2 FROM colonization_missions_tracking_10"
    mission_11_sql = "SELECT name, asteroid_id, req_1_wallet, req_1_crew_id, req_1_timestamp, req_1 FROM colonization_missions_tracking_11"

    with con:
        cur = con.cursor()
        cur.execute("%s" % mission_1_sql)
        mission_1_rows = cur.fetchall()
        cur.execute("%s" % mission_2_sql)
        mission_2_rows = cur.fetchall()
        cur.execute("%s" % mission_3_sql)
        mission_3_rows = cur.fetchall()
        cur.execute("%s" % mission_4_sql)
        mission_4_rows = cur.fetchall()
        cur.execute("%s" % mission_5_sql)
        mission_5_rows = cur.fetchall()
        cur.execute("%s" % mission_6_sql)
        mission_6_rows = cur.fetchall()
        cur.execute("%s" % mission_7_sql)
        mission_7_rows = cur.fetchall()
        cur.execute("%s" % mission_8_sql)
        mission_8_rows = cur.fetchall()
        cur.execute("%s" % mission_9_sql)
        mission_9_rows = cur.fetchall()
        cur.execute("%s" % mission_10_sql)
        mission_10_rows = cur.fetchall()
        cur.execute("%s" % mission_11_sql)
        mission_11_rows = cur.fetchall()
        cur.close()

        mission_1_results = processGlobalMission(mission_1_rows, asteroids)
        mission_2_results = processGlobalMission(mission_2_rows, asteroids)
        mission_3_results = processGlobalMission(mission_3_rows, asteroids)
        mission_4_results = processGlobalMission(mission_4_rows, asteroids)
        mission_5_results = processGlobalMission(mission_5_rows, asteroids)
        mission_6_results = processGlobalMission(mission_6_rows, asteroids)
        mission_7_results = processGlobalMission(mission_7_rows, asteroids)
        mission_8_results = processGlobalMission(mission_8_rows, asteroids)
        mission_9_results = processGlobalMission(mission_9_rows, asteroids)
        mission_10_results = processGlobalMission(mission_10_rows, asteroids)
        mission_11_results = processGlobalMission(mission_11_rows, asteroids)

        mission_index = {}
        for asteroid_id in asteroids:
            mission_1_name, mission_1_state, mission_1_wallet = parseMissionState(asteroid_id, mission_1_results)
            mission_2_name, mission_2_state, mission_2_wallet = parseMissionState(asteroid_id, mission_2_results)
            mission_3_name, mission_3_state, mission_3_wallet = parseMissionState(asteroid_id, mission_3_results)
            mission_4_name, mission_4_state, mission_4_wallet = parseMissionState(asteroid_id, mission_4_results)
            mission_5_name, mission_5_state, mission_5_wallet = parseMissionState(asteroid_id, mission_5_results)
            mission_6_name, mission_6_state, mission_6_wallet = parseMissionState(asteroid_id, mission_6_results)
            mission_7_name, mission_7_state, mission_7_wallet = parseMissionState(asteroid_id, mission_7_results)
            mission_8_name, mission_8_state, mission_8_wallet = parseMissionState(asteroid_id, mission_8_results)
            mission_9_name, mission_9_state, mission_9_wallet = parseMissionState(asteroid_id, mission_9_results)
            mission_10_name, mission_10_state, mission_10_wallet = parseMissionState(asteroid_id, mission_10_results)
            mission_11_name, mission_11_state, mission_11_wallet = parseMissionState(asteroid_id, mission_11_results)

            mission_index={asteroid_id: {1: mission_1_wallet, 2: mission_2_wallet, 3: mission_3_wallet, 4: mission_4_wallet, 5: mission_5_wallet, 6: mission_6_wallet, 7: mission_7_wallet, 8: mission_8_wallet, 9: mission_9_wallet, 10: mission_10_wallet, 11: mission_11_wallet}}
            missions.append(mission_index)

    return missions


def parseMissionState(asteroid_id, mission_results):

    mission_name = None
    mission_state = False
    for mission_results in mission_results:
        mission_name = mission_results['name']
        if mission_results['asteroid_id'] == asteroid_id:
            mission_state = mission_results['completed']
            if mission_state is False:
                mission_wallet = None
            else:
                mission_wallet = mission_results['wallet']

    return mission_name, mission_state, mission_wallet


def getMissionSummary(con, wallet):

    missions = []
    asteroids = getAsteroids(con, wallet)
    missions = getColonizationMissions(con, missions, asteroids)

    return missions


def getAsteroids(con, wallet):

    asteroids=[]
    if wallet is not None:
        sql = ("SELECT asteroid_id FROM asteroids WHERE asteroid_owner = '%s' ORDER BY asteroid_id" % wallet)
        print(sql)
    else:
        sql = "SELECT asteroid_id FROM colonization_missions_tracking_1 ORDER BY asteroid_id"
        print(sql)

    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return asteroids

    for row in rows:
        asteroids.append(row[0])

    return asteroids


def processMission(mission_data):

    mission_foo = {}
    for row in mission_data:
        name=row[0]
        wallet=row[1]
        crew_id=row[2]
        timestamp=str(row[3])

    mission_foo = {"name": name, "wallet": wallet, "crew": crew_id, "timestamp": timestamp}
    return mission_foo


def processGlobalMission(mission_data, asteroids):

    mission_foo = []
    for row in mission_data:
        name=row[0]
        asteroid_id=row[1]
        wallet=row[2]
        crew_id=row[3]
        timestamp=str(row[4])
        result=row[5]

        if asteroid_id in asteroids:
            if result == 0:
                completed = False
            else:
                completed = True

            mission_foo.append({"asteroid_id": asteroid_id, "name": name, "completed": completed, "wallet": wallet})

    return mission_foo


def getColonizationMissions(con, missions, asteroids):

    missions = []
    
    for asteroid_id in asteroids:
        mission_1_sql = ("SELECT name, req_1_wallet, req_1_crew_id, req_2_timestamp, req_2 FROM colonization_missions_tracking_1 WHERE asteroid_id = %s" % asteroid_id)
        mission_2_sql = ("SELECT name, req_1_wallet, req_1_crew_id, req_2_timestamp, req_2 FROM colonization_missions_tracking_2 WHERE asteroid_id = %s" % asteroid_id)
        mission_3_sql = ("SELECT name, req_1_wallet, req_1_crew_id, req_2_timestamp, req_2 FROM colonization_missions_tracking_3 WHERE asteroid_id = %s" % asteroid_id)
        mission_4_sql = ("SELECT name, req_1_wallet, req_1_crew_id, req_2_timestamp, req_2 FROM colonization_missions_tracking_4 WHERE asteroid_id = %s" % asteroid_id)
        mission_5_sql = ("SELECT name, req_1_wallet, req_1_crew_id, req_2_timestamp, req_2 FROM colonization_missions_tracking_5 WHERE asteroid_id = %s" % asteroid_id)
        mission_6_sql = ("SELECT name, req_1_wallet, req_1_crew_id, req_2_timestamp, req_2 FROM colonization_missions_tracking_6 WHERE asteroid_id = %s" % asteroid_id)
        mission_7_sql = ("SELECT name, req_1_wallet, req_1_crew_id, req_2_timestamp, req_2 FROM colonization_missions_tracking_7 WHERE asteroid_id = %s" % asteroid_id)
        mission_8_sql = ("SELECT name, req_1_wallet, req_1_crew_id, req_2_timestamp, req_2 FROM colonization_missions_tracking_8 WHERE asteroid_id = %s" % asteroid_id)
        mission_9_sql = ("SELECT name, req_1_wallet, req_1_crew_id, req_2_timestamp, req_2 FROM colonization_missions_tracking_9 WHERE asteroid_id = %s" % asteroid_id)
        mission_10_sql = ("SELECT name, req_1_wallet, req_1_crew_id, req_2_timestamp, req_2 FROM colonization_missions_tracking_10 WHERE asteroid_id = %s" % asteroid_id)
        mission_11_sql = ("SELECT name, req_1_wallet, req_1_crew_id, req_1_timestamp, req_1 FROM colonization_missions_tracking_11 WHERE asteroid_id = %s" % asteroid_id)

        with con:
            cur = con.cursor()
            cur.execute("%s" % mission_1_sql)
            mission_1_rows = cur.fetchall()
            cur.execute("%s" % mission_2_sql)
            mission_2_rows = cur.fetchall()
            cur.execute("%s" % mission_3_sql)
            mission_3_rows = cur.fetchall()
            cur.execute("%s" % mission_4_sql)
            mission_4_rows = cur.fetchall()
            cur.execute("%s" % mission_5_sql)
            mission_5_rows = cur.fetchall()
            cur.execute("%s" % mission_6_sql)
            mission_6_rows = cur.fetchall()
            cur.execute("%s" % mission_7_sql)
            mission_7_rows = cur.fetchall()
            cur.execute("%s" % mission_8_sql)
            mission_8_rows = cur.fetchall()
            cur.execute("%s" % mission_9_sql)
            mission_9_rows = cur.fetchall()
            cur.execute("%s" % mission_10_sql)
            mission_10_rows = cur.fetchall()
            cur.execute("%s" % mission_11_sql)
            mission_11_rows = cur.fetchall()
            cur.close()

        mission_1_results = processMission(mission_1_rows)
        mission_2_results = processMission(mission_2_rows)
        mission_3_results = processMission(mission_3_rows)
        mission_4_results = processMission(mission_4_rows)
        mission_5_results = processMission(mission_5_rows)
        mission_6_results = processMission(mission_6_rows)
        mission_7_results = processMission(mission_7_rows)
        mission_8_results = processMission(mission_8_rows)
        mission_9_results = processMission(mission_9_rows)
        mission_10_results = processMission(mission_10_rows)
        mission_11_results = processMission(mission_11_rows)

        missions.append({"asteroid_id": asteroid_id, "mission_1": mission_1_results, "mission_2": mission_2_results, "mission_3": mission_3_results, "mission_4": mission_4_results, "mission_5": mission_5_results, "mission_6": mission_6_results, "mission_7": mission_7_results, "mission_8": mission_8_results, "mission_9": mission_9_results, "mission_10": mission_10_results, "mission_11": mission_11_results})

    return missions


def getCrewParticipation(con, wallet, mission_id):

    if mission_id == 1:
        wallet_amount_col = "mission_1_wallet_amount"
        wallet_status_col = "mission_1_wallet_status"
    elif mission_id == 2:
        wallet_amount_col = "mission_2_wallet_amount"
        wallet_status_col = "mission_2_wallet_status"
    elif mission_id == 3:
        wallet_amount_col = "mission_3_wallet_amount"
        wallet_status_col = "mission_3_wallet_status"
    elif mission_id == 4:
        wallet_amount_col = "mission_4_wallet_amount"
        wallet_status_col = "mission_4_wallet_status"
    elif mission_id == 5:
        wallet_amount_col = "mission_5_wallet_amount"
        wallet_status_col = "mission_5_wallet_status"
    elif mission_id == 6:
        wallet_amount_col = "mission_6_wallet_amount"
        wallet_status_col = "mission_6_wallet_status"
    elif mission_id == 7:
        wallet_amount_col = "mission_7_wallet_amount"
        wallet_status_col = "mission_7_wallet_status"
    elif mission_id == 8:
        wallet_amount_col = "mission_8_wallet_amount"
        wallet_status_col = "mission_8_wallet_status"

    crews = []
    sql = ("SELECT crew_id, %s FROM community_missions_tracking WHERE %s = 1 AND wallet = '%s'" % (wallet_amount_col, wallet_status_col, wallet))

    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    for row in rows:
        crew_id=row[0]
        wallet_amount=row[1]
        crews.append(crew_id)

    return crews


def colonizationMissionsSummary(wallet):

    result = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    wallet = fix_address.padAddress(wallet)
    result = getMissionSummary(con, wallet)
    con.close()
    return result


def colonizationGlobalReport():

    result = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    result = getGlobalReport(con)
    con.close()
    return result


def colonizationAsteroidStatus(asteroid_id):

    result = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    result = getAsteroidStatus(con, asteroid_id)
    con.close()
    return result
