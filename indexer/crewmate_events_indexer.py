#!/home/bios/.pyenv/shims/python3

import asyncio
import logging
import os
import sys
import pymysql
import warnings
import traceback
import configparser
from time import strftime, localtime

from apibara.indexer import IndexerRunner, IndexerRunnerConfiguration, Info
from apibara.indexer.indexer import IndexerConfiguration
from apibara.protocol.proto.stream_pb2 import Cursor, DataFinality
from apibara.starknet import EventFilter, Filter, StarkNetIndexer, felt
from apibara.starknet.cursor import starknet_cursor
from apibara.starknet.proto.starknet_pb2 import Block
from apibara.indexer.indexer import Reconnect

import db.crewmate_db as crewmate_db
import db.txn_db as txn_db
import sdk.grab_file as grab

filename = __file__
config_path = filename.split('/')[3]
phase = config_path.split('_')[1]
config_file = "/home/bios/" + config_path + "/indexer.conf"
mongo_table = phase + "-crewmate-events"

root_logger = logging.getLogger("apibara")
# change to `logging.DEBUG` to print more information
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(logging.StreamHandler())

class DispatcherIndexer(StarkNetIndexer):
    def indexer_id(self) -> str:
        return mongo_table

    async def handle_reconnect(self, exc: Exception, retry_count: int) -> Reconnect:
        # check some conditions, optionally sleep
        await asyncio.sleep(10)
        return Reconnect(reconnect=True)

    def initial_configuration(self) -> Filter:
        # Return initial configuration of the indexer.
        return IndexerConfiguration(
            filter=Filter()
            .with_header(weak=False)
            .add_event(
                EventFilter()
                .with_from_address(crewmate_address)
                .with_keys([crewmate_transfer_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(crewmate_address)
                .with_keys([bridged_from_l1_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(crewmate_address)
                .with_keys([bridged_to_l1_key])
            ),
            #starting_cursor=starknet_cursor(847_000),
            starting_cursor=starknet_cursor(starting_block),
            finality=DataFinality.DATA_STATUS_ACCEPTED,
        )


    async def handle_data(self, info: Info, data: Block):

        block_number = int(info.end_cursor.order_key)
        txns = []

        # Handle one block of data
        for event_with_tx in data.events:
            event = event_with_tx.event
            from_address = felt.to_hex(event_with_tx.transaction.invoke_v1.sender_address)
            tx_hash = felt.to_hex(event_with_tx.transaction.meta.hash)
            receipt = event_with_tx.receipt
            event_hex = event.keys[0]
            fee = round((felt.to_int(receipt.actual_fee) / 1000000000))
            timestamp = data.header.timestamp.seconds
            timestamp = strftime('%Y-%m-%d %H:%M:%S', localtime(timestamp))

            if tx_hash not in txns:
                txns.append(tx_hash)

            if event_hex == crewmate_transfer_key:
                await processCrewmateTransfer(tx_hash, event, block_number, fee, timestamp)

            if event_hex == bridged_from_l1_key:
                from_address = felt.to_hex(event_with_tx.event.from_address)
                await processBridgedFromL1(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == bridged_to_l1_key:
                await processBridgedToL1(tx_hash, event, block_number, from_address, fee, timestamp)

        if len(txns) > 0:
            txn_db.txnCounter(block_number, len(txns), timestamp, "crewmate_txns_per_block")


    async def handle_invalidate(self, _info: Info, _cursor: Cursor):
        raise ValueError("data must be finalized")


async def processCrewmateTransfer(tx_hash, event, block_number, fee, timestamp):

    event_type = "CrewmateTransfer"
    from_address = felt.to_hex(event.data[0])
    to_address = felt.to_hex(event.data[1])
    crewmate_id = felt.to_int(event.data[2])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, crewmate_id: %s, to_addr: %s" % (block_number, event_type, tx_hash, from_address, crewmate_id, to_address))
    crewmate_db.crewmatesTransfer(tx_hash, block_number, crewmate_id, from_address, to_address, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "crewmate")


async def processBridgedFromL1(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type = "BridgedFromL1"
    crewmate_id = felt.to_int(event.data[0])
    to_address = felt.to_hex(event.data[2])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, crewmate_id: %s, to_addr: %s" % (block_number, event_type, tx_hash, from_address, crewmate_id, to_address))
    grab.snagCrewmate(crewmate_id, crewmates_storage, network)
    crewmate_db.bridgedFromL1(tx_hash, block_number, from_address, crewmate_id, to_address, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "crewmate")


async def processBridgedToL1(tx_hash, event, block_number, from_address, fee, timestamp):

    print("tx_hash: %s" % tx_hash)
    event_type = "BridgedToL1"
    crewmate_id = felt.to_int(event.data[0])
    from_address = felt.to_hex(event.data[1])
    eth_address = hex(felt.to_int(event.data[3]))

    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, crewmate_id: %s, eth_address: %s" % (block_number, event_type, tx_hash, from_address, crewmate_id, eth_address))
    crewmate_db.bridgedToL1(tx_hash, block_number, from_address, crewmate_id, eth_address, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "crewmate")


async def main():

    global starting_block
    global crewmates_storage
    global network
    global crewmate_address
    global crewmate_transfer_key
    global bridged_from_l1_key
    global bridged_to_l1_key

    if os.path.exists(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        testnet_node_url = config.get('blockchain', 'testnet_pathfinder')
        mainnet_node_url = config.get('blockchain', 'mainnet_pathfinder')
        network = config.get('blockchain', 'network')
        starting_block = int(config.get('indexer', 'starting_block'))
        dna_url = config.get('indexer', 'dna_url')
        dna_restart = config.get('indexer', 'dna_restart')
        mongo_url = config.get('mongodb', 'mongo_url')
        crewmates_storage = config.get('storage', 'crewmates')
        crewmate_address = felt.from_hex(config.get('contracts', 'crewmate_address'))
        crewmate_transfer_key = felt.from_hex(config.get('selectors', 'transfer_key'))
        bridged_from_l1_key = felt.from_hex(config.get('selectors', 'bridged_from_l1_key'))
        bridged_to_l1_key = felt.from_hex(config.get('selectors', 'bridged_to_l1_key'))

    else:
        raise Exception(config_file)

    if dna_restart == 'False':
        dna_restart = False
    else:
        dna_restart = True

    restart = dna_restart

    runner = IndexerRunner(
        config=IndexerRunnerConfiguration(
            stream_url=dna_url,
            storage_url=mongo_url,
            stream_ssl=False,
        ),
        client_options=[
            ("grpc.max_receive_message_length", 256 * 1_000_000),  # ~256 MB
        ],
        reset_state=restart,
        timeout=90
    )

    dispatcher_name = "starknet-" + network
    await runner.run(DispatcherIndexer(), ctx={"network": dispatcher_name})

if __name__ == "__main__":
    asyncio.run(main())
