import sys
import os
import pymysql
import warnings
import traceback
import configparser
import time
from datetime import datetime

sys.path.insert(0,'../')
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


def convertFinishTime(finish_time):

    days = finish_time // (60 * 60 * 24)
    hours = (finish_time % (60 * 60 * 24)) // (60 * 60)
    minutes = (finish_time % (60 * 60)) // 60
    seconds = finish_time % 60
    days = int(days)
    hours = int(hours)
    minutes = int(minutes)
    seconds = int(seconds)
    duration_string = f"{days} days, {hours:02d}:{minutes:02d}:{seconds:02d}"
    return duration_string


def getWalletLeases(con, wallet):

    leases=[]
    sql = ("SELECT b.txn_id, b.crew_id, b.asteroid_id, b.lot_id, b.term, c.crew_id, c.name, d.timestamp FROM prepaid_agreements b, crews c, dispatcher_prepaid_agreement_accepted d WHERE b.caller_address = '%s' AND b.crew_id = c.crew_id and b.target_label = 4 and b.txn_id = d.txn_id" % wallet)

    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return leases

    for row in rows:
        txn_id=row[0]
        crew_id=row[1]
        asteroid_id=row[2]
        lot_id=row[3]
        term=row[4]
        crew_id_2=row[5]
        crew_name=row[6]
        timestamp=str(row[7])
        timestamp_dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        timestamp_seconds = timestamp_dt.timestamp()
        expire_seconds = (timestamp_seconds + term)
        current_datetime = datetime.now()
        current_seconds = current_datetime.timestamp()
        remaining_seconds = (expire_seconds - current_seconds)
        readable_time = convertFinishTime(remaining_seconds)

        leases.append({"crew_id": crew_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "crew_name": crew_name, "remaining_time": readable_time})

    return leases


def walletLeases(wallet):

    leases = None
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    wallet = fix_address.padAddress(wallet)
    leases = getWalletLeases(con, wallet)
    con.close()
    return leases

