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


def getMissionSummary(con, wallet):

    crews = []
    missions = []
    summary = getSummary(con)
    missions = getSoloMissions(con, wallet, summary)

    return missions


def getMissionResultsReq1(con, sql):

    crews = []
    mission_name = None
    mission_req_1_goal = None
    mission_req_1_actual = None

    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if len(rows) == 0:
        return crews, mission_name, mission_req_1_goal, mission_req_1_actual

    for row in rows:
        crew_id=row[0]
        mission_name=row[1]
        mission_req_1_goal=row[2]
        mission_req_1_actual=row[3]
        if crew_id not in crews:
            crews.append(crew_id)

    return crews, mission_name, mission_req_1_goal, mission_req_1_actual


def verifyDataReq1(mission_identifier, mission_name, mission_req_1_goal, mission_req_1_actual, summary):

    mission_name = summary[mission_identifier]['name']
    mission_req_1_goal = summary[mission_identifier]['Requirement 1 Goal']
    mission_req_1_actual = 0
    return mission_name, mission_req_1_goal, mission_req_1_actual


def verifyDataReq2(mission_identifier, mission_name, mission_req_1_goal, mission_req_1_actual, mission_req_2_goal, mission_req_2_actual, summary):

    mission_name = summary[mission_identifier]['name']
    mission_req_1_goal = summary[mission_identifier]['Requirement 1 Goal']
    mission_req_1_actual = 0
    mission_req_2_goal = summary[mission_identifier]['Requirement 2 Goal']
    mission_req_2_actual = 0
    return mission_name, mission_req_1_goal, mission_req_1_actual, mission_req_2_goal, mission_req_2_actual


def getMissionResultsReq2(con, sql):

    #print(sql)
    crews = []
    mission_name = None
    mission_req_1_goal = None
    mission_req_1_actual = None
    mission_req_2_goal = None
    mission_req_2_actual = None

    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if len(rows) == 0:
        return crews, mission_name, mission_req_1_goal, mission_req_1_actual, mission_req_2_goal, mission_req_2_actual

    for row in rows:
        crew_id=row[0]
        mission_name=row[1]
        mission_req_1_goal=row[2]
        mission_req_1_actual=row[3]
        mission_req_2_goal=row[4]
        mission_req_2_actual=row[5]
        if crew_id not in crews:
            crews.append(crew_id)

    return crews, mission_name, mission_req_1_goal, mission_req_1_actual, mission_req_2_goal, mission_req_2_actual


