#!/bin/bash

pkill -ef /home/bios/indexer_mainnet/colonization_missions_aggregator.py

echo
sleep 1

cd /home/bios/indexer_mainnet

screen -dmS colonization_missions_mainnet -L -Logfile /home/bios/indexer_mainnet/logs/colonization_missions.log /home/bios/.pyenv/shims/python3 /home/bios/indexer_mainnet/colonization_missions_aggregator.py


echo "Restarted colonization_missions_aggregator"
