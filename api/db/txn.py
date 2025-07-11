import sys
import os
import pymysql
import warnings
import traceback
import configparser
import time
from datetime import datetime
from collections import defaultdict

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


def getTxnsTime(con, start_time, end_time, hours, tablename):

    txn_data = []
    if hours is None:
        sql = ("SELECT block_number, timestamp, txns, asteroid_txns, crewmate_txns, crew_txns, ship_txns, dispatcher_txns FROM %s WHERE timestamp >= '%s' AND timestamp <= '%s' ORDER BY block_number" % (tablename, start_time, end_time))
    else:
        sql = ("SELECT block_number, timestamp, txns Fasteroid_txns, crewmate_txns, crew_txns, ship_txns, dispatcher_txns FROM %s WHERE timestamp >= (NOW() - INTERVAL %s HOUR) ORDER BY block_number" % (tablename, hours))
    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return txn_data

    for row in rows:
        block_number = row[0]
        timestamp = row[1]
        txns = row[2]
        asteroid_txns = row[3]
        crewmate_txns = row[4]
        crew_txns = row[5]
        ship_txns = row[6]
        dispatcher_txns = row[7]

        txn_data.append({"block_number": block_number, "timestamp": str(timestamp), "txns": txns, "dispatcher": dispatcher_txns, "asteroid": asteroid_txns, "crewmate": crewmate_txns, "crew": crew_txns, "ship": ship_txns})

    return txn_data


def searchTxns(block_number, search_list):

    txn_count = 0
    for row in search_list:
        if row['block_number'] == block_number:
            if row['txns'] > txn_count:
                return row['txns']

    return txn_count


def getTickLimit(txn_len):

    if txn_len > 80000:
        tick_limit = 320
    elif txn_len > 40000:
        tick_limit = 160
    elif txn_len > 30000:
        tick_limit = 120
    elif txn_len > 20000:
        tick_limit = 80
    elif txn_len > 16000:
        tick_limit = 62
    elif txn_len > 14000:
        tick_limit = 55
    elif txn_len > 12000:
        tick_limit = 50
    elif txn_len > 10000:
        tick_limit = 40
    elif txn_len > 8000:
        tick_limit = 32
    elif txn_len > 6000:
        tick_limit = 25
    elif txn_len > 4000:
        tick_limit = 16
    elif txn_len > 2000:
        tick_limit = 8
    elif txn_len > 1000:
        tick_limit = 4
    elif txn_len > 500:
        tick_limit = 2
    else:
        tick_limit = 1

    return tick_limit


def aggValues(txn_list, tick_limit):

    global_txns = 0
    dispatcher_txns = 0
    asteroid_txns = 0
    crewmate_txns = 0
    crew_txns = 0
    ship_txns = 0

    for row in txn_list:
        block_number = row['block_number']
        timestamp = row['timestamp']

        new_global_txns = row['txns']
        new_dispatcher_txns = row['dispatcher']
        new_asteroid_txns = row['asteroid']
        new_crewmate_txns = row['crewmate']
        new_crew_txns = row['crew']
        new_ship_txns = row['ship']

        global_txns = (global_txns + new_global_txns)
        dispatcher_txns = (dispatcher_txns + new_dispatcher_txns)
        asteroid_txns = (asteroid_txns + new_asteroid_txns)
        crewmate_txns = (crewmate_txns + new_crewmate_txns)
        crew_txns = (crew_txns + new_crew_txns)
        ship_txns = (ship_txns + new_ship_txns)

    global_txn_average = round((global_txns / tick_limit), 4)
    dispatcher_txn_average = round((dispatcher_txns / tick_limit), 4)
    asteroid_txn_average = round((asteroid_txns / tick_limit), 4)
    crewmate_txn_average = round((crewmate_txns / tick_limit), 4)
    crew_txn_average = round((crew_txns / tick_limit), 4)
    ship_txn_average = round((ship_txns / tick_limit), 4)
    influence_txn_average = (dispatcher_txn_average + asteroid_txn_average + crewmate_txn_average + crew_txn_average + ship_txn_average)
    influence_percentage = round(((influence_txn_average / global_txn_average) * 100), 3)

    return ({"block_number": block_number, "timestamp": timestamp, "txns": global_txn_average, "dispatcher_txns": dispatcher_txn_average, "asteroid_txns": asteroid_txn_average, "crewmate_txns": crewmate_txn_average, "crew_txns": crew_txn_average, "ship_txns": ship_txn_average, "influence_total_txns": influence_txn_average, "percentage_of_global": influence_percentage})


