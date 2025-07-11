#!/bin/bash

pkill -ef /home/bios/indexer_mainnet/asteroid_events_indexer.py

echo
sleep 1

cd /home/bios/indexer_mainnet

screen -dmS asteroid_events_indexer_mainnet -L -Logfile /home/bios/indexer_mainnet/logs/asteroid_events_indexer.log /home/bios/.pyenv/shims/python3 /home/bios/indexer_mainnet/asteroid_events_indexer.py


echo "Restarted asteroid_events_indexer"
