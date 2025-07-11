import sys
import os
import pymysql
import warnings
import traceback
import configparser
import time

sys.path.insert(0,'../')
import db.get_types as inf

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


def getCrewmatesRecruited(con, start_time, end_time, hours):

    crewmates = []
    if hours is None:
        sql = ("SELECT b.crewmate_id, b.caller_crew_id, b.name, b.collection, b.class, b.title, b.station_label, b.station_id, b.impactful_1, b.impactful_2, b.impactful_3, b.timestamp, c.asteroid_id, c.lot_id, c.building_id FROM dispatcher_crewmate_recruited_v1 b, buildings c WHERE b.timestamp >= '%s' AND b.timestamp <= '%s' AND b.station_id = c.building_id ORDER BY b.block_number" % (start_time, end_time))
    else:
        sql = ("SELECT b.crewmate_id, b.caller_crew_id, b.name, b.collection, b.class, b.title, b.station_label, b.station_id, b.impactful_1, b.impactful_2, b.impactful_3, b.timestamp, c.asteroid_id, c.lot_id, c.building_id FROM dispatcher_crewmate_recruited_v1 b, buildings c WHERE b.timestamp >= (NOW() - INTERVAL %s HOUR) AND b.station_id = c.building_id ORDER BY b.block_number" % (hours))
    #print(sql)

    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return crewmates

    for row in rows:
        crewmate_id=row[0]
        crew_id=row[1]
        name=row[2]
        collection_id=row[3]
        class_id=int(row[4])
        title_id=int(row[5])
        station_label=row[6]
        station_id=row[7]
        impactful_1=row[8]
        impactful_2=row[9]
        impactful_3=row[10]
        timestamp=row[11]
        asteroid_id=row[12]
        lot_id=row[13]

        collection_name = inf.getCrewCollectionTypes(collection_id)
        class_name = inf.getClassTypes(class_id)
        title_name = inf.getTitleTypes(title_id)
        impactful_1_name = inf.getCrewTraitTypes(impactful_1)
        impactful_2_name = inf.getCrewTraitTypes(impactful_2)
        impactful_3_name = inf.getCrewTraitTypes(impactful_3)

        crewmates.append({"crewmate_id": crewmate_id, "name": name, "crew_id": crew_id, "collection": collection_name, "title": title_name, "class_name": class_name, "impactful_1": impactful_1_name, "impactful_2": impactful_2_name, "impactful_3": impactful_3_name, "station_id": station_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "timestamp": str(timestamp)})

    return crewmates


def getCrewsMinted(con, start_time, end_time, hours):

    crews = []
    if hours is None:
        sql = ("SELECT block_number, timestamp FROM crews WHERE timestamp >= '%s' AND timestamp <= '%s' ORDER BY block_number" % (start_time, end_time))
    else:
        sql = ("SELECT block_number, timestamp FROM crews WHERE timestamp >= (NOW() - INTERVAL %s HOUR) ORDER BY block_number" % (hours))
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return crews

    block_list = []
    mint_count = 0
    for row in rows:
        block_number = row[0]
        timestamp = row[2]
        if block_number not in block_list:
            mint_count+=1
            block_list.append(block_number)

        crews.append({"txn_id": txn_id, "block": block_number, "wallet": wallet, "crew_id": crew_id, "ship_id": ship_id, "fuel_burned": fuel_burned, "burn_type": burn_type, "timestamp": str(timestamp)})

    return crews


