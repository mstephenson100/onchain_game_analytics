#!/home/bios/.pyenv/shims/python3

import sys
import os
import json
import time
import os.path
import pymysql
import configparser
import warnings

# curl https://influence.infura-ipfs.io/ipfs/QmdJ7kY74efg8PvcbZ7AzuVdfZAksUiAVUL7koznvYWUq4 -o /home/bios/indexer_testnet/schema/asteroids_snapshot.json

def main():

    cwd = os.getcwd()
    config_path = cwd.split('/')[3]
    phase = config_path.split('_')[1]
    config_file = "/home/bios/" + config_path + "/indexer.conf"
    snapshot_json = "/home/bios/" + config_path + "/schema/asteroids_snapshot.json"

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
        asteroid_id = row['i']
        asteroid_name = row['name']
        radius = row['r']
        spectral_type = row['spectralType']
        bonuses = row['bonuses']
        scan_status = row['scanStatus']
        purchase_order = row['purchaseOrder']

        insert_sql = ("INSERT IGNORE INTO asteroid_metadata_l1 (asteroid_id, name, radius, spectral_type, bonuses, scan_status, purchase_order) VALUES (%s, '%s', %s, %s, %s, %s, %s)" % (asteroid_id, asteroid_name, radius, spectral_type, bonuses, scan_status, purchase_order))

        con = pymysql.connect("127.0.0.1", db_user, db_password, db)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
        with con:
            cur = con.cursor()
            cur.execute("%s" % insert_sql)


if __name__ == "__main__" : main()

