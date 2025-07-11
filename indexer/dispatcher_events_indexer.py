#!/home/bios/.pyenv/shims/python3

import asyncio
import logging
import os
import sys
import pymysql
import warnings
import traceback
import configparser
import time
from time import strftime, localtime

from apibara.indexer import IndexerRunner, IndexerRunnerConfiguration, Info
from apibara.indexer.indexer import IndexerConfiguration
from apibara.protocol.proto.stream_pb2 import Cursor, DataFinality
from apibara.starknet import EventFilter, Filter, StarkNetIndexer, felt
from apibara.starknet.cursor import starknet_cursor
from apibara.starknet.proto.starknet_pb2 import Block
from apibara.indexer.indexer import Reconnect
from apibara.starknet import TransactionFilter

import db.dispatcher_db as dispatcher_db
import db.txn_db as txn_db
import sdk.sdk as sdk
import sdk.types as types
import sdk.grab_file as grab

filename = __file__
config_path = filename.split('/')[3]
phase = config_path.split('_')[1]
config_file = "/home/bios/" + config_path + "/indexer.conf"
mongo_table = phase + "-dispatcher-events"

root_logger = logging.getLogger("apibara")
# change to `logging.DEBUG` to print more information
#root_logger.setLevel(logging.INFO)
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(logging.StreamHandler())