def getResourcesExtracted(con, start_time, end_time, hours):

    extracted_resources = []
    resource_list = []
    if hours is None:
        sql = ("SELECT finish_txn_id, finish_block_number, resource_id, resource_name, resource_yield, finish_timestamp FROM extractions WHERE status = 2 AND finish_timestamp >= '%s' AND finish_timestamp <= '%s' ORDER BY finish_block_number" % (start_time, end_time))
    else:
        sql = ("SELECT finish_txn_id, finish_block_number, resource_id, resource_name, resource_yield, finish_timestamp FROM extractions WHERE status = 2 AND finish_timestamp >= (NOW() - INTERVAL %s HOUR) ORDER BY finish_block_number" % (hours))
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return extracted_resources

    for row in rows:
        txn_id=row[0]
        block_number=[1]
        resource_id=row[2]
        resource_name=row[3]
        resource_yield=row[4]
        timestamp=row[5]

        if resource_name in resource_list:
            for resource_dict in extracted_resources:
                if resource_dict['resource_name'] == resource_name:
                    resource_dict['amount'] += resource_yield
        else:
            resource_list.append(resource_name)
            extracted_resources.append({"resource_name": resource_name, "amount": resource_yield})


    sorted_extracted_resources = sorted(extracted_resources, key = lambda i: i['amount'], reverse=True)
    return sorted_extracted_resources


def getProductsProduced(con, start_time, end_time, hours):

    products_produced = []
    products_list = []
    if hours is None:
        sql = ("SELECT txn_id, block_number, resource_id, resource_name, resource_amount, timestamp FROM products_produced WHERE timestamp >= '%s' AND timestamp <= '%s' ORDER BY block_number" % (start_time, end_time))
    else:
        sql = ("SELECT txn_id, block_number, resource_id, resource_name, resource_amount, timestamp FROM products_produced WHERE timestamp >= (NOW() - INTERVAL %s HOUR) ORDER BY block_number" % (hours))
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return products_produced

    for row in rows:
        txn_id=row[0]
        block_number=[1]
        product_id=row[2]
        product_name=row[3].lower()
        product_yield=row[4]
        timestamp=row[5]

        if product_name in products_list:
            for product_dict in products_produced:
                if product_dict['product_name'] == product_name:
                    product_dict['amount'] += product_yield
        else:
            products_list.append(product_name)
            products_produced.append({"product_name": product_name, "amount": product_yield})


    sorted_products_produced = sorted(products_produced, key = lambda i: i['amount'], reverse=True)
    return sorted_products_produced


def getProductsConsumed(con, start_time, end_time, hours):

    products_consumed = []
    products_list = []
    if hours is None:
        sql = ("SELECT txn_id, block_number, resource_id, resource_name, resource_amount, timestamp FROM products_consumed WHERE timestamp >= '%s' AND timestamp <= '%s' ORDER BY block_number" % (start_time, end_time))
    else:
        sql = ("SELECT txn_id, block_number, resource_id, resource_name, resource_amount, timestamp FROM products_consumed WHERE timestamp >= (NOW() - INTERVAL %s HOUR) ORDER BY block_number" % (hours))
    #print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return products_consumed

    for row in rows:
        txn_id=row[0]
        block_number=[1]
        product_id=row[2]
        product_name=row[3].lower()
        product_yield=row[4]
        timestamp=row[5]

        if product_name in products_list:
            for product_dict in products_consumed:
                if product_dict['product_name'] == product_name:
                    product_dict['amount'] += product_yield
        else:
            products_list.append(product_name)
            products_consumed.append({"product_name": product_name, "amount": product_yield})


    sorted_products_consumed = sorted(products_consumed, key = lambda i: i['amount'], reverse=True)
    return sorted_products_consumed


def crewmatesRecruited(start_time, end_time, hours):

    crewmates = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    crewmates = getCrewmatesRecruited(con, start_time, end_time, hours)
    con.close()
    return crewmates


def crewsMinted(start_time, end_time, hours):

    crews = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    crews = getCrewsMinted(con, start_time, end_time, hours)
    con.close()
    return crews


def crewsModified(start_time, end_time, hours):

    crews = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    crews = getCrewsMinted(con, start_time, end_time, hours)
    con.close()
    return crews


def resourcesExtracted(start_time, end_time, hours):

    resources = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    resources = getResourcesExtracted(con, start_time, end_time, hours)
    con.close()
    return resources


def productsProduced(start_time, end_time, hours):

    products = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    products = getProductsProduced(con, start_time, end_time, hours)
    con.close()
    return products


def productsConsumed(start_time, end_time, hours):

    products = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    products = getProductsConsumed(con, start_time, end_time, hours)
    con.close()
    return products