def getSummary(con):


    missions = []
    sql = "SELECT mission_1_name, mission_1_req_1_goal, 0, mission_1_req_2_goal, 0, mission_2_name, mission_2_req_1_goal, 0, mission_2_req_2_goal, 0, mission_3_name, mission_3_req_1_goal, 0, mission_3_req_2_goal, 0, mission_4_name, mission_4_req_1_goal, 0, mission_4_req_2_goal, 0, mission_5_name, mission_5_req_1_goal, 0, mission_6_name, mission_6_req_1_goal, 0, mission_6_req_2_goal, 0, mission_7_name, mission_7_req_1_goal, 0, mission_8_name, mission_8_req_1_goal, 0, mission_9_name, mission_9_req_1_goal, 0 FROM solo_missions_tracking LIMIT 1"

    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    for row in rows:
        mission_1_name=row[0]
        mission_1_req_1_description="Recruit five crewmates"
        mission_1_req_1_goal=row[1]
        mission_1_req_1_actual=row[2]
        mission_1_req_2_description="Recruit at least two different classes of crewmate"
        mission_1_req_2_goal=row[3]
        mission_1_req_2_actual=row[4]
        mission_2_name=row[5]
        mission_2_req_1_description="Puchase or manufacture at least five core drills"
        mission_2_req_1_goal=row[6]
        mission_2_req_1_actual=row[7]
        mission_2_req_2_description="Take core samples of at least five different raw materials"
        mission_2_req_2_goal=row[8]
        mission_2_req_2_actual=row[9]
        mission_3_name=row[10]
        mission_3_req_1_description="Place at least three market buy and three market sell orders"
        mission_3_req_1_goal=row[11]
        mission_3_req_1_actual=row[12]
        mission_3_req_2_description="Place at least three limit buy and three limit sell orders"
        mission_3_req_2_goal=row[13]
        mission_3_req_2_actual=row[14]
        mission_4_name=row[15]
        mission_4_req_1_description="Mine at least 10k tonnes of any raw materials"
        mission_4_req_1_goal=row[16]
        mission_4_req_1_actual=row[17]
        mission_4_req_2_description="Mine at least 4 different types of raw material"
        mission_4_req_2_goal=row[18]
        mission_4_req_2_actual=row[19]
        mission_5_name=row[20]
        mission_5_req_1_description="Build at least five buildings that are not warehouses or extractors"
        mission_5_req_1_goal=row[21]
        mission_5_req_1_actual=row[22]
        mission_6_name=row[23]
        mission_6_req_1_description="Construct at least one ship"
        mission_6_req_1_goal=row[24]
        mission_6_req_1_actual=row[25]
        mission_6_req_2_description="Arrive in orbit around any asteroid other than Adalia Prime as the commanding crew of a ship"
        mission_6_req_2_goal=row[26]
        mission_6_req_2_actual=row[27]
        mission_7_name=row[28]
        mission_7_req_1_description="Build at least one building on an asteroid other than Adalia Prime"
        mission_7_req_1_goal=row[29]
        mission_7_req_1_actual=row[30]
        mission_8_name=row[31]
        mission_8_req_1_description="Arrive in orbit around any asteroid as the commanding crew of a ship whose cargo hold contains at least 1000 tonnes of goods of any type"
        mission_8_req_1_goal=row[32]
        mission_8_req_1_actual=row[33]
        mission_9_name=row[34]
        mission_9_req_1_description="Feed your crew a total of at least 10 tonnes of food"
        mission_9_req_1_goal=row[35]
        mission_9_req_1_actual=row[36]

        mission_1 = {"name": mission_1_name, "Requirement 1": mission_1_req_1_description, "Requirement 1 Goal": mission_1_req_1_goal, "Requirement 1 Actual": mission_1_req_1_actual, "Requirement 2": mission_1_req_2_description, "Requirement 2 Goal": mission_1_req_2_goal, "Requirement 2 Actual": mission_1_req_2_actual}
        mission_2 = {"name": mission_2_name, "Requirement 1": mission_2_req_1_description, "Requirement 1 Goal": mission_2_req_1_goal, "Requirement 1 Actual": mission_2_req_1_actual, "Requirement 2": mission_2_req_2_description, "Requirement 2 Goal": mission_2_req_2_goal, "Requirement 2 Actual": mission_2_req_2_actual}
        mission_3 = {"name": mission_3_name, "Requirement 1": mission_3_req_1_description, "Requirement 1 Goal": mission_3_req_1_goal, "Requirement 1 Actual": mission_3_req_1_actual, "Requirement 2": mission_3_req_2_description, "Requirement 2 Goal": mission_3_req_2_goal, "Requirement 3 Actual": mission_3_req_2_actual}
        mission_4 = {"name": mission_4_name, "Requirement 1": mission_4_req_1_description, "Requirement 1 Goal": mission_4_req_1_goal, "Requirement 1 Actual": mission_4_req_1_actual, "Requirement 2": mission_4_req_2_description, "Requirement 2 Goal": mission_4_req_2_goal, "Requirement 4 Actual": mission_4_req_2_actual}
        mission_5 = {"name": mission_5_name, "Requirement 1": mission_5_req_1_description, "Requirement 1 Goal": mission_5_req_1_goal, "Requirement 1 Actual": mission_5_req_1_actual}
        mission_6 = {"name": mission_6_name, "Requirement 1": mission_6_req_1_description, "Requirement 1 Goal": mission_6_req_1_goal, "Requirement 1 Actual": mission_6_req_1_actual, "Requirement 2": mission_6_req_2_description, "Requirement 2 Goal": mission_6_req_2_goal, "Requirement 4 Actual": mission_6_req_2_actual}
        mission_7 = {"name": mission_7_name, "Requirement 1": mission_7_req_1_description, "Requirement 1 Goal": mission_7_req_1_goal, "Requirement 1 Actual": mission_7_req_1_actual}
        mission_8 = {"name": mission_8_name, "Requirement 1": mission_8_req_1_description, "Requirement 1 Goal": mission_8_req_1_goal, "Requirement 1 Actual": mission_8_req_1_actual}
        mission_9 = {"name": mission_9_name, "Requirement 1": mission_9_req_1_description, "Requirement 1 Goal": mission_9_req_1_goal, "Requirement 1 Actual": mission_9_req_1_actual}
        missions = {"mission_1": mission_1, "mission_2": mission_2, "mission_3": mission_3, "mission_4": mission_4, "mission_5": mission_5, "mission_6": mission_6, "mission_7": mission_7, "mission_8": mission_8, "mission_9": mission_9}

        return missions


