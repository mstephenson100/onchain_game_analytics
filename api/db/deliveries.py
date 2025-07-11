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


def parseBuildingType(building_type):

    if building_type == 'warehouse':
        building_type = 1

    if building_type == 'extractor':
        building_type = 2

    if building_type == 'refinery':
        building_type = 3

    if building_type == 'bioreactor':
        building_type = 4

    if building_type == 'factory':
        building_type = 5

    if building_type == 'shipyard':
        building_type = 6

    if building_type == 'spaceport':
        building_type = 7

    if building_type == 'marketplace':
        building_type = 8

    if building_type == 'habitat':
        building_type = 9

    return building_type


def getDeliveriesState(con, parameter1, parameter2, state, start_block, end_block):

    deliveries = []
    if state == "pending" or state == "finished":
        pre_sql="SELECT start_txn_id, start_block_number, finish_txn_id, finish_block_number, caller_address, crew_id, origin_id, origin_type, origin_slot, origin_asteroid_id, origin_lot_id, dest_id, dest_type, dest_slot, dest_asteroid_id, dest_lot_id, delivery_id, finish_time, product_id, product_name, product_amount "
        print(pre_sql)
        if state == "pending":
            status = 1
        elif state == "finished":
            status = 2
        if parameter1 == "wallet":
            from_sql=("FROM deliveries WHERE caller_address = '%s' AND status = %s AND start_block_number > %s" % (parameter2, status, start_block))
        elif parameter1 == "crew":
            from_sql=("FROM deliveries WHERE crew_id = %s AND status = %s AND start_block_number > %s" % (parameter2, status, start_block))
            print("from_sql: %s" % from_sql)
        if status == 2 and end_block > 0:
            finish_sql=(" AND finish_block_number <= %s ORDER BY start_block_number" % end_block)
        else:
            finish_sql=" ORDER BY start_block_number"
        
    elif state == "started":
        pre_sql="SELECT txn_id, block_number, NULL, NULL, caller_address, caller_crew_id, origin_id, origin_type, origin_slot, origin_asteroid_id, origin_lot_id, dest_id, dest_type, dest_slot, dest_asteroid_id, dest_lot_id, delivery_id, finish_time, product_id, product_name, product_amount FROM dispatcher_delivery_started "
        print(pre_sql)
        if parameter1 == "wallet":
            from_sql=("WHERE caller_address = '%s' AND block_number > %s" % (parameter2, start_block))
        elif parameter1 == "crew":
            from_sql=("WHERE caller_crew_id = %s AND block_number > %s" % (parameter2, start_block))
            print("from_sql: %s" % from_sql)
        if end_block > 0:
            finish_sql=(" AND block_number <= %s ORDER BY block_number" % end_block)
        else:
            finish_sql=" ORDER BY block_number"

    sql = pre_sql + from_sql + finish_sql

    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return deliveries

    for row in rows:
        start_txn_id=row[0]
        start_block_number=row[1]
        finish_txn_id=row[2]
        finish_block_number=row[3]
        caller_address=row[4]
        crew_id=row[5]
        origin_id=row[6]
        origin_type=row[7]
        origin_slot=row[8]
        origin_asteroid_id=row[9]
        origin_lot_id=row[10]
        dest_id=row[11]
        dest_type=row[12]
        dest_slot=row[13]
        dest_asteroid_id=row[14]
        dest_lot_id=row[15]
        delivery_id=row[16]
        finish_time=row[17]
        product_id=row[18]
        product_name=row[19]
        product_amount=row[20]

        deliveries.append({"start_txn_id": start_txn_id, "start_block_number": start_block_number, "finish_txn_id": finish_txn_id, "finish_block_number": finish_block_number, "caller_address": caller_address, "crew_id": crew_id, "origin_id": origin_id, "origin_type": origin_type, "origin_slot": origin_slot, "origin_asteroid_id": origin_asteroid_id, "origin_lot_id": origin_lot_id, "dest_id": dest_id, "dest_type": dest_type, "dest_slot": dest_slot, "dest_asteroid_id": dest_asteroid_id, "dest_lot_id": dest_lot_id, "delivery_id": delivery_id, "finish_time": finish_time, "product_id": product_id, "product_name": product_name, "product_amount": product_amount})

    return deliveries


