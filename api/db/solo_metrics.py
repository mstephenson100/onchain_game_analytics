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
    crews = getOwnedCrew(con, wallet)
    if len(crews) == 0:
        missions = getSummary(con)
    else:
        missions = getSoloMissions(con, crews)

    return missions


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
        mission_6_req_1_description="Purchase or construct at least one ship"
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

        missions.append({"crew_id": None, "name": None, "mission_1": mission_1, "mission_2": mission_2, "mission_3": mission_3, "mission_4": mission_4, "mission_5": mission_5, "mission_6": mission_6, "mission_7": mission_7, "mission_8": mission_8, "mission_9": mission_9})

        return missions


def getSoloMissions(con, crews):

    crew_list = []
    missions = []
    for crew_row in crews:
        crew_list.append(crew_row['crew_id'])

    str_crew_list = str(crew_list)
    str_crew_list = str_crew_list.replace('[', '(').replace(']', ')')
    
    sql = ("SELECT crew_id, mission_1_name, mission_1_req_1_goal, mission_1_req_1, mission_1_req_2_goal, mission_1_req_2, mission_2_name, mission_2_req_1_goal, mission_2_req_1, mission_2_req_2_goal, mission_2_req_2, mission_3_name, mission_3_req_1_goal, mission_3_req_1, mission_3_req_2_goal, mission_3_req_2, mission_4_name, mission_4_req_1_goal, mission_4_req_1, mission_4_req_2_goal, mission_4_req_2, mission_5_name, mission_5_req_1_goal, mission_5_req_1, mission_6_name, mission_6_req_1_goal, mission_6_req_1, mission_6_req_2_goal, mission_6_req_2, mission_7_name, mission_7_req_1_goal, mission_7_req_1, mission_8_name, mission_8_req_1_goal, mission_8_req_1, mission_9_name, mission_9_req_1_goal, mission_9_req_1 FROM solo_missions_tracking WHERE crew_id in %s" % str_crew_list)
    print(sql)

    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return crew

    for row in rows:
        crew_id=row[0]
        mission_1_name=row[1]
        mission_1_req_1_description="Recruit five crewmates"
        mission_1_req_1_goal=row[2]
        mission_1_req_1_actual=row[3]
        mission_1_req_2_description="Recruit at least two different classes of crewmate"
        mission_1_req_2_goal=row[4]
        mission_1_req_2_actual=row[5]
        mission_1 = {"name": mission_1_name, "Requirement 1": mission_1_req_1_description, "Requirement 1 Goal": mission_1_req_1_goal, "Requirement 1 Actual": mission_1_req_1_actual, "Requirement 2": mission_1_req_2_description, "Requirement 2 Goal": mission_1_req_2_goal, "Requirement 2 Actual": mission_1_req_2_actual}

        mission_2_name=row[6]
        mission_2_req_1_description="Puchase or manufacture at least five core drills"
        mission_2_req_1_goal=row[7]
        mission_2_req_1_actual=row[8]
        mission_2_req_2_description="Take core samples of at least five different raw materials"
        mission_2_req_2_goal=row[9]
        mission_2_req_2_actual=row[10]
        mission_2 = {"name": mission_2_name, "Requirement 1": mission_2_req_1_description, "Requirement 1 Goal": mission_2_req_1_goal, "Requirement 1 Actual": mission_2_req_1_actual, "Requirement 2": mission_2_req_2_description, "Requirement 2 Goal": mission_2_req_2_goal, "Requirement 2 Actual": mission_2_req_2_actual}

        mission_3_name=row[11]
        mission_3_req_1_description="Place at least three market buy and three market sell orders"
        mission_3_req_1_goal=row[12]
        mission_3_req_1_actual=row[13]
        mission_3_req_2_description="Place at least three limit buy and three limit sell orders"
        mission_3_req_2_goal=row[14]
        mission_3_req_2_actual=row[15]
        mission_3 = {"name": mission_3_name, "Requirement 1": mission_3_req_1_description, "Requirement 1 Goal": mission_3_req_1_goal, "Requirement 1 Actual": mission_3_req_1_actual, "Requirement 2": mission_3_req_2_description, "Requirement 2 Goal": mission_3_req_2_goal, "Requirement 2 Actual": mission_3_req_2_actual}

        mission_4_name=row[16]
        mission_4_req_1_description="Mine at least 10k tonnes of any raw materials"
        mission_4_req_1_goal=row[17]
        mission_4_req_1_actual=row[18]
        mission_4_req_2_description="Mine at least 4 different types of raw material"
        mission_4_req_2_goal=row[19]
        mission_4_req_2_actual=row[20]
        mission_4 = {"name": mission_4_name, "Requirement 1": mission_4_req_1_description, "Requirement 1 Goal": mission_4_req_1_goal, "Requirement 1 Actual": mission_4_req_1_actual, "Requirement 2": mission_4_req_2_description, "Requirement 2 Goal": mission_4_req_2_goal, "Requirement 2 Actual": mission_4_req_2_actual}

        mission_5_name=row[21]
        mission_5_req_1_description="Build at least five buildings that are not warehouses or extractors"
        mission_5_req_1_goal=row[22]
        mission_5_req_1_actual=row[23]
        mission_5 = {"name": mission_5_name, "Requirement 1": mission_5_req_1_description, "Requirement 1 Goal": mission_5_req_1_goal, "Requirement 1 Actual": mission_5_req_1_actual}

        mission_6_name=row[24]
        mission_6_req_1_description="Purchase or construct at least one ship"
        mission_6_req_1_goal=row[25]
        mission_6_req_1_actual=row[26]
        mission_6_req_2_description="Arrive in orbit around any asteroid other than Adalia Prime as the commanding crew of a ship"
        mission_6_req_2_goal=row[27]
        mission_6_req_2_actual=row[28]
        mission_6 = {"name": mission_6_name, "Requirement 1": mission_6_req_1_description, "Requirement 1 Goal": mission_6_req_1_goal, "Requirement 1 Actual": mission_6_req_1_actual, "Requirement 2": mission_6_req_2_description, "Requirement 2 Goal": mission_6_req_2_goal, "Requirement 2 Actual": mission_6_req_2_actual}

        mission_7_name=row[29]
        mission_7_req_1_description="Build at least one building on an asteroid other than Adalia Prime"
        mission_7_req_1_goal=row[30]
        mission_7_req_1_actual=row[31]
        mission_7 = {"name": mission_7_name, "Requirement 1": mission_7_req_1_description, "Requirement 1 Goal": mission_7_req_1_goal, "Requirement 1 Actual": mission_7_req_1_actual}

        mission_8_name=row[32]
        mission_8_req_1_description="Arrive in orbit around any asteroid as the commanding crew of a ship whose cargo hold contains at least 1000 tonnes of goods of any type"
        mission_8_req_1_goal=row[33]
        mission_8_req_1_actual=row[34]
        mission_8 = {"name": mission_8_name, "Requirement 1": mission_8_req_1_description, "Requirement 1 Goal": mission_8_req_1_goal, "Requirement 1 Actual": mission_8_req_1_actual}

        mission_9_name=row[35]
        mission_9_req_1_description="Feed your crew a total of at least 10 tonnes of food"
        mission_9_req_1_goal=row[36]
        mission_9_req_1_actual=row[37]
        mission_9 = {"name": mission_9_name, "Requirement 1": mission_9_req_1_description, "Requirement 1 Goal": mission_9_req_1_goal, "Requirement 1 Actual": mission_9_req_1_actual}

        for name_row in crews:
            if name_row['crew_id'] == crew_id:
                crew_name = name_row['crew_name']

        #missions.append({"crew_id": crew_id, "mission_1_name": mission_1_name, "mission_1_req_1_description": mission_1_req_1_description, "mission_1_req_1_goal": mission_1_req_1_goal, "mission_1_req_1_actual": mission_1_req_1_actual, "mission_1_req_2_description": mission_1_req_2_description, "mission_1_req_2_goal": mission_1_req_2_goal, "mission_1_req_2_actual": mission_1_req_2_actual, "mission_2_name": mission_2_name, "mission_2_req_1_description": mission_2_req_1_description, "mission_2_req_1_goal": mission_2_req_1_goal, "mission_2_req_1_actual": mission_2_req_1_actual, "mission_2_req_2_description": mission_2_req_2_description, "mission_2_req_2_goal": mission_2_req_2_goal, "mission_2_req_2_actual": mission_2_req_2_actual, "mission_3_name": mission_3_name, "mission_3_req_1_description": mission_3_req_1_description, "mission_3_req_1_goal": mission_3_req_1_goal, "mission_3_req_1_actual": mission_3_req_1_actual, "mission_3_req_2_description": mission_3_req_2_description, "mission_3_req_2_goal": mission_3_req_2_goal, "mission_3_req_2_actual": mission_3_req_2_actual, "mission_4_name": mission_4_name, "mission_4_name": mission_4_name, "mission_4_req_1_goal": mission_4_req_1_goal, "mission_4_req_1_actual": mission_4_req_1_actual, "mission_4_req_2_description": mission_4_req_2_description, "mission_4_req_2_goal": mission_4_req_2_goal, "mission_4_req_2_actual": mission_4_req_2_actual, "mission_5_name": mission_5_name, "mission_5_req_1_description": mission_5_req_1_description, "mission_5_req_1_goal": mission_5_req_1_goal, "mission_5_req_1_actual": mission_5_req_1_actual, "mission_6_name": mission_6_name, "mission_6_req_1_description": mission_6_req_1_description, "mission_6_req_1_goal": mission_6_req_1_goal, "mission_6_req_1_actual": mission_6_req_1_actual, "mission_6_req_2_description": mission_6_req_2_description, "mission_6_req_2_goal": mission_6_req_2_goal, "mission_6_req_2_actual": mission_6_req_2_actual, "mission_7_name": mission_7_name, "mission_7_req_1_description": mission_7_req_1_description, "mission_7_req_1_goal": mission_7_req_1_goal, "mission_7_req_1_actual": mission_7_req_1_actual, "mission_8_name": mission_8_name, "mission_8_req_1_description": mission_8_req_1_description, "mission_8_req_1_goal": mission_8_req_1_goal, "mission_8_req_1_actual": mission_8_req_1_actual, "mission_9_name": mission_9_name, "mission_9_req_1_description": mission_9_req_1_description, "mission_9_req_1_goal": mission_9_req_1_goal, "mission_9_req_1_actual": mission_9_req_1_actual})
        missions.append({"crew_id": crew_id, "name": crew_name, "mission_1": mission_1, "mission_2": mission_2, "mission_3": mission_3, "mission_4": mission_4, "mission_5": mission_5, "mission_6": mission_6, "mission_7": mission_7, "mission_8": mission_8, "mission_9": mission_9})

    return missions


def getOwnedCrew(con, wallet):

    crew=[]
    sql = ("SELECT crew_id, name FROM crews WHERE crew_owner = '%s'" % (wallet))
    print(sql)

    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return crew

    for row in rows:
        crew_id=row[0]
        crew_name=row[1]
        crew.append({"crew_id": crew_id, "crew_name": crew_name})

    return crew


def soloMissionsSummary(wallet):

    result = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    wallet = fix_address.padAddress(wallet)
    result = getMissionSummary(con, wallet)
    con.close()
    return result

