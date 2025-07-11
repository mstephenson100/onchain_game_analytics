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


def parseProcessorType(processor_type):

    if processor_type is None:
        processor_type = None

    if processor_type == 'refinery':
        processor_type = 3

    if processor_type == 'bioreactor':
        processor_type = 4

    if processor_type == 'factory':
        processor_type = 5

    if processor_type == 'shipyard':
        processor_type = 6

    return processor_type


def getInputs(con, txn_id):

    inputs = []
    sql = ("SELECT resource_id, resource_name, resource_amount FROM dispatcher_material_processing_started_inputs WHERE txn_id = '%s'" % txn_id)
    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return inputs

    for row in rows:
        input_id=row[0]
        input_name=row[1]
        input_amount=row[2]
        inputs.append({"resource_id": input_id, "resource_name": input_name, "resource_amount": input_amount})

    return inputs


def getOutputs(con, txn_id):

    outputs = []
    sql = ("SELECT resource_id, resource_name, resource_amount FROM dispatcher_material_processing_started_outputs WHERE txn_id = '%s'" % txn_id)
    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return outputs

    for row in rows:
        output_id=row[0]
        output_name=row[1]
        output_amount=row[2]
        outputs.append({"resource_id": output_id, "resource_name": output_name, "resource_amount": output_amount})

    return outputs


def getProcessingState(con, parameter1, parameter2, state, processor, start_block, end_block):

    processing = []
    inputs = []
    outputs = []
    processor_type = parseProcessorType(processor)
    if state == "pending" or state == "finished":
        pre_sql="SELECT start_txn_id, start_block_number, finish_txn_id, finish_block_number, caller_address, crew_id, process_id, process_name, processor_id, processor_type, processor_asteroid_id, processor_lot_id, processor_slot, processor_label, origin_id, origin_type, origin_asteroid_id, origin_lot_id, origin_slot, origin_label, destination_id, destination_type, destination_asteroid_id, destination_lot_id, destination_slot, destination_label "
        print(pre_sql)
        if state == "pending":
            status = 1
        elif state == "finished":
            status = 2
        if parameter1 == "wallet":
            from_sql=("FROM processing_actions WHERE caller_address = '%s' AND processor_type = %s AND status = %s AND start_block_number > %s" % (parameter2, processor_type, status, start_block))
        elif parameter1 == "crew":
            from_sql=("FROM processing_actions WHERE crew_id = %s AND processor_type = %s AND status = %s AND start_block_number > %s" % (parameter2, processor_type, status, start_block))
            print("from_sql: %s" % from_sql)
        if status == 2 and end_block > 0:
            finish_sql=(" AND finish_block_number <= %s ORDER BY start_block_number" % end_block)
        else:
            finish_sql=" ORDER BY start_block_number"
        
    elif state == "started":
        pre_sql="SELECT txn_id, block_number, NULL, NULL, caller_address, caller_crew_id, process_id, process_name, processor_id, processor_type, processor_asteroid_id, processor_lot_id, processor_slot, processor_label, origin_id, origin_type, origin_asteroid_id, origin_lot_id, origin_slot, origin_label, destination_id, destination_type, destination_asteroid_id, destination_lot_id, destination_slot, destination_label "
        print(pre_sql)
        if parameter1 == "wallet":
            from_sql=("FROM dispatcher_material_processing_started_v1 WHERE caller_address = '%s' AND processor_type = %s AND block_number > %s" % (parameter2, processor_type, start_block))
        elif parameter1 == "crew":
            from_sql=("FROM dispatcher_material_processing_started_v1 WHERE caller_crew_id = %s AND processor_type = %s AND block_number > %s" % (parameter2, processor_type, start_block))
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
        return processing

    for row in rows:
        start_txn_id=row[0]
        start_block_number=row[1]
        finish_txn_id=row[2]
        finish_block_number=row[3]
        caller_address=row[4]
        crew_id=row[5]
        process_id=row[6]
        process_name=row[7]
        processor_id=row[8]
        processor_type=row[9]
        processor_asteroid_id=row[10]
        processor_lot_id=row[11]
        processor_slot=row[12]
        processor_label=row[13]
        origin_id=row[14]
        origin_type=row[15]
        origin_asteroid_id=row[16]
        origin_lot_id=row[17]
        origin_slot=row[18]
        origin_label=row[19]
        destination_id=row[20]
        destination_type=row[21]
        destination_asteroid_id=row[22]
        destination_lot_id=row[23]
        destination_slot=row[24]
        destination_label=row[25]

        inputs=getInputs(con, start_txn_id)
        outputs=getOutputs(con, start_txn_id)

        processing.append({"start_txn_id": start_txn_id, "start_block_number": start_block_number, "finish_txn_id": finish_txn_id, "finish_block_number": finish_block_number, "caller_address": caller_address, "crew_id": crew_id, "process_id": process_id, "process_name": process_name, "processor_id": processor_id, "processor_type": processor_type, "processor_asteroid_id": processor_asteroid_id, "processor_asteroid_id": processor_asteroid_id, "processor_lot_id": processor_lot_id, "processor_slot": processor_slot, "processor_label": processor_label, "origin_id": origin_id, "origin_type": origin_type, "origin_asteroid_id": origin_asteroid_id, "origin_lot_id": origin_lot_id, "origin_slot": origin_slot, "origin_label": origin_label, "destination_id": destination_id, "destination_type": destination_type, "destination_asteroid_id": destination_asteroid_id, "destination_lot_id": destination_lot_id, "destination_slot": destination_slot, "destination_label": destination_label, "inputs": inputs, "outputs": outputs})

    return processing