def getDeliveriesOnAsteroid(con, asteroid_id, parameter1, parameter2, state, start_block, end_block):

    deliveries = []
    if state == "pending" or state == "finished":
        pre_sql="SELECT start_txn_id, start_block_number, finish_txn_id, finish_block_number, caller_address, crew_id, origin_id, origin_type, origin_slot, origin_asteroid_id, origin_lot_id, dest_id, dest_type, dest_slot, dest_asteroid_id, dest_lot_id, delivery_id, finish_time, product_id, product_name, product_amount "
        print(pre_sql)
        if state == "pending":
            status = 1
        elif state == "finished":
            status = 2
        if parameter1 == "wallet":
            from_sql=("FROM deliveries WHERE (origin_asteroid_id = %s OR dest_asteroid_id = %s) AND caller_address = '%s' AND status = %s AND start_block_number > %s" % (asteroid_id, asteroid_id, parameter2, status, start_block))
        elif parameter1 == "crew":
            from_sql=("FROM deliveries WHERE (origin_asteroid_id = %s OR dest_asteroid_id = %s) AND crew_id = %s AND status = %s AND start_block_number > %s" % (asteroid_id, asteroid_id, parameter2, status, start_block))
            print("from_sql: %s" % from_sql)
        if status == 2 and end_block > 0:
            finish_sql=(" AND finish_block_number <= %s ORDER BY start_block_number" % end_block)
        else:
            finish_sql=" ORDER BY start_block_number"
        
    elif state == "started":
        pre_sql="SELECT txn_id, block_number, NULL, NULL, caller_address, caller_crew_id, origin_id, origin_type, origin_slot, origin_asteroid_id, origin_lot_id, dest_id, dest_type, dest_slot, dest_asteroid_id, dest_lot_id, delivery_id, finish_time, product_id, product_name, product_amount FROM dispatcher_delivery_started "
        print(pre_sql)
        if parameter1 == "wallet":
            from_sql=("WHERE (origin_asteroid_id = %s OR dest_asteroid_id = %s) AND caller_address = '%s' AND block_number > %s" % (asteroid_id, asteroid_id, parameter2, start_block))
        elif parameter1 == "crew":
            from_sql=("WHERE (origin_asteroid_id = %s OR dest_asteroid_id = %s) AND caller_crew_id = %s AND block_number > %s" % (asteroid_id, asteroid_id, parameter2, start_block))
            print("from_sql: %s" % from_sql)
        if end_block > 0:
            finish_sql=(" AND block_number <= %s ORDER BY block_number" % end_block)
        else:
            finish_sql=" ORDER BY block_number"

    sql = pre_sql + from_sql + finish_sql

    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return deliveries

    for row in rows:
        start_txn_id=row[0]
        start_block_number=row[1]
        finish_txn_id=row[2]
        finish_block_number=row[3]
        caller_address=row[4]
        crew_id=row[5]
        origin_id=row[6]
        origin_type=row[7]
        origin_slot=row[8]
        origin_asteroid_id=row[9]
        origin_lot_id=row[10]
        dest_id=row[11]
        dest_type=row[12]
        dest_slot=row[13]
        dest_asteroid_id=row[14]
        dest_lot_id=row[15]
        delivery_id=row[16]
        finish_time=row[17]
        product_id=row[18]
        product_name=row[19]
        product_amount=row[20]

        deliveries.append({"start_txn_id": start_txn_id, "start_block_number": start_block_number, "finish_txn_id": finish_txn_id, "finish_block_number": finish_block_number, "caller_address": caller_address, "crew_id": crew_id, "origin_id": origin_id, "origin_type": origin_type, "origin_slot": origin_slot, "origin_asteroid_id": origin_asteroid_id, "origin_lot_id": origin_lot_id, "dest_id": dest_id, "dest_type": dest_type, "dest_slot": dest_slot, "dest_asteroid_id": dest_asteroid_id, "dest_lot_id": dest_lot_id, "delivery_id": delivery_id, "finish_time": finish_time, "product_id": product_id, "product_name": product_name, "product_amount": product_amount})

    return deliveries


