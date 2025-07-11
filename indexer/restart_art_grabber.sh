#!/bin/bash

pkill -ef /home/bios/indexer_mainnet/art_grabber.py

echo
sleep 1

cd /home/bios/indexer_mainnet

screen -dmS art_grabber_mainnet -L -Logfile /home/bios/indexer_mainnet/logs/art_grabber.log /home/bios/.pyenv/shims/python3 /home/bios/indexer_mainnet/art_grabber.py


echo "Restarted art_grabber"
