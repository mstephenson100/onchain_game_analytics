#!/bin/bash

pkill -ef /home/bios/indexer_mainnet/crewmate_events_indexer.py

echo
sleep 1

cd /home/bios/indexer_mainnet

screen -dmS crewmate_events_indexer_mainnet -L -Logfile /home/bios/indexer_mainnet/logs/crewmate_events_indexer.log /home/bios/.pyenv/shims/python3 /home/bios/indexer_mainnet/crewmate_events_indexer.py


echo "Restarted crewmate_events_indexer"
