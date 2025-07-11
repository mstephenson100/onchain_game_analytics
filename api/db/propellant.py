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


def getPropellantProducedLong(con, start_time, end_time, hours):

    propellant = []
    if hours is None:
        sql = ("SELECT txn_id, block_number, caller_address, crew_id, destination_label, destination_id, destination_type, asteroid_id, lot_id, amount, method, timestamp FROM propellant_produced WHERE timestamp >= '%s' AND timestamp <= '%s' ORDER BY block_number" % (start_time, end_time))
    else:
        sql = ("SELECT txn_id, block_number, caller_address, crew_id, destination_label, destination_id, destination_type, asteroid_id, lot_id, amount, method, timestamp FROM propellant_produced  WHERE timestamp >= (NOW() - INTERVAL %s HOUR) ORDER BY block_number" % (hours))
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return propellant

    for row in rows:
        txn_id = row[0]
        block_number = row[1]
        wallet = row[2]
        crew_id = row[3]
        inventory_label = row[4]
        inventory_id = row[5]
        inventory_type = row[6]
        asteroid_id = row[7]
        lot_id = row[8]
        amount = row[9]
        method = row[10]
        timestamp = row[11]

        propellant.append({"txn_id": txn_id, "block": block_number, "wallet": wallet, "crew_id": crew_id, "inventory_label": inventory_label, "inventory_id": inventory_id, "inventory_type": inventory_type, "asteroid_id": asteroid_id, "lot_id": lot_id, "amount": amount, "method": e, "timestamp": str(timestamp)})

    return propellant


def getPropellantProduced(con, start_time, end_time, hours):

    propellant = []
    if hours is None:
        sql = ("SELECT txn_id, block_number, amount, timestamp FROM propellant_produced  WHERE timestamp >= '%s' AND timestamp <= '%s' ORDER BY block_number" % (start_time, end_time))
    else:
        sql = ("SELECT txn_id, block_number, amount, timestamp FROM propellant_produced  WHERE timestamp >= (NOW() - INTERVAL %s HOUR) ORDER BY block_number" % (hours))
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return propellant

    for row in rows:
        txn_id = row[0]
        block_number = row[1]
        amount = row[2]
        timestamp = row[3]

        propellant.append({"txn_id": txn_id, "block": block_number, "amount": amount, "timestamp": str(timestamp)})

    return propellant


def getPropellantBurnedLong(con, start_time, end_time, hours):

    propellant = []
    if hours is None:
        sql = ("SELECT txn_id, block_number, caller_address, crew_id, ship_id, fuel_burned, burn_type, timestamp FROM propellant_burned  WHERE timestamp >= '%s' AND timestamp <= '%s' ORDER BY block_number" % (start_time, end_time))
    else:
        sql = ("SELECT txn_id, block_number, caller_address, crew_id, ship_id, fuel_burned, burn_type, timestamp FROM propellant_burned  WHERE timestamp >= (NOW() - INTERVAL %s HOUR) ORDER BY block_number" % (hours))
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return propellant

    for row in rows:
        txn_id = row[0]
        block_number = row[1]
        wallet = row[2]
        crew_id = row[3]
        ship_id = row[4]
        fuel_burned = row[5]
        burn_type = row[6]
        timestamp = row[7]

        propellant.append({"txn_id": txn_id, "block": block_number, "wallet": wallet, "crew_id": crew_id, "ship_id": ship_id, "fuel_burned": fuel_burned, "burn_type": burn_type, "timestamp": str(timestamp)})

    return propellant


def getPropellantBurned(con, start_time, end_time, hours):

    propellant = []
    if hours is None:
        sql = ("SELECT txn_id, block_number, fuel_burned, timestamp FROM propellant_burned  WHERE timestamp >= '%s' AND timestamp <= '%s' ORDER BY block_number" % (start_time, end_time))
    else:
        sql = ("SELECT txn_id, block_number, fuel_burned, timestamp FROM propellant_burned  WHERE timestamp >= (NOW() - INTERVAL %s HOUR) ORDER BY block_number" % (hours))
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return propellant

    for row in rows:
        txn_id = row[0]
        block_number = row[1]
        fuel_burned = row[2]
        timestamp = row[3]

        propellant.append({"txn_id": txn_id, "block": block_number, "amount": fuel_burned, "timestamp": str(timestamp)})

    return propellant


def getShortReport(con, start_time, end_time, hours):

    produced = getPropellantProduced(con, start_time, end_time, hours)
    burned = getPropellantBurned(con, start_time, end_time, hours)

    propellant = []
    timestamps = []
    for produced_row in produced:
        if produced_row['timestamp'] not in timestamps:
            timestamps.append(produced_row['timestamp'])

    for burned_row in burned:
        if burned_row['timestamp'] not in timestamps:
            timestamps.append(burned_row['timestamp'])

    for timestamp in timestamps:
        produced_count = 0
        burned_count = 0
        for p_row in produced:
            if p_row['timestamp'] == timestamp:
                produced_count+=p_row['amount']
        for b_row in burned:
            if b_row['timestamp'] == timestamp:
                burned_count+=b_row['amount']

        propellant.append({"timestamp": timestamp, "burned": burned_count, "produced": produced_count})

    sorted_propellant = sorted(propellant, key = lambda i: i['timestamp'])
    return sorted_propellant


def propellantReport(start_time, end_time, hours):

    propellant = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    propellant = getShortReport(con, start_time, end_time, hours)
    con.close()
    return propellant


def propellantConsumed(start_time, end_time, hours):

    propellant = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    propellant = getPropellantBurned(con, start_time, end_time, hours)
    con.close()
    return propellant

