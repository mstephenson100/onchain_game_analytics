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
import pymongo

def updateSql(sql):

    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)

    cur.close()
    con.close()


def getWork(db_user, db_password, db, column_name):

    work = []
    sql = ("SELECT block_number FROM txns_per_block WHERE %s is NULL ORDER BY block_number LIMIT 50" % column_name)
    #print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()

    if rows == None:
        return None

    for row in rows:
        block_number = row[0]
        work.append(block_number)

    cur.close()
    con.close()

    return work


def getUserTxns(db_user, db_password, db, block_number, tablename):

    txns = 0
    sql =("SELECT txns FROM %s WHERE block_number = %s" % (tablename, block_number))
    #print(sql)
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        if result is None:
            return txns
        else:
            txns=result[0]

    cur.close()
    con.close()

    return txns


def getMongoBlock(mongo_collection):

    mongo_block_number = None
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client[mongo_collection]
    col = db["_apibara"]
    result = col.find_one()
    mongo_block_number = result['cursor']['order_key']
    client.close()

    return mongo_block_number


def processWork(db_user, db_password, db, work, txn_column, status_column, table_name):

    for block_number in work:
        txns = getUserTxns(db_user, db_password, db, block_number, table_name)
        sql = ("UPDATE txns_per_block SET %s = %s, %s = 1 WHERE block_number = %s" % (txn_column, txns, status_column, block_number))
        print(sql)
        updateSql(sql)


async def log_loop(poll_interval, db_user, db_password, db, phase):

    while True:

        dispatcher_work = getWork(db_user, db_password, db, "dispatcher_status")
        if len(dispatcher_work) > 0:
            largest_block_number = max(dispatcher_work)
            mongo_collection = phase + "_dispatcher_events"
            dispatcher_mongo_block = getMongoBlock(mongo_collection)
            if dispatcher_mongo_block >= largest_block_number:
                processWork(db_user, db_password, db, dispatcher_work, "dispatcher_txns", "dispatcher_status", "dispatcher_txns_per_block")

        asteroid_work = getWork(db_user, db_password, db, "asteroid_status")
        if len(asteroid_work) > 0:
            largest_block_number = max(asteroid_work)
            mongo_collection = phase + "_asteroid_events"
            asteroid_mongo_block = getMongoBlock(mongo_collection)
            if asteroid_mongo_block >= largest_block_number:
                processWork(db_user, db_password, db, asteroid_work, "asteroid_txns", "asteroid_status", "asteroid_txns_per_block")

        crewmate_work = getWork(db_user, db_password, db, "crewmate_status")
        if len(crewmate_work) > 0:
            largest_block_number = max(crewmate_work)
            mongo_collection = phase + "_crewmate_events"
            crewmate_mongo_block = getMongoBlock(mongo_collection)
            if crewmate_mongo_block >= largest_block_number:
                processWork(db_user, db_password, db, crewmate_work, "crewmate_txns", "crewmate_status", "crewmate_txns_per_block")

        crew_work = getWork(db_user, db_password, db, "crew_status")
        if len(crew_work) > 0:
            largest_block_number = max(crew_work)
            mongo_collection = phase + "_crew_events"
            crew_mongo_block = getMongoBlock(mongo_collection)
            if crew_mongo_block >= largest_block_number:
                processWork(db_user, db_password, db, crew_work, "crew_txns", "crew_status", "crew_txns_per_block")

        ship_work = getWork(db_user, db_password, db, "ship_status")
        if len(ship_work) > 0:
            largest_block_number = max(ship_work)
            mongo_collection = phase + "_ship_events"
            ship_mongo_block = getMongoBlock(mongo_collection)
            if ship_mongo_block >= largest_block_number:
                processWork(db_user, db_password, db, ship_work, "ship_txns", "ship_status", "ship_txns_per_block")

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

    poll_interval=1
    loop = asyncio.get_event_loop()
    try:
        print("*** Starting txn oracle")
        loop.run_until_complete(
            asyncio.gather(
                log_loop(poll_interval, db_user, db_password, db, phase)))
    finally:
        loop.close()


if __name__ == "__main__" : main()

