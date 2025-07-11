#!/bin/bash

pkill -ef /home/bios/indexer_mainnet/txn_counter.py

echo
sleep 1

cd /home/bios/indexer_mainnet

screen -dmS txn_counter_mainnet -L -Logfile /home/bios/indexer_mainnet/logs/txn_counter.log /home/bios/.pyenv/shims/python3 /home/bios/indexer_mainnet/txn_counter.py


echo "Restarted txn_counter"
