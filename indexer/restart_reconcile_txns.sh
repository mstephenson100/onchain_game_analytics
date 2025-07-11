#!/bin/bash

pkill -ef /home/bios/indexer_mainnet/reconcile_txns.py

echo
sleep 1

cd /home/bios/indexer_mainnet

screen -dmS reconcile_txns_mainnet -L -Logfile /home/bios/indexer_mainnet/logs/reconcile_txns.log /home/bios/.pyenv/shims/python3 /home/bios/indexer_mainnet/reconcile_txns.py


echo "Restarted reconcile_txns"