def getProcessingOnAsteroid(con, asteroid_id, parameter1, parameter2, state, processor, start_block, end_block):

    processing = []
    inputs = []
    outputs = []
    processor_type = parseProcessorType(processor)
    if state == "pending" or state == "finished":
        pre_sql="SELECT start_txn_id, start_block_number, finish_txn_id, finish_block_number, caller_address, crew_id, process_id, process_name, processor_id, processor_type, processor_asteroid_id, processor_lot_id, processor_slot, processor_label, origin_id, origin_type, origin_asteroid_id, origin_lot_id, origin_slot, origin_label, destination_id, destination_type, destination_asteroid_id, destination_lot_id, destination_slot, destination_label "
        print(pre_sql)
        if state == "pending":
            status = 1
        elif state == "finished":
            status = 2
        if parameter1 == "wallet":
            from_sql=("FROM processing_actions WHERE caller_address = '%s' AND processor_type = %s AND processor_asteroid_id = %s AND status = %s AND start_block_number > %s" % (parameter2, processor_type, asteroid_id, status, start_block))
        elif parameter1 == "crew":
            from_sql=("FROM processing_actions WHERE crew_id = %s AND processor_type = %s AND processor_asteroid_id = %s AND status = %s AND start_block_number > %s" % (parameter2, processor_type, asteroid_id, status, start_block))
            print("from_sql: %s" % from_sql)
        if status == 2 and end_block > 0:
            finish_sql=(" AND finish_block_number <= %s ORDER BY start_block_number" % end_block)
        else:
            finish_sql=" ORDER BY start_block_number"

    elif state == "started":
        pre_sql="SELECT start_txn_id, start_block_number, finish_txn_id, finish_block_number, caller_address, caller_crew_id, process_id, process_name, processor_id, processor_type, processor_asteroid_id, processor_lot_id, processor_slot, processor_label, origin_id, origin_type, origin_asteroid_id, origin_lot_id, origin_slot, origin_label, destination_id, destination_type, destination_asteroid_id, destination_lot_id, destination_slot, destination_label "
        print(pre_sql)
        if parameter1 == "wallet":
            from_sql=("FROM dispatcher_material_processing_started_v1 WHERE caller_address = '%s' AND processor_type = %s AND processor_asteroid_id = %s AND block_number > %s" % (parameter2, processor_type, asteroid_id, start_block))
        elif parameter1 == "crew":
            from_sql=("FROM dispatcher_material_processing_started_v1 WHERE caller_crew_id = %s AND processor_type = %s AND processor_asteroid_id = %s AND block_number > %s" % (parameter2, processor_type, asteroid_id, start_block))
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
        return processing

    for row in rows:
        start_txn_id=row[0]
        start_block_number=row[1]
        finish_txn_id=row[2]
        finish_block_number=row[3]
        caller_address=row[4]
        crew_id=row[5]
        process_id=row[6]
        process_name=row[7]
        processor_id=row[8]
        processor_type=row[9]
        processor_asteroid_id=row[10]
        processor_lot_id=row[11]
        processor_slot=row[12]
        processor_label=row[13]
        origin_id=row[14]
        origin_type=row[15]
        origin_asteroid_id=row[16]
        origin_lot_id=row[17]
        origin_slot=row[18]
        origin_label=row[19]
        destination_id=row[20]
        destination_type=row[21]
        destination_asteroid_id=row[22]
        destination_lot_id=row[23]
        destination_slot=row[24]
        destination_label=row[25]

        inputs=getInputs(con, start_txn_id)
        outputs=getOutputs(con, start_txn_id)

        processing.append({"start_txn_id": start_txn_id, "start_block_number": start_block_number, "finish_txn_id": finish_txn_id, "finish_block_number": finish_block_number, "caller_address": caller_address, "crew_id": crew_id, "process_id": process_id, "process_name": process_name, "processor_id": processor_id, "processor_type": processor_type, "processor_asteroid_id": processor_asteroid_id, "processor_asteroid_id": processor_asteroid_id, "processor_lot_id": processor_lot_id, "processor_slot": processor_slot, "processor_label": processor_label, "origin_id": origin_id, "origin_type": origin_type, "origin_asteroid_id": origin_asteroid_id, "origin_lot_id": origin_lot_id, "origin_slot": origin_slot, "origin_label": origin_label, "destination_id": destination_id, "destination_type": destination_type, "destination_asteroid_id": destination_asteroid_id, "destination_lot_id": destination_lot_id, "destination_slot": destination_slot, "destination_label": destination_label, "inputs": inputs, "outputs": outputs})

    return processing


