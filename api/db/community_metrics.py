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

    missions = []
    missions = getCommunityMissions(con, missions, wallet)

    return missions



def getCommunityMissions(con, missions, wallet):

    missions = []
    sql = "SELECT mission_id, mission_name, mission_required, mission_cap, mission_actual, mission_crews, mission_description FROM community_missions_summary"

    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    for row in rows:
        mission_id=row[0]
        mission_name=row[1]
        mission_required=row[2]
        mission_cap=row[3]
        mission_actual=row[4]
        mission_crews=row[5]
        mission_description=row[6]
        crews = getCrewParticipation(con, wallet, mission_id)
        missions.append({"mission_id": mission_id, "mission_name": mission_name, "mission_required": mission_required, "mission_cap": mission_cap, "mission_actual": mission_actual, "mission_crews": mission_crews, "crews": crews, "mission_description": mission_description})

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


def communityMissionsSummary(wallet):

    result = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    wallet = fix_address.padAddress(wallet)
    result = getMissionSummary(con, wallet)
    con.close()
    return result

