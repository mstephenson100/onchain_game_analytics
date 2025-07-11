#!/bin/bash

pkill -ef /home/bios/indexer_mainnet/crew_events_indexer.py

echo
sleep 1

cd /home/bios/indexer_mainnet

screen -dmS crew_events_indexer_mainnet -L -Logfile /home/bios/indexer_mainnet/logs/crew_events_indexer.log /home/bios/.pyenv/shims/python3 /home/bios/indexer_mainnet/crew_events_indexer.py


echo "Restarted crew_events_indexer"
