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

import db.crew_db as crew_db
import db.txn_db as txn_db

filename = __file__
config_path = filename.split('/')[3]
phase = config_path.split('_')[1]
config_file = "/home/bios/" + config_path + "/indexer.conf"
mongo_table = phase + "-crew-events"

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
                .with_from_address(crew_address)
                .with_keys([crew_transfer_key])
            ),
            starting_cursor=starknet_cursor(starting_block),
            finality=DataFinality.DATA_STATUS_ACCEPTED,
        )


    async def handle_data(self, info: Info, data: Block):

        # Handle one block of data

        block_number = int(info.end_cursor.order_key)
        txns = []

        for event_with_tx in data.events:
            event = event_with_tx.event
            tx_hash = felt.to_hex(event_with_tx.transaction.meta.hash)
            from_address = felt.to_hex(event_with_tx.transaction.invoke_v1.sender_address)
            receipt = event_with_tx.receipt
            event_hex = event.keys[0]
            fee = round((felt.to_int(receipt.actual_fee) / 1000000000))
            timestamp = data.header.timestamp.seconds
            timestamp = strftime('%Y-%m-%d %H:%M:%S', localtime(timestamp))

            if tx_hash not in txns:
                txns.append(tx_hash)

            if event_hex == crew_transfer_key:
                await processCrewTransfer(tx_hash, event, block_number, fee, timestamp)

        if len(txns) > 0:
            txn_db.txnCounter(block_number, len(txns), timestamp, "crew_txns_per_block")


    async def handle_invalidate(self, _info: Info, _cursor: Cursor):
        raise ValueError("data must be finalized")


async def processCrewTransfer(tx_hash, event, block_number, fee, timestamp):

    event_type = "CrewTransfer"
    from_address = felt.to_hex(event.data[0])
    to_address = felt.to_hex(event.data[1])
    token_id = felt.to_int(event.data[2])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, to_addr: %s, token_id: %s" % (block_number, event_type, tx_hash, from_address, to_address, token_id))
    crew_db.crewTransfer(tx_hash, block_number, from_address, to_address, token_id, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "crew")


async def main():

    global con
    global crew_address
    global crew_transfer_key
    global starting_block

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
        crew_address = felt.from_hex(config.get('contracts', 'crew_address'))
        crew_transfer_key = felt.from_hex(config.get('selectors', 'transfer_key'))

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
        reset_state=restart,
        timeout=90
    )

    dispatcher_name = "starknet-" + network
    await runner.run(DispatcherIndexer(), ctx={"network": dispatcher_name})

if __name__ == "__main__":
    asyncio.run(main())