def getProcessingOnLot(con, asteroid_id, lot_id, parameter1, parameter2, state, processor, start_block, end_block):

    processing = []
    inputs = []
    outputs = []
    processor_type = parseProcessorType(processor)
    if state == "pending" or state == "finished":
        pre_sql="SELECT start_txn_id, start_block_number, finish_txn_id, finish_block_number, caller_address, crew_id, process_id, process_name, processor_id, processor_type, processor_asteroid_id, processor_lot_id, processor_slot, processor_label, origin_id, origin_type, origin_asteroid_id, origin_lot_id, origin_slot, origin_label, destination_id, destination_type, destination_asteroid_id, destination_lot_id, destination_slot, destination_label "
        print(pre_sql)
        if state == "pending":
            status = 1
        elif state == "finished":
            status = 2
        if parameter1 == "wallet":
            from_sql=("FROM processing_actions WHERE caller_address = '%s' AND processor_type = %s AND processor_asteroid_id = %s AND processor_lot_id = %s AND status = %s AND start_block_number > %s" % (parameter2, processor_type, asteroid_id, lot_id, status, start_block))
        elif parameter1 == "crew":
            from_sql=("FROM processing_actions WHERE crew_id = %s AND processor_type = %s AND processor_asteroid_id = %s AND processor_lot_id = %s AND status = %s AND start_block_number > %s" % (parameter2, processor_type, asteroid_id, lot_id, status, start_block))
            print("from_sql: %s" % from_sql)
        if status == 2 and end_block > 0:
            finish_sql=(" AND finish_block_number <= %s ORDER BY start_block_number" % end_block)
        else:
            finish_sql=" ORDER BY start_block_number"

    elif state == "started":
        pre_sql="SELECT start_txn_id, start_block_number, finish_txn_id, finish_block_number, caller_address, caller_crew_id, process_id, process_name, processor_id, processor_type, processor_asteroid_id, processor_lot_id, processor_slot, processor_label, origin_id, origin_type, origin_asteroid_id, origin_lot_id, origin_slot, origin_label, destination_id, destination_type, destination_asteroid_id, destination_lot_id, destination_slot, destination_label "
        print(pre_sql)
        if parameter1 == "wallet":
            from_sql=("FROM dispatcher_material_processing_started_v1 WHERE caller_address = '%s' AND processor_type = %s AND processor_asteroid_id = %s AND processor_lot_id = %s AND block_number > %s" % (parameter2, processor_type, asteroid_id, lot_id, start_block))
        elif parameter1 == "crew":
            from_sql=("FROM dispatcher_material_processing_started_v1 WHERE caller_crew_id = %s AND processor_type = %s AND processor_asteroid_id = %s AND processor_lot_id = %s AND block_number > %s" % (parameter2, processor_type, asteroid_id, lot_id, start_block))
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
        return processing

    for row in rows:
        start_txn_id=row[0]
        start_block_number=row[1]
        finish_txn_id=row[2]
        finish_block_number=row[3]
        caller_address=row[4]
        crew_id=row[5]
        process_id=row[6]
        process_name=row[7]
        processor_id=row[8]
        processor_type=row[9]
        processor_asteroid_id=row[10]
        processor_lot_id=row[11]
        processor_slot=row[12]
        processor_label=row[13]
        origin_id=row[14]
        origin_type=row[15]
        origin_asteroid_id=row[16]
        origin_lot_id=row[17]
        origin_slot=row[18]
        origin_label=row[19]
        destination_id=row[20]
        destination_type=row[21]
        destination_asteroid_id=row[22]
        destination_lot_id=row[23]
        destination_slot=row[24]
        destination_label=row[25]

        inputs=getInputs(con, start_txn_id)
        outputs=getOutputs(con, start_txn_id)

        processing.append({"start_txn_id": start_txn_id, "start_block_number": start_block_number, "finish_txn_id": finish_txn_id, "finish_block_number": finish_block_number, "caller_address": caller_address, "crew_id": crew_id, "process_id": process_id, "process_name": process_name, "processor_id": processor_id, "processor_type": processor_type, "processor_asteroid_id": processor_asteroid_id, "processor_asteroid_id": processor_asteroid_id, "processor_lot_id": processor_lot_id, "processor_slot": processor_slot, "processor_label": processor_label, "origin_id": origin_id, "origin_type": origin_type, "origin_asteroid_id": origin_asteroid_id, "origin_lot_id": origin_lot_id, "origin_slot": origin_slot, "origin_label": origin_label, "destination_id": destination_id, "destination_type": destination_type, "destination_asteroid_id": destination_asteroid_id, "destination_lot_id": destination_lot_id, "destination_slot": destination_slot, "destination_label": destination_label, "inputs": inputs, "outputs": outputs})

    return processing


