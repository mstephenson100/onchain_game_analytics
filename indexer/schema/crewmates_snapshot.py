#!/home/bios/.pyenv/shims/python3

import sys
import os
import json
import time
import os.path
import pymysql
import configparser
import warnings

# curl https://influence.infura-ipfs.io/ipfs/QmPjtFx2b8gx4kBEX3xZmCafmyWdfDj8UkNqfQGmFvtg4U -o /home/bios/indexer_testnet/schema/crewmates_snapshot.json

def main():

    cwd = os.getcwd()
    config_path = cwd.split('/')[3]
    phase = config_path.split('_')[1]
    config_file = "/home/bios/" + config_path + "/indexer.conf"
    snapshot_json = "/home/bios/" + config_path + "/schema/crewmates_snapshot.json"

    if os.path.exists(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        db_user = config.get('credentials', 'db_user')
        db_password = config.get('credentials', 'db_password')
        db = config.get('credentials', 'db')
    else:
        raise Exception(config_file)

    con = pymysql.connect("127.0.0.1", db_user, db_password, db)

    f = open(snapshot_json)
    data = json.load(f)
    for row in data:

        crewmate_id = row['i']
        crewmate_name = row['name']
        collection = row['collection']
        crewmate_class = row['class']
        title = row['title']

        insert_sql = ("INSERT IGNORE INTO crewmate_metadata_l1 (crewmate_id, name, collection, class, title) VALUES (%s, '%s', %s, %s, %s)" % (crewmate_id, crewmate_name, collection, crewmate_class, title))

        con = pymysql.connect("127.0.0.1", db_user, db_password, db)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
        with con:
            cur = con.cursor()
            cur.execute("%s" % insert_sql)


if __name__ == "__main__" : main()