def getSoloMissions(con, wallet, summary):

    missions = []
    mission_1_req_1_sql = ("SELECT crew_id, mission_1_name, mission_1_req_1_goal, mission_1_req_1 FROM solo_missions_tracking WHERE (mission_1_req_1_goal = mission_1_req_1) AND wallet = '%s'" % wallet)
    mission_1_req_2_sql = ("SELECT crew_id, mission_1_name, mission_1_req_2_goal, mission_1_req_2 FROM solo_missions_tracking WHERE (mission_1_req_2_goal = mission_1_req_2) AND wallet = '%s'" % wallet)
    mission_1_req_1_description="Recruit five crewmates"
    mission_1_req_2_description="Recruit at least two different classes of crewmate"
    mission_1_req_1_crews, mission_1_name, mission_1_req_1_goal, mission_1_req_1_actual = getMissionResultsReq1(con, mission_1_req_1_sql)
    mission_1_req_2_crews, mission_1_name, mission_1_req_2_goal, mission_1_req_2_actual = getMissionResultsReq1(con, mission_1_req_2_sql)
    mission_1_name, mission_1_req_1_goal, mission_1_req_1_actual = verifyDataReq1("mission_1", mission_1_name, mission_1_req_1_goal, mission_1_req_1_actual, summary)
    mission_1_name, mission_1_req_2_goal, mission_1_req_2_actual = verifyDataReq1("mission_1", mission_1_name, mission_1_req_1_goal, mission_1_req_1_actual, summary)
    mission_1_results = {"mission_id": 1, "mission_name": mission_1_name, "requirement_1": mission_1_req_1_description, "requirement_1_crews": mission_1_req_1_crews, "requirement_2": mission_1_req_2_description, "requirement_2_crews": mission_1_req_2_crews}

    mission_2_req_1_sql = ("SELECT crew_id, mission_2_name, mission_2_req_1_goal, mission_2_req_1 FROM solo_missions_tracking WHERE (mission_2_req_1_goal = mission_2_req_1) AND wallet = '%s'" % wallet)
    mission_2_req_2_sql = ("SELECT crew_id, mission_2_name, mission_2_req_2_goal, mission_2_req_2 FROM solo_missions_tracking WHERE (mission_2_req_2_goal = mission_2_req_2) AND wallet = '%s'" % wallet)
    mission_2_req_1_description="Puchase or manufacture at least five core drills"
    mission_2_req_2_description="Take core samples of at least five different raw materials"
    mission_2_req_1_crews, mission_2_name, mission_2_req_1_goal, mission_2_req_1_actual = getMissionResultsReq1(con, mission_2_req_1_sql)
    mission_2_req_2_crews, mission_2_name, mission_2_req_2_goal, mission_2_req_2_actual = getMissionResultsReq1(con, mission_2_req_2_sql)
    mission_2_name, mission_2_req_1_goal, mission_2_req_1_actual = verifyDataReq1("mission_2", mission_2_name, mission_2_req_1_goal, mission_2_req_1_actual, summary)
    mission_2_name, mission_2_req_2_goal, mission_2_req_2_actual = verifyDataReq1("mission_2", mission_2_name, mission_2_req_1_goal, mission_2_req_1_actual, summary)
    mission_2_results = {"mission_id": 2, "mission_name": mission_2_name, "requirement_1": mission_2_req_1_description, "requirement_1_crews": mission_2_req_1_crews, "requirement_2": mission_2_req_2_description, "requirement_2_crews": mission_2_req_2_crews}

    mission_3_req_1_sql = ("SELECT crew_id, mission_3_name, mission_3_req_1_goal, mission_3_req_1 FROM solo_missions_tracking WHERE (mission_3_req_1_goal = mission_3_req_1) AND wallet = '%s'" % wallet)
    mission_3_req_2_sql = ("SELECT crew_id, mission_3_name, mission_3_req_2_goal, mission_3_req_2 FROM solo_missions_tracking WHERE (mission_3_req_2_goal = mission_3_req_2) AND wallet = '%s'" % wallet)
    mission_3_req_1_description="Place at least three market buy and three market sell orders"
    mission_3_req_2_description="Place at least three limit buy and three limit sell orders"
    mission_3_req_1_crews, mission_3_name, mission_3_req_1_goal, mission_3_req_1_actual = getMissionResultsReq1(con, mission_3_req_1_sql)
    mission_3_req_2_crews, mission_3_name, mission_3_req_2_goal, mission_3_req_2_actual = getMissionResultsReq1(con, mission_3_req_2_sql)
    mission_3_name, mission_3_req_1_goal, mission_3_req_1_actual = verifyDataReq1("mission_3", mission_3_name, mission_3_req_1_goal, mission_3_req_1_actual, summary)
    mission_3_name, mission_3_req_2_goal, mission_3_req_2_actual = verifyDataReq1("mission_3", mission_3_name, mission_3_req_1_goal, mission_3_req_1_actual, summary)
    mission_3_results = {"mission_id": 3, "mission_name": mission_3_name, "requirement_1": mission_3_req_1_description, "requirement_1_crews": mission_3_req_1_crews, "requirement_2": mission_3_req_2_description, "requirement_2_crews": mission_3_req_2_crews}

    mission_4_req_1_sql = ("SELECT crew_id, mission_4_name, mission_4_req_1_goal, mission_4_req_1 FROM solo_missions_tracking WHERE (mission_4_req_1_goal = mission_4_req_1) AND wallet = '%s'" % wallet)
    mission_4_req_2_sql = ("SELECT crew_id, mission_4_name, mission_4_req_2_goal, mission_4_req_2 FROM solo_missions_tracking WHERE (mission_4_req_2_goal = mission_4_req_2) AND wallet = '%s'" % wallet)
    mission_4_req_1_description="Mine at least 10k tonnes of any raw materials"
    mission_4_req_2_description="Mine at least 4 different types of raw material"
    mission_4_req_1_crews, mission_4_name, mission_4_req_1_goal, mission_4_req_1_actual = getMissionResultsReq1(con, mission_4_req_1_sql)
    mission_4_req_2_crews, mission_4_name, mission_4_req_2_goal, mission_4_req_2_actual = getMissionResultsReq1(con, mission_4_req_2_sql)
    mission_4_name, mission_4_req_1_goal, mission_4_req_1_actual = verifyDataReq1("mission_4", mission_4_name, mission_4_req_1_goal, mission_4_req_1_actual, summary)
    mission_4_name, mission_4_req_2_goal, mission_4_req_2_actual = verifyDataReq1("mission_4", mission_4_name, mission_4_req_1_goal, mission_4_req_1_actual, summary)
    mission_4_results = {"mission_id": 4, "mission_name": mission_4_name, "requirement_1": mission_4_req_1_description, "requirement_1_crews": mission_4_req_1_crews, "requirement_2": mission_4_req_2_description, "requirement_2_crews": mission_4_req_2_crews}

    mission_5_req_1_sql = ("SELECT crew_id, mission_5_name, mission_5_req_1_goal, mission_5_req_1 FROM solo_missions_tracking WHERE (mission_5_req_1_goal = mission_5_req_1) AND wallet = '%s'" % wallet)
    mission_5_req_1_description="Build at least five buildings that are not warehouses or extractors"
    mission_5_req_1_crews, mission_5_name, mission_5_req_1_goal, mission_5_req_1_actual = getMissionResultsReq1(con, mission_5_req_1_sql)
    mission_5_name, mission_5_req_1_goal, mission_5_req_1_actual = verifyDataReq1("mission_5", mission_5_name, mission_5_req_1_goal, mission_5_req_1_actual, summary)
    mission_5_results = {"mission_id": 5, "mission_name": mission_5_name, "requirement_1": mission_5_req_1_description, "requirement_1_crews": mission_5_req_1_crews}


    mission_6_sql = ("SELECT crew_id, mission_6_name, mission_6_req_1_goal, mission_6_req_1, mission_6_req_2_goal, mission_6_req_2 FROM solo_missions_tracking WHERE ((mission_6_req_1_goal = mission_6_req_1) OR (mission_6_req_2_goal = mission_6_req_2)) AND wallet = '%s'" % wallet)
    mission_6_req_1_sql = ("SELECT crew_id, mission_6_name, mission_6_req_1_goal, mission_6_req_1 FROM solo_missions_tracking WHERE (mission_6_req_1_goal = mission_6_req_1) AND wallet = '%s'" % wallet)
    mission_6_req_2_sql = ("SELECT crew_id, mission_6_name, mission_6_req_2_goal, mission_6_req_2 FROM solo_missions_tracking WHERE (mission_6_req_2_goal = mission_6_req_2) AND wallet = '%s'" % wallet)
    mission_6_req_1_description="Construct at least one ship"
    mission_6_req_2_description="Arrive in orbit around any asteroid other than Adalia Prime as the commanding crew of a ship"
    mission_6_req_1_crews, mission_6_name, mission_6_req_1_goal, mission_6_req_1_actual = getMissionResultsReq1(con, mission_6_req_1_sql)
    mission_6_req_2_crews, mission_6_name, mission_6_req_2_goal, mission_6_req_2_actual = getMissionResultsReq1(con, mission_6_req_2_sql)
    mission_6_name, mission_6_req_1_goal, mission_6_req_1_actual = verifyDataReq1("mission_6", mission_6_name, mission_6_req_1_goal, mission_6_req_1_actual, summary)
    mission_6_name, mission_6_req_2_goal, mission_6_req_2_actual = verifyDataReq1("mission_6", mission_6_name, mission_6_req_1_goal, mission_6_req_1_actual, summary)
    mission_6_results = {"mission_id": 6, "mission_name": mission_6_name, "requirement_1": mission_6_req_1_description, "requirement_1_crews": mission_6_req_1_crews, "requirement_2": mission_6_req_2_description, "requirement_2_crews": mission_6_req_2_crews}

    mission_7_req_1_sql = ("SELECT crew_id, mission_7_name, mission_7_req_1_goal, mission_7_req_1 FROM solo_missions_tracking WHERE (mission_7_req_1_goal = mission_7_req_1) AND wallet = '%s'" % wallet)
    mission_7_req_1_description="Build at least one building on an asteroid other than Adalia Prime"
    mission_7_req_1_crews, mission_7_name, mission_7_req_1_goal, mission_7_req_1_actual = getMissionResultsReq1(con, mission_7_req_1_sql)
    mission_7_name, mission_7_req_1_goal, mission_7_req_1_actual = verifyDataReq1("mission_7", mission_7_name, mission_7_req_1_goal, mission_7_req_1_actual, summary)
    mission_7_results = {"mission_id": 7, "mission_name": mission_7_name, "requirement_1": mission_7_req_1_description, "requirement_1_crews": mission_7_req_1_crews}

    mission_8_req_1_sql = ("SELECT crew_id, mission_8_name, mission_8_req_1_goal, mission_8_req_1 FROM solo_missions_tracking WHERE (mission_8_req_1_goal = mission_8_req_1) AND wallet = '%s'" % wallet)
    mission_8_req_1_description="Arrive in orbit around any asteroid as the commanding crew of a ship whose cargo hold contains at least 1000 tonnes of goods of any type"
    mission_8_req_1_crews, mission_8_name, mission_8_req_1_goal, mission_8_req_1_actual = getMissionResultsReq1(con, mission_8_req_1_sql)
    mission_8_name, mission_8_req_1_goal, mission_8_req_1_actual = verifyDataReq1("mission_8", mission_8_name, mission_8_req_1_goal, mission_8_req_1_actual, summary)
    mission_8_results = {"mission_id": 8, "mission_name": mission_8_name, "requirement_1": mission_8_req_1_description, "requirement_1_crews": mission_8_req_1_crews}

    mission_9_req_1_sql = ("SELECT crew_id, mission_9_name, mission_9_req_1_goal, mission_9_req_1 FROM solo_missions_tracking WHERE (mission_9_req_1_goal = mission_9_req_1) AND wallet = '%s'" % wallet)
    mission_9_req_1_description="Feed your crew a total of at least 10 tonnes of food"
    mission_9_req_1_crews, mission_9_name, mission_9_req_1_goal, mission_9_req_1_actual = getMissionResultsReq1(con, mission_9_req_1_sql)
    mission_9_name, mission_9_req_1_goal, mission_9_req_1_actual = verifyDataReq1("mission_9", mission_9_name, mission_9_req_1_goal, mission_9_req_1_actual, summary)
    mission_9_results = {"mission_id": 9, "mission_name": mission_9_name, "requirement_1": mission_9_req_1_description, "requirement_1_crews": mission_9_req_1_crews}

    missions = {"mission_1": mission_1_results, "mission_2": mission_2_results, "mission_3": mission_3_results, "mission_4": mission_4_results, "mission_5": mission_5_results, "mission_6": mission_6_results, "mission_7": mission_7_results, "mission_8": mission_8_results, "mission_9": mission_9_results}

    return missions
    

def soloMissionsSummary(wallet):

    result = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    wallet = fix_address.padAddress(wallet)
    result = getMissionSummary(con, wallet)
    con.close()
    return result