def getDeliveriesFromLot(con, asteroid_id, lot_id, parameter1, parameter2, state, start_block, end_block):

    deliveries = []
    if state == "pending" or state == "finished":
        pre_sql="SELECT start_txn_id, start_block_number, finish_txn_id, finish_block_number, caller_address, crew_id, origin_id, origin_type, origin_slot, origin_asteroid_id, origin_lot_id, dest_id, dest_type, dest_slot, dest_asteroid_id, dest_lot_id, delivery_id, finish_time, product_id, product_name, product_amount "
        print(pre_sql)
        if state == "pending":
            status = 1
        elif state == "finished":
            status = 2
        if parameter1 == "wallet":
            from_sql=("FROM deliveries WHERE (origin_asteroid_id = %s OR dest_asteroid_id = %s) AND origin_lot_id = %s AND caller_address = '%s' AND status = %s AND start_block_number > %s" % (asteroid_id, asteroid_id, lot_id, parameter2, status, start_block))
        elif parameter1 == "crew":
            from_sql=("FROM deliveries WHERE (origin_asteroid_id = %s OR dest_asteroid_id = %s) AND origin_lot_id = %s AND crew_id = %s AND status = %s AND start_block_number > %s" % (asteroid_id, asteroid_id, lot_id, parameter2, status, start_block))
            print("from_sql: %s" % from_sql)
        if status == 2 and end_block > 0:
            finish_sql=(" AND finish_block_number <= %s ORDER BY start_block_number" % end_block)
        else:
            finish_sql=" ORDER BY start_block_number"

    elif state == "started":
        pre_sql="SELECT txn_id, block_number, NULL, NULL, caller_address, caller_crew_id, origin_id, origin_type, origin_slot, origin_asteroid_id, origin_lot_id, dest_id, dest_type, dest_slot, dest_asteroid_id, dest_lot_id, delivery_id, finish_time, product_id, product_name, product_amount FROM dispatcher_delivery_started "
        print(pre_sql)
        if parameter1 == "wallet":
            from_sql=("WHERE (origin_asteroid_id = %s OR dest_asteroid_id = %s) AND origin_lot_id = %s AND caller_address = '%s' AND block_number > %s" % (asteroid_id, asteroid_id, lot_id, parameter2, start_block))
        elif parameter1 == "crew":
            from_sql=("WHERE (origin_asteroid_id = %s OR dest_asteroid_id = %s) AND origin_lot_id = %s AND caller_crew_id = %s AND block_number > %s" % (asteroid_id, asteroid_id, lot_id, parameter2, start_block))
            print("from_sql: %s" % from_sql)
        if end_block > 0:
            finish_sql=(" AND block_number <= %s ORDER BY block_number" % end_block)
        else:
            finish_sql=" ORDER BY block_number"

    sql = pre_sql + from_sql + finish_sql

    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return deliveries

    for row in rows:
        start_txn_id=row[0]
        start_block_number=row[1]
        finish_txn_id=row[2]
        finish_block_number=row[3]
        caller_address=row[4]
        crew_id=row[5]
        origin_id=row[6]
        origin_type=row[7]
        origin_slot=row[8]
        origin_asteroid_id=row[9]
        origin_lot_id=row[10]
        dest_id=row[11]
        dest_type=row[12]
        dest_slot=row[13]
        dest_asteroid_id=row[14]
        dest_lot_id=row[15]
        delivery_id=row[16]
        finish_time=row[17]
        product_id=row[18]
        product_name=row[19]
        product_amount=row[20]

        deliveries.append({"start_txn_id": start_txn_id, "start_block_number": start_block_number, "finish_txn_id": finish_txn_id, "finish_block_number": finish_block_number, "caller_address": caller_address, "crew_id": crew_id, "origin_id": origin_id, "origin_type": origin_type, "origin_slot": origin_slot, "origin_asteroid_id": origin_asteroid_id, "origin_lot_id": origin_lot_id, "dest_id": dest_id, "dest_type": dest_type, "dest_slot": dest_slot, "dest_asteroid_id": dest_asteroid_id, "dest_lot_id": dest_lot_id, "delivery_id": delivery_id, "finish_time": finish_time, "product_id": product_id, "product_name": product_name, "product_amount": product_amount})

    return deliveries