class DispatcherIndexer(StarkNetIndexer):
    def indexer_id(self) -> str:
        #return "testnet-dispatcher-events"
        return mongo_table

    async def handle_reconnect(self, exc: Exception, retry_count: int) -> Reconnect:
        # check some conditions, optionally sleep
        await asyncio.sleep(10)
        return Reconnect(reconnect=True)

    def initial_configuration(self) -> Filter:
        # Return initial configuration of the indexer.
        return IndexerConfiguration(
            filter = Filter()
            .with_header(weak=False)
            .add_transaction(
                TransactionFilter.any()
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([system_registered_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([surface_scan_started_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([suface_scan_finished_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([crewmate_recruited_v1_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([asteroid_managed_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([asteroid_initialized_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([asteroid_purchased_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([crewmate_purchased_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([crewmate_arranged_v1_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([crewmates_exchanged_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([constant_registered_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([contract_registered_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([public_policy_assigned_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([crew_formed_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([construction_deconstructed_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([crewmate_recruited_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([component_updated_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([resource_scan_started_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([resource_scan_finished_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([construction_planned_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([construction_started_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([construction_finished_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([name_changed_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([sampling_deposit_started_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([sampling_deposit_finished_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([sampling_deposit_started_v1_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([delivery_started_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([delivery_finished_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([delivery_finished_v1_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([construction_abandoned_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([resource_extraction_started_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([resource_extraction_finished_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([material_processing_started_v1_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([material_processing_finished_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([food_supplied_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([food_supplied_v1_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([ship_undocked_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([ship_docked_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([crew_stationed_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([crew_stationed_v1_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([ship_assembly_started_v1_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([ship_assembly_finished_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([emergency_propellant_collected_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([emergency_activated_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([emergency_deactivated_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([delivery_sent_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([delivery_received_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([delivery_packaged_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([delivery_packaged_v1_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([delivery_cancelled_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([contract_agreement_accepted_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([prepaid_merkle_agreement_accepted_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([prepaid_agreement_accepted_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([prepaid_agreement_extended_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([prepaid_agreement_cancelled_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([removed_from_whitelist_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([removed_from_whitelist_v1_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([added_to_whitelist_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([added_to_whitelist_v1_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([added_account_to_whitelist_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([ship_commandeered_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([lot_reclaimed_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([building_repossessed_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([crew_delegated_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([crew_ejected_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([deposit_listed_for_sale_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([deposit_purchased_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([deposit_purchased_v1_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([deposit_unlisted_for_sale_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([sell_order_created_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([sell_order_filled_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([sell_order_cancelled_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([buy_order_created_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([buy_order_filled_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([buy_order_cancelled_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([contract_policy_assigned_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([prepaid_merkle_policy_assigned_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([prepaid_policy_assigned_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([contract_policy_removed_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([prepaid_policy_removed_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([prepaid_merkle_policy_removed_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([public_policy_removed_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([random_event_resolved_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([transit_finished_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([transit_started_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([arrival_reward_claimed_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([prepare_for_launch_reward_claimed_key])
            )
            .add_event(
                EventFilter()
                .with_from_address(dispatcher_address)
                .with_keys([exchange_configured_key])
            ),
            #starting_cursor=starknet_cursor(846_000),
            starting_cursor=starknet_cursor(starting_block),
            finality=DataFinality.DATA_STATUS_ACCEPTED,
        )

    async def handle_data(self, info: Info, data: Block):

        block_number = int(info.end_cursor.order_key)
        print("block_number: %s" % block_number)
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

            if event_hex == system_registered_key:
                await processSystemRegistered(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == surface_scan_started_key:
                await processSurfaceScanStarted(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == suface_scan_finished_key:
                await processSurfaceScanFinished(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == crewmate_recruited_v1_key:
                await processCrewmateRecruitedV1(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == crewmate_recruited_key:
                await processCrewmateRecruited(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == crew_formed_key:
                await processCrewFormed(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == asteroid_initialized_key:
                await processAsteroidInitialized(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == asteroid_managed_key:
                await processAsteroidManaged(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == asteroid_purchased_key:
                await processAsteroidPurchased(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == crewmate_purchased_key:
                await processCrewmatePurchased(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == crewmate_arranged_v1_key:
                await processCrewmateArrangedV1(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == crewmates_exchanged_key:
                await processCrewmatesExchanged(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == constant_registered_key:
                await processConstantRegistered(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == contract_registered_key:
                await processContractRegistered(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == public_policy_assigned_key:
                await processPublicPolicyAssigned(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == name_changed_key:
                await processNameChanged(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == resource_scan_started_key:
                await processResourceScanStarted(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == resource_scan_finished_key:
                await processResourceScanFinished(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == construction_planned_key:
                await processConstructionPlanned(tx_hash, event, block_number, from_address, fee, timestamp)
                events_count = 0
                for row in receipt.events:
                    events_count+=1
                if events_count > 9:
                    seed_events = data.events
                    index = event.index
                    await processColonySeed(tx_hash, event, block_number, from_address, index, seed_events, fee, timestamp)

            if event_hex == construction_started_key:
                await processConstructionStarted(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == construction_finished_key:
                start_inventory = []
                for inventory_event_with_tx in data.events:
                    embedded_tx_hash = felt.to_hex(inventory_event_with_tx.transaction.meta.hash)
                    if embedded_tx_hash == tx_hash:
                        inventory_event = inventory_event_with_tx.event
                        inventory_event_hex = inventory_event.keys[0]
                        selector_hex = felt.to_hex(inventory_event_hex)
                        if inventory_event_hex == component_updated_key:
                            event_key = felt.to_hex(inventory_event.keys[0])
                            event_name = bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode()
                            if bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode() == 'Inventory':
                                if inventory_event.index == 5:
                                    start_inventory = await processInventory(inventory_event, "construction")

                await processConstructionFinished(tx_hash, event, block_number, from_address, start_inventory, fee, timestamp)

            if event_hex == construction_abandoned_key:
                await processConstructionAbandoned(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == sampling_deposit_started_key:
                await processSamplingDepositStarted(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == sampling_deposit_finished_key:
                await processSamplingDepositFinished(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == sampling_deposit_started_v1_key:
                inventory_event = None
                origin_inventory = []
                for inventory_event_with_tx in data.events:
                    embedded_tx_hash = felt.to_hex(inventory_event_with_tx.transaction.meta.hash)
                    if embedded_tx_hash == tx_hash:
                        inventory_event = inventory_event_with_tx.event
                        inventory_event_hex = inventory_event.keys[0]
                        selector_hex = felt.to_hex(inventory_event_hex)
                        if inventory_event_hex == component_updated_key:
                            event_key = felt.to_hex(inventory_event.keys[0])
                            event_name = bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode()
                            if bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode() == 'Inventory':
                                if inventory_event.index == 0:
                                    origin_inventory = await processInventory(inventory_event, "sampling")

                await processSamplingDepositStartedV1(tx_hash, event, block_number, from_address, origin_inventory, fee, timestamp)

            if event_hex == delivery_started_key:
                origin_inventory = []
                for inventory_event_with_tx in data.events:
                    embedded_tx_hash = felt.to_hex(inventory_event_with_tx.transaction.meta.hash)
                    if embedded_tx_hash == tx_hash:
                        inventory_event = inventory_event_with_tx.event
                        inventory_event_hex = inventory_event.keys[0]
                        selector_hex = felt.to_hex(inventory_event_hex)
                        if inventory_event_hex == component_updated_key:
                            event_key = felt.to_hex(inventory_event.keys[0])
                            event_name = bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode()
                            if bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode() == 'Inventory':
                                if inventory_event.index == 0:
                                    origin_inventory = await processInventory(inventory_event, "delivery")

                await processDeliveryStarted(tx_hash, event, block_number, from_address, origin_inventory, fee, timestamp)

            if event_hex == delivery_finished_key:
                destination_inventory = []
                for inventory_event_with_tx in data.events:
                    embedded_tx_hash = felt.to_hex(inventory_event_with_tx.transaction.meta.hash)
                    if embedded_tx_hash == tx_hash:
                        inventory_event = inventory_event_with_tx.event
                        inventory_event_hex = inventory_event.keys[0]
                        selector_hex = felt.to_hex(inventory_event_hex)
                        if inventory_event_hex == component_updated_key:
                            event_key = felt.to_hex(inventory_event.keys[0])
                            event_name = bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode()
                            if bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode() == 'Inventory':
                                if inventory_event.index == 0:
                                    destination_inventory = await processInventory(inventory_event, "delivery")

                await processDeliveryFinished(tx_hash, event, block_number, from_address, destination_inventory, fee, timestamp)

            if event_hex == delivery_finished_v1_key:
                destination_inventory = []
                for inventory_event_with_tx in data.events:
                    embedded_tx_hash = felt.to_hex(inventory_event_with_tx.transaction.meta.hash)
                    if embedded_tx_hash == tx_hash:
                        inventory_event = inventory_event_with_tx.event
                        inventory_event_hex = inventory_event.keys[0]
                        selector_hex = felt.to_hex(inventory_event_hex)
                        if inventory_event_hex == component_updated_key:
                            event_key = felt.to_hex(inventory_event.keys[0])
                            event_name = bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode()
                            if bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode() == 'Inventory':
                                if inventory_event.index == 0:
                                    destination_inventory = await processInventory(inventory_event, "delivery")

                await processDeliveryFinishedV1(tx_hash, event, block_number, from_address, destination_inventory, fee, timestamp)

            if event_hex == resource_extraction_started_key:
                await processResourceExtractionStarted(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == resource_extraction_finished_key:
                inventory_event = None
                destination_inventory = []
                inventory_event_index = (event.index - 2)
                for inventory_event_with_tx in data.events:
                    embedded_tx_hash = felt.to_hex(inventory_event_with_tx.transaction.meta.hash)
                    if embedded_tx_hash == tx_hash:
                        inventory_event = inventory_event_with_tx.event
                        inventory_event_hex = inventory_event.keys[0]
                        selector_hex = felt.to_hex(inventory_event_hex)
                        if inventory_event_hex == component_updated_key:
                            event_key = felt.to_hex(inventory_event.keys[0])
                            event_name = bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode()
                            if bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode() == 'Inventory':
                                #if inventory_event.index == 0 or inventory_event.index == 1:
                                if inventory_event.index == inventory_event_index:
                                    destination_inventory = await processInventory(inventory_event, "extraction")

                await processResourceExtractionFinished(tx_hash, event, block_number, from_address, destination_inventory, fee, timestamp)

            if event_hex == construction_deconstructed_key:
                await processConstructionDeconstructed(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == material_processing_started_v1_key:
                inventory_event = None
                origin_inventory = []
                for inventory_event_with_tx in data.events:
                    embedded_tx_hash = felt.to_hex(inventory_event_with_tx.transaction.meta.hash)
                    if embedded_tx_hash == tx_hash:
                        inventory_event = inventory_event_with_tx.event
                        inventory_event_hex = inventory_event.keys[0]
                        selector_hex = felt.to_hex(inventory_event_hex)
                        if inventory_event_hex == component_updated_key:
                            event_key = felt.to_hex(inventory_event.keys[0])
                            event_name = bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode()
                            if bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode() == 'Inventory':
                                if inventory_event.index == 0:
                                    origin_inventory = await processInventory(inventory_event, "processing")

                await processMaterialProcessingStartedV1(tx_hash, event, block_number, from_address, origin_inventory, fee, timestamp)

            if event_hex == material_processing_finished_key:
                inventory_event_index = (event.index - 2)
                print("inventory_event_index: %s" % inventory_event_index)

                inventory_event = None
                destination_inventory = []
                for inventory_event_with_tx in data.events:
                    embedded_tx_hash = felt.to_hex(inventory_event_with_tx.transaction.meta.hash)
                    if embedded_tx_hash == tx_hash:
                        inventory_event = inventory_event_with_tx.event
                        inventory_event_hex = inventory_event.keys[0]
                        selector_hex = felt.to_hex(inventory_event_hex)
                        if inventory_event_hex == component_updated_key:
                            event_key = felt.to_hex(inventory_event.keys[0])
                            event_name = bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode()
                            if bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode() == 'Inventory':
                                #if inventory_event.index == 0:
                                if inventory_event.index == inventory_event_index:
                                    destination_inventory = await processInventory(inventory_event, "processing")

                await processMaterialProcessingFinished(tx_hash, event, block_number, from_address, destination_inventory, fee, timestamp)

            if event_hex == food_supplied_key:
                await processFoodSupplied(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == food_supplied_v1_key:
                inventory_event = None
                origin_inventory = []
                for inventory_event_with_tx in data.events:
                    embedded_tx_hash = felt.to_hex(inventory_event_with_tx.transaction.meta.hash)
                    if embedded_tx_hash == tx_hash:
                        inventory_event = inventory_event_with_tx.event
                        inventory_event_hex = inventory_event.keys[0]
                        selector_hex = felt.to_hex(inventory_event_hex)
                        if inventory_event_hex == component_updated_key:
                            event_key = felt.to_hex(inventory_event.keys[0])
                            event_name = bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode()
                            if bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode() == 'Inventory':
                                if inventory_event.index == 0:
                                    origin_inventory = await processInventory(inventory_event, "food_supplied")

                await processFoodSuppliedV1(tx_hash, event, block_number, from_address, origin_inventory, fee, timestamp)

            if event_hex == ship_undocked_key:
                inventory_event = None
                for transit_event_with_tx in data.events:
                    embedded_tx_hash = felt.to_hex(transit_event_with_tx.transaction.meta.hash)
                    if embedded_tx_hash == tx_hash:
                        transit_event_hex = None
                        event_name = None
                        receipt = None
                        selector_hex = None
                        transit_event = transit_event_with_tx.event
                        receipt = event_with_tx.receipt
                        transit_event_hex = transit_event.keys[0]
                        selector_hex = felt.to_hex(transit_event_hex)
                        if transit_event_hex == component_updated_key:
                            event_key = felt.to_hex(transit_event.keys[0])
                            event_name = bytes.fromhex(hex(felt.to_int(transit_event.keys[1]))[2:]).decode()
                            if bytes.fromhex(hex(felt.to_int(transit_event.keys[1]))[2:]).decode() == 'Inventory':
                                if len(transit_event.data) == 12:
                                    inventory_event = transit_event

                await processShipUndocked(tx_hash, event, block_number, from_address, fee, timestamp, inventory_event)


            if event_hex == ship_docked_key:
                inventory_event = None
                for transit_event_with_tx in data.events:
                    embedded_tx_hash = felt.to_hex(transit_event_with_tx.transaction.meta.hash)
                    if embedded_tx_hash == tx_hash:
                        transit_event_hex = None
                        event_name = None
                        receipt = None
                        selector_hex = None
                        transit_event = transit_event_with_tx.event
                        receipt = event_with_tx.receipt
                        transit_event_hex = transit_event.keys[0]
                        selector_hex = felt.to_hex(transit_event_hex)
                        if transit_event_hex == component_updated_key:
                            event_key = felt.to_hex(transit_event.keys[0])
                            event_name = bytes.fromhex(hex(felt.to_int(transit_event.keys[1]))[2:]).decode()
                            if bytes.fromhex(hex(felt.to_int(transit_event.keys[1]))[2:]).decode() == 'Inventory':
                                if len(transit_event.data) == 12:
                                    inventory_event = transit_event

                await processShipDocked(tx_hash, event, block_number, from_address, fee, timestamp, inventory_event)

            if event_hex == ship_assembly_started_v1_key:
                inventory_event = None
                origin_inventory = []
                for inventory_event_with_tx in data.events:
                    embedded_tx_hash = felt.to_hex(inventory_event_with_tx.transaction.meta.hash)
                    if embedded_tx_hash == tx_hash:
                        inventory_event = inventory_event_with_tx.event
                        inventory_event_hex = inventory_event.keys[0]
                        selector_hex = felt.to_hex(inventory_event_hex)
                        if inventory_event_hex == component_updated_key:
                            event_key = felt.to_hex(inventory_event.keys[0])
                            event_name = bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode()
                            if bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode() == 'Inventory':
                                if inventory_event.index == 0:
                                    origin_inventory = await processInventory(inventory_event, "ship")

                await processShipAssemblyStartedV1(tx_hash, event, block_number, from_address, origin_inventory, fee, timestamp)

            if event_hex == ship_assembly_finished_key:
                await processShipAssemblyFinished(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == crew_stationed_key:
                await processCrewStationed(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == crew_stationed_v1_key:
                await processCrewStationedV1(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == emergency_propellant_collected_key:
                inventory_event = None
                for transit_event_with_tx in data.events:
                    embedded_tx_hash = felt.to_hex(transit_event_with_tx.transaction.meta.hash)
                    if embedded_tx_hash == tx_hash:
                        transit_event_hex = None
                        event_name = None
                        receipt = None
                        selector_hex = None
                        transit_event = transit_event_with_tx.event
                        receipt = event_with_tx.receipt
                        transit_event_hex = transit_event.keys[0]
                        selector_hex = felt.to_hex(transit_event_hex)
                        if transit_event_hex == component_updated_key:
                            event_key = felt.to_hex(transit_event.keys[0])
                            event_name = bytes.fromhex(hex(felt.to_int(transit_event.keys[1]))[2:]).decode()
                            if bytes.fromhex(hex(felt.to_int(transit_event.keys[1]))[2:]).decode() == 'Inventory':
                                if len(transit_event.data) >= 12:
                                    inventory_event = transit_event

                await processEmergencyPropellantCollected(tx_hash, event, block_number, from_address, fee, timestamp, inventory_event)

            if event_hex == emergency_activated_key:
                await processEmergencyActivated(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == emergency_deactivated_key:
                inventory_event = None
                for transit_event_with_tx in data.events:
                    embedded_tx_hash = felt.to_hex(transit_event_with_tx.transaction.meta.hash)
                    if embedded_tx_hash == tx_hash:
                        transit_event_hex = None
                        event_name = None
                        receipt = None
                        selector_hex = None
                        transit_event = transit_event_with_tx.event
                        receipt = event_with_tx.receipt
                        transit_event_hex = transit_event.keys[0]
                        selector_hex = felt.to_hex(transit_event_hex)
                        if transit_event_hex == component_updated_key:
                            event_key = felt.to_hex(transit_event.keys[0])
                            event_name = bytes.fromhex(hex(felt.to_int(transit_event.keys[1]))[2:]).decode()
                            if bytes.fromhex(hex(felt.to_int(transit_event.keys[1]))[2:]).decode() == 'Inventory':
                                if len(transit_event.data) == 12:
                                    inventory_event = transit_event

                await processEmergencyDeactivated(tx_hash, event, block_number, from_address, fee, timestamp, inventory_event)

            if event_hex == delivery_sent_key:
                #origin_inventory = []
                destination_inventory = []
                delivery_manifest = []
                sell_order_filled = False
                sell_order_cancelled = False

                for inventory_event_with_tx in data.events:
                    embedded_tx_hash = felt.to_hex(inventory_event_with_tx.transaction.meta.hash)
                    if embedded_tx_hash == tx_hash:
                        inventory_event = inventory_event_with_tx.event
                        inventory_event_hex = inventory_event.keys[0]
                        selector_hex = felt.to_hex(inventory_event_hex)
                        if inventory_event_hex == sell_order_filled_key:
                            sell_order_filled = True

                for inventory_event_with_tx in data.events:
                    embedded_tx_hash = felt.to_hex(inventory_event_with_tx.transaction.meta.hash)
                    if embedded_tx_hash == tx_hash:
                        inventory_event = inventory_event_with_tx.event
                        inventory_event_hex = inventory_event.keys[0]
                        selector_hex = felt.to_hex(inventory_event_hex)
                        if inventory_event_hex == sell_order_cancelled_key:
                            sell_order_cancelled = True

                if sell_order_filled is True:
                    origin_inventory = None
                    for inventory_event_with_tx in data.events:
                        embedded_tx_hash = felt.to_hex(inventory_event_with_tx.transaction.meta.hash)
                        if embedded_tx_hash == tx_hash:
                            inventory_event = inventory_event_with_tx.event
                            inventory_event_hex = inventory_event.keys[0]
                            selector_hex = felt.to_hex(inventory_event_hex)
                            if inventory_event_hex == component_updated_key:
                                event_key = felt.to_hex(inventory_event.keys[0])
                                event_name = bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode()
                                if bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode() == 'Inventory':
                                    destination_inventory = await processInventory(inventory_event, "delivery")

                                if bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode() == 'Delivery':
                                    delivery_manifest = await processDeliveryManifest(inventory_event, "delivery")

                elif sell_order_cancelled is True:
                    origin_inventory = None
                    for inventory_event_with_tx in data.events:
                        embedded_tx_hash = felt.to_hex(inventory_event_with_tx.transaction.meta.hash)
                        if embedded_tx_hash == tx_hash:
                            inventory_event = inventory_event_with_tx.event
                            inventory_event_hex = inventory_event.keys[0]
                            selector_hex = felt.to_hex(inventory_event_hex)
                            if inventory_event_hex == component_updated_key:
                                event_key = felt.to_hex(inventory_event.keys[0])
                                event_name = bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode()
                                if bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode() == 'Delivery':
                                    delivery_manifest = await processDeliveryManifest(inventory_event, "delivery")
                                    destination_inventory = delivery_manifest

                else:
                    origin_inventory = None
                    for inventory_event_with_tx in data.events:
                        embedded_tx_hash = felt.to_hex(inventory_event_with_tx.transaction.meta.hash)
                        if embedded_tx_hash == tx_hash:
                            inventory_event = inventory_event_with_tx.event
                            inventory_event_hex = inventory_event.keys[0]
                            selector_hex = felt.to_hex(inventory_event_hex)
                            if inventory_event_hex == component_updated_key:
                                event_key = felt.to_hex(inventory_event.keys[0])
                                event_name = bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode()
                                if bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode() == 'Inventory':
                                    if inventory_event.index == 0:
                                        destination_inventory = await processInventory(inventory_event, "delivery")

                    for inventory_event_with_tx in data.events:
                        embedded_tx_hash = felt.to_hex(inventory_event_with_tx.transaction.meta.hash)
                        if embedded_tx_hash == tx_hash:
                            inventory_event = inventory_event_with_tx.event
                            inventory_event_hex = inventory_event.keys[0]
                            selector_hex = felt.to_hex(inventory_event_hex)
                            if inventory_event_hex == component_updated_key:
                                event_key = felt.to_hex(inventory_event.keys[0])
                                event_name = bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode()
                                if bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode() == 'Inventory':
                                    if inventory_event.index == 1:
                                        origin_inventory = await processInventory(inventory_event, "delivery")

                    for inventory_event_with_tx in data.events:
                        embedded_tx_hash = felt.to_hex(inventory_event_with_tx.transaction.meta.hash)
                        if embedded_tx_hash == tx_hash:
                            inventory_event = inventory_event_with_tx.event
                            inventory_event_hex = inventory_event.keys[0]
                            selector_hex = felt.to_hex(inventory_event_hex)
                            if inventory_event_hex == component_updated_key:
                                event_key = felt.to_hex(inventory_event.keys[0])
                                event_name = bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode()
                                if bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode() == 'Delivery':
                                    delivery_manifest = await processDeliveryManifest(inventory_event, "delivery")

                await processDeliverySent(tx_hash, event, block_number, from_address, destination_inventory, origin_inventory, delivery_manifest, fee, timestamp)


            if event_hex == delivery_received_key:
                destination_inventory = []
                delivery_manifest = []
                for inventory_event_with_tx in data.events:
                    embedded_tx_hash = felt.to_hex(inventory_event_with_tx.transaction.meta.hash)
                    if embedded_tx_hash == tx_hash:
                        inventory_event = inventory_event_with_tx.event
                        inventory_event_hex = inventory_event.keys[0]
                        #selector_hex = felt.to_hex(inventory_event_hex)
                        if inventory_event_hex == component_updated_key:
                            event_key = felt.to_hex(inventory_event.keys[0])
                            event_name = bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode()
                            if bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode() == 'Inventory':
                                inventory_event_index = inventory_event.index
                                destination_inventory = await processInventory(inventory_event, "delivery")

                            if bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode() == 'Delivery':
                                if inventory_event.index == (inventory_event_index + 1):
                                    #if inventory_event.index == 1:
                                    delivery_manifest = await processDeliveryManifest(inventory_event, "delivery")
                                    await processDeliveryReceived(tx_hash, event, block_number, from_address, destination_inventory, delivery_manifest, fee, timestamp)

                                            
            if event_hex == delivery_packaged_key:
                origin_inventory = []
                for inventory_event_with_tx in data.events:
                    embedded_tx_hash = felt.to_hex(inventory_event_with_tx.transaction.meta.hash)
                    if embedded_tx_hash == tx_hash:
                        inventory_event = inventory_event_with_tx.event
                        inventory_event_hex = inventory_event.keys[0]
                        selector_hex = felt.to_hex(inventory_event_hex)
                        if inventory_event_hex == component_updated_key:
                            event_key = felt.to_hex(inventory_event.keys[0])
                            event_name = bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode()
                            if bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode() == 'Inventory':
                                if inventory_event.index == 0:
                                    origin_inventory = await processInventory(inventory_event, "delivery")

                await processDeliveryPackaged(tx_hash, event, block_number, from_address, origin_inventory, fee, timestamp)

            if event_hex == delivery_packaged_v1_key:
                origin_inventory = []
                for inventory_event_with_tx in data.events:
                    embedded_tx_hash = felt.to_hex(inventory_event_with_tx.transaction.meta.hash)
                    if embedded_tx_hash == tx_hash:
                        inventory_event = inventory_event_with_tx.event
                        inventory_event_hex = inventory_event.keys[0]
                        selector_hex = felt.to_hex(inventory_event_hex)
                        if inventory_event_hex == component_updated_key:
                            event_key = felt.to_hex(inventory_event.keys[0])
                            event_name = bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode()
                            if bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode() == 'Inventory':
                                if inventory_event.index == 0:
                                    origin_inventory = await processInventory(inventory_event, "delivery")

                await processDeliveryPackagedV1(tx_hash, event, block_number, from_address, origin_inventory, fee, timestamp)

            if event_hex == delivery_cancelled_key:
                origin_inventory = []
                for inventory_event_with_tx in data.events:
                    embedded_tx_hash = felt.to_hex(inventory_event_with_tx.transaction.meta.hash)
                    if embedded_tx_hash == tx_hash:
                        inventory_event = inventory_event_with_tx.event
                        inventory_event_hex = inventory_event.keys[0]
                        selector_hex = felt.to_hex(inventory_event_hex)
                        if inventory_event_hex == component_updated_key:
                            event_key = felt.to_hex(inventory_event.keys[0])
                            event_name = bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode()
                            if bytes.fromhex(hex(felt.to_int(inventory_event.keys[1]))[2:]).decode() == 'Inventory':
                                if inventory_event.index == 0:
                                    origin_inventory = await processInventory(inventory_event, "delivery")

                await processDeliveryCancelled(tx_hash, event, block_number, from_address, origin_inventory, fee, timestamp)

            if event_hex == contract_agreement_accepted_key:
                await processContractAgreementAccepted(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == prepaid_merkle_agreement_accepted_key:
                await processPrepaidMerkleAgreementAccepted(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == prepaid_agreement_accepted_key:
                await processPrepaidAgreementAccepted(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == prepaid_agreement_extended_key:
                await processPrepaidAgreementExtended(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == prepaid_agreement_cancelled_key:
                await processPrepaidAgreementCancelled(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == removed_from_whitelist_key:
                await processRemovedFromWhitelist(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == removed_from_whitelist_v1_key:
                await processRemovedFromWhitelistV1(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == added_to_whitelist_v1_key:
                await processAddedToWhitelistV1(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == added_account_to_whitelist_key:
                await processAddedAccountToWhitelist(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == ship_commandeered_key:
                await processShipCommandeered(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == lot_reclaimed_key:
                await processLotReclaimed(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == building_repossessed_key:
                await processBuildingRepossessed(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == crew_delegated_key:
                await processCrewDelegated(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == crew_ejected_key:
                await processCrewEjected(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == deposit_listed_for_sale_key:
                await processDepositListedForSale(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == deposit_purchased_key:
                await processDepositPurchased(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == deposit_purchased_v1_key:
                await processDepositPurchasedV1(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == deposit_unlisted_for_sale_key:
                await processDepositUnlistedForSale(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == sell_order_created_key:
                await processSellOrderCreated(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == sell_order_filled_key:
                fill_count = 0
                events_count = 0
                for row in receipt.events:
                    events_count+=1
                if events_count > 13:
                    seed_events = data.events
                    index = event.index
                    fill_count = await processSellMarketOrderFilled(tx_hash, event, block_number, from_address, index, seed_events, fee, timestamp)

                await processSellOrderFilled(tx_hash, event, block_number, from_address, fill_count, fee, timestamp)

            if event_hex == sell_order_cancelled_key:
                delivery_event = None
                cancel_event = None
                for cancel_event_with_tx in data.events:
                    embedded_tx_hash = felt.to_hex(cancel_event_with_tx.transaction.meta.hash)
                    if embedded_tx_hash == tx_hash:
                        cancel_event_hex = None
                        event_name = None
                        receipt = None
                        selector_hex = None
                        cancel_event = cancel_event_with_tx.event
                        receipt = event_with_tx.receipt
                        cancel_event_hex = cancel_event.keys[0]
                        selector_hex = felt.to_hex(cancel_event_hex)
                        if cancel_event_hex == delivery_sent_key:
                            delivery_event = cancel_event

                await processSellOrderCancelled(tx_hash, event, delivery_event, block_number, from_address, fee, timestamp)

            if event_hex == buy_order_created_key:
                await processBuyOrderCreated(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == buy_order_filled_key:
                fill_count = 0
                events_count = 0
                for row in receipt.events:
                    events_count+=1
                if events_count > 13:
                    seed_events = data.events
                    index = event.index
                    fill_count = await processBuyMarketOrderFilled(tx_hash, event, block_number, from_address, index, seed_events, fee, timestamp)

                await processBuyOrderFilled(tx_hash, event, block_number, from_address, fill_count, fee, timestamp)

            if event_hex == buy_order_cancelled_key:
                await processBuyOrderCancelled(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == contract_policy_assigned_key:
                await processContractPolicyAssigned(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == prepaid_merkle_policy_assigned_key:
                await processPrepaidMerklePolicyAssigned(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == prepaid_policy_assigned_key:
                await processPrepaidPolicyAssigned(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == contract_policy_removed_key:
                await processContractPolicyRemoved(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == prepaid_policy_removed_key:
                await processPrepaidPolicyRemoved(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == prepaid_merkle_policy_removed_key:
                await processPrepaidMerklePolicyRemoved(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == public_policy_removed_key:
                await processPublicPolicyRemoved(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == random_event_resolved_key:
                await processRandomEventResolved(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == transit_finished_key:
                await processTransitFinished(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == transit_started_key:
                for transit_event_with_tx in data.events:
                    embedded_tx_hash = felt.to_hex(transit_event_with_tx.transaction.meta.hash)
                    if embedded_tx_hash == tx_hash:
                        transit_event = transit_event_with_tx.event
                        receipt = event_with_tx.receipt
                        transit_event_hex = transit_event.keys[0]
                        selector_hex = felt.to_hex(transit_event_hex)
                        if transit_event_hex == component_updated_key:
                            event_key = felt.to_hex(transit_event.keys[0])
                            event_name = bytes.fromhex(hex(felt.to_int(transit_event.keys[1]))[2:]).decode()
                            if event_name == 'Inventory':
                                if len(transit_event.data) >= 12:
                                    inventory_event = transit_event

                await processTransitStarted(tx_hash, event, block_number, from_address, fee, timestamp, inventory_event)

            if event_hex == arrival_reward_claimed_key:
                ships = await processArrivalComponentsLT(tx_hash, event, block_number, from_address, data.events, data.transactions, fee, timestamp)
                await processArrivalRewardClaimed(tx_hash, event, block_number, from_address, ships, fee, timestamp)

            if event_hex == prepare_for_launch_reward_claimed_key:
                await processPrepareForLaunchRewardClaimed(tx_hash, event, block_number, from_address, fee, timestamp)

            if event_hex == exchange_configured_key:
                await processExchangeConfigured(tx_hash, event, block_number, from_address, fee, timestamp)

        
        if len(txns) > 0:
            txn_db.txnCounter(block_number, len(txns), timestamp, "dispatcher_txns_per_block")


    async def handle_invalidate(self, _info: Info, _cursor: Cursor):
        raise ValueError("data must be finalized")


async def processSystemRegistered(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type = "SystemRegistered"
    name = bytes.fromhex(hex(felt.to_int(event.data[0]))[2:]).decode()
    class_hash = felt.to_hex(event.data[1])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, name: %s, class_hash: %s" % (block_number, event_type, tx_hash, from_address, name, class_hash))
    dispatcher_db.systemRegistered(tx_hash, block_number, from_address, class_hash, name, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processSurfaceScanStarted(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type = "SurfaceScanStarted"
    asteroid_label = felt.to_int(event.data[0])
    asteroid_id = felt.to_int(event.data[1])
    finish_time = felt.to_int(event.data[2])
    caller_crew_label = felt.to_int(event.data[3])
    caller_crew_id = felt.to_int(event.data[4])
    caller_address = felt.to_hex(event.data[5])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, asteroid_label: %s, asteroid_id: %s, caller_crew_label: %s, caller_crew_id: %s, finish_time: %s" % (block_number, event_type, tx_hash, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id, finish_time))
    dispatcher_db.surfaceScanStarted(tx_hash, block_number, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id, finish_time, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processSurfaceScanFinished(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type = "SurfaceScanFinished"
    asteroid_label = felt.to_int(event.data[0])
    asteroid_id = felt.to_int(event.data[1])
    bonuses = felt.to_int(event.data[2])
    caller_crew_label = felt.to_int(event.data[3])
    caller_crew_id = felt.to_int(event.data[4])
    caller_address = felt.to_hex(event.data[5])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, asteroid_label: %s, asteroid_id: %s, caller_crew_label: %s, caller_crew_id: %s, bonuses: %s" % (block_number, event_type, tx_hash, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id, bonuses))
    dispatcher_db.surfaceScanFinished(tx_hash, block_number, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id, bonuses, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processCrewmateRecruitedV1(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type = "CrewmateRecruitedV1"
    crewmate_label = felt.to_int(event.data[0])
    crewmate_id = felt.to_int(event.data[1])
    collection = felt.to_int(event.data[2])
    class_name = felt.to_int(event.data[3])
    title = felt.to_int(event.data[4])
    impactful_count = felt.to_int(event.data[5])
    impactful_start_pos = 6
    impactful_traits = []
    composition_traits = []
    cosmetic_traits = []

    if impactful_count == 1:
        impactful_end_pos = (impactful_start_pos + 1)
        impactful_traits.append(felt.to_int(event.data[impactful_start_pos]))
    else:
        impactful_end_pos = (impactful_start_pos + impactful_count)
        count = impactful_start_pos
        while count < impactful_end_pos:
            impactful_traits.append(felt.to_int(event.data[count]))
            count+=1


    cosmetic_count = felt.to_int(event.data[impactful_end_pos])
    cosmetic_start_pos = (impactful_end_pos + 1)

    if cosmetic_count == 1:
        cosmetic_end_pos = (cosmetic_start_pos + 1)
        cosmetic_traits.append(felt.to_int(event.data[cosmetic_start_pos]))
    else:
        cosmetic_end_pos = (cosmetic_start_pos + cosmetic_count)
        count = cosmetic_start_pos
        while count < cosmetic_end_pos:
            cosmetic_traits.append(felt.to_int(event.data[count]))
            count+=1


    gender_pos = cosmetic_end_pos
    body_pos = (gender_pos + 1)
    face_pos = (body_pos + 1)
    hair_pos = (face_pos + 1)
    hair_color_pos = (hair_pos + 1)
    clothes_pos = (hair_color_pos + 1)
    head_pos = (clothes_pos + 1)
    item_pos = (head_pos + 1)
    name_pos = (item_pos + 1)
    station_label_pos = (name_pos + 1)
    station_id_pos = (station_label_pos + 1)
    composition_count_pos = (station_id_pos + 1)
    composition_count = felt.to_int(event.data[composition_count_pos])
    composition_start_pos = (composition_count_pos + 1)

    if composition_count == 1:
        composition_end_pos = (composition_start_pos + 1)
        composition_traits.append(felt.to_int(event.data[composition_start_pos]))
    else:
        composition_end_pos = (composition_start_pos + composition_count)
        count = composition_start_pos
        while count < composition_end_pos:
            composition_traits.append(felt.to_int(event.data[count]))
            count+=1

    caller_crew_label_pos = composition_end_pos
    caller_crew_id_pos = (caller_crew_label_pos + 1)
    caller_address_pos = (caller_crew_id_pos + 1)

    gender = felt.to_int(event.data[gender_pos])
    body = felt.to_int(event.data[body_pos])
    face = felt.to_int(event.data[face_pos])
    hair = felt.to_int(event.data[hair_pos])
    hair_color = felt.to_int(event.data[hair_color_pos])
    clothes = felt.to_int(event.data[clothes_pos])
    head = felt.to_int(event.data[head_pos])
    item = felt.to_int(event.data[item_pos])
    name = bytes.fromhex(hex(felt.to_int(event.data[name_pos]))[2:]).decode()
    station_label = felt.to_int(event.data[station_label_pos])
    station_id = felt.to_int(event.data[station_id_pos])
    caller_crew_label = felt.to_int(event.data[caller_crew_label_pos])
    caller_crew_id = felt.to_int(event.data[caller_crew_id_pos])
    caller_address = felt.to_hex(event.data[caller_address_pos])

    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_id: %s, caller_crew_label: %s, crewmate_label: %s, crewmate_id: %s, collection: %s, class_name: %s, title: %s, impactful_traits: %s, cosmetic_traits: %s, gender: %s, body: %s, face: %s, hair: %s, hair_color: %s, clothes: %s, head: %s, item: %s, name: %s, station_label: %s, station_id: %s, composition_traits: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_id, caller_crew_label, crewmate_label, crewmate_id, collection, class_name, title, impactful_traits, cosmetic_traits, gender, body, face, hair, hair_color, clothes, head, item, name, station_label, station_id, composition_traits))
    dispatcher_db.crewmateRecruitedV1(tx_hash, block_number, from_address, caller_address, caller_crew_id, caller_crew_label, crewmate_label, crewmate_id, collection, class_name, title, impactful_traits, name, station_label, station_id, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processAsteroidManaged(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type = "AsteroidManaged"
    asteroid_label = felt.to_int(event.data[0])
    asteroid_id = felt.to_int(event.data[1])
    caller_crew_label = felt.to_int(event.data[2])
    caller_crew_id = felt.to_int(event.data[3])
    caller_address = felt.to_hex(event.data[4])

    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, asteroid_label: %s, asteroid_id: %s, caller_crew_label: %s, caller_crew_id: %s" % (block_number, event_type, tx_hash, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id))
    dispatcher_db.asteroidManaged(tx_hash, block_number, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processAsteroidInitialized(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type = "AsteroidInitialized"
    asteroid_label = felt.to_int(event.data[0])
    asteroid_id = felt.to_int(event.data[1])

    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, asteroid_label: %s, asteroid_id: %s" % (block_number, event_type, tx_hash, from_address, asteroid_label, asteroid_id))
    dispatcher_db.asteroidInitialized(tx_hash, block_number, from_address, asteroid_label, asteroid_id, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processAsteroidPurchased(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type = "AsteroidPurchased"
    asteroid_label = felt.to_int(event.data[0])
    asteroid_id = felt.to_int(event.data[1])
    caller_crew_label = felt.to_int(event.data[2])
    caller_crew_id = felt.to_int(event.data[3])
    caller_address = felt.to_hex(event.data[4])

    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_address: %s, asteroid_label: %s, asteroid_id: %s, caller_crew_label: %s, caller_crew_id: %s" % (block_number, event_type, tx_hash, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id))
    dispatcher_db.asteroidPurchased(tx_hash, block_number, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processCrewmatePurchased(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type = "CrewmatePurchased"
    crewmate_label = felt.to_int(event.data[0])
    crewmate_id = felt.to_int(event.data[1])
    caller_address = felt.to_hex(event.data[2])

    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_address: %s, crewmate_label: %s, crewmate_id: %s" % (block_number, event_type, tx_hash, from_address, caller_address, crewmate_label, crewmate_id))
    dispatcher_db.crewmatePurchased(tx_hash, block_number, from_address, caller_address, crewmate_label, crewmate_id, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processCrewmateArrangedV1(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type = "CremateArrangedV1"
    composition_old_count_pos = 0
    composition_old_count = felt.to_int(event.data[0])
    composition_old_start_pos = 1
    composition_old = []
    composition_new = []

    if composition_old_count == 1:
        composition_old_end_pos = (composition_old_start_pos + 1)
        composition_old.append(felt.to_int(event.data[composition_old_start_pos]))
    else:
        composition_old_end_pos = (composition_old_start_pos + composition_old_count)
        count = composition_old_start_pos
        while count < composition_old_end_pos:
            composition_old.append(felt.to_int(event.data[count]))
            count+=1

    composition_new_count_pos = (composition_old_end_pos)
    composition_new_count = felt.to_int(event.data[composition_new_count_pos])
    composition_new_start_pos = (composition_new_count_pos + 1)

    if composition_new_count == 1:
        composition_new_end_pos = (composition_new_start_pos + 1)
        composition_new.append(felt.to_int(event.data[composition_new_start_pos]))
    else:
        composition_new_end_pos = (composition_new_start_pos + composition_new_count)
        count = composition_new_start_pos
        while count < composition_new_end_pos:
            composition_new.append(felt.to_int(event.data[count]))
            count+=1

    caller_crew_label_pos = composition_new_end_pos
    caller_crew_id_pos = (caller_crew_label_pos + 1)
    caller_address_pos = (caller_crew_id_pos + 1)

    caller_crew_label = felt.to_int(event.data[caller_crew_label_pos])
    caller_crew_id = felt.to_int(event.data[caller_crew_id_pos])
    caller_address = felt.to_hex(event.data[caller_address_pos])

    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_address: %s, composition_old: %s, composition_new: %s, crew_label: %s, crew_id: %s" % (block_number, event_type, tx_hash, from_address, caller_address, composition_old, composition_new, caller_crew_label, caller_crew_id))
    dispatcher_db.crewmatesArrangedV1(tx_hash, block_number, from_address, caller_address, composition_old, composition_new, caller_crew_label, caller_crew_id, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processCrewmatesExchanged(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type = "CrematesExchanged"
    crew1_label = felt.to_int(event.data[0])
    crew1_id = felt.to_int(event.data[1])
    crew1_old_count = felt.to_int(event.data[2])
    crew1_start_pos = 3
    crew1_composition_old = []
    crew1_composition_new = []

    if crew1_old_count == 1:
        crew1_end_pos = (crew1_start_pos + 1)
        crew1_composition_old.append(felt.to_int(event.data[crew1_start_pos]))
    else:
        crew1_end_pos = (crew1_start_pos + crew1_old_count)
        count = crew1_start_pos
        while count < crew1_end_pos:
            crew1_composition_old.append(felt.to_int(event.data[count]))
            count+=1

    crew1_new_count_pos = (crew1_end_pos)
    crew1_new_count = felt.to_int(event.data[crew1_new_count_pos])
    crew1_new_start_pos = (crew1_new_count_pos + 1)

    if crew1_new_count == 1:
        crew1_new_end_pos = (crew1_new_start_pos + 1)
        crew1_composition_new.append(felt.to_int(event.data[crew1_new_start_pos]))
    else:
        crew1_new_end_pos = (crew1_new_start_pos + crew1_new_count)
        count = crew1_new_start_pos
        while count < crew1_new_end_pos:
            crew1_composition_new.append(felt.to_int(event.data[count]))
            count+=1

    crew2_label_pos = (crew1_new_end_pos)
    crew2_id_pos = (crew2_label_pos + 1)
    crew2_label = felt.to_int(event.data[crew2_label_pos])
    crew2_id = felt.to_int(event.data[crew2_id_pos])

    crew2_old_count_pos = (crew2_id_pos + 1)
    crew2_old_count = felt.to_int(event.data[crew2_old_count_pos])
    crew2_old_start_pos = (crew2_old_count_pos + 1)
    crew2_composition_old = []
    crew2_composition_new = []

    if crew2_old_count == 1:
        crew2_old_end_pos = (crew2_old_start_pos + 1)
        crew2_composition_old.append(felt.to_int(event.data[crew2_old_start_pos]))
    else:
        crew2_old_end_pos = (crew2_old_start_pos + crew2_old_count)
        count = crew2_old_start_pos
        while count < crew2_old_end_pos:
            crew2_composition_old.append(felt.to_int(event.data[count]))
            count+=1

    crew2_new_count_pos = (crew2_old_end_pos)
    crew2_new_count = felt.to_int(event.data[crew2_new_count_pos])
    crew2_new_start_pos = (crew2_new_count_pos + 1)

    if crew2_new_count == 1:
        crew2_new_end_pos = (crew2_new_start_pos + 1)
        crew2_composition_new.append(felt.to_int(event.data[crew2_new_start_pos]))
    else:
        crew2_new_end_pos = (crew2_new_start_pos + crew2_new_count)
        count = crew2_new_start_pos
        while count < crew2_new_end_pos:
            crew2_composition_new.append(felt.to_int(event.data[count]))
            count+=1

    caller_address_pos = crew2_new_end_pos
    caller_address = felt.to_hex(event.data[caller_address_pos])

    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_address: %s, crew1_label: %s, crew1_id: %s, crew1_composition_old: %s, crew1_composition_new: %s, crew2_label: %s, crew2_id: %s, crew2_composition_old: %s, crew2_composition_new: %s" % (block_number, event_type, tx_hash, from_address, caller_address, crew1_label, crew1_id, crew1_composition_old, crew1_composition_new, crew2_label, crew2_id, crew2_composition_old, crew2_composition_new))


    dispatcher_db.crewmatesExchanged(tx_hash, block_number, from_address, caller_address, crew1_label, crew1_id, crew1_composition_old, crew1_composition_new, crew2_label, crew2_id, crew2_composition_old, crew2_composition_new, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processCrewFormed(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type = "CrewFormed"
    composition_count_pos = 0
    composition_count = felt.to_int(event.data[composition_count_pos])
    composition_start_pos = (composition_count_pos + 1)
    composition = []

    if composition_count == 1:
        composition_end_pos = (composition_start_pos + 1)
        composition.append(felt.to_int(event.data[composition_start_pos]))
    else:
        composition_end_pos = (composition_start_pos + composition_count)
        count = composition_start_pos
        while count < composition_end_pos:
            composition.append(felt.to_int(event.data[count]))
            count+=1

    caller_crew_label_pos = composition_end_pos
    caller_crew_label = felt.to_int(event.data[caller_crew_label_pos])
    caller_crew_id_pos = (caller_crew_label_pos + 1)
    caller_crew_id = felt.to_int(event.data[caller_crew_id_pos])
    caller_address_pos = (caller_crew_id_pos + 1)
    caller_address = felt.to_hex(event.data[caller_address_pos])

    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_address: %s, composition: %s, caller_crew_label: %s, caller_crew_id: %s" % (block_number, event_type, tx_hash, from_address, caller_address, composition, caller_crew_label, caller_crew_id))
    dispatcher_db.crewFormed(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, composition, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processCrewmateRecruited(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type = "CrewmateRecruited"
    crewmate_label = felt.to_int(event.data[0])
    crewmate_id = felt.to_int(event.data[1])
    collection = felt.to_int(event.data[2])
    class_name = felt.to_int(event.data[3])
    title = felt.to_int(event.data[4])
    impactful_count = felt.to_int(event.data[5])
    impactful_start_pos = 6
    impactful_traits = []
    composition_traits = []
    cosmetic_traits = []

    if impactful_count == 1:
        impactful_end_pos = (impactful_start_pos + 1)
        impactful_traits.append(felt.to_int(event.data[impactful_start_pos]))
    else:
        impactful_end_pos = (impactful_start_pos + impactful_count)
        count = impactful_start_pos
        while count < impactful_end_pos:
            impactful_traits.append(felt.to_int(event.data[count]))
            count+=1

    cosmetic_count = felt.to_int(event.data[impactful_end_pos])
    cosmetic_start_pos = (impactful_end_pos + 1)

    if cosmetic_count == 1:
        cosmetic_end_pos = (cosmetic_start_pos + 1)
        cosmetic_traits.append(felt.to_int(event.data[cosmetic_start_pos]))
    else:
        cosmetic_end_pos = (cosmetic_start_pos + cosmetic_count)
        count = cosmetic_start_pos
        while count < cosmetic_end_pos:
            cosmetic_traits.append(felt.to_int(event.data[count]))
            count+=1

    gender_pos = cosmetic_end_pos
    body_pos = (gender_pos + 1)
    face_pos = (body_pos + 1)
    hair_pos = (face_pos + 1)
    hair_color_pos = (hair_pos + 1)
    clothes_pos = (hair_color_pos + 1)
    head_pos = (clothes_pos + 1)
    item_pos = (head_pos + 1)
    station_label_pos = (item_pos + 1)
    station_id_pos = (station_label_pos + 1)
    caller_crew_label_pos = (station_id_pos + 1)
    caller_crew_id_pos = (caller_crew_label_pos + 1)
    caller_address_pos = (caller_crew_id_pos + 1)
    gender = felt.to_int(event.data[gender_pos])
    body = felt.to_int(event.data[body_pos])
    face = felt.to_int(event.data[face_pos])
    hair = felt.to_int(event.data[hair_pos])
    hair_color = felt.to_int(event.data[hair_color_pos])
    clothes = felt.to_int(event.data[clothes_pos])
    head = felt.to_int(event.data[head_pos])
    item = felt.to_int(event.data[item_pos])
    station_label = felt.to_int(event.data[station_label_pos])
    station_id = felt.to_int(event.data[station_id_pos])
    caller_crew_label = felt.to_int(event.data[caller_crew_label_pos])
    caller_crew_id = felt.to_int(event.data[caller_crew_id_pos])
    caller_address = felt.to_hex(event.data[caller_address_pos])

    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_id: %s, caller_crew_label: %s, crewmate_label: %s, crewmate_id: %s, collection: %s, class_name: %s, title: %s, impactful_traits: %s, cosmetic_traits: %s, gender: %s, body: %s, face: %s, hair: %s, hair_color: %s, clothes: %s, head: %s, item: %s, station_label: %s, station_id: %s, composition_traits: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_id, caller_crew_label, crewmate_label, crewmate_id, collection, class_name, title, impactful_traits, cosmetic_traits, gender, body, face, hair, hair_color, clothes, head, item, station_label, station_id, composition_traits))
    dispatcher_db.crewmateRecruited(tx_hash, block_number, from_address, caller_address, caller_crew_id, caller_crew_label, crewmate_label, crewmate_id, collection, class_name, title, impactful_traits, station_label, station_id, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processConstantRegistered(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type = "ConstantRegistered"
    name = bytes.fromhex(hex(felt.to_int(event.data[0]))[2:]).decode()
    value = felt.to_int(event.data[1])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, name: %s, value: %s" % (block_number, event_type, tx_hash, from_address, name, value))
    dispatcher_db.constantRegistered(tx_hash, block_number, from_address, name, value, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processContractRegistered(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type = "ContractRegistered"
    name = bytes.fromhex(hex(felt.to_int(event.data[0]))[2:]).decode()
    address = felt.to_hex(event.data[1])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, name: %s, address: %s" % (block_number, event_type, tx_hash, from_address, name, address))
    dispatcher_db.contractRegistered(tx_hash, block_number, from_address, name, address, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processPublicPolicyAssigned(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="PublicPolicyAssigned"
    entity_label = felt.to_int(event.data[0])
    entity_id = felt.to_int(event.data[1])
    permission = felt.to_int(event.data[2])
    caller_crew_label = felt.to_int(event.data[3])
    caller_crew_id = felt.to_int(event.data[4])
    caller_address = felt.to_hex(event.data[5])
    entity_name = types.getEntityName(entity_id)
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, entity_label: %s, entity_id: %s, permission: %s, caller_crew_label: %s, caller_crew_id: %s, entity_name: %s" % (block_number, event_type, tx_hash, from_address, caller_address, entity_label, entity_id, permission, caller_crew_label, caller_crew_id, entity_name))
    dispatcher_db.publicPolicyAssigned(tx_hash, event, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, entity_name, fee, timestamp) 
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processConstructionFinished(tx_hash, event, block_number, from_address, start_inventory, fee, timestamp):

    event_type = "ConstructionFinished"
    building_label = felt.to_int(event.data[0])
    building_id = felt.to_int(event.data[1])
    caller_crew_label = felt.to_int(event.data[2])
    caller_crew_id = felt.to_int(event.data[3])
    caller_address = felt.to_hex(event.data[4])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, building_label: %s, building_id: %s, caller_crew_label: %s, caller_crew_id: %s, start_inventory: %s" % (block_number, event_type, tx_hash, from_address, caller_address, building_label, building_id, caller_crew_label, caller_crew_id, start_inventory))
    dispatcher_db.constructionFinished(tx_hash, block_number, from_address, caller_address, building_label, building_id, caller_crew_label, caller_crew_id, start_inventory, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processConstructionDeconstructed(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type = "ConstructionDeconstructed"
    building_label = felt.to_int(event.data[0])
    building_id = felt.to_int(event.data[1])
    caller_crew_label = felt.to_int(event.data[2])
    caller_crew_id = felt.to_int(event.data[3])
    caller_address = felt.to_hex(event.data[4])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, building_label: %s, building_id: %s, caller_crew_label: %s, caller_crew_id: %s" % (block_number, event_type, tx_hash, from_address, caller_address, building_label, building_id, caller_crew_label, caller_crew_id))
    dispatcher_db.constructionDeconstructed(tx_hash, block_number, from_address, caller_address, building_label, building_id, caller_crew_label, caller_crew_id, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processNameChanged(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="NameChanged"
    entity_label = felt.to_int(event.data[0])
    entity_id = felt.to_int(event.data[1])
    name = bytes.fromhex(hex(felt.to_int(event.data[2]))[2:]).decode()
    caller_crew_label = felt.to_int(event.data[3])
    caller_crew_id = felt.to_int(event.data[4])
    caller_address = felt.to_hex(event.data[5])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, entity_label: %s, entity_id: %s, name: %s, caller_crew_label: %s, caller_crew_id: %s" % (block_number, event_type, tx_hash, from_address, caller_address, entity_label, entity_id, name, caller_crew_label, caller_crew_id))
    dispatcher_db.nameChanged(tx_hash, block_number, from_address, caller_address, entity_label, entity_id, name, caller_crew_label, caller_crew_id, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processResourceScanStarted(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="ResourceScanStarted"
    asteroid_label = felt.to_int(event.data[0])
    asteroid_id = felt.to_int(event.data[1])
    finish_time = felt.to_int(event.data[2])
    caller_crew_label = felt.to_int(event.data[3])
    caller_crew_id = felt.to_int(event.data[4])
    caller_address = felt.to_hex(event.data[5])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, asteroid_label: %s, asteroid_id: %s, caller_crew_label: %s, caller_crew_id: %s, finish_time: %s" % (block_number, event_type, tx_hash, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id, finish_time))
    dispatcher_db.resourceScanStarted(tx_hash, block_number, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id, finish_time, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processConstructionPlanned(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="ConstructionPlanned"
    building_label = felt.to_int(event.data[0])
    building_id = felt.to_int(event.data[1])
    building_type = felt.to_int(event.data[2])
    asteroid_label = felt.to_int(event.data[3])
    asteroid_id = felt.to_int(event.data[4])
    lot_label = felt.to_int(event.data[5])
    packed_lot_id = felt.to_int(event.data[6])
    entity = sdk.unpackLot(packed_lot_id)
    lot_id = entity['lotIndex']
    grace_period_end = felt.to_int(event.data[7])
    caller_crew_label = felt.to_int(event.data[8])
    caller_crew_id = felt.to_int(event.data[9])
    caller_address = felt.to_hex(event.data[10])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, asteroid_label: %s, asteroid_id: %s, caller_crew_label: %s, caller_crew_id: %s, building_label: %s, building_id: %s, building_type: %s, lot_label: %s, lot_id: %s, packed_lot_id: %s, grace_period_end: %s" % (block_number, event_type, tx_hash, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id, building_label, building_id, building_type, lot_label, lot_id, packed_lot_id, grace_period_end))
    dispatcher_db.constructionPlanned(tx_hash, block_number, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id, building_label, building_id, building_type, lot_label, lot_id, packed_lot_id, grace_period_end, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processHabitatPolicies(tx_hash, event, block_number, from_address, index, seed_events, building_id, building_type, asteroid_id, packed_lot_id, lot_id, caller_crew_id, caller_address):

    policy_event_1 = (int(index) + 8)
    policy_event_2 = (int(index) + 9)
    trackable_events = (policy_event_1, policy_event_2)

    policy_event_1_v2 = (int(index) - 2)
    policy_event_2_v2 = (int(index) - 3)
    trackable_events_v2 = (policy_event_1_v2, policy_event_2_v2)

    counter = 0
    for seed_event_with_tx in seed_events:
        seed_tx_hash = felt.to_hex(seed_event_with_tx.transaction.meta.hash)
        if seed_tx_hash == tx_hash:
            seed_event_hex = None
            event_name = None
            selector_hex = None
            for policy_event_id in trackable_events:
                if int(policy_event_id) == int(seed_event_with_tx.event.index):
                    seed_event = seed_event_with_tx.event
                    seed_event_hex = seed_event.keys[0]
                    selector_hex = felt.to_hex(seed_event_hex)
                    if seed_event_hex == component_updated_key:
                        event_key = felt.to_hex(seed_event.keys[0])
                        event_name = bytes.fromhex(hex(felt.to_int(seed_event.keys[1]))[2:]).decode()
                        if event_name == 'PublicPolicy':
                            permission = seed_event.data[2]
                            permission = felt.to_int(seed_event.data[2])
                            counter+=1
                            dispatcher_db.setPublicPolicy(tx_hash, block_number, from_address, caller_address, caller_crew_id, building_id, building_type, asteroid_id, lot_id, permission)

    if counter == 0:
        for seed_event_with_tx in seed_events:
            if seed_tx_hash == tx_hash:
                seed_event_hex = None
                event_name = None
                selector_hex = None
                for policy_event_id in trackable_events_v2:
                    if int(policy_event_id) == int(seed_event_with_tx.event.index):
                        seed_event = seed_event_with_tx.event
                        seed_event_hex = seed_event.keys[0]
                        selector_hex = felt.to_hex(seed_event_hex)
                        if seed_event_hex == component_updated_key:
                            event_key = felt.to_hex(seed_event.keys[0])
                            event_name = bytes.fromhex(hex(felt.to_int(seed_event.keys[1]))[2:]).decode()
                            if event_name == 'PublicPolicy':
                                permission = seed_event.data[2]
                                permission = felt.to_int(seed_event.data[2])
                                print("%s PERMISSION: %s" % (building_id, permission))
                                dispatcher_db.setPublicPolicy(tx_hash, block_number, from_address, caller_address, caller_crew_id, building_id, building_type, asteroid_id, lot_id, permission)


async def processWarehousePolicies(tx_hash, event, block_number, from_address, index, seed_events, building_id, building_type, asteroid_id, packed_lot_id, lot_id, caller_crew_id, caller_address):

    policy_event_1 = (int(index) - 3)
    policy_event_2 = (int(index) - 2)
    trackable_events = (policy_event_1, policy_event_2)

    policy_event_1_v2 = (int(index) + 8)
    policy_event_2_v2 = (int(index) + 9)
    trackable_events_v2 = (policy_event_1_v2, policy_event_2_v2)

    counter = 0
    for seed_event_with_tx in seed_events:
        seed_tx_hash = felt.to_hex(seed_event_with_tx.transaction.meta.hash)
        if seed_tx_hash == tx_hash:
            seed_event_hex = None
            event_name = None
            selector_hex = None
            for policy_event_id in trackable_events:
                if int(policy_event_id) == int(seed_event_with_tx.event.index):
                    seed_event = seed_event_with_tx.event
                    seed_event_hex = seed_event.keys[0]
                    selector_hex = felt.to_hex(seed_event_hex)
                    if seed_event_hex == component_updated_key:
                        event_key = felt.to_hex(seed_event.keys[0])
                        event_name = bytes.fromhex(hex(felt.to_int(seed_event.keys[1]))[2:]).decode()
                        if event_name == 'PublicPolicy':
                            permission = seed_event.data[2]
                            permission = felt.to_int(seed_event.data[2])
                            counter+=1
                            dispatcher_db.setPublicPolicy(tx_hash, block_number, from_address, caller_address, caller_crew_id, building_id, building_type, asteroid_id, lot_id, permission)

    if counter == 0:
        for seed_event_with_tx in seed_events:
            if seed_tx_hash == tx_hash:
                seed_event_hex = None
                event_name = None
                selector_hex = None
                for policy_event_id in trackable_events_v2:
                    if int(policy_event_id) == int(seed_event_with_tx.event.index):
                        seed_event = seed_event_with_tx.event
                        seed_event_hex = seed_event.keys[0]
                        selector_hex = felt.to_hex(seed_event_hex)
                        if seed_event_hex == component_updated_key:
                            event_key = felt.to_hex(seed_event.keys[0])
                            event_name = bytes.fromhex(hex(felt.to_int(seed_event.keys[1]))[2:]).decode()
                            if event_name == 'PublicPolicy':
                                permission = seed_event.data[2]
                                permission = felt.to_int(seed_event.data[2])
                                dispatcher_db.setPublicPolicy(tx_hash, block_number, from_address, caller_address, caller_crew_id, building_id, building_type, asteroid_id, lot_id, permission)


async def processMarketplacePolicies(tx_hash, event, block_number, from_address, index, seed_events, building_id, building_type, asteroid_id, packed_lot_id, lot_id, caller_crew_id, caller_address):

    policy_event_1 = (int(index) - 5)
    policy_event_2 = (int(index) - 4)
    policy_event_3 = (int(index) - 3)
    policy_event_4 = (int(index) - 2)
    trackable_events = (policy_event_1, policy_event_2, policy_event_3, policy_event_4)

    for seed_event_with_tx in seed_events:
        seed_tx_hash = felt.to_hex(seed_event_with_tx.transaction.meta.hash)
        if seed_tx_hash == tx_hash:
            seed_event_hex = None
            event_name = None
            selector_hex = None
            for policy_event_id in trackable_events:
                if int(policy_event_id) == int(seed_event_with_tx.event.index):
                    seed_event = seed_event_with_tx.event
                    seed_event_hex = seed_event.keys[0]
                    selector_hex = felt.to_hex(seed_event_hex)
                    if seed_event_hex == component_updated_key:
                        event_key = felt.to_hex(seed_event.keys[0])
                        event_name = bytes.fromhex(hex(felt.to_int(seed_event.keys[1]))[2:]).decode()
                        if event_name == 'PublicPolicy':
                            permission = seed_event.data[2]
                            permission = felt.to_int(seed_event.data[2])
                            dispatcher_db.setPublicPolicy(tx_hash, block_number, from_address, caller_address, caller_crew_id, building_id, building_type, asteroid_id, lot_id, permission)


async def processSpaceportPolicies(tx_hash, event, block_number, from_address, index, seed_events, building_id, building_type, asteroid_id, packed_lot_id, lot_id, caller_crew_id, caller_address):

    policy_event_1 = (int(index) - 2)
    policy_event_1_v2 = (int(index) + 8)

    counter = 0
    for seed_event_with_tx in seed_events:
        seed_tx_hash = felt.to_hex(seed_event_with_tx.transaction.meta.hash)
        if seed_tx_hash == tx_hash:
            seed_event_hex = None
            event_name = None
            selector_hex = None
            if int(policy_event_1) == int(seed_event_with_tx.event.index):
                seed_event = seed_event_with_tx.event
                seed_event_hex = seed_event.keys[0]
                selector_hex = felt.to_hex(seed_event_hex)
                if seed_event_hex == component_updated_key:
                    event_key = felt.to_hex(seed_event.keys[0])
                    event_name = bytes.fromhex(hex(felt.to_int(seed_event.keys[1]))[2:]).decode()
                    if event_name == 'PublicPolicy':
                        permission = seed_event.data[2]
                        permission = felt.to_int(seed_event.data[2])
                        counter+=1
                        dispatcher_db.setPublicPolicy(tx_hash, block_number, from_address, caller_address, caller_crew_id, building_id, building_type, asteroid_id, lot_id, permission)

    if counter == 0:
        for seed_event_with_tx in seed_events:
            if seed_tx_hash == tx_hash:
                seed_event_hex = None
                event_name = None
                selector_hex = None
                if int(policy_event_1_v2) == int(seed_event_with_tx.event.index):
                    seed_event = seed_event_with_tx.event
                    seed_event_hex = seed_event.keys[0]
                    selector_hex = felt.to_hex(seed_event_hex)
                    if seed_event_hex == component_updated_key:
                        event_key = felt.to_hex(seed_event.keys[0])
                        event_name = bytes.fromhex(hex(felt.to_int(seed_event.keys[1]))[2:]).decode()
                        if event_name == 'PublicPolicy':
                            permission = seed_event.data[2]
                            permission = felt.to_int(seed_event.data[2])
                            dispatcher_db.setPublicPolicy(tx_hash, block_number, from_address, caller_address, caller_crew_id, building_id, building_type, asteroid_id, lot_id, permission)


async def processInventory(inventory_event, action):

    if action == "processing" or action == "sampling" or action == "food_supplied" or action == "ship" or action == "construction" or action == "delivery" or action == "order" or action == "extraction":
        inventory = []
        inventory_len = felt.to_int(inventory_event.data[9])
        inventory_start_pos = 10
        inventory_len_doubled = (inventory_len * 2)
        inventory_end_pos = (inventory_start_pos + inventory_len_doubled)
        count = inventory_len
        anchor_pos = inventory_start_pos
        while count > 0:
            while anchor_pos < inventory_end_pos:
                resource_id = felt.to_int(inventory_event.data[anchor_pos])
                anchor_pos+=1
                resource_amount = felt.to_int(inventory_event.data[anchor_pos])
                resource_name = types.getProductName(resource_id)
                inventory.append({"resource_id": resource_id, "resource_amount": resource_amount, "resource_name": resource_name})
                anchor_pos+=1
                count-=1

        return inventory


async def processDeliveryManifest(delivery_event, action):

    if action == "delivery":
        delivery = []
        delivery_len = felt.to_int(delivery_event.data[10])
        delivery_start_pos = 11
        delivery_len_doubled = (delivery_len * 2)
        delivery_end_pos = (delivery_start_pos + delivery_len_doubled)
        count = delivery_len
        anchor_pos = delivery_start_pos
        while count > 0:
            while anchor_pos < delivery_end_pos:
                resource_id = felt.to_int(delivery_event.data[anchor_pos])
                anchor_pos+=1
                resource_amount = felt.to_int(delivery_event.data[anchor_pos])
                resource_name = types.getProductName(resource_id)
                delivery.append({"resource_id": resource_id, "resource_amount": resource_amount, "resource_name": resource_name})
                anchor_pos+=1
                count-=1

    return delivery


async def processArrivalComponentsLT(tx_hash, event, block_number, from_address, txn_events, txns, fee, timestamp):

    event_type=("ProcessArrivalComponentsLT")
    ship_1_type = None
    ship_2_type = None
    ship_3_type = None
    ship_4_type = None
    ship_5_type = None
    ship_6_type = None
    ships = []

    events_count = 0
    for txn in txns:
        if tx_hash == felt.to_hex(txn.transaction.meta.hash):
            print(type(txn.receipt))
            for event in txn.receipt.events:
                print(event)
                events_count+=1

    if events_count == 13 or events_count == 12:
        ship_1_type = 2
        ship_1_type_name = types.getShipName(ship_1_type)
        ship_1_transfer_index = 1
        ship_1_propellant_index = 7
        ship_1_inventory_index = 8
        for txn in txns:
            if tx_hash == felt.to_hex(txn.transaction.meta.hash):
                for event in txn.receipt.events:
                    if int(event.index) == ship_1_transfer_index:
                        ship_1_transfer_event = event
                    elif int(event.index) == ship_1_propellant_index:
                        ship_1_propellant_event = event
                    elif int(event.index) == ship_1_inventory_index:
                        ship_1_inventory_event = event

        ship_1_products = []
        ship_1_owner = felt.to_hex(ship_1_transfer_event.data[1])
        ship_1_owner = from_address
        ship_1_id = felt.to_int(ship_1_transfer_event.data[2])
        ship_1_propellant = felt.to_int(ship_1_propellant_event.data[11])

        product_id_1 = felt.to_int(ship_1_inventory_event.data[12])
        product_id_1_name = types.getProductName(product_id_1)
        product_id_1_amount = felt.to_int(ship_1_inventory_event.data[13])
        ship_1_products.append({"product_id": product_id_1, "product_name": product_id_1_name, "product_amount": product_id_1_amount})

        product_id_2 = felt.to_int(ship_1_inventory_event.data[14])
        product_id_2_name = types.getProductName(product_id_2)
        product_id_2_amount = felt.to_int(ship_1_inventory_event.data[15])
        ship_1_products.append({"product_id": product_id_2, "product_name": product_id_2_name, "product_amount": product_id_2_amount})

        product_id_3 = felt.to_int(ship_1_inventory_event.data[16])
        product_id_3_name = types.getProductName(product_id_3)
        product_id_3_amount = felt.to_int(ship_1_inventory_event.data[17])
        ship_1_products.append({"product_id": product_id_3, "product_name": product_id_3_name, "product_amount": product_id_3_amount})

        product_id_4 = felt.to_int(ship_1_inventory_event.data[18])
        product_id_4_name = types.getProductName(product_id_4)
        product_id_4_amount = felt.to_int(ship_1_inventory_event.data[19])
        ship_1_products.append({"product_id": product_id_4, "product_name": product_id_4_name, "product_amount": product_id_4_amount})

        product_id_5 = felt.to_int(ship_1_inventory_event.data[20])
        product_id_5_name = types.getProductName(product_id_5)
        product_id_5_amount = felt.to_int(ship_1_inventory_event.data[21])
        ship_1_products.append({"product_id": product_id_5, "product_name": product_id_5_name, "product_amount": product_id_5_amount})

        product_id_6 = felt.to_int(ship_1_inventory_event.data[22])
        product_id_6_name = types.getProductName(product_id_6)
        product_id_6_amount = felt.to_int(ship_1_inventory_event.data[23])
        ship_1_products.append({"product_id": product_id_6, "product_name": product_id_6_name, "product_amount": product_id_6_amount})
        ships.append({"ship_id": ship_1_id, "ship_type": ship_1_type, "ship_type_name": ship_1_type_name, "ship_owner": ship_1_owner, "propellant": ship_1_propellant, "products": ship_1_products})

    if events_count == 27 or events_count == 26:
        ship_1_type = 2
        ship_1_type_name = types.getShipName(ship_1_type)
        ship_1_transfer_index = 1
        ship_1_propellant_index = 7
        ship_1_inventory_index = 8
        for txn in txns:
            if tx_hash == felt.to_hex(txn.transaction.meta.hash):
                for event in txn.receipt.events:
                    if int(event.index) == ship_1_transfer_index:
                        ship_1_transfer_event = event
                    elif int(event.index) == ship_1_propellant_index:
                        ship_1_propellant_event = event
                    elif int(event.index) == ship_1_inventory_index:
                        ship_1_inventory_event = event

        ship_1_products = []
        ship_1_owner = felt.to_hex(ship_1_transfer_event.data[1])
        ship_1_owner = from_address
        ship_1_id = felt.to_int(ship_1_transfer_event.data[2])
        ship_1_propellant = felt.to_int(ship_1_propellant_event.data[11])

        product_id_1 = felt.to_int(ship_1_inventory_event.data[12])
        product_id_1_name = types.getProductName(product_id_1)
        product_id_1_amount = felt.to_int(ship_1_inventory_event.data[13])
        ship_1_products.append({"product_id": product_id_1, "product_name": product_id_1_name, "product_amount": product_id_1_amount})

        product_id_2 = felt.to_int(ship_1_inventory_event.data[14])
        product_id_2_name = types.getProductName(product_id_2)
        product_id_2_amount = felt.to_int(ship_1_inventory_event.data[15])
        ship_1_products.append({"product_id": product_id_2, "product_name": product_id_2_name, "product_amount": product_id_2_amount})

        product_id_3 = felt.to_int(ship_1_inventory_event.data[16])
        product_id_3_name = types.getProductName(product_id_3)
        product_id_3_amount = felt.to_int(ship_1_inventory_event.data[17])
        ship_1_products.append({"product_id": product_id_3, "product_name": product_id_3_name, "product_amount": product_id_3_amount})

        product_id_4 = felt.to_int(ship_1_inventory_event.data[18])
        product_id_4_name = types.getProductName(product_id_4)
        product_id_4_amount = felt.to_int(ship_1_inventory_event.data[19])
        ship_1_products.append({"product_id": product_id_4, "product_name": product_id_4_name, "product_amount": product_id_4_amount})

        product_id_5 = felt.to_int(ship_1_inventory_event.data[20])
        product_id_5_name = types.getProductName(product_id_5)
        product_id_5_amount = felt.to_int(ship_1_inventory_event.data[21])
        ship_1_products.append({"product_id": product_id_5, "product_name": product_id_5_name, "product_amount": product_id_5_amount})

        product_id_6 = felt.to_int(ship_1_inventory_event.data[22])
        product_id_6_name = types.getProductName(product_id_6)
        product_id_6_amount = felt.to_int(ship_1_inventory_event.data[23])
        ship_1_products.append({"product_id": product_id_6, "product_name": product_id_6_name, "product_amount": product_id_6_amount})
        ships.append({"ship_id": ship_1_id, "ship_type": ship_1_type, "ship_type_name": ship_1_type_name, "ship_owner": ship_1_owner, "propellant": ship_1_propellant, "products": ship_1_products})

        ship_2_type = 2
        ship_2_type_name = types.getShipName(ship_2_type)
        ship_2_transfer_index = 10
        for txn in txns:
            if tx_hash == felt.to_hex(txn.transaction.meta.hash):
                for event in txn.receipt.events:
                    if int(event.index) == ship_2_transfer_index:
                        ship_2_transfer_event = event

        ship_2_products = []
        ship_2_owner = felt.to_hex(ship_2_transfer_event.data[1])
        ship_2_owner = from_address
        ship_2_id = felt.to_int(ship_2_transfer_event.data[2])
        ships.append({"ship_id": ship_2_id, "ship_type": ship_2_type, "ship_type_name": ship_2_type_name, "ship_owner": ship_2_owner, "propellant": 0, "products": ship_2_products})

        ship_3_type = 4
        ship_3_type_name = types.getShipName(ship_3_type)
        ship_3_transfer_index = 17
        for txn in txns:
            if tx_hash == felt.to_hex(txn.transaction.meta.hash):
                for event in txn.receipt.events:
                    if int(event.index) == ship_3_transfer_index:
                        ship_3_transfer_event = event

        ship_3_products = []
        ship_3_owner = felt.to_hex(ship_3_transfer_event.data[1])
        ship_3_owner = from_address
        ship_3_id = felt.to_int(ship_3_transfer_event.data[2])
        ships.append({"ship_id": ship_3_id, "ship_type": ship_3_type, "ship_type_name": ship_3_type_name, "ship_owner": ship_3_owner, "propellant": 0, "products": ship_3_products})


    if events_count == 48 or events_count == 47:
        ship_1_type = 2
        ship_1_type_name = types.getShipName(ship_1_type)
        ship_1_transfer_index = 1
        ship_1_propellant_index = 7
        ship_1_inventory_index = 8
        for txn in txns:
            if tx_hash == felt.to_hex(txn.transaction.meta.hash):
                for event in txn.receipt.events:
                    if int(event.index) == ship_1_transfer_index:
                        ship_1_transfer_event = event
                    elif int(event.index) == ship_1_propellant_index:
                        ship_1_propellant_event = event
                    elif int(event.index) == ship_1_inventory_index:
                        ship_1_inventory_event = event

        ship_1_products = []
        ship_1_owner = felt.to_hex(ship_1_transfer_event.data[1])
        ship_1_owner = from_address
        ship_1_id = felt.to_int(ship_1_transfer_event.data[2])
        ship_1_propellant = felt.to_int(ship_1_propellant_event.data[11])

        product_id_1 = felt.to_int(ship_1_inventory_event.data[12])
        product_id_1_name = types.getProductName(product_id_1)
        product_id_1_amount = felt.to_int(ship_1_inventory_event.data[13])
        ship_1_products.append({"product_id": product_id_1, "product_name": product_id_1_name, "product_amount": product_id_1_amount})

        product_id_2 = felt.to_int(ship_1_inventory_event.data[14])
        product_id_2_name = types.getProductName(product_id_2)
        product_id_2_amount = felt.to_int(ship_1_inventory_event.data[15])
        ship_1_products.append({"product_id": product_id_2, "product_name": product_id_2_name, "product_amount": product_id_2_amount})

        product_id_3 = felt.to_int(ship_1_inventory_event.data[16])
        product_id_3_name = types.getProductName(product_id_3)
        product_id_3_amount = felt.to_int(ship_1_inventory_event.data[17])
        ship_1_products.append({"product_id": product_id_3, "product_name": product_id_3_name, "product_amount": product_id_3_amount})

        product_id_4 = felt.to_int(ship_1_inventory_event.data[18])
        product_id_4_name = types.getProductName(product_id_4)
        product_id_4_amount = felt.to_int(ship_1_inventory_event.data[19])
        ship_1_products.append({"product_id": product_id_4, "product_name": product_id_4_name, "product_amount": product_id_4_amount})

        product_id_5 = felt.to_int(ship_1_inventory_event.data[20])
        product_id_5_name = types.getProductName(product_id_5)
        product_id_5_amount = felt.to_int(ship_1_inventory_event.data[21])
        ship_1_products.append({"product_id": product_id_5, "product_name": product_id_5_name, "product_amount": product_id_5_amount})

        product_id_6 = felt.to_int(ship_1_inventory_event.data[22])
        product_id_6_name = types.getProductName(product_id_6)
        product_id_6_amount = felt.to_int(ship_1_inventory_event.data[23])
        ship_1_products.append({"product_id": product_id_6, "product_name": product_id_6_name, "product_amount": product_id_6_amount})
        ships.append({"ship_id": ship_1_id, "ship_type": ship_1_type, "ship_type_name": ship_1_type_name, "ship_owner": ship_1_owner, "propellant": ship_1_propellant, "products": ship_1_products})

        ship_2_type = 2
        ship_2_type_name = types.getShipName(ship_2_type)
        ship_2_transfer_index = 10
        for txn in txns:
            if tx_hash == felt.to_hex(txn.transaction.meta.hash):
                for event in txn.receipt.events:
                    if int(event.index) == ship_2_transfer_index:
                        ship_2_transfer_event = event

        ship_2_products = []
        ship_2_owner = felt.to_hex(ship_2_transfer_event.data[1])
        ship_2_owner = from_address
        ship_2_id = felt.to_int(ship_2_transfer_event.data[2])
        ships.append({"ship_id": ship_2_id, "ship_type": ship_2_type, "ship_type_name": ship_2_type_name, "ship_owner": ship_2_owner, "propellant": 0, "products": ship_2_products})

        ship_3_type = 2
        ship_3_type_name = types.getShipName(ship_3_type)
        ship_3_transfer_index = 17
        for txn in txns:
            if tx_hash == felt.to_hex(txn.transaction.meta.hash):
                for event in txn.receipt.events:
                    if int(event.index) == ship_3_transfer_index:
                        ship_3_transfer_event = event

        ship_3_products = []
        ship_3_owner = felt.to_hex(ship_3_transfer_event.data[1])
        ship_3_owner = from_address
        ship_3_id = felt.to_int(ship_3_transfer_event.data[2])
        ships.append({"ship_id": ship_3_id, "ship_type": ship_3_type, "ship_type_name": ship_3_type_name, "ship_owner": ship_3_owner, "propellant": 0, "products": ship_3_products})

        ship_4_type = 4
        ship_4_type_name = types.getShipName(ship_4_type)
        ship_4_transfer_index = 24
        for txn in txns:
            if tx_hash == felt.to_hex(txn.transaction.meta.hash):
                for event in txn.receipt.events:
                    if int(event.index) == ship_4_transfer_index:
                        ship_4_transfer_event = event

        ship_4_products = []
        ship_4_owner = felt.to_hex(ship_4_transfer_event.data[1])
        ship_4_owner = from_address
        ship_4_id = felt.to_int(ship_4_transfer_event.data[2])
        ships.append({"ship_id": ship_4_id, "ship_type": ship_4_type, "ship_type_name": ship_4_type_name, "ship_owner": ship_4_owner, "propellant": 0, "products": ship_4_products})

        ship_5_type = 4
        ship_5_type_name = types.getShipName(ship_5_type)
        ship_5_transfer_index = 31
        for txn in txns:
            if tx_hash == felt.to_hex(txn.transaction.meta.hash):
                for event in txn.receipt.events:
                    if int(event.index) == ship_5_transfer_index:
                        ship_5_transfer_event = event

        ship_5_products = []
        ship_5_owner = felt.to_hex(ship_5_transfer_event.data[1])
        ship_5_owner = from_address
        ship_5_id = felt.to_int(ship_5_transfer_event.data[2])
        ships.append({"ship_id": ship_5_id, "ship_type": ship_5_type, "ship_type_name": ship_5_type_name, "ship_owner": ship_5_owner, "propellant": 0, "products": ship_5_products})

        ship_6_type = 3
        ship_6_type_name = types.getShipName(ship_6_type)
        ship_6_transfer_index = 38
        for txn in txns:
            if tx_hash == felt.to_hex(txn.transaction.meta.hash):
                for event in txn.receipt.events:
                    if int(event.index) == ship_6_transfer_index:
                        ship_6_transfer_event = event

        ship_6_products = []
        ship_6_owner = felt.to_hex(ship_6_transfer_event.data[1])
        ship_6_owner = from_address
        ship_6_id = felt.to_int(ship_6_transfer_event.data[2])
        ships.append({"ship_id": ship_6_id, "ship_type": ship_6_type, "ship_type_name": ship_6_type_name, "ship_owner": ship_6_owner, "propellant": 0, "products": ship_6_products})


    print(ships)
    return ships


async def processSellMarketOrderFilled(tx_hash, event, block_number, from_address, index, market_events, fee, timestamp):

    event_type=("SellMarketOrderFilled")
    counter = 0
    for market_event_with_tx in market_events:
        market_tx_hash = felt.to_hex(market_event_with_tx.transaction.meta.hash)
        if market_tx_hash == tx_hash:
            market_event = market_event_with_tx.event
            market_event_hex = market_event.keys[0]
            selector_hex = market_event_hex
            if selector_hex == sell_order_filled_key:
                counter+=1

    return counter


async def processBuyMarketOrderFilled(tx_hash, event, block_number, from_address, index, market_events, fee, timestamp):

    event_type=("BuylMarketOrderFilled")
    counter = 0
    for market_event_with_tx in market_events:
        market_tx_hash = felt.to_hex(market_event_with_tx.transaction.meta.hash)
        if market_tx_hash == tx_hash:
            market_event = market_event_with_tx.event
            market_event_hex = market_event.keys[0]
            selector_hex = market_event_hex
            if selector_hex == buy_order_filled_key:
                counter+=1

    return counter


async def processColonySeed(tx_hash, event, block_number, from_address, index, seed_events, fee, timestamp):

    event_type="ColonySeed"
    building_label = felt.to_int(event.data[0])
    building_id = felt.to_int(event.data[1])
    building_type = felt.to_int(event.data[2])
    asteroid_label = felt.to_int(event.data[3])
    asteroid_id = felt.to_int(event.data[4])
    lot_label = felt.to_int(event.data[5])
    packed_lot_id = felt.to_int(event.data[6])
    entity = sdk.unpackLot(packed_lot_id)
    lot_id = entity['lotIndex']
    caller_crew_label = felt.to_int(event.data[8])
    caller_crew_id = felt.to_int(event.data[9])
    caller_address = felt.to_hex(event.data[10])

    if building_type == 9:
        print("Habitat Colony Policy Seed")
        await processHabitatPolicies(tx_hash, event, block_number, from_address, index, seed_events, building_id, building_type, asteroid_id, packed_lot_id, lot_id, caller_crew_id, caller_address)

    if building_type == 8:
        print("Marketplace Colony Policy Seed")
        await processMarketplacePolicies(tx_hash, event, block_number, from_address, index, seed_events, building_id, building_type, asteroid_id, packed_lot_id, lot_id, caller_crew_id, caller_address)

    if building_type == 7:
        print("Spaceport Colony Policy Seed")
        await processSpaceportPolicies(tx_hash, event, block_number, from_address, index, seed_events, building_id, building_type, asteroid_id, packed_lot_id, lot_id, caller_crew_id, caller_address)

    if building_type == 1:
        print("Warehouse Colony Policy Seed")
        await processWarehousePolicies(tx_hash, event, block_number, from_address, index, seed_events, building_id, building_type, asteroid_id, packed_lot_id, lot_id, caller_crew_id, caller_address)


async def processConstructionAbandoned(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="ConstructionAbandoned"
    building_label = felt.to_int(event.data[0])
    building_id = felt.to_int(event.data[1])
    caller_crew_label = felt.to_int(event.data[2])
    caller_crew_id = felt.to_int(event.data[3])
    caller_address = felt.to_hex(event.data[4])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, building_label: %s, building_id: %s, caller_crew_label: %s, caller_crew_id: %s" % (block_number, event_type, tx_hash, from_address, caller_address, building_label, building_id, caller_crew_label, caller_crew_id))
    dispatcher_db.constructionAbandoned(tx_hash, block_number, from_address, caller_address, building_label, building_id, caller_crew_label, caller_crew_id, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processConstructionStarted(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="ConstructionFinished"
    building_label = felt.to_int(event.data[0])
    building_id = felt.to_int(event.data[1])
    finish_time = felt.to_int(event.data[2])
    caller_crew_label = felt.to_int(event.data[3])
    caller_crew_id = felt.to_int(event.data[4])
    caller_address = felt.to_hex(event.data[5])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, building_label: %s, building_id: %s, finish_time: %s, caller_crew_label: %s, caller_crew_id: %s" % (block_number, event_type, tx_hash, from_address, caller_address, building_label, building_id, finish_time, caller_crew_label, caller_crew_id))
    dispatcher_db.constructionStarted(tx_hash, block_number, from_address, caller_address, building_label, building_id, finish_time, caller_crew_label, caller_crew_id, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processSamplingDepositStarted(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="SamplingDepositStarted"
    deposit_label = felt.to_int(event.data[0])
    deposit_id = felt.to_int(event.data[1])
    lot_label = felt.to_int(event.data[2])
    packed_lot_id = felt.to_int(event.data[3])
    entity = sdk.unpackLot(packed_lot_id)
    asteroid_id = entity['asteroidId']
    lot_id = entity['lotIndex']
    resource_id = felt.to_int(event.data[4])
    finish_time = felt.to_int(event.data[5])
    caller_crew_label = felt.to_int(event.data[6])
    caller_crew_id = felt.to_int(event.data[7])
    caller_address = felt.to_hex(event.data[8])
    resource_name = types.getRawName(resource_id)
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, deposit_label: %s, deposit_id: %s, lot_label: %s, lot_id: %s, packed_lot_id: %s, resource_id: %s, resource_name: %s, finish_time: %s, asteroid_id: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, lot_label, lot_id, packed_lot_id, resource_id, resource_name, finish_time, asteroid_id))
    dispatcher_db.samplingDepositStarted(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, lot_label, lot_id, packed_lot_id, resource_id, resource_name, finish_time, asteroid_id, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processSamplingDepositStartedV1(tx_hash, event, block_number, from_address, origin_inventory, fee, timestamp):

    event_type="SamplingDepositStartedV1"
    deposit_label = felt.to_int(event.data[0])
    deposit_id = felt.to_int(event.data[1])
    lot_label = felt.to_int(event.data[2])
    packed_lot_id = felt.to_int(event.data[3])
    entity = sdk.unpackLot(packed_lot_id)
    asteroid_id = entity['asteroidId']
    lot_id = entity['lotIndex']
    resource_id = felt.to_int(event.data[4])
    improving = felt.to_int(event.data[5])
    origin_label = felt.to_int(event.data[6])
    origin_id = felt.to_int(event.data[7])
    origin_slot = felt.to_int(event.data[8])
    finish_time = felt.to_int(event.data[9])
    caller_crew_label = felt.to_int(event.data[10])
    caller_crew_id = felt.to_int(event.data[11])
    caller_address = felt.to_hex(event.data[12])
    resource_name = types.getRawName(resource_id)
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, deposit_label: %s, deposit_id: %s, lot_label: %s, lot_id: %s, packed_lot_id: %s, resource_id: %s, resource_name: %s, improving: %s, origin_label: %s, origin_id: %s, origin_slot: %s, finish_time: %s, asteroid_id: %s, origin_inventory: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, lot_label, lot_id, packed_lot_id, resource_id, resource_name, improving, origin_label, origin_id, origin_slot, finish_time, asteroid_id, origin_inventory))
    dispatcher_db.samplingDepositStartedV1(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, lot_label, lot_id, packed_lot_id, resource_id, resource_name, improving, origin_label, origin_id, origin_slot, finish_time, asteroid_id, origin_inventory, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processSamplingDepositFinished(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="SamplingDepositFinished"
    deposit_label = felt.to_int(event.data[0])
    deposit_id = felt.to_int(event.data[1])
    initial_yield = felt.to_int(event.data[2])
    caller_crew_label = felt.to_int(event.data[3])
    caller_crew_id = felt.to_int(event.data[4])
    caller_address = felt.to_hex(event.data[5])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, deposit_label: %s, deposit_id: %s, initial_yield: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, initial_yield))
    dispatcher_db.samplingDepositFinished(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, initial_yield, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processResourceExtractionStarted(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="ResourceExtractionStarted"
    deposit_label = felt.to_int(event.data[0])
    deposit_id = felt.to_int(event.data[1])
    resource_id = felt.to_int(event.data[2])
    resource_name = types.getRawName(resource_id)
    resource_yield = felt.to_int(event.data[3])
    extractor_label = felt.to_int(event.data[4])
    extractor_id = felt.to_int(event.data[5])
    extractor_slot = felt.to_int(event.data[6])
    destination_label = felt.to_int(event.data[7])
    destination_id = felt.to_int(event.data[8])
    destination_slot = felt.to_int(event.data[9])
    finish_time = felt.to_int(event.data[10])
    caller_crew_label = felt.to_int(event.data[11])
    caller_crew_id = felt.to_int(event.data[12])
    caller_address = felt.to_hex(event.data[13])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, deposit_label: %s, deposit_id: %s, resource_yield: %s, extractor_label: %s, extractor_id: %s, extractor_slot: %s, destination_label: %s, destination_id: %s, destination_slot: %s, finish_time: %s, resource_id: %s, resource_name: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, resource_yield, extractor_label, extractor_id, extractor_slot, destination_label, destination_id, destination_slot, finish_time, resource_id, resource_name))
    dispatcher_db.resourceExtractionStarted(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, resource_id, resource_name, resource_yield, extractor_label, extractor_id, extractor_slot, destination_label, destination_id, destination_slot, finish_time, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processResourceExtractionFinished(tx_hash, event, block_number, from_address, destination_inventory, fee, timestamp):

    event_type="ResourceExtractionFinished"
    extractor_label = felt.to_int(event.data[0])
    extractor_id = felt.to_int(event.data[1])
    extractor_slot = felt.to_int(event.data[2])
    resource_id = felt.to_int(event.data[3])
    resource_name = types.getRawName(resource_id)
    resource_yield = felt.to_int(event.data[4])
    destination_label = felt.to_int(event.data[5])
    destination_id = felt.to_int(event.data[6])
    destination_slot = felt.to_int(event.data[7])
    caller_crew_label = felt.to_int(event.data[8])
    caller_crew_id = felt.to_int(event.data[9])
    caller_address = felt.to_hex(event.data[10])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, extractor_label: %s, extractor_id: %s, extractor_slot: %s, resource_id: %s, resource_name: %s, resource_yield: %s, destination_label: %s, destination_id: %s, destination_slot: %s, destination_inventory: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, extractor_label, extractor_id, extractor_slot, resource_id, resource_name, resource_yield, destination_label, destination_id, destination_slot, destination_inventory))
    dispatcher_db.resourceExtractionFinished(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, extractor_label, extractor_id, extractor_slot, resource_id, resource_name, resource_yield, destination_label, destination_id, destination_slot, destination_inventory, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processMaterialProcessingStartedV1(tx_hash, event, block_number, from_address, origin_inventory, fee, timestamp):

    event_type="MaterialProcessingStartedV1"
    inputs = []
    processor_label = felt.to_int(event.data[0])
    processor_id = felt.to_int(event.data[1])
    processor_slot = felt.to_int(event.data[2])
    process_id = felt.to_int(event.data[3])
    process_name = types.getProcessName(process_id)
    inputs_len = felt.to_int(event.data[4])
    inputs_start_pos = 5

    print("inputs_start_pos: %s" % inputs_start_pos)

    if inputs_len == 1:
        inputs_end_pos = (inputs_start_pos + 1)
        product_id = felt.to_int(event.data[inputs_start_pos])
        product_amount = felt.to_int(event.data[inputs_end_pos])
        origin_label_pos = (inputs_end_pos + 1)
        print("product_id: %s" % product_id)
        print("product_amount: %s" % product_amount)
        product_name = types.getProductName(product_id)
        inputs.append({"id": product_id, "amount": product_amount, "name": product_name})
    else:
        inputs_len_doubled = (inputs_len * 2)
        inputs_end_pos = (inputs_start_pos + inputs_len_doubled)
        origin_label_pos = inputs_end_pos
        count = inputs_len
        anchor_pos = inputs_start_pos
        print("count before loop is %s" % count)
        print("anchor_pos before loop is %s" % anchor_pos)
        while count > 0:
            print("count in loop is %s" % count)
            while anchor_pos < inputs_end_pos:
                product_id = felt.to_int(event.data[anchor_pos])
                print("product_id: %s" % product_id)
                anchor_pos+=1
                print("anchor_pos in loop: %s" % anchor_pos)
                product_amount = felt.to_int(event.data[anchor_pos])
                print("product_amount: %s" % product_amount)
                product_name = types.getProductName(product_id)
                inputs.append({"id": product_id, "amount": product_amount, "name": product_name})
                anchor_pos+=1
                print("anchor_pos in loop: %s" % anchor_pos)
                count-=1

    print("inputs: %s" % inputs)

    origin_label = felt.to_int(event.data[origin_label_pos])
    origin_id_pos = (origin_label_pos + 1)
    origin_id = felt.to_int(event.data[origin_id_pos])
    origin_slot_pos = (origin_id_pos + 1)
    origin_slot = felt.to_int(event.data[origin_slot_pos])
    outputs_len_pos = (origin_slot_pos + 1)
    outputs_len = felt.to_int(event.data[outputs_len_pos])
    outputs_start_pos = (outputs_len_pos + 1)

    outputs = []
    if outputs_len == 1:
        outputs_end_pos = (outputs_start_pos + 1)
        destination_label_pos = (outputs_end_pos + 1)
        product_id = felt.to_int(event.data[outputs_start_pos])
        product_amount = felt.to_int(event.data[outputs_end_pos])
        print("product_id: %s" % product_id)
        print("product_amount: %s" % product_amount)
        product_name = types.getProductName(product_id)
        outputs.append({"id": product_id, "amount": product_amount, "name": product_name})
    else:
        outputs_len_doubled = (outputs_len * 2)
        outputs_end_pos = (outputs_start_pos + outputs_len_doubled)
        destination_label_pos = outputs_end_pos
        count = outputs_len
        anchor_pos = outputs_start_pos
        print("count before loop is %s" % count)
        print("anchor_pos before loop is %s" % anchor_pos)
        while count > 0:
            print("count in loop is %s" % count)
            while anchor_pos < outputs_end_pos:
                product_id = felt.to_int(event.data[anchor_pos])
                print("product_id: %s" % product_id)
                anchor_pos+=1
                print("anchor_pos in loop: %s" % anchor_pos)
                product_amount = felt.to_int(event.data[anchor_pos])
                print("product_amount: %s" % product_amount)
                product_name = types.getProductName(product_id)
                outputs.append({"id": product_id, "amount": product_amount, "name": product_name})
                anchor_pos+=1
                print("anchor_pos in loop: %s" % anchor_pos)
                count-=1

    print("outputs: %s" % outputs)
    destination_label = felt.to_int(event.data[destination_label_pos])
    destination_id_pos = (destination_label_pos + 1)
    destination_id = felt.to_int(event.data[destination_id_pos])
    destination_slot_pos = (destination_id_pos + 1)
    destination_slot = felt.to_int(event.data[destination_slot_pos])
    finish_time_pos = (destination_slot_pos + 1)
    finish_time = felt.to_int(event.data[finish_time_pos])
    caller_crew_label_pos = (finish_time_pos + 1)
    caller_crew_label = felt.to_int(event.data[caller_crew_label_pos])
    caller_crew_id_pos = (caller_crew_label_pos + 1)
    caller_crew_id = felt.to_int(event.data[caller_crew_id_pos])
    caller_address_pos = (caller_crew_id_pos + 1)
    caller_address = felt.to_hex(event.data[caller_address_pos])

    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, processor_label: %s, processor_id: %s, processor_slot: %s, process_id: %s, process_name: %s, inputs: %s, origin_label: %s, origin_id: %s, origin_slot: %s, outputs: %s, destination_label: %s, destination_id: %s, destination_slot: %s, finish_time: %s, origin_inventory: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, processor_label, processor_id, processor_slot, process_id, process_name, inputs, origin_label, origin_id, origin_slot, outputs, destination_label, destination_id, destination_slot, finish_time, origin_inventory))
    dispatcher_db.materialProcessingStartedV1(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, processor_label, processor_id, processor_slot, process_id, process_name, inputs, origin_label, origin_id, origin_slot, outputs, destination_label, destination_id, destination_slot, finish_time, origin_inventory, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processMaterialProcessingFinished(tx_hash, event, block_number, from_address, destination_inventory, fee, timestamp):

    event_type="MaterialProcessingFinished"
    processor_label = felt.to_int(event.data[0])
    processor_id = felt.to_int(event.data[1])
    processor_slot = felt.to_int(event.data[2])
    caller_crew_label = felt.to_int(event.data[3])
    caller_crew_id = felt.to_int(event.data[4])
    caller_address = felt.to_hex(event.data[5])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, processor_label: %s, processor_id: %s, processor_slot: %s, destination_inventory: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, processor_label, processor_id, processor_slot, destination_inventory))
    dispatcher_db.materialProcessingFinished(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, processor_label, processor_id, processor_slot, destination_inventory, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processFoodSupplied(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="FoodSupplied"
    food = felt.to_int(event.data[0])
    last_fed = felt.to_int(event.data[1])
    caller_crew_label = felt.to_int(event.data[2])
    caller_crew_id = felt.to_int(event.data[3])
    caller_address = felt.to_hex(event.data[4])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, food: %s, last_fed: %s, caller_crew_id: %s, caller_crew_label: %s" % (block_number, event_type, tx_hash, from_address, caller_address, food, last_fed, caller_crew_id, caller_crew_label))
    dispatcher_db.foodSupplied(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, food, last_fed, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processFoodSuppliedV1(tx_hash, event, block_number, from_address, origin_inventory, fee, timestamp):

    event_type="FoodSuppliedV1"
    food = felt.to_int(event.data[0])
    last_fed = felt.to_int(event.data[1])
    origin_label = felt.to_int(event.data[2])
    origin_id = felt.to_int(event.data[3])
    origin_slot = felt.to_int(event.data[4])
    caller_crew_label = felt.to_int(event.data[5])
    caller_crew_id = felt.to_int(event.data[6])
    caller_address = felt.to_hex(event.data[7])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, food: %s, last_fed: %s, caller_crew_id: %s, caller_crew_label: %s, origin_label: %s, origin_id: %s, origin_slot: %s, origin_inventory: %s" % (block_number, event_type, tx_hash, from_address, caller_address, food, last_fed, caller_crew_id, caller_crew_label, origin_label, origin_id, origin_slot, origin_inventory))
    dispatcher_db.foodSuppliedV1(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, food, last_fed, origin_label, origin_id, origin_slot, origin_inventory, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processShipUndocked(tx_hash, event, block_number, from_address, fee, timestamp, inventory_event):

    event_type="ShipUndocked"
    asteroid_id = "NULL"
    lot_id = "NULL"
    ship_label = felt.to_int(event.data[0])
    ship_id = felt.to_int(event.data[1])
    dock_label = felt.to_int(event.data[2])
    dock_id = felt.to_int(event.data[3])
    caller_crew_label = felt.to_int(event.data[4])
    caller_crew_id = felt.to_int(event.data[5])
    caller_address = felt.to_hex(event.data[6])
    if dock_label == 4:
        entity = sdk.unpackLot(dock_id)
        asteroid_id = entity['asteroidId']
        lot_id = entity['lotIndex']

    if inventory_event is not None:
        print(inventory_event.data)
        new_fuel = felt.to_int(inventory_event.data[11])
    else:
        new_fuel = None

    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, ship_label: %s, ship_id: %s, dock_label: %s, dock_id: %s, caller_crew_id: %s, caller_crew_label: %s, asteroid_id: %s, lot_id: %s, new_fuel: %s" % (block_number, event_type, tx_hash, from_address, caller_address, ship_label, ship_id, dock_label, dock_id, caller_crew_id, caller_crew_label, asteroid_id, lot_id, new_fuel))
    dispatcher_db.shipUndocked(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, dock_label, dock_id, asteroid_id, lot_id, fee, timestamp, new_fuel)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processShipDocked(tx_hash, event, block_number, from_address, fee, timestamp, inventory_event):

    event_type="ShipDocked"
    asteroid_id = "NULL"
    lot_id = "NULL"
    ship_label = felt.to_int(event.data[0])
    ship_id = felt.to_int(event.data[1])
    dock_label = felt.to_int(event.data[2])
    dock_id = felt.to_int(event.data[3])
    caller_crew_label = felt.to_int(event.data[4])
    caller_crew_id = felt.to_int(event.data[5])
    caller_address = felt.to_hex(event.data[6])
    if dock_label == 4:
        entity = sdk.unpackLot(dock_id)
        asteroid_id = entity['asteroidId']
        lot_id = entity['lotIndex']

    if inventory_event is not None:
        print(inventory_event.data)
        new_fuel = felt.to_int(inventory_event.data[11])
    else:
        new_fuel = None

    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, ship_label: %s, ship_id: %s, dock_label: %s, dock_id: %s, caller_crew_id: %s, caller_crew_label: %s, asteroid_id: %s, lot_id: %s, new_fuel: %s" % (block_number, event_type, tx_hash, from_address, caller_address, ship_label, ship_id, dock_label, dock_id, caller_crew_id, caller_crew_label, asteroid_id, lot_id, new_fuel))
    dispatcher_db.shipDocked(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, dock_label, dock_id, asteroid_id, lot_id, fee, timestamp, new_fuel)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processShipAssemblyStartedV1(tx_hash, event, block_number, from_address, origin_inventory, fee, timestamp):

    event_type="ShipAssemblyStartedV1"
    ship_label = felt.to_int(event.data[0])
    ship_id = felt.to_int(event.data[1])
    ship_type = felt.to_int(event.data[2])
    ship_type_name = types.getShipName(ship_type)
    dry_dock_label = felt.to_int(event.data[3])
    dry_dock_id = felt.to_int(event.data[4])
    dry_dock_slot = felt.to_int(event.data[5])
    origin_label = felt.to_int(event.data[6])
    origin_id = felt.to_int(event.data[7])
    origin_slot = felt.to_int(event.data[8])
    finish_time = felt.to_int(event.data[9])
    caller_crew_label = felt.to_int(event.data[10])
    caller_crew_id = felt.to_int(event.data[11])
    caller_address = felt.to_hex(event.data[12])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, ship_label: %s, ship_id: %s, ship_type: %s, ship_type_name: %s, dry_dock_label: %s, dry_dock_id: %s, dry_dock_slot: %s, origin_label: %s, origin_id: %s, origin_slot: %s, finish_time: %s, caller_crew_id: %s, caller_crew_label: %s, origin_inventory: %s" % (block_number, event_type, tx_hash, from_address, caller_address, ship_label, ship_id, ship_type, ship_type_name, dry_dock_label, dry_dock_id, dry_dock_slot, origin_label, origin_id, origin_slot, finish_time, caller_crew_id, caller_crew_label, origin_inventory))
    dispatcher_db.shipAssemblyStartedV1(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, ship_type, ship_type_name, dry_dock_label, dry_dock_id, dry_dock_slot, origin_label, origin_id, origin_slot, finish_time, origin_inventory, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processShipAssemblyFinished(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="ShipAssemblyFinished"
    ship_label = felt.to_int(event.data[0])
    ship_id = felt.to_int(event.data[1])
    dry_dock_label = felt.to_int(event.data[2])
    dry_dock_id = felt.to_int(event.data[3])
    dry_dock_slot = felt.to_int(event.data[4])
    destination_label = felt.to_int(event.data[5])
    destination_id = felt.to_int(event.data[6])
    finish_time = felt.to_int(event.data[7])
    caller_crew_label = felt.to_int(event.data[8])
    caller_crew_id = felt.to_int(event.data[9])
    caller_address = felt.to_hex(event.data[10])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, ship_label: %s, ship_id: %s, dry_dock_label: %s, dry_dock_id: %s, dry_dock_slot: %s, destination_label: %s, destination_id: %s, finish_time: %s, caller_crew_label: %s, caller_crew_id: %s, caller_address: %s" % (block_number, event_type, tx_hash, from_address, caller_address, ship_label, ship_id, dry_dock_label, dry_dock_id, dry_dock_slot, destination_label, destination_id, finish_time, caller_crew_label, caller_crew_id, caller_address))
    dispatcher_db.shipAssemblyFinished(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, dry_dock_label, dry_dock_id, dry_dock_slot, destination_label, destination_id, finish_time, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processCrewStationed(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="CrewStationed"
    station_label = felt.to_int(event.data[0])
    station_id = felt.to_int(event.data[1])
    finish_time = felt.to_int(event.data[2])
    caller_crew_label = felt.to_int(event.data[3])
    caller_crew_id = felt.to_int(event.data[4])
    caller_address = felt.to_hex(event.data[5])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, station_label: %s, station_id: %s, finish_time: %s, caller_crew_label: %s, caller_crew_id: %s" % (block_number, event_type, tx_hash, from_address, caller_address, station_label, station_id, finish_time, caller_crew_label, caller_crew_id))
    dispatcher_db.crewStationed(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, station_label, station_id, finish_time, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processCrewStationedV1(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="CrewStationedV1"
    origin_station_label = felt.to_int(event.data[0])
    origin_station_id = felt.to_int(event.data[1])
    destination_station_label = felt.to_int(event.data[2])
    destination_station_id = felt.to_int(event.data[3])
    finish_time = felt.to_int(event.data[4])
    caller_crew_label = felt.to_int(event.data[5])
    caller_crew_id = felt.to_int(event.data[6])
    caller_address = felt.to_hex(event.data[7])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, origin_station_label: %s, origin_station_id: %s, destination_station_label: %s, destination_station_id: %s, finish_time: %s, caller_crew_label: %s, caller_crew_id: %s" % (block_number, event_type, tx_hash, from_address, caller_address, origin_station_label, origin_station_id, destination_station_label, destination_station_id, finish_time, caller_crew_label, caller_crew_id))
    dispatcher_db.crewStationedV1(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, origin_station_label, origin_station_id, destination_station_label, destination_station_id, finish_time, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processEmergencyPropellantCollected(tx_hash, event, block_number, from_address, fee, timestamp, inventory_event):

    event_type="EmergencyPropellantCollected"
    ship_label = felt.to_int(event.data[0])
    ship_id = felt.to_int(event.data[1])
    amount = felt.to_int(event.data[2])
    caller_crew_label = felt.to_int(event.data[3])
    caller_crew_id = felt.to_int(event.data[4])
    caller_address = felt.to_hex(event.data[5])
    new_fuel = felt.to_int(inventory_event.data[11])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s ship_label: %s, ship_id: %s, amount: %s, caller_crew_label: %s, caller_crew_id: %s, caller_address: %s, new_fuel: %s" % (block_number, event_type, tx_hash, from_address, caller_address, ship_label, ship_id, amount, caller_crew_label, caller_crew_id, caller_address, new_fuel))
    dispatcher_db.emergencyPropellantCollected(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, amount, fee, timestamp, new_fuel)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processEmergencyActivated(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="EmergencyActivated"
    ship_label = felt.to_int(event.data[0])
    ship_id = felt.to_int(event.data[1])
    caller_crew_label = felt.to_int(event.data[2])
    caller_crew_id = felt.to_int(event.data[3])
    caller_address = felt.to_hex(event.data[4])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s ship_label: %s, ship_id: %s, caller_crew_label: %s, caller_crew_id: %s, caller_address: %s" % (block_number, event_type, tx_hash, from_address, caller_address, ship_label, ship_id, caller_crew_label, caller_crew_id, caller_address))
    dispatcher_db.emergencyActivated(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processEmergencyDeactivated(tx_hash, event, block_number, from_address, fee, timestamp, inventory_event):

    event_type="EmergencyDeactivated"
    ship_label = felt.to_int(event.data[0])
    ship_id = felt.to_int(event.data[1])
    caller_crew_label = felt.to_int(event.data[2])
    caller_crew_id = felt.to_int(event.data[3])
    caller_address = felt.to_hex(event.data[4])
    if inventory_event is not None:
        new_fuel = felt.to_int(inventory_event.data[11])
    else:
        new_fuel = None

    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s ship_label: %s, ship_id: %s, caller_crew_label: %s, caller_crew_id: %s, caller_address: %s, new_fuel: %s" % (block_number, event_type, tx_hash, from_address, caller_address, ship_label, ship_id, caller_crew_label, caller_crew_id, caller_address, new_fuel))
    dispatcher_db.emergencyDeactivated(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, fee, timestamp, new_fuel)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processDeliveryStarted(tx_hash, event, block_number, from_address, origin_inventory, fee, timestamp):

    event_type="DeliveryStarted"
    products = []
    for item in event.data:
        print("item: %s" % felt.to_int(item))

    origin_label = felt.to_int(event.data[0])
    origin_id = felt.to_int(event.data[1])
    origin_slot = felt.to_int(event.data[2])
    product_len = felt.to_int(event.data[3])
    product_start_pos = 4

    if product_len == 1:
        product_end_pos = (product_start_pos + 1)
        product_id = felt.to_int(event.data[product_start_pos])
        product_amount = felt.to_int(event.data[product_end_pos])
        product_name = types.getProductName(product_id)
        products.append({"id": product_id, "amount": product_amount, "name": product_name})
    else:
        product_len_doubled = (product_len * 2)
        product_end_pos = (product_start_pos + product_len_doubled)
        count = product_len
        anchor_pos = product_start_pos
        while count > 0:
            while anchor_pos < product_end_pos:
                product_id = felt.to_int(event.data[anchor_pos])
                anchor_pos+=1
                product_amount = felt.to_int(event.data[anchor_pos])
                product_name = types.getProductName(product_id)
                products.append({"id": product_id, "amount": product_amount, "name": product_name})
                anchor_pos+=1
                count-=1

    print("products: %s" % products)

    if product_len > 1:
        dest_label_pos = product_end_pos
    else:
        dest_label_pos = (product_end_pos + 1)

    dest_label = felt.to_int(event.data[dest_label_pos])
    dest_id_pos = (dest_label_pos + 1)
    dest_id = felt.to_int(event.data[dest_id_pos])
    dest_slot_pos = (dest_id_pos + 1)
    dest_slot = felt.to_int(event.data[dest_slot_pos])
    delivery_label_pos = (dest_slot_pos + 1)
    delivery_label = felt.to_int(event.data[delivery_label_pos])
    delivery_id_pos = (delivery_label_pos + 1)
    delivery_id = felt.to_int(event.data[delivery_id_pos])
    finish_time_pos = (delivery_id_pos + 1)
    finish_time = felt.to_int(event.data[finish_time_pos])
    caller_crew_label_pos = (finish_time_pos + 1)
    caller_crew_label = felt.to_int(event.data[caller_crew_label_pos])
    caller_crew_id_pos = (caller_crew_label_pos + 1)
    caller_crew_id = felt.to_int(event.data[caller_crew_id_pos])
    caller_address_pos = (caller_crew_id_pos + 1)
    caller_address = felt.to_hex(event.data[caller_address_pos])

    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, origin_label: %s, origin_id: %s, origin_slot: %s, dest_label: %s, dest_id: %s, dest_slot: %s, delivery_label: %s, delivery_id: %s, finish_time: %s, caller_crew_label: %s, caller_crew_id: %s, caller_address: %s, products: %s, origin_inventory: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_slot, dest_label, dest_id, dest_slot, delivery_label, delivery_id, finish_time, caller_crew_label, caller_crew_id, caller_address, products, origin_inventory))
    dispatcher_db.deliveryStarted(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_slot, dest_label, dest_id, dest_slot, delivery_label, delivery_id, finish_time, products, origin_inventory, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processDeliverySent(tx_hash, event, block_number, from_address, destination_inventory, origin_inventory, delivery_manifest, fee, timestamp):

    event_type="DeliverySent"

    products = []
    for item in event.data:
        print("item: %s" % felt.to_int(item))

    origin_label = felt.to_int(event.data[0])
    origin_id = felt.to_int(event.data[1])
    origin_slot = felt.to_int(event.data[2])
    product_len = felt.to_int(event.data[3])
    product_start_pos = 4

    if product_len == 0:
        return

    if product_len == 1:
        product_end_pos = (product_start_pos + 1)
        product_id = felt.to_int(event.data[product_start_pos])
        product_amount = felt.to_int(event.data[product_end_pos])
        product_name = types.getProductName(product_id)
        products.append({"id": product_id, "amount": product_amount, "name": product_name})
    else:
        product_len_doubled = (product_len * 2)
        product_end_pos = (product_start_pos + product_len_doubled)
        count = product_len
        anchor_pos = product_start_pos
        while count > 0:
            while anchor_pos < product_end_pos:
                product_id = felt.to_int(event.data[anchor_pos])
                anchor_pos+=1
                product_amount = felt.to_int(event.data[anchor_pos])
                product_name = types.getProductName(product_id)
                products.append({"id": product_id, "amount": product_amount, "name": product_name})
                anchor_pos+=1
                count-=1

    if product_len > 1:
        dest_label_pos = product_end_pos
    else:
        dest_label_pos = (product_end_pos + 1)

    dest_label = felt.to_int(event.data[dest_label_pos])
    dest_id_pos = (dest_label_pos + 1)
    dest_id = felt.to_int(event.data[dest_id_pos])
    dest_slot_pos = (dest_id_pos + 1)
    dest_slot = felt.to_int(event.data[dest_slot_pos])
    delivery_label_pos = (dest_slot_pos + 1)
    delivery_label = felt.to_int(event.data[delivery_label_pos])
    delivery_id_pos = (delivery_label_pos + 1)
    delivery_id = felt.to_int(event.data[delivery_id_pos])
    finish_time_pos = (delivery_id_pos + 1)
    finish_time = felt.to_int(event.data[finish_time_pos])
    caller_crew_label_pos = (finish_time_pos + 1)
    caller_crew_label = felt.to_int(event.data[caller_crew_label_pos])
    caller_crew_id_pos = (caller_crew_label_pos + 1)
    caller_crew_id = felt.to_int(event.data[caller_crew_id_pos])
    caller_address_pos = (caller_crew_id_pos + 1)
    caller_address = felt.to_hex(event.data[caller_address_pos])

    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, origin_label: %s, origin_id: %s, origin_slot: %s, dest_label: %s, dest_id: %s, dest_slot: %s, delivery_label: %s, delivery_id: %s, finish_time: %s, caller_crew_label: %s, caller_crew_id: %s, caller_address: %s, products: %s, destination_inventory: %s, origin_inventory: %s, delivery_manifest: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_slot, dest_label, dest_id, dest_slot, delivery_label, delivery_id, finish_time, caller_crew_label, caller_crew_id, caller_address, products, destination_inventory, origin_inventory, delivery_manifest))
    dispatcher_db.deliverySent(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_slot, dest_label, dest_id, dest_slot, delivery_label, delivery_id, finish_time, products, destination_inventory, origin_inventory, delivery_manifest, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processDeliveryReceived(tx_hash, event, block_number, from_address, destination_inventory, delivery_manifest, fee, timestamp):

    event_type="DeliveryReceived"
    products = []
    for item in event.data:
        print("item: %s" % felt.to_int(item))

    origin_label = felt.to_int(event.data[0])
    origin_id = felt.to_int(event.data[1])
    origin_slot = felt.to_int(event.data[2])
    product_len = felt.to_int(event.data[3])
    product_start_pos = 4

    if product_len == 0:
        return

    if product_len == 1:
        product_end_pos = (product_start_pos + 1)
        product_id = felt.to_int(event.data[product_start_pos])
        product_amount = felt.to_int(event.data[product_end_pos])
        product_name = types.getProductName(product_id)
        products.append({"id": product_id, "amount": product_amount, "name": product_name})
    else:
        product_len_doubled = (product_len * 2)
        product_end_pos = (product_start_pos + product_len_doubled)
        count = product_len
        anchor_pos = product_start_pos
        while count > 0:
            while anchor_pos < product_end_pos:
                product_id = felt.to_int(event.data[anchor_pos])
                anchor_pos+=1
                product_amount = felt.to_int(event.data[anchor_pos])
                product_name = types.getProductName(product_id)
                products.append({"id": product_id, "amount": product_amount, "name": product_name})
                anchor_pos+=1
                count-=1

    if product_len > 1:
        dest_label_pos = product_end_pos
    else:
        dest_label_pos = (product_end_pos + 1)

    dest_label = felt.to_int(event.data[dest_label_pos])
    dest_id_pos = (dest_label_pos + 1)
    dest_id = felt.to_int(event.data[dest_id_pos])
    dest_slot_pos = (dest_id_pos + 1)
    dest_slot = felt.to_int(event.data[dest_slot_pos])
    delivery_label_pos = (dest_slot_pos + 1)
    delivery_label = felt.to_int(event.data[delivery_label_pos])
    delivery_id_pos = (delivery_label_pos + 1)
    delivery_id = felt.to_int(event.data[delivery_id_pos])
    caller_crew_label_pos = (delivery_id_pos + 1)
    caller_crew_label = felt.to_int(event.data[caller_crew_label_pos])
    caller_crew_id_pos = (caller_crew_label_pos + 1)
    caller_crew_id = felt.to_int(event.data[caller_crew_id_pos])
    caller_address_pos = (caller_crew_id_pos + 1)
    caller_address = felt.to_hex(event.data[caller_address_pos])

    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, origin_label: %s, origin_id: %s, origin_slot: %s, dest_label: %s, dest_id: %s, dest_slot: %s, delivery_label: %s, delivery_id: %s, caller_crew_label: %s, caller_crew_id: %s, caller_address: %s, products: %s, destination_inventory: %s, delivery_manifest: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_slot, dest_label, dest_id, dest_slot, delivery_label, delivery_id, caller_crew_label, caller_crew_id, caller_address, products, destination_inventory, delivery_manifest))
    dispatcher_db.deliveryReceived(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_slot, dest_label, dest_id, dest_slot, delivery_label, delivery_id, products, destination_inventory, delivery_manifest, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processDeliveryCancelled(tx_hash, event, block_number, from_address, origin_inventory, fee, timestamp):

    event_type="DeliveryCancelled"
    products = []
    for item in event.data:
        print("item: %s" % felt.to_int(item))

    origin_label = felt.to_int(event.data[0])
    origin_id = felt.to_int(event.data[1])
    origin_slot = felt.to_int(event.data[2])
    product_len = felt.to_int(event.data[3])
    product_start_pos = 4

    if product_len == 1:
        product_end_pos = (product_start_pos + 1)
        product_id = felt.to_int(event.data[product_start_pos])
        product_amount = felt.to_int(event.data[product_end_pos])
        product_name = types.getProductName(product_id)
        products.append({"id": product_id, "amount": product_amount, "name": product_name})
    else:
        product_len_doubled = (product_len * 2)
        product_end_pos = (product_start_pos + product_len_doubled)
        count = product_len
        anchor_pos = product_start_pos
        while count > 0:
            while anchor_pos < product_end_pos:
                product_id = felt.to_int(event.data[anchor_pos])
                anchor_pos+=1
                product_amount = felt.to_int(event.data[anchor_pos])
                product_name = types.getProductName(product_id)
                products.append({"id": product_id, "amount": product_amount, "name": product_name})
                anchor_pos+=1
                count-=1

    if product_len > 1:
        dest_label_pos = product_end_pos
    else:
        dest_label_pos = (product_end_pos + 1)

    dest_label = felt.to_int(event.data[dest_label_pos])
    dest_id_pos = (dest_label_pos + 1)
    dest_id = felt.to_int(event.data[dest_id_pos])
    dest_slot_pos = (dest_id_pos + 1)
    dest_slot = felt.to_int(event.data[dest_slot_pos])
    delivery_label_pos = (dest_slot_pos + 1)
    delivery_label = felt.to_int(event.data[delivery_label_pos])
    delivery_id_pos = (delivery_label_pos + 1)
    delivery_id = felt.to_int(event.data[delivery_id_pos])
    caller_crew_label_pos = (delivery_id_pos + 1)
    caller_crew_label = felt.to_int(event.data[caller_crew_label_pos])
    caller_crew_id_pos = (caller_crew_label_pos + 1)
    caller_crew_id = felt.to_int(event.data[caller_crew_id_pos])
    caller_address_pos = (caller_crew_id_pos + 1)
    caller_address = felt.to_hex(event.data[caller_address_pos])

    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, origin_label: %s, origin_id: %s, origin_slot: %s, dest_label: %s, dest_id: %s, dest_slot: %s, delivery_label: %s, delivery_id: %s, caller_crew_label: %s, caller_crew_id: %s, caller_address: %s, products: %s, origin_inventory: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_slot, dest_label, dest_id, dest_slot, delivery_label, delivery_id, caller_crew_label, caller_crew_id, caller_address, products, origin_inventory))
    dispatcher_db.deliveryCancelled(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_slot, dest_label, dest_id, dest_slot, delivery_label, delivery_id, products, origin_inventory, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processDeliveryPackaged(tx_hash, event, block_number, from_address, origin_inventory, fee, timestamp):

    event_type="DeliveryPackaged"
    products = []
    for item in event.data:
        print("item: %s" % felt.to_int(item))

    origin_label = felt.to_int(event.data[0])
    origin_id = felt.to_int(event.data[1])
    origin_slot = felt.to_int(event.data[2])
    product_len = felt.to_int(event.data[3])
    product_start_pos = 4

    if product_len == 1:
        product_end_pos = (product_start_pos + 1)
        product_id = felt.to_int(event.data[product_start_pos])
        product_amount = felt.to_int(event.data[product_end_pos])
        product_name = types.getProductName(product_id)
        products.append({"id": product_id, "amount": product_amount, "name": product_name})
    else:
        product_len_doubled = (product_len * 2)
        product_end_pos = (product_start_pos + product_len_doubled)
        count = product_len
        anchor_pos = product_start_pos
        while count > 0:
            while anchor_pos < product_end_pos:
                product_id = felt.to_int(event.data[anchor_pos])
                anchor_pos+=1
                product_amount = felt.to_int(event.data[anchor_pos])
                product_name = types.getProductName(product_id)
                products.append({"id": product_id, "amount": product_amount, "name": product_name})
                anchor_pos+=1
                count-=1

    if product_len > 1:
        dest_label_pos = product_end_pos
    else:
        dest_label_pos = (product_end_pos + 1)

    dest_label = felt.to_int(event.data[dest_label_pos])
    dest_id_pos = (dest_label_pos + 1)
    dest_id = felt.to_int(event.data[dest_id_pos])
    dest_slot_pos = (dest_id_pos + 1)
    dest_slot = felt.to_int(event.data[dest_slot_pos])
    delivery_label_pos = (dest_slot_pos + 1)
    delivery_label = felt.to_int(event.data[delivery_label_pos])
    delivery_id_pos = (delivery_label_pos + 1)
    delivery_id = felt.to_int(event.data[delivery_id_pos])
    caller_crew_label_pos = (delivery_id_pos + 1)
    caller_crew_label = felt.to_int(event.data[caller_crew_label_pos])
    caller_crew_id_pos = (caller_crew_label_pos + 1)
    caller_crew_id = felt.to_int(event.data[caller_crew_id_pos])
    caller_address_pos = (caller_crew_id_pos + 1)
    caller_address = felt.to_hex(event.data[caller_address_pos])
    price = 0

    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, origin_label: %s, origin_id: %s, origin_slot: %s, dest_label: %s, dest_id: %s, dest_slot: %s, price: %s, delivery_label: %s, delivery_id: %s, caller_crew_label: %s, caller_crew_id: %s, caller_address: %s, products: %s, origin_inventory: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_slot, dest_label, dest_id, dest_slot, price, delivery_label, delivery_id, caller_crew_label, caller_crew_id, caller_address, products, origin_inventory))
    dispatcher_db.deliveryPackaged(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_slot, dest_label, dest_id, dest_slot, price, delivery_label, delivery_id, products, origin_inventory, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processDeliveryPackagedV1(tx_hash, event, block_number, from_address, origin_inventory, fee, timestamp):

    event_type="DeliveryPackagedV1"
    products = []
    for item in event.data:
        print("item: %s" % felt.to_int(item))

    origin_label = felt.to_int(event.data[0])
    origin_id = felt.to_int(event.data[1])
    origin_slot = felt.to_int(event.data[2])
    product_len = felt.to_int(event.data[3])
    product_start_pos = 4

    if product_len == 1:
        product_end_pos = (product_start_pos + 1)
        product_id = felt.to_int(event.data[product_start_pos])
        product_amount = felt.to_int(event.data[product_end_pos])
        product_name = types.getProductName(product_id)
        products.append({"id": product_id, "amount": product_amount, "name": product_name})
    else:
        product_len_doubled = (product_len * 2)
        product_end_pos = (product_start_pos + product_len_doubled)
        count = product_len
        anchor_pos = product_start_pos
        while count > 0:
            while anchor_pos < product_end_pos:
                product_id = felt.to_int(event.data[anchor_pos])
                anchor_pos+=1
                product_amount = felt.to_int(event.data[anchor_pos])
                product_name = types.getProductName(product_id)
                products.append({"id": product_id, "amount": product_amount, "name": product_name})
                anchor_pos+=1
                count-=1

    if product_len > 1:
        dest_label_pos = product_end_pos
    else:
        dest_label_pos = (product_end_pos + 1)

    dest_label = felt.to_int(event.data[dest_label_pos])
    dest_id_pos = (dest_label_pos + 1)
    dest_id = felt.to_int(event.data[dest_id_pos])
    dest_slot_pos = (dest_id_pos + 1)
    dest_slot = felt.to_int(event.data[dest_slot_pos])
    price_pos = (dest_slot_pos + 1)
    price = felt.to_int(event.data[price_pos])
    delivery_label_pos = (price_pos + 1)
    delivery_label = felt.to_int(event.data[delivery_label_pos])
    delivery_id_pos = (delivery_label_pos + 1)
    delivery_id = felt.to_int(event.data[delivery_id_pos])
    caller_crew_label_pos = (delivery_id_pos + 1)
    caller_crew_label = felt.to_int(event.data[caller_crew_label_pos])
    caller_crew_id_pos = (caller_crew_label_pos + 1)
    caller_crew_id = felt.to_int(event.data[caller_crew_id_pos])
    caller_address_pos = (caller_crew_id_pos + 1)
    caller_address = felt.to_hex(event.data[caller_address_pos])

    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, origin_label: %s, origin_id: %s, origin_slot: %s, dest_label: %s, dest_id: %s, dest_slot: %s, price: %s, delivery_label: %s, delivery_id: %s, caller_crew_label: %s, caller_crew_id: %s, caller_address: %s, products: %s, origin_inventory: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_slot, dest_label, dest_id, dest_slot, price, delivery_label, delivery_id, caller_crew_label, caller_crew_id, caller_address, products, origin_inventory))
    dispatcher_db.deliveryPackaged(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_slot, dest_label, dest_id, dest_slot, price, delivery_label, delivery_id, products, origin_inventory, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processResourceScanFinished(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="ResourceScanFinished"
    asteroid_label = felt.to_int(event.data[0])
    asteroid_id = felt.to_int(event.data[1])
    abundances_len = felt.to_int(event.data[2])
    water = felt.to_int(event.data[3])
    hydrogen = felt.to_int(event.data[4])
    amonia = felt.to_int(event.data[5])
    nitrogen = felt.to_int(event.data[6])
    sulfur_dioxide = felt.to_int(event.data[7])
    carbon_dioxide = felt.to_int(event.data[8])
    carbon_monoxide = felt.to_int(event.data[9])
    methane = felt.to_int(event.data[10])
    apatite = felt.to_int(event.data[11])
    bitumen = felt.to_int(event.data[12])
    calcite = felt.to_int(event.data[13])
    feldspar = felt.to_int(event.data[14])
    olivine = felt.to_int(event.data[15])
    pyroxene = felt.to_int(event.data[16])
    coffinite = felt.to_int(event.data[17])
    merrillite = felt.to_int(event.data[18])
    xenotime = felt.to_int(event.data[19])
    rhadbdite = felt.to_int(event.data[20])
    graphite = felt.to_int(event.data[21])
    taenite = felt.to_int(event.data[22])
    troilite = felt.to_int(event.data[23])
    uranite = felt.to_int(event.data[24])
    caller_crew_label = felt.to_int(event.data[25])
    caller_crew_id = felt.to_int(event.data[26])
    caller_address = felt.to_hex(event.data[27])

    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, asteroid_label: %s, asteroid_id: %s, caller_crew_label: %s, caller_crew_id: %s, water: %s, hydrogen: %s, amonia: %s, nitrogen: %s, sulfur_dioxide: %s, carbon_dioxide: %s, carbon_monoxide: %s, methane: %s, apatite: %s, bitumen: %s, calcite: %s, feldspar: %s, olivine: %s, pyroxene: %s, coffinite: %s, merrillite: %s, xenotime: %s, rhadbdite: %s, graphite: %s, taenite: %s, troilite: %s, uranite: %s" % (block_number, event_type, tx_hash, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id, water, hydrogen, amonia, nitrogen, sulfur_dioxide, carbon_dioxide, carbon_monoxide, methane, apatite, bitumen, calcite, feldspar, olivine, pyroxene, coffinite, merrillite, xenotime, rhadbdite, graphite, taenite, troilite, uranite))
    dispatcher_db.resourceScanFinished(block_number, event_type, tx_hash, from_address, caller_address, asteroid_label, asteroid_id, caller_crew_label, caller_crew_id, water, hydrogen, amonia, nitrogen, sulfur_dioxide, carbon_dioxide, carbon_monoxide, methane, apatite, bitumen, calcite, feldspar, olivine, pyroxene, coffinite, merrillite, xenotime, rhadbdite, graphite, taenite, troilite, uranite, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processDeliveryFinished(tx_hash, event, block_number, from_address, destination_inventory, fee, timestamp):

    event_type="DeliveryFinished"
    delivery_label = felt.to_int(event.data[0])
    delivery_id = felt.to_int(event.data[1])
    caller_crew_label = felt.to_int(event.data[2])
    caller_crew_id = felt.to_int(event.data[3])
    caller_address = felt.to_hex(event.data[4])

    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, delivery_label: %s, delivery_id: %s, destination_inventory: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, delivery_label, delivery_id, destination_inventory))
    dispatcher_db.deliveryFinished(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, delivery_label, delivery_id, destination_inventory, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processDeliveryFinishedV1(tx_hash, event, block_number, from_address, destination_inventory, fee, timestamp):

    event_type="DeliveryFinishedV1"
    products = []
    for item in event.data:
        print("item: %s" % felt.to_int(item))

    origin_label = felt.to_int(event.data[0])
    origin_id = felt.to_int(event.data[1])
    origin_slot = felt.to_int(event.data[2])
    product_len = felt.to_int(event.data[3])
    product_start_pos = 4

    if product_len == 1:
        product_end_pos = (product_start_pos + 1)
        product_id = felt.to_int(event.data[product_start_pos])
        product_amount = felt.to_int(event.data[product_end_pos])
        product_name = types.getProductName(product_id)
        products.append({"id": product_id, "amount": product_amount, "name": product_name})
    else:
        product_len_doubled = (product_len * 2)
        product_end_pos = (product_start_pos + product_len_doubled)
        count = product_len
        anchor_pos = product_start_pos
        while count > 0:
            while anchor_pos < product_end_pos:
                product_id = felt.to_int(event.data[anchor_pos])
                anchor_pos+=1
                product_amount = felt.to_int(event.data[anchor_pos])
                product_name = types.getProductName(product_id)
                products.append({"id": product_id, "amount": product_amount, "name": product_name})
                anchor_pos+=1
                count-=1

    if product_len > 1:
        dest_label_pos = product_end_pos
    else:
        dest_label_pos = (product_end_pos + 1)

    dest_label = felt.to_int(event.data[dest_label_pos])
    dest_id_pos = (dest_label_pos + 1)
    dest_id = felt.to_int(event.data[dest_id_pos])
    dest_slot_pos = (dest_id_pos + 1)
    dest_slot = felt.to_int(event.data[dest_slot_pos])
    delivery_label_pos = (dest_slot_pos + 1)
    delivery_label = felt.to_int(event.data[delivery_label_pos])
    delivery_id_pos = (delivery_label_pos + 1)
    delivery_id = felt.to_int(event.data[delivery_id_pos])
    caller_crew_label_pos = (delivery_id_pos + 1)
    caller_crew_label = felt.to_int(event.data[caller_crew_label_pos])
    caller_crew_id_pos = (caller_crew_label_pos + 1)
    caller_crew_id = felt.to_int(event.data[caller_crew_id_pos])
    caller_address_pos = (caller_crew_id_pos + 1)
    caller_address = felt.to_hex(event.data[caller_address_pos])

    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, origin_label: %s, origin_id: %s, origin_slot: %s, dest_label: %s, dest_id: %s, dest_slot: %s, delivery_label: %s, delivery_id: %s, caller_crew_label: %s, caller_crew_id: %s, caller_address: %s, products: %s, destination_inventory: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_slot, dest_label, dest_id, dest_slot, delivery_label, delivery_id, caller_crew_label, caller_crew_id, caller_address, products, destination_inventory))
    dispatcher_db.deliveryFinishedV1(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, origin_label, origin_id, origin_slot, dest_label, dest_id, dest_slot, delivery_label, delivery_id, products, destination_inventory, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processComponentUpdated(tx_hash, event, block_number, from_address, event_key, event_name, fee, timestamp):

    event_type="ComponentUpdated"
    data_length = len(event.data)
    print("%s: %s" % (event_name, data_length))


async def processContractAgreementAccepted(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="ContractAgreementAccepted"
    target_label = felt.to_int(event.data[0])
    target_id = felt.to_int(event.data[1])
    permission = felt.to_int(event.data[2])
    permitted_label = felt.to_int(event.data[3])
    permitted_id = felt.to_int(event.data[4])
    contract_address = felt.to_hex(event.data[5])
    caller_crew_label = felt.to_int(event.data[6])
    caller_crew_id = felt.to_int(event.data[7])
    caller_address = felt.to_hex(event.data[8])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, target_label: %s, target_id: %s, permission: %s, permitted_label: %s, permitted_id: %s, contract_address: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permission, permitted_label, permitted_id, contract_address))
    dispatcher_db.contractAgreementAccepted(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permission, permitted_label, permitted_id, contract_address, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processPrepaidMerkleAgreementAccepted(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="PrepaidMerkleAgreementAccepted"
    sys.exit(1)


async def processPrepaidAgreementAccepted(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="PrepaidAgreementAccepted"
    target_label = felt.to_int(event.data[0])
    target_id = felt.to_int(event.data[1])
    entity = sdk.unpackLot(target_id)
    asteroid_id = entity['asteroidId']
    lot_id = entity['lotIndex']
    permission = felt.to_int(event.data[2])
    permitted_label = felt.to_int(event.data[3])
    permitted_id = felt.to_int(event.data[4])
    term = felt.to_int(event.data[5])
    rate = felt.to_int(event.data[6])
    initial_term = felt.to_int(event.data[7])
    notice_period = felt.to_int(event.data[8])
    caller_crew_label = felt.to_int(event.data[9])
    caller_crew_id = felt.to_int(event.data[10])
    caller_address = felt.to_hex(event.data[11])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, target_label: %s, target_id: %s, permission: %s, permitted_label: %s, permitted_id: %s, term: %s, rate: %s, initial_term: %s, notice_period: %s, asteroid_id: %s, lot_id: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permission, permitted_label, permitted_id, term, rate, initial_term, notice_period, asteroid_id, lot_id))
    dispatcher_db.prepaidAgreementAccepted(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permission, permitted_label, permitted_id, term, rate, initial_term, notice_period, asteroid_id, lot_id, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processPrepaidAgreementExtended(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="PrepaidAgreementExtended"
    target_label = felt.to_int(event.data[0])
    target_id = felt.to_int(event.data[1])
    entity = sdk.unpackLot(target_id)
    asteroid_id = entity['asteroidId']
    lot_id = entity['lotIndex']
    permission = felt.to_int(event.data[2])
    permitted_label = felt.to_int(event.data[3])
    permitted_id = felt.to_int(event.data[4])
    term = felt.to_int(event.data[5])
    rate = felt.to_int(event.data[6])
    initial_term = felt.to_int(event.data[7])
    notice_period = felt.to_int(event.data[8])
    caller_crew_label = felt.to_int(event.data[9])
    caller_crew_id = felt.to_int(event.data[10])
    caller_address = felt.to_hex(event.data[11])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, target_label: %s, target_id: %s, permission: %s, permitted_label: %s, permitted_id: %s, term: %s, rate: %s, initial_term: %s, notice_period: %s, asteroid_id: %s, lot_id: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permission, permitted_label, permitted_id, term, rate, initial_term, notice_period, asteroid_id, lot_id))
    dispatcher_db.prepaidAgreementExtended(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permission, permitted_label, permitted_id, term, rate, initial_term, notice_period, asteroid_id, lot_id, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processPrepaidAgreementCancelled(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="PrepaidAgreementCancelled"
    target_label = felt.to_int(event.data[0])
    target_id = felt.to_int(event.data[1])
    entity = sdk.unpackLot(target_id)
    asteroid_id = entity['asteroidId']
    lot_id = entity['lotIndex']
    permission = felt.to_int(event.data[2])
    permitted_label = felt.to_int(event.data[3])
    permitted_id = felt.to_int(event.data[4])
    eviction_time = felt.to_int(event.data[5])
    caller_crew_label = felt.to_int(event.data[6])
    caller_crew_id = felt.to_int(event.data[7])
    caller_address = felt.to_hex(event.data[8])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, target_label: %s, target_id: %s, permission: %s, permitted_label: %s, permitted_id: %s, eviction_time: %s, asteroid_id: %s, lot_id: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permission, permitted_label, permitted_id, eviction_time, asteroid_id, lot_id))
    dispatcher_db.prepaidAgreementCancelled(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permission, permitted_label, permitted_id, eviction_time, asteroid_id, lot_id, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processRemovedFromWhitelist(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="RemovedFromWhitelist"
    entity_label = felt.to_int(event.data[0])
    entity_id = felt.to_int(event.data[1])
    permission = felt.to_int(event.data[2])
    target_label = felt.to_int(event.data[3])
    target_id = felt.to_int(event.data[4])
    caller_crew_label = felt.to_int(event.data[5])
    caller_crew_id = felt.to_int(event.data[6])
    caller_address = felt.to_hex(event.data[7])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, entity_label: %s, entity_id: %s, permission: %s, target_label: %s, target_id: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, target_label, target_id, permission))
    dispatcher_db.removedFromWhitelist(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, target_label, target_id, permission, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processRemovedFromWhitelistV1(tx_hash, event, block_number, from_address, fee, timestamp):
                
    event_type="RemovedFromWhitelistV1"
    target_label = felt.to_int(event.data[0])
    target_id = felt.to_int(event.data[1])
    permission = felt.to_int(event.data[2])
    permitted_label = felt.to_int(event.data[3])
    permitted_id = felt.to_int(event.data[4])
    caller_crew_label = felt.to_int(event.data[5])
    caller_crew_id = felt.to_int(event.data[6])
    caller_address = felt.to_hex(event.data[7])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, target_label: %s, target_id: %s, permission: %s, permitted_label: %s, permitted_id: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permitted_label, permitted_id, permission))
    dispatcher_db.removedFromWhitelistV1(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permitted_label, permitted_id, permission, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processAddedToWhitelist(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="AddedToWhitelist"
    entity_label = felt.to_int(event.data[0])
    entity_id = felt.to_int(event.data[1])
    permission = felt.to_int(event.data[2])
    target_label = felt.to_int(event.data[3])
    target_id = felt.to_int(event.data[4])
    caller_crew_label = felt.to_int(event.data[5])
    caller_crew_id = felt.to_int(event.data[6])
    caller_address = felt.to_hex(event.data[7])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, entity_label: %s, entity_id: %s, permission: %s, target_label: %s, target_id: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, target_label, target_id, permission))
    dispatcher_db.addedToWhitelist(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, target_label, target_id, permission, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processAddedToWhitelistV1(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="AddedToWhitelistV1"
    target_label = felt.to_int(event.data[0])
    target_id = felt.to_int(event.data[1])
    permission = felt.to_int(event.data[2])
    permitted_label = felt.to_int(event.data[3])
    permitted_id = felt.to_int(event.data[4])
    caller_crew_label = felt.to_int(event.data[5])
    caller_crew_id = felt.to_int(event.data[6])
    caller_address = felt.to_hex(event.data[7])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, target_label: %s, target_id: %s,  permission: %s, permitted_label: %s, permitted_id: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permission, permitted_label, permitted_id))
    dispatcher_db.addedToWhitelistV1(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permission, permitted_label, permitted_id, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processAddedAccountToWhitelist(tx_hash, event, block_number, from_address, fee, timestamp):
                
    event_type="AddedAccountToWhitelist"
    target_label = felt.to_int(event.data[0])
    target_id = felt.to_int(event.data[1])
    permission = felt.to_int(event.data[2])
    permitted = felt.to_hex(event.data[3])
    caller_crew_label = felt.to_int(event.data[4])
    caller_crew_id = felt.to_int(event.data[5])
    caller_address = felt.to_hex(event.data[6])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, target_label: %s, target_id: %s,  permission: %s, permitted: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permission, permitted))
    dispatcher_db.addedAccountToWhitelist(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, target_label, target_id, permission, permitted, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processShipCommandeered(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="ShipCommandeered"
    ship_label = felt.to_int(event.data[0])
    ship_id = felt.to_int(event.data[1])
    caller_crew_label = felt.to_int(event.data[2])
    caller_crew_id = felt.to_int(event.data[3])
    caller_address = felt.to_hex(event.data[4])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, ship_label: %s, ship_id: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id))
    dispatcher_db.shipCommandeered(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processLotReclaimed(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="LotReclaimed"
    lot_label = felt.to_int(event.data[0])
    lot_id = felt.to_int(event.data[1])
    caller_crew_label = felt.to_int(event.data[2])
    caller_crew_id = felt.to_int(event.data[3])
    caller_address = felt.to_hex(event.data[4])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, lot_label: %s, lot_id: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, lot_label, lot_id))
    dispatcher_db.lotReclaimed(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, lot_label, lot_id, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")
    sys.exit(1)


async def processBuildingRepossessed(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="BuildingRepossessed"
    building_label = felt.to_int(event.data[0])
    building_id = felt.to_int(event.data[1])
    caller_crew_label = felt.to_int(event.data[2])
    caller_crew_id = felt.to_int(event.data[3])
    caller_address = felt.to_hex(event.data[4])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, building_label: %s, building_id: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, building_label, building_id))
    dispatcher_db.buildingRepossessed(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, building_label, building_id, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processCrewDelegated(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="CrewDelegated"
    delegated_to = felt.to_hex(event.data[0])
    caller_crew_label = felt.to_int(event.data[1])
    caller_crew_id = felt.to_int(event.data[2])
    caller_address = felt.to_hex(event.data[3])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, delegated_to: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, delegated_to))
    dispatcher_db.crewDelegated(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, delegated_to, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processCrewEjected(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="CrewEjected"
    station_label = felt.to_int(event.data[0])
    station_id = felt.to_int(event.data[1])
    ejected_crew_label = felt.to_int(event.data[2])
    ejected_crew_id = felt.to_int(event.data[3])
    finish_time = felt.to_int(event.data[4])
    caller_crew_label = felt.to_int(event.data[5])
    caller_crew_id = felt.to_int(event.data[6])
    caller_address = felt.to_hex(event.data[7])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, ejected_crew_label: %s, ejected_crew_id: %s, finish_time: %s, station_label: %s, station_id: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, ejected_crew_label, ejected_crew_id, finish_time, station_label, station_id))
    dispatcher_db.crewEjected(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ejected_crew_label, ejected_crew_id, finish_time, station_label, station_id, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processDepositListedForSale(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="DepositListedForSale"
    deposit_label = felt.to_int(event.data[0])
    deposit_id = felt.to_int(event.data[1])
    price = felt.to_int(event.data[2])
    caller_crew_label = felt.to_int(event.data[3])
    caller_crew_id = felt.to_int(event.data[4])
    caller_address = felt.to_hex(event.data[5])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, deposit_label: %s, deposit_id: %s, price: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, price))
    dispatcher_db.depositListedForSale(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, price, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")
    #sys.exit(1)


async def processDepositPurchased(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="DepositPurchased"
    deposit_label = felt.to_int(event.data[0])
    deposit_id = felt.to_int(event.data[1])
    price = felt.to_int(event.data[2])
    caller_crew_label = felt.to_int(event.data[3])
    caller_crew_id = felt.to_int(event.data[4])
    caller_address = felt.to_hex(event.data[5])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, deposit_label: %s, deposit_id: %s, price: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, price))
    dispatcher_db.depositPurchased(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, price, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processDepositPurchasedV1(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="DepositPurchasedV1"
    deposit_label = felt.to_int(event.data[0])
    deposit_id = felt.to_int(event.data[1])
    price = felt.to_int(event.data[2])
    seller_crew_label = felt.to_int(event.data[3])
    seller_crew_id = felt.to_int(event.data[4])
    caller_crew_label = felt.to_int(event.data[5])
    caller_crew_id = felt.to_int(event.data[6])
    caller_address = felt.to_hex(event.data[7])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, deposit_label: %s, deposit_id: %s, price: %s, seller_crew_label: %s, seller_crew_id: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, price, seller_crew_label, seller_crew_id))
    dispatcher_db.depositPurchasedV1(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, seller_crew_label, seller_crew_id, price, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processDepositUnlistedForSale(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="DepositUnlistedForSale"
    deposit_label = felt.to_int(event.data[0])
    deposit_id = felt.to_int(event.data[1])
    caller_crew_label = felt.to_int(event.data[2])
    caller_crew_id = felt.to_int(event.data[3])
    caller_address = felt.to_hex(event.data[4])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, deposit_label: %s, deposit_id: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id))
    dispatcher_db.depositUnlistedForSale(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, deposit_label, deposit_id, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processSellOrderCreated(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="SellOrderCreated"
    exchange_label = felt.to_int(event.data[0])
    exchange_id = felt.to_int(event.data[1])
    product_id = felt.to_int(event.data[2])
    amount = felt.to_int(event.data[3])
    price = felt.to_int(event.data[4])
    storage_label = felt.to_int(event.data[5])
    storage_id = felt.to_int(event.data[6])
    storage_slot = felt.to_int(event.data[7])
    valid_time = felt.to_int(event.data[8])
    maker_fee = felt.to_int(event.data[9])
    caller_crew_label = felt.to_int(event.data[10])
    caller_crew_id = felt.to_int(event.data[11])
    caller_address = felt.to_hex(event.data[12])
    product_name = types.getProductName(product_id)
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, exchange_label: %s, exchange_id: %s, product_id: %s, product_name: %s, amount: %s, price: %s, storage_label: %s, storage_id: %s, storage_slot: %s, valid_time: %s, maker_fee: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, exchange_label, exchange_id, product_id, product_name, amount, price, storage_label, storage_id, storage_slot, valid_time, maker_fee))
    dispatcher_db.sellOrderCreated(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, exchange_label, exchange_id, product_id, product_name, amount, price, storage_label, storage_id, storage_slot, valid_time, maker_fee, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processSellOrderFilled(tx_hash, event, block_number, from_address, fill_count, fee, timestamp):

    event_type="SellOrderFilled"
    seller_crew_label = felt.to_int(event.data[0])
    seller_crew_id = felt.to_int(event.data[1])
    exchange_label = felt.to_int(event.data[2])
    exchange_id = felt.to_int(event.data[3])
    product_id = felt.to_int(event.data[4])
    amount = felt.to_int(event.data[5])
    price = felt.to_int(event.data[6])
    storage_label = felt.to_int(event.data[7])
    storage_id = felt.to_int(event.data[8])
    storage_slot = felt.to_int(event.data[9])
    destination_label = felt.to_int(event.data[10])
    destination_id = felt.to_int(event.data[11])
    destination_slot = felt.to_int(event.data[12])
    caller_crew_label = felt.to_int(event.data[13])
    caller_crew_id = felt.to_int(event.data[14])
    caller_address = felt.to_hex(event.data[15])
    product_name = types.getProductName(product_id)
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, seller_crew_label: %s, seller_crew_id: %s, exchange_label: %s, exchange_id: %s, product_id: %s, product_name: %s, amount: %s, price: %s, storage_label: %s, storage_id: %s, storage_slot: %s, destination_label: %s, destination_id: %s, destination_slot: %s, fill_count: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, seller_crew_label, seller_crew_id, exchange_label, exchange_id, product_id, product_name, amount, price, storage_label, storage_id, storage_slot, destination_label, destination_id, destination_slot, fill_count))
    dispatcher_db.sellOrderFilled(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, seller_crew_label, seller_crew_id, exchange_label, exchange_id, product_id, product_name, amount, price, storage_label, storage_id, storage_slot, destination_label, destination_id, destination_slot, fill_count, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processSellOrderCancelled(tx_hash, event, delivery_event, block_number, from_address, fee, timestamp):

    event_type="SellOrderCancelled"
    seller_crew_label = felt.to_int(event.data[0])
    seller_crew_id = felt.to_int(event.data[1])
    exchange_label = felt.to_int(event.data[2])
    exchange_id = felt.to_int(event.data[3])
    product_id = felt.to_int(event.data[4])
    price = felt.to_int(event.data[5])
    storage_label = felt.to_int(event.data[6])
    storage_id = felt.to_int(event.data[7])
    storage_slot = felt.to_int(event.data[8])
    caller_crew_label = felt.to_int(event.data[9])
    caller_crew_id = felt.to_int(event.data[10])
    caller_address = felt.to_hex(event.data[11])
    product_name = types.getProductName(product_id)

    d_products = []
    for item in delivery_event.data:
        print("item: %s" % felt.to_int(item))

    d_origin_label = felt.to_int(delivery_event.data[0])
    d_origin_id = felt.to_int(delivery_event.data[1])
    d_origin_slot = felt.to_int(delivery_event.data[2])
    d_product_len = felt.to_int(delivery_event.data[3])
    d_product_start_pos = 4

    if d_product_len == 1:
        d_product_end_pos = (d_product_start_pos + 1)
        d_product_id = felt.to_int(delivery_event.data[d_product_start_pos])
        d_product_amount = felt.to_int(delivery_event.data[d_product_end_pos])
        d_product_name = types.getProductName(d_product_id)
        d_products.append({"id": d_product_id, "amount": d_product_amount, "name": d_product_name})
    else:
        d_product_len_doubled = (d_product_len * 2)
        d_product_end_pos = (d_product_start_pos + d_product_len_doubled)
        d_count = d_product_len
        d_anchor_pos = d_product_start_pos
        while d_count > 0:
            while d_anchor_pos < d_product_end_pos:
                d_product_id = felt.to_int(delivery_event.data[d_anchor_pos])
                d_anchor_pos+=1
                d_product_amount = felt.to_int(delivery_event.data[d_anchor_pos])
                d_product_name = types.getProductName(d_product_id)
                d_products.append({"id": d_product_id, "amount": d_product_amount, "name": d_product_name})
                d_anchor_pos+=1
                count-=1

    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, seller_crew_label: %s, seller_crew_id: %s, exchange_label: %s, exchange_id: %s, product_id: %s, product_name: %s, price: %s, storage_label: %s, storage_id: %s, storage_slot: %s, products: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, seller_crew_label, seller_crew_id, exchange_label, exchange_id, product_id, product_name, price, storage_label, storage_id, storage_slot, d_products))
    dispatcher_db.sellOrderCancelled(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, seller_crew_label, seller_crew_id, exchange_label, exchange_id, product_id, product_name, price, storage_label, storage_id, storage_slot, d_products, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processBuyOrderCreated(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="BuyOrderCreated"
    exchange_label = felt.to_int(event.data[0])
    exchange_id = felt.to_int(event.data[1])
    product_id = felt.to_int(event.data[2])
    amount = felt.to_int(event.data[3])
    price = felt.to_int(event.data[4])
    storage_label = felt.to_int(event.data[5])
    storage_id = felt.to_int(event.data[6])
    storage_slot = felt.to_int(event.data[7])
    valid_time = felt.to_int(event.data[8])
    maker_fee = felt.to_int(event.data[9])
    caller_crew_label = felt.to_int(event.data[10])
    caller_crew_id = felt.to_int(event.data[11])
    caller_address = felt.to_hex(event.data[12])
    product_name = types.getProductName(product_id)
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, exchange_label: %s, exchange_id: %s, product_id: %s, product_name: %s, amount: %s, price: %s, storage_label: %s, storage_id: %s, storage_slot: %s, valid_time: %s, maker_fee: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, exchange_label, exchange_id, product_id, product_name, amount, price, storage_label, storage_id, storage_slot, valid_time, maker_fee))
    dispatcher_db.buyOrderCreated(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, exchange_label, exchange_id, product_id, product_name, amount, price, storage_label, storage_id, storage_slot, valid_time, maker_fee, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processBuyOrderFilled(tx_hash, event, block_number, from_address, fill_count, fee, timestamp):

    event_type="BuyOrderFilled"
    buyer_crew_label = felt.to_int(event.data[0])
    buyer_crew_id = felt.to_int(event.data[1])
    exchange_label = felt.to_int(event.data[2])
    exchange_id = felt.to_int(event.data[3])
    product_id = felt.to_int(event.data[4])
    amount = felt.to_int(event.data[5])
    price = felt.to_int(event.data[6])
    storage_label = felt.to_int(event.data[7])
    storage_id = felt.to_int(event.data[8])
    storage_slot = felt.to_int(event.data[9])
    origin_label = felt.to_int(event.data[10])
    origin_id = felt.to_int(event.data[11])
    origin_slot = felt.to_int(event.data[12])
    caller_crew_label = felt.to_int(event.data[13])
    caller_crew_id = felt.to_int(event.data[14])
    caller_address = felt.to_hex(event.data[15])
    product_name = types.getProductName(product_id)
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, buyer_crew_label: %s, buyer_crew_id: %s, exchange_label: %s, exchange_id: %s, product_id: %s, product_name: %s, amount: %s, price: %s, storage_label: %s, storage_id: %s, storage_slot: %s, origin_label: %s, origin_id: %s, origin_slot: %s, fill_count: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, buyer_crew_label, buyer_crew_id, exchange_label, exchange_id, product_id, product_name, amount, price, storage_label, storage_id, storage_slot, origin_label, origin_id, origin_slot, fill_count))
    dispatcher_db.buyOrderFilled(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, buyer_crew_label, buyer_crew_id, exchange_label, exchange_id, product_id, product_name, amount, price, storage_label, storage_id, storage_slot, origin_label, origin_id, origin_slot, fill_count, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processBuyOrderCancelled(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="BuyOrderCancelled"
    buyer_crew_label = felt.to_int(event.data[0])
    buyer_crew_id = felt.to_int(event.data[1])
    exchange_label = felt.to_int(event.data[2])
    exchange_id = felt.to_int(event.data[3])
    product_id = felt.to_int(event.data[4])
    amount = felt.to_int(event.data[5])
    price = felt.to_int(event.data[6])
    storage_label = felt.to_int(event.data[7])
    storage_id = felt.to_int(event.data[8])
    storage_slot = felt.to_int(event.data[9])
    caller_crew_label = felt.to_int(event.data[10])
    caller_crew_id = felt.to_int(event.data[11])
    caller_address = felt.to_hex(event.data[12])
    product_name = types.getProductName(product_id)
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, buyer_crew_label: %s, buyer_crew_id: %s, exchange_label: %s, exchange_id: %s, product_id: %s, product_name: %s, amount: %s, price: %s, storage_label: %s, storage_id: %s, storage_slot: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, buyer_crew_label, buyer_crew_id, exchange_label, exchange_id, product_id, product_name, amount, price, storage_label, storage_id, storage_slot))
    dispatcher_db.buyOrderCancelled(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, buyer_crew_label, buyer_crew_id, exchange_label, exchange_id, product_id, product_name, amount, price, storage_label, storage_id, storage_slot, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processContractPolicyAssigned(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="ContractPolicyAssigned"
    entity_label = felt.to_int(event.data[0])
    entity_id = felt.to_int(event.data[1])
    permission = felt.to_int(event.data[2])
    contract = felt.to_hex(event.data[3])
    caller_crew_label = felt.to_int(event.data[4])
    caller_crew_id = felt.to_int(event.data[5])
    caller_address = felt.to_hex(event.data[6])
    entity_name = types.getEntityName(entity_id)
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, entity_label: %s, entity_id: %s, permission: %s, contract: %s, entity_name: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, contract, entity_name))
    dispatcher_db.contractPolicyAssigned(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, contract, entity_name, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processPrepaidMerklePolicyAssigned(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="PrepaidMerklePolicyAssigned"
    sys.exit(1)


async def processPrepaidPolicyAssigned(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="PrepaidPolicyAssigned"
    entity_label = felt.to_int(event.data[0])
    entity_id = felt.to_int(event.data[1])
    permission = felt.to_int(event.data[2])
    rate = felt.to_int(event.data[3])
    initial_term = felt.to_int(event.data[4])
    notice_period = felt.to_int(event.data[5])
    caller_crew_label = felt.to_int(event.data[6])
    caller_crew_id = felt.to_int(event.data[7])
    caller_address = felt.to_hex(event.data[8])
    entity_name = types.getEntityName(entity_id)
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, entity_label: %s, entity_id: %s, permission: %s, rate: %s, initial_term: %s, notice_period: %s, entity_name: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, rate, initial_term, notice_period, entity_name))
    dispatcher_db.prepaidPolicyAssigned(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, rate, initial_term, notice_period, entity_name, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processContractPolicyRemoved(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="ContractPolicyRemoved"
    entity_label = felt.to_int(event.data[0])
    entity_id = felt.to_int(event.data[1])
    permission = felt.to_int(event.data[2])
    caller_crew_label = felt.to_int(event.data[3])
    caller_crew_id = felt.to_int(event.data[4])
    caller_address = felt.to_hex(event.data[5])
    entity_name = types.getEntityName(entity_id)
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, entity_label: %s, entity_id: %s, permission: %s, entity_name: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, entity_name))
    dispatcher_db.contractPolicyRemoved(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, entity_name, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processPrepaidPolicyRemoved(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="PrepaidPolicyRemoved"
    entity_label = felt.to_int(event.data[0])
    entity_id = felt.to_int(event.data[1])
    permission = felt.to_int(event.data[2])
    caller_crew_label = felt.to_int(event.data[3])
    caller_crew_id = felt.to_int(event.data[4])
    caller_address = felt.to_hex(event.data[5])
    entity_name = types.getEntityName(entity_id)
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, entity_label: %s, entity_id: %s, permission: %s, entity_name: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, entity_name))
    dispatcher_db.prepaidPolicyRemoved(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, entity_name, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processPrepaidMerklePolicyRemoved(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="PrepaidMerklePolicyRemoved"
    entity_label = felt.to_int(event.data[0])
    entity_id = felt.to_int(event.data[1])
    permission = felt.to_int(event.data[2])
    caller_crew_label = felt.to_int(event.data[3])
    caller_crew_id = felt.to_int(event.data[4])
    caller_address = felt.to_hex(event.data[5])
    entity_name = types.getEntityName(entity_id)
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, entity_label: %s, entity_id: %s, permission: %s, entity_name: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, entity_name))
    dispatcher_db.prepaidMerklePolicyRemoved(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, entity_name, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")
    sys.exit(1)


async def processPublicPolicyRemoved(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="PublicPolicyRemoved"
    entity_label = felt.to_int(event.data[0])
    entity_id = felt.to_int(event.data[1])
    permission = felt.to_int(event.data[2])
    caller_crew_label = felt.to_int(event.data[3])
    caller_crew_id = felt.to_int(event.data[4])
    caller_address = felt.to_hex(event.data[5])
    entity_name = types.getEntityName(entity_id)
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, entity_label: %s, entity_id: %s, permission: %s, entity_name: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, entity_name))
    dispatcher_db.publicPolicyRemoved(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, entity_label, entity_id, permission, entity_name, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processExchangeConfigured(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="ExchangeConfigured"
    exchange_label = felt.to_int(event.data[0])
    exchange_id = felt.to_int(event.data[1])
    caller_crew_label = felt.to_int(event.data[2])
    caller_crew_id = felt.to_int(event.data[3])
    caller_address = felt.to_hex(event.data[4])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, exchange_label: %s, exchange_id: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, exchange_label, exchange_id))
    dispatcher_db.exchangeConfigured(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, exchange_label, exchange_id, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processRandomEventResolved(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="RandomEventResolved"
    random_event = felt.to_int(event.data[0])
    choice = felt.to_int(event.data[1])
    action_type = felt.to_int(event.data[2])
    action_target_label = felt.to_int(event.data[3])
    action_target_id = felt.to_int(event.data[4])
    caller_crew_label = felt.to_int(event.data[5])
    caller_crew_id = felt.to_int(event.data[6])
    caller_address = felt.to_hex(event.data[7])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, random_event: %s, choice: %s, action_type: %s, action_target_label: %s, action_target_id: %ss" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, random_event, choice, action_type, action_target_label, action_target_id))
    dispatcher_db.randomEventResolved(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, random_event, choice, action_type, action_target_label, action_target_id, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processTransitFinished(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="TransitFinished"
    ship_label = felt.to_int(event.data[0])
    ship_id = felt.to_int(event.data[1])
    origin_label = felt.to_int(event.data[2])
    origin_id = felt.to_int(event.data[3])
    destination_label = felt.to_int(event.data[4])
    destination_id = felt.to_int(event.data[5])
    departure = felt.to_int(event.data[6])
    arrival = felt.to_int(event.data[7])
    caller_crew_label = felt.to_int(event.data[8])
    caller_crew_id = felt.to_int(event.data[9])
    caller_address = felt.to_hex(event.data[10])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, ship_label: %s, ship_id: %s, origin_label: %s, origin_id: %s, destination_label: %s, destination_id: %s, departure: %s, arrival: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, origin_label, origin_id, destination_label, destination_id, departure, arrival))
    dispatcher_db.transitFinished(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, origin_label, origin_id, destination_label, destination_id, departure, arrival, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processTransitStarted(tx_hash, event, block_number, from_address, fee, timestamp, inventory_event):

    event_type="TransitStarted"
    ship_label = felt.to_int(event.data[0])
    ship_id = felt.to_int(event.data[1])
    origin_label = felt.to_int(event.data[2])
    origin_id = felt.to_int(event.data[3])
    destination_label = felt.to_int(event.data[4])
    destination_id = felt.to_int(event.data[5])
    departure = felt.to_int(event.data[6])
    arrival = felt.to_int(event.data[7])
    finish_time = felt.to_int(event.data[8])
    caller_crew_label = felt.to_int(event.data[9])
    caller_crew_id = felt.to_int(event.data[10])
    caller_address = felt.to_hex(event.data[11])
    new_fuel = felt.to_int(inventory_event.data[11])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, ship_label: %s, ship_id: %s, origin_label: %s, origin_id: %s, destination_label: %s, destination_id: %s, departure: %s, arrival: %s, finish_time: %s, new_fuel: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, origin_label, origin_id, destination_label, destination_id, departure, arrival, finish_time, new_fuel))
    dispatcher_db.transitStarted(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, ship_label, ship_id, origin_label, origin_id, destination_label, destination_id, departure, arrival, finish_time, fee, timestamp, new_fuel)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processArrivalRewardClaimed(tx_hash, event, block_number, from_address, ships, fee, timestamp):

    event_type="ArrivalRewardClaimed"
    asteroid_label = felt.to_int(event.data[0])
    asteroid_id = felt.to_int(event.data[1])
    caller_crew_label = felt.to_int(event.data[2])
    caller_crew_id = felt.to_int(event.data[3])
    caller_address = felt.to_hex(event.data[4])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, caller_crew_label: %s, caller_crew_id: %s, asteroid_label: %s, asteroid_id: %s, ships: %s" % (block_number, event_type, tx_hash, from_address, caller_address, caller_crew_label, caller_crew_id, asteroid_label, asteroid_id, ships))
    dispatcher_db.arrivalRewardClaimed(tx_hash, block_number, from_address, caller_address, caller_crew_label, caller_crew_id, asteroid_label, asteroid_id, ships, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def processPrepareForLaunchRewardClaimed(tx_hash, event, block_number, from_address, fee, timestamp):

    event_type="PrepareForLaunchRewardClaimed"
    asteroid_label = felt.to_int(event.data[0])
    asteroid_id = felt.to_int(event.data[1])
    caller_address = felt.to_hex(event.data[2])
    print("block_number: %s, event_type: %s, txn_id: %s, from_addr: %s, caller_addr: %s, asteroid_label: %s, asteroid_id: %s" % (block_number, event_type, tx_hash, from_address, caller_address, asteroid_label, asteroid_id))
    dispatcher_db.prepareForLaunchRewardClaimed(tx_hash, block_number, from_address, caller_address, asteroid_label, asteroid_id, fee, timestamp)
    txn_db.feeLogger(tx_hash, block_number, fee, timestamp, "dispatcher")


async def main():

    global starting_block
    global asteroids_storage
    global dispatcher_address
    global system_registered_key
    global suface_scan_finished_key
    global crewmate_recruited_v1_key
    global surface_scan_started_key
    global asteroid_managed_key
    global asteroid_initialized_key
    global asteroid_purchased_key
    global crewmate_purchased_key
    global crewmate_arranged_v1_key
    global crewmates_exchanged_key
    global constant_registered_key
    global contract_registered_key
    global public_policy_assigned_key
    global crew_formed_key
    global construction_finished_key
    global crewmate_recruited_key
    global name_changed_key
    global component_updated_key
    global resource_scan_started_key
    global resource_scan_finished_key
    global construction_planned_key
    global sampling_deposit_started_key
    global sampling_deposit_finished_key
    global sampling_deposit_started_v1_key
    global delivery_started_key
    global delivery_finished_key
    global delivery_finished_v1_key
    global construction_started_key
    global construction_abandoned_key
    global construction_deconstructed_key
    global resource_extraction_started_key
    global resource_extraction_finished_key
    global material_processing_started_v1_key
    global material_processing_finished_key
    global food_supplied_key
    global food_supplied_v1_key
    global ship_undocked_key
    global ship_docked_key
    global crew_stationed_key
    global crew_stationed_v1_key
    global ship_assembly_finished_key
    global ship_assembly_started_v1_key
    global emergency_propellant_collected_key
    global emergency_activated_key
    global emergency_deactivated_key
    global delivery_sent_key
    global delivery_received_key
    global delivery_cancelled_key
    global delivery_packaged_key
    global delivery_packaged_v1_key
    global contract_agreement_accepted_key
    global prepaid_merkle_agreement_accepted_key
    global prepaid_agreement_accepted_key
    global prepaid_agreement_extended_key
    global prepaid_agreement_cancelled_key
    global removed_from_whitelist_key
    global added_to_whitelist_key
    global added_to_whitelist_v1_key
    global ship_commandeered_key
    global lot_reclaimed_key
    global building_repossessed_key
    global crew_delegated_key
    global crew_ejected_key
    global deposit_listed_for_sale_key
    global deposit_purchased_key
    global deposit_unlisted_for_sale_key
    global sell_order_created_key
    global sell_order_filled_key
    global sell_order_cancelled_key
    global buy_order_created_key
    global buy_order_filled_key
    global buy_order_cancelled_key
    global contract_policy_assigned_key
    global prepaid_merkle_policy_assigned_key
    global prepaid_policy_assigned_key
    global contract_policy_removed_key
    global prepaid_policy_removed_key
    global prepaid_merkle_policy_removed_key
    global public_policy_removed_key
    global random_event_resolved_key
    global transit_finished_key
    global transit_started_key
    global arrival_reward_claimed_key
    global prepare_for_launch_reward_claimed_key
    global exchange_configured_key
    global added_account_to_whitelist_key
    global removed_from_whitelist_v1_key
    global deposit_purchased_v1_key

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
        asteroids_storage = config.get('storage', 'asteroids')
        dispatcher_address = felt.from_hex(config.get('contracts', 'dispatcher_address'))
        system_registered_key = felt.from_hex(config.get('selectors', 'system_registered_key'))
        suface_scan_finished_key = felt.from_hex(config.get('selectors', 'suface_scan_finished_key'))
        crewmate_recruited_v1_key = felt.from_hex(config.get('selectors', 'crewmate_recruited_v1_key'))
        surface_scan_started_key = felt.from_hex(config.get('selectors', 'surface_scan_started_key'))
        asteroid_managed_key = felt.from_hex(config.get('selectors', 'asteroid_managed_key'))
        asteroid_initialized_key = felt.from_hex(config.get('selectors', 'asteroid_initialized_key'))
        asteroid_purchased_key = felt.from_hex(config.get('selectors', 'asteroid_purchased_key'))
        crewmate_purchased_key = felt.from_hex(config.get('selectors', 'crewmate_purchased_key'))
        crewmate_arranged_v1_key = felt.from_hex(config.get('selectors', 'crewmate_arranged_v1_key'))
        crewmates_exchanged_key = felt.from_hex(config.get('selectors', 'crewmates_exchanged_key'))
        constant_registered_key = felt.from_hex(config.get('selectors', 'constant_registered_key'))
        contract_registered_key = felt.from_hex(config.get('selectors', 'contract_registered_key'))
        public_policy_assigned_key = felt.from_hex(config.get('selectors', 'public_policy_assigned_key'))
        crew_formed_key = felt.from_hex(config.get('selectors', 'crew_formed_key'))
        construction_finished_key = felt.from_hex(config.get('selectors', 'construction_finished_key'))
        crewmate_recruited_key = felt.from_hex(config.get('selectors', 'crewmate_recruited_key'))
        name_changed_key = felt.from_hex(config.get('selectors', 'name_changed_key'))
        component_updated_key = felt.from_hex(config.get('selectors', 'component_updated_key'))
        resource_scan_started_key = felt.from_hex(config.get('selectors', 'resource_scan_started_key'))
        resource_scan_finished_key = felt.from_hex(config.get('selectors', 'resource_scan_finished_key'))
        construction_planned_key = felt.from_hex(config.get('selectors', 'construction_planned_key'))
        sampling_deposit_started_key = felt.from_hex(config.get('selectors', 'sampling_deposit_started_key'))
        sampling_deposit_finished_key = felt.from_hex(config.get('selectors', 'sampling_deposit_finished_key'))
        sampling_deposit_started_v1_key = felt.from_hex(config.get('selectors', 'sampling_deposit_started_v1_key'))
        delivery_started_key = felt.from_hex(config.get('selectors', 'delivery_started_key'))
        delivery_finished_key = felt.from_hex(config.get('selectors', 'delivery_finished_key'))
        delivery_finished_v1_key = felt.from_hex(config.get('selectors', 'delivery_finished_v1_key'))
        construction_started_key = felt.from_hex(config.get('selectors', 'construction_started_key'))
        construction_abandoned_key = felt.from_hex(config.get('selectors', 'construction_abandoned_key'))
        construction_deconstructed_key = felt.from_hex(config.get('selectors', 'construction_deconstructed_key'))
        resource_extraction_started_key = felt.from_hex(config.get('selectors', 'resource_extraction_started_key'))
        resource_extraction_finished_key = felt.from_hex(config.get('selectors', 'resource_extraction_finished_key'))
        material_processing_started_v1_key = felt.from_hex(config.get('selectors', 'material_processing_started_v1_key'))
        material_processing_finished_key = felt.from_hex(config.get('selectors', 'material_processing_finished_key'))
        food_supplied_key = felt.from_hex(config.get('selectors', 'food_supplied_key'))
        food_supplied_v1_key = felt.from_hex(config.get('selectors', 'food_supplied_v1_key'))
        ship_undocked_key = felt.from_hex(config.get('selectors', 'ship_undocked_key'))
        ship_docked_key = felt.from_hex(config.get('selectors', 'ship_docked_key'))
        crew_stationed_key = felt.from_hex(config.get('selectors', 'crew_stationed_key'))
        crew_stationed_v1_key = felt.from_hex(config.get('selectors', 'crew_stationed_v1_key'))
        ship_assembly_started_v1_key = felt.from_hex(config.get('selectors', 'ship_assembly_started_v1_key'))
        ship_assembly_finished_key = felt.from_hex(config.get('selectors', 'ship_assembly_finished_key'))
        emergency_propellant_collected_key = felt.from_hex(config.get('selectors', 'emergency_propellant_collected_key'))
        emergency_activated_key = felt.from_hex(config.get('selectors', 'emergency_activated_key'))
        emergency_deactivated_key = felt.from_hex(config.get('selectors', 'emergency_deactivated_key'))
        delivery_sent_key= felt.from_hex(config.get('selectors', 'delivery_sent_key'))
        delivery_received_key = felt.from_hex(config.get('selectors', 'delivery_received_key'))
        delivery_packaged_key = felt.from_hex(config.get('selectors', 'delivery_packaged_key'))
        delivery_cancelled_key = felt.from_hex(config.get('selectors', 'delivery_cancelled_key'))
        delivery_packaged_v1_key = felt.from_hex(config.get('selectors', 'delivery_packaged_v1_key'))
        contract_agreement_accepted_key = felt.from_hex(config.get('selectors', 'contract_agreement_accepted_key'))
        prepaid_merkle_agreement_accepted_key = felt.from_hex(config.get('selectors', 'prepaid_merkle_agreement_accepted_key'))
        prepaid_agreement_accepted_key = felt.from_hex(config.get('selectors', 'prepaid_agreement_accepted_key'))
        prepaid_agreement_extended_key = felt.from_hex(config.get('selectors', 'prepaid_agreement_extended_key'))
        prepaid_agreement_cancelled_key = felt.from_hex(config.get('selectors', 'prepaid_agreement_cancelled_key'))
        removed_from_whitelist_key = felt.from_hex(config.get('selectors', 'removed_from_whitelist_key'))
        added_to_whitelist_key = felt.from_hex(config.get('selectors', 'added_to_whitelist_key'))
        added_to_whitelist_v1_key = felt.from_hex(config.get('selectors', 'added_to_whitelist_v1_key'))
        ship_commandeered_key = felt.from_hex(config.get('selectors', 'ship_commandeered_key'))
        lot_reclaimed_key = felt.from_hex(config.get('selectors', 'lot_reclaimed_key'))
        building_repossessed_key = felt.from_hex(config.get('selectors', 'building_repossessed_key'))
        crew_delegated_key = felt.from_hex(config.get('selectors', 'crew_delegated_key'))
        crew_ejected_key = felt.from_hex(config.get('selectors', 'crew_ejected_key'))
        deposit_listed_for_sale_key = felt.from_hex(config.get('selectors', 'deposit_listed_for_sale_key'))
        deposit_purchased_key = felt.from_hex(config.get('selectors', 'deposit_purchased_key'))
        deposit_unlisted_for_sale_key = felt.from_hex(config.get('selectors', 'deposit_unlisted_for_sale_key'))
        sell_order_created_key = felt.from_hex(config.get('selectors', 'sell_order_created_key'))
        sell_order_filled_key = felt.from_hex(config.get('selectors', 'sell_order_filled_key'))
        sell_order_cancelled_key = felt.from_hex(config.get('selectors', 'sell_order_cancelled_key'))
        buy_order_created_key = felt.from_hex(config.get('selectors', 'buy_order_created_key'))
        buy_order_filled_key = felt.from_hex(config.get('selectors', 'buy_order_filled_key'))
        buy_order_cancelled_key = felt.from_hex(config.get('selectors', 'buy_order_cancelled_key'))
        contract_policy_assigned_key = felt.from_hex(config.get('selectors', 'contract_policy_assigned_key'))
        prepaid_merkle_policy_assigned_key = felt.from_hex(config.get('selectors', 'prepaid_merkle_policy_assigned_key'))
        prepaid_policy_assigned_key = felt.from_hex(config.get('selectors', 'prepaid_policy_assigned_key'))
        contract_policy_removed_key = felt.from_hex(config.get('selectors', 'contract_policy_removed_key'))
        prepaid_policy_removed_key = felt.from_hex(config.get('selectors', 'prepaid_policy_removed_key'))
        prepaid_merkle_policy_removed_key = felt.from_hex(config.get('selectors', 'prepaid_merkle_policy_removed_key'))
        public_policy_removed_key = felt.from_hex(config.get('selectors', 'public_policy_removed_key'))
        random_event_resolved_key = felt.from_hex(config.get('selectors', 'random_event_resolved_key'))
        transit_finished_key = felt.from_hex(config.get('selectors', 'transit_finished_key'))
        transit_started_key = felt.from_hex(config.get('selectors', 'transit_started_key'))
        arrival_reward_claimed_key = felt.from_hex(config.get('selectors', 'arrival_reward_claimed_key'))
        prepare_for_launch_reward_claimed_key = felt.from_hex(config.get('selectors', 'prepare_for_launch_reward_claimed_key'))
        exchange_configured_key = felt.from_hex(config.get('selectors', 'exchange_configured_key'))
        added_account_to_whitelist_key = felt.from_hex(config.get('selectors', 'added_account_to_whitelist_key'))
        removed_from_whitelist_v1_key = felt.from_hex(config.get('selectors', 'removed_from_whitelist_v1_key'))
        deposit_purchased_v1_key = felt.from_hex(config.get('selectors', 'deposit_purchased_v1_key'))

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
        client_options=[
            ("grpc.max_receive_message_length", 512 * 1_000_000),  # ~256 MB
        ],
        timeout=90
    )

    dispatcher_name = "starknet-" + network
    await runner.run(DispatcherIndexer(), ctx={"network": dispatcher_name})

if __name__ == "__main__":
    asyncio.run(main())
