#!/bin/bash

pkill -ef /home/bios/indexer_mainnet/dispatcher_events_indexer.py

echo
sleep 1

cd /home/bios/indexer_mainnet

screen -dmS dispatcher_events_indexer_mainnet -L -Logfile /home/bios/indexer_mainnet/logs/dispatcher_events_indexer.log /home/bios/.pyenv/shims/python3 /home/bios/indexer_mainnet/dispatcher_events_indexer.py


echo "Restarted dispatcher_events_indexer"