def getDeliveriesToLot(con, asteroid_id, lot_id, parameter1, parameter2, state, start_block, end_block):

    deliveries = []
    if state == "pending" or state == "finished":
        pre_sql="SELECT start_txn_id, start_block_number, finish_txn_id, finish_block_number, caller_address, crew_id, origin_id, origin_type, origin_slot, origin_asteroid_id, origin_lot_id, dest_id, dest_type, dest_slot, dest_asteroid_id, dest_lot_id, delivery_id, finish_time, product_id, product_name, product_amount "
        print(pre_sql)
        if state == "pending":
            status = 1
        elif state == "finished":
            status = 2
        if parameter1 == "wallet":
            from_sql=("FROM deliveries WHERE (origin_asteroid_id = %s OR dest_asteroid_id = %s) AND dest_lot_id = %s AND caller_address = '%s' AND status = %s AND start_block_number > %s" % (asteroid_id, asteroid_id, lot_id, parameter2, status, start_block))
        elif parameter1 == "crew":
            from_sql=("FROM deliveries WHERE (origin_asteroid_id = %s OR dest_asteroid_id = %s) AND dest_lot_id = %s AND crew_id = %s AND status = %s AND start_block_number > %s" % (asteroid_id, asteroid_id, lot_id, parameter2, status, start_block))
            print("from_sql: %s" % from_sql)
        if status == 2 and end_block > 0:
            finish_sql=(" AND finish_block_number <= %s ORDER BY start_block_number" % end_block)
        else:
            finish_sql=" ORDER BY start_block_number"

    elif state == "started":
        pre_sql="SELECT txn_id, block_number, NULL, NULL, caller_address, caller_crew_id, origin_id, origin_type, origin_slot, origin_asteroid_id, origin_lot_id, dest_id, dest_type, dest_slot, dest_asteroid_id, dest_lot_id, delivery_id, finish_time, product_id, product_name, product_amount FROM dispatcher_delivery_started "
        print(pre_sql)
        if parameter1 == "wallet":
            from_sql=("WHERE (origin_asteroid_id = %s OR dest_asteroid_id = %s) AND dest_lot_id = %s AND caller_address = '%s' AND block_number > %s" % (asteroid_id, asteroid_id, lot_id, parameter2, start_block))
        elif parameter1 == "crew":
            from_sql=("WHERE (origin_asteroid_id = %s OR dest_asteroid_id = %s) AND dest_lot_id = %s AND caller_crew_id = %s AND block_number > %s" % (asteroid_id, asteroid_id, lot_id, parameter2, start_block))
            print("from_sql: %s" % from_sql)
        if end_block > 0:
            finish_sql=(" AND block_number <= %s ORDER BY block_number" % end_block)
        else:
            finish_sql=" ORDER BY block_number"

    sql = pre_sql + from_sql + finish_sql

    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return deliveries

    for row in rows:
        start_txn_id=row[0]
        start_block_number=row[1]
        finish_txn_id=row[2]
        finish_block_number=row[3]
        caller_address=row[4]
        crew_id=row[5]
        origin_id=row[6]
        origin_type=row[7]
        origin_slot=row[8]
        origin_asteroid_id=row[9]
        origin_lot_id=row[10]
        dest_id=row[11]
        dest_type=row[12]
        dest_slot=row[13]
        dest_asteroid_id=row[14]
        dest_lot_id=row[15]
        delivery_id=row[16]
        finish_time=row[17]
        product_id=row[18]
        product_name=row[19]
        product_amount=row[20]

        deliveries.append({"start_txn_id": start_txn_id, "start_block_number": start_block_number, "finish_txn_id": finish_txn_id, "finish_block_number": finish_block_number, "caller_address": caller_address, "crew_id": crew_id, "origin_id": origin_id, "origin_type": origin_type, "origin_slot": origin_slot, "origin_asteroid_id": origin_asteroid_id, "origin_lot_id": origin_lot_id, "dest_id": dest_id, "dest_type": dest_type, "dest_slot": dest_slot, "dest_asteroid_id": dest_asteroid_id, "dest_lot_id": dest_lot_id, "delivery_id": delivery_id, "finish_time": finish_time, "product_id": product_id, "product_name": product_name, "product_amount": product_amount})

    return deliveries