def getSearchComponent(con, parameter1, parameter2, parameter3, parameter4, processor, start_block, end_block):

    processing = []
    inputs = []
    outputs = []
    processor_type = parseProcessorType(processor)
    if parameter3 == "inputs":
        table_name = "dispatcher_material_processing_started_inputs"
    elif parameter3 == "outputs":
        table_name = "dispatcher_material_processing_started_outputs"

    pre_sql="SELECT txn_id "

    if parameter1 == "wallet":
        from_sql=("FROM %s WHERE resource_id = %s AND caller_address = '%s' AND block_number > %s" % (table_name, parameter4, parameter2, start_block))
    elif parameter2 == "crew":
        from_sql=("FROM %s WHERE resource_id = %s AND AND crew_id = %s AND block_number > %s" % (table_name, parameter4, parameter2, start_block))

    if end_block > 0:
        finish_sql=(" AND block_number <= %s ORDER BY block_number" % end_block)
    else:
        finish_sql=" ORDER BY block_number"

    sql1 = pre_sql + from_sql + finish_sql
    print(sql1)

    with con:
        cur = con.cursor()
        cur.execute("%s" % sql1)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return processing

    txns = []
    for row in rows:
        txn_id=row[0]
        txns.append(txn_id)

        if processor is None:
            sql2=("SELECT start_txn_id, start_block_number, finish_txn_id, finish_block_number, caller_address, crew_id, process_id, process_name, processor_id, processor_type, processor_asteroid_id, processor_lot_id, processor_slot, processor_label, origin_id, origin_type, origin_asteroid_id, origin_lot_id, origin_slot, origin_label, destination_id, destination_type, destination_asteroid_id, destination_lot_id, destination_slot, destination_label FROM processing_actions WHERE start_txn_id = '%s' AND status = 2" % txn_id)
        else:
            sql2=("SELECT start_txn_id, start_block_number, finish_txn_id, finish_block_number, caller_address, crew_id, process_id, process_name, processor_id, processor_type, processor_asteroid_id, processor_lot_id, processor_slot, processor_label, origin_id, origin_type, origin_asteroid_id, origin_lot_id, origin_slot, origin_label, destination_id, destination_type, destination_asteroid_id, destination_lot_id, destination_slot, destination_label FROM processing_actions WHERE start_txn_id = '%s' AND processor_type = %s AND status = 2" % (txn_id, processor_type))

        print(sql2)
        with con:
            cur = con.cursor()
            cur.execute("%s" % sql2)
            rows2 = cur.fetchall()
            cur.close()

        if rows2 == None:
            return processing

        for row2 in rows2:
            start_txn_id=row2[0]
            start_block_number=row2[1]
            finish_txn_id=row2[2]
            finish_block_number=row2[3]
            caller_address=row2[4]
            crew_id=row2[5]
            process_id=row2[6]
            process_name=row2[7]
            processor_id=row2[8]
            processor_type=row2[9]
            processor_asteroid_id=row2[10]
            processor_lot_id=row2[11]
            processor_slot=row2[12]
            processor_label=row2[13]
            origin_id=row2[14]
            origin_type=row2[15]
            origin_asteroid_id=row2[16]
            origin_lot_id=row2[17]
            origin_slot=row2[18]
            origin_label=row2[19]
            destination_id=row2[20]
            destination_type=row2[21]
            destination_asteroid_id=row2[22]
            destination_lot_id=row2[23]
            destination_slot=row2[24]
            destination_label=row2[25]

            inputs=getInputs(con, start_txn_id)
            outputs=getOutputs(con, start_txn_id)

            processing.append({"start_txn_id": start_txn_id, "start_block_number": start_block_number, "finish_txn_id": finish_txn_id, "finish_block_number": finish_block_number, "caller_address": caller_address, "crew_id": crew_id, "process_id": process_id, "process_name": process_name, "processor_id": processor_id, "processor_type": processor_type, "processor_asteroid_id": processor_asteroid_id, "processor_asteroid_id": processor_asteroid_id, "processor_lot_id": processor_lot_id, "processor_slot": processor_slot, "processor_label": processor_label, "origin_id": origin_id, "origin_type": origin_type, "origin_asteroid_id": origin_asteroid_id, "origin_lot_id": origin_lot_id, "origin_slot": origin_slot, "origin_label": origin_label, "destination_id": destination_id, "destination_type": destination_type, "destination_asteroid_id": destination_asteroid_id, "destination_lot_id": destination_lot_id, "destination_slot": destination_slot, "destination_label": destination_label, "inputs": inputs, "outputs": outputs})

    return processing


def processingState(parameter1, parameter2, state, processor, start_block, end_block):

    processing = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    processing = getProcessingState(con, parameter1, parameter2, state, processor, start_block, end_block)
    con.close()
    return processing
    

def processingOnAsteroid(asteroid_id, parameter1, parameter2, state, processor, start_block, end_block):

    processing = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    processing = getProcessingOnAsteroid(con, asteroid_id, parameter1, parameter2, state, processor, start_block, end_block)
    con.close()
    return processing


def processingOnLot(asteroid_id, lot_id, parameter1, parameter2, state, processor, start_block, end_block):

    processing = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    processing = getProcessingOnLot(con, asteroid_id, lot_id, parameter1, parameter2, state, processor, start_block, end_block)
    con.close()
    return processing


def processingSearchComponent(parameter1, parameter2, parameter3, parameter4, processor, start_block, end_block):

    processing = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    processing = getSearchComponent(con, parameter1, parameter2, parameter3, parameter4, processor, start_block, end_block)
    con.close()
    return processing