def normalizeTicks(unsorted_txn_list):

    txn_averages = []
    txn_list = sorted(unsorted_txn_list, key = lambda i: i['block_number'], reverse=True)
    txn_len = len(txn_list)
    tick_limit = getTickLimit(txn_len)
    while len(txn_list) > 0:
        return_list = aggValues(txn_list[:tick_limit], tick_limit)
        txn_averages.append(return_list)
        del txn_list[:tick_limit]

    return txn_averages


def getTxnsBetweenTimes(con, start_time, end_time, hours):

    txns = []
    txns = getTxnsTime(con, start_time, end_time, hours, "txns_per_block")
    unsorted_normalized_txns = normalizeTicks(txns)
    sorted_normalized_txns = sorted(unsorted_normalized_txns, key = lambda i: i['block_number'])
    return sorted_normalized_txns


def getFees(con, start_time, end_time, hours, all_contracts):

    fees = []
    dispatcher = []
    asteroid = []
    crew = []
    crewmate = []
    ship = []
    txn_list = []

    if hours is None:
        sql = ("SELECT contract, fee, timestamp, txn_id FROM influence_txns WHERE timestamp >= '%s' AND timestamp <= '%s' ORDER BY block_number" % (start_time, end_time))
    else:
        sql = ("SELECT contract, fee, timestamp, txn_id FROM influence_txns WHERE timestamp >= (NOW() - INTERVAL %s HOUR) ORDER BY block_number" % (hours))

    print(sql)
    tic = time.time()
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return fees

    for row in rows:
        contract = row[0]
        fee = row[1]
        timestamp = str(row[2])
        txn_id = row[3]
        fees.append({"fee": fee, "timestamp": timestamp})

    toc = time.time()

    if all_contracts is True:
        fees = []
        fees.append({"dispatcher": dispatcher, "asteroid": asteroid, "crew": crew, "crewmate": crewmate, "ship": ship})

    fees_by_date = defaultdict(int)
    for item in fees:
        date = datetime.strptime(item['timestamp'], '%Y-%m-%d %H:%M:%S').date()
        fees_by_date[date] += item['fee']


    fees_by_date_human_readable = {date.strftime('%Y-%m-%d'): total_fee for date, total_fee in fees_by_date.items()}

    revised_fees = []
    for key, value in fees_by_date_human_readable.items():
        revised_fees.append({"fee": value, "timestamp": key})

    return revised_fees


def getTxnsByContract(con, start_time, end_time, hours):

    txns = []
    dispatcher = []
    asteroid = []
    crew = []
    crewmate = []
    ship = []

    dispatcher_count = 0
    asteroid_count = 0
    crew_count = 0
    crewmate_count = 0
    ship_count = 0

    if hours is None:
        sql = ("SELECT contract, timestamp, txn_id FROM influence_txns WHERE timestamp >= '%s' AND timestamp <= '%s' ORDER BY block_number" % (start_time, end_time))
    else:
        sql = ("SELECT contract, timestamp, txn_id FROM influence_txns WHERE timestamp >= (NOW() - INTERVAL %s HOUR) ORDER BY block_number" % (hours))
    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return txns

    for row in rows:
        contract = row[0]
        timestamp = str(row[1])
        txn_id = row[2]

        if contract == 'dispatcher':
            dispatcher_count+=1
        elif contract == 'asteroid':
            asteroid_count+=1
        elif contract == 'crew':
            crew_count+=1
        elif contract == 'crewmate':
            crewmate_count+=1
        elif contract == 'ship':
            ship_count+=1

    txns.append({"dispatcher": dispatcher_count, "asteroid": asteroid_count, "crew": crew_count, "crewmate": crewmate_count, "ship": ship_count})

    return txns


def txnsBetweenTimes(start_time, end_time, hours):

    txns = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    txns = getTxnsBetweenTimes(con, start_time, end_time, hours)
    con.close()
    return txns


def txnsByContract(start_time, end_time, hours):

    txns = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    txns = getTxnsByContract(con, start_time, end_time, hours)
    con.close()
    return txns


def feesConsumed(start_time, end_time, hours, all_contracts):

    fees = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    fees = getFees(con, start_time, end_time, hours, all_contracts)
    con.close()
    return fees