def getWarehouseInventory(con, capable_id):

    inventory = []
    txn_id = None
    txn_sql = ("SELECT txn_id FROM warehouse_inventory_changed WHERE capable_id = %s ORDER BY block_number DESC LIMIT 1" % capable_id)
    print(txn_sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % txn_sql)
        result = cur.fetchone()
        txn_id=result[0]
        cur.close()

    inventory_sql = ("SELECT b.txn_id, b.block_number, b.from_address, b.capable_id, b.capable_owner, b.resource_id, b.quantity, b.volume, b.mass, b.inventory_id, b.resource_ids_len, c.crew_id, c.lot_id, c.asteroid_id FROM warehouse_inventory_changed b, lots c WHERE b.capable_id = c.capable_id AND c.capable_type = 1 AND b.capable_id = %s AND b.txn_id = '%s'" % (capable_id, txn_id))
    print(inventory_sql)

    with con:
        cur = con.cursor()
        cur.execute("%s" % inventory_sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return inventory

    resources = []
    for row in rows:
        txn_id=row[0]
        block_number=row[1]
        from_address=row[2]
        capable_id=row[3]
        capable_owner=row[4]
        resources.append({"resource_id": row[5], "quantity": row[6], "volume": row[7], "mass": row[8]})
        inventory_id=row[9]
        resource_len=row[10]
        crew_id=row[11]
        lot_id=row[12]
        asteroid_id=row[13]

    inventory.append({"capable_id": capable_id, "capable_owner": capable_owner, "asteroid_id": asteroid_id, "lot_id": lot_id, "crew_id": crew_id, "wallet": from_address, "txn_id": txn_id, "block_number": block_number, "resource_len": resource_len, "resources": resources})

    return inventory


def getOwnedWarehouses(con, parameter1, parameter2):

    owned_warehouses = []
    if parameter1 == 'wallet':
        sql = ("SELECT txn_id, block_number, asteroid_id, lot_id, crew_id, capable_type, capable_id, occupier_address FROM lots WHERE occupier_address = '%s' AND capable_type = 1" % parameter2)
    if parameter1 == 'crew':
        sql = ("SELECT txn_id, block_number, asteroid_id, lot_id, crew_id, capable_type, capable_id, occupier_address FROM lots WHERE crew_id = %s AND capable_type = 1" % parameter2)

    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return owned_warehouses

    for row in rows:
        asteroid_id=row[2]
        lot_id=row[3]
        crew_id=row[4]
        capable_id=row[6]
        occupier_address=row[7]
        owned_warehouses.append(capable_id)

    return owned_warehouses


def getOwnedWarehousesOnAsteroid(con, asteroid_id, parameter1, parameter2):

    owned_warehouses = []
    if parameter1 == 'wallet':
        sql = ("SELECT txn_id, block_number, asteroid_id, lot_id, crew_id, capable_type, capable_id, occupier_address FROM lots WHERE occupier_address = '%s' AND capable_type = 1 AND asteroid_id = %s" % (parameter2, asteroid_id))
    if parameter1 == 'crew':
        sql = ("SELECT txn_id, block_number, asteroid_id, lot_id, crew_id, capable_type, capable_id, occupier_address FROM lots WHERE crew_id = %s AND capable_type = 1 AND asteroid_id = %s" % (parameter2, asteroid_id))

    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return owned_warehouses

    for row in rows:
        asteroid_id=row[2]
        lot_id=row[3]
        crew_id=row[4]
        capable_id=row[6]
        occupier_address=row[7]
        owned_warehouses.append(capable_id)

    return owned_warehouses


def getOwnedWarehousesAll(con, parameter1, parameter2):

    owned_warehouses = []
    if parameter1 == 'wallet':
        sql = ("SELECT txn_id, block_number, asteroid_id, lot_id, crew_id, capable_type, capable_id, occupier_address FROM lots WHERE occupier_address = '%s' AND capable_type = 1" % parameter2)
    if parameter1 == 'crew':
        sql = ("SELECT txn_id, block_number, asteroid_id, lot_id, crew_id, capable_type, capable_id, occupier_address FROM lots WHERE crew_id = %s AND capable_type = 1" % parameter2)

    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return owned_warehouses

    for row in rows:
        asteroid_id=row[2]
        lot_id=row[3]
        crew_id=row[4]
        capable_id=row[6]
        occupier_address=row[7]
        owned_warehouses.append(capable_id)

    return owned_warehouses


def getWarehouseInventoryOnAsteroid(con, asteroid_id, parameter1, parameter2):

    inventory = []
    mega_list = []
    owned_warehouses = getOwnedWarehousesOnAsteroid(con, asteroid_id, parameter1, parameter2)

    if len(owned_warehouses) == 0:
        return inventory

    for capable_id in owned_warehouses:
        inventory_id = []
        txn_id = None
        txn_sql = ("SELECT txn_id FROM warehouse_inventory_changed WHERE capable_id = %s ORDER BY block_number DESC LIMIT 1" % capable_id)
        print(txn_sql)

        with con:
            cur = con.cursor()
            cur.execute("%s" % txn_sql)
            result = cur.fetchone()
            cur.close()
            if result is not None:
                txn_id=result[0]
                inventory_sql = ("SELECT b.txn_id, b.block_number, b.from_address, b.capable_id, b.capable_owner, b.resource_id, b.quantity, b.volume, b.mass, b.inventory_id, b.resource_ids_len, c.crew_id, c.lot_id, c.asteroid_id FROM warehouse_inventory_changed b, lots c WHERE b.capable_id = c.capable_id AND c.capable_type = 1 AND b.capable_id = %s AND b.txn_id = '%s'" % (capable_id, txn_id))
                print(inventory_sql)
                with con:
                    cur = con.cursor()
                    cur.execute("%s" % inventory_sql)
                    rows = cur.fetchall()
                    cur.close()


                    inventory = []
                    resources_list = []
                    if rows is not None:
                        for row in rows:
                            resources=[]
                            txn_id=row[0]
                            block_number=row[1]
                            from_address=row[2]
                            capable_id=row[3]
                            capable_owner=row[4]
                            resources.append({"resource_id": row[5], "quantity": row[6], "volume": row[7], "mass": row[8]})
                            inventory_id=row[9]
                            resource_len=row[10]
                            crew_id=row[11]
                            lot_id=row[12]
                            asteroid_id=row[13]
                            resources_list.append(resources)

                        inventory.append({"capable_id": capable_id, "capable_owner": capable_owner, "asteroid_id": asteroid_id, "lot_id": lot_id, "crew_id": crew_id, "wallet": from_address, "txn_id": txn_id, "block_number": block_number, "resource_len": resource_len, "resources": resources_list})
                        mega_list.append({"capable_id": inventory})

    return mega_list


def getWarehouseInventoryAll(con, parameter1, parameter2):

    inventory = []
    mega_list = []
    owned_warehouses = getOwnedWarehousesAll(con, parameter1, parameter2)

    if len(owned_warehouses) == 0:
        return inventory

    for capable_id in owned_warehouses:
        inventory_id = []
        txn_id = None
        txn_sql = ("SELECT txn_id FROM warehouse_inventory_changed WHERE capable_id = %s ORDER BY block_number DESC LIMIT 1" % capable_id)
        print(txn_sql)

        with con:
            cur = con.cursor()
            cur.execute("%s" % txn_sql)
            result = cur.fetchone()
            cur.close()
            if result is not None:
                txn_id=result[0]
                inventory_sql = ("SELECT b.txn_id, b.block_number, b.from_address, b.capable_id, b.capable_owner, b.resource_id, b.quantity, b.volume, b.mass, b.inventory_id, b.resource_ids_len, c.crew_id, c.lot_id, c.asteroid_id FROM warehouse_inventory_changed b, lots c WHERE b.capable_id = c.capable_id AND c.capable_type = 1 AND b.capable_id = %s AND b.txn_id = '%s'" % (capable_id, txn_id))
                print(inventory_sql)
                with con:
                    cur = con.cursor()
                    cur.execute("%s" % inventory_sql)
                    rows = cur.fetchall()
                    cur.close()

                    inventory = []
                    resources_list = []
                    if rows is not None:
                        for row in rows:
                            resources=[]
                            txn_id=row[0]
                            block_number=row[1]
                            from_address=row[2]
                            capable_id=row[3]
                            capable_owner=row[4]
                            resources.append({"resource_id": row[5], "quantity": row[6], "volume": row[7], "mass": row[8]})
                            inventory_id=row[9]
                            resource_len=row[10]
                            crew_id=row[11]
                            lot_id=row[12]
                            asteroid_id=row[13]
                            resources_list.append(resources)

                        inventory.append({"capable_id": capable_id, "capable_owner": capable_owner, "asteroid_id": asteroid_id, "lot_id": lot_id, "crew_id": crew_id, "wallet": from_address, "txn_id": txn_id, "block_number": block_number, "resource_len": resource_len, "resources": resources_list})
                        mega_list.append({"capable_id": inventory})

    return mega_list


def allDeliveries(parameter1, parameter2, state, start_block, end_block):

    deliveries = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    deliveries = getDeliveriesState(con, parameter1, parameter2, state, start_block, end_block)
    con.close()
    return deliveries
    

def deliveriesOnAsteroid(asteroid_id, parameter1, parameter2, state, start_block, end_block):

    deliveries = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    deliveries = getDeliveriesOnAsteroid(con, asteroid_id, parameter1, parameter2, state, start_block, end_block)
    con.close()
    return deliveries


def deliveriesFromLot(asteroid_id, lot_id, parameter1, parameter2, state, start_block, end_block):

    deliveries = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    deliveries = getDeliveriesFromLot(con, asteroid_id, lot_id, parameter1, parameter2, state, start_block, end_block)
    con.close()
    return deliveries


def deliveriesToLot(asteroid_id, lot_id, parameter1, parameter2, state, start_block, end_block):

    deliveries = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    deliveries = getDeliveriesToLot(con, asteroid_id, lot_id, parameter1, parameter2, state, start_block, end_block)
    con.close()
    return deliveries


def warehouseInventory(capable_id):

    inventory = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    inventory = getWarehouseInventory(con, capable_id)
    con.close()
    return inventory


def warehouseInventoryOnAsteroid(asteroid_id, parameter1, parameter2):

    inventory = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    inventory = getWarehouseInventoryOnAsteroid(con, asteroid_id, parameter1, parameter2)
    con.close()
    return inventory


def warehouseInventoryAll(parameter1, parameter2):

    inventory = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    inventory = getWarehouseInventoryAll(con, parameter1, parameter2)
    con.close()
    return inventory

