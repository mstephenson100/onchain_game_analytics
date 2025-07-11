#!/bin/bash

pkill -ef /home/bios/indexer_mainnet/community_missions_aggregator.py

echo
sleep 1

cd /home/bios/indexer_mainnet

screen -dmS community_missions_mainnet -L -Logfile /home/bios/indexer_mainnet/logs/community_missions.log /home/bios/.pyenv/shims/python3 /home/bios/indexer_mainnet/community_missions_aggregator.py


echo "Restarted community_missions_aggregator"
