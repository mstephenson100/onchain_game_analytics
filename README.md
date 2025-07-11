# Overview

This is something I built to provide onchain analytics for a Starknet blockchain game called Influence. There are 3 core components to this stack.

## Pathfinder and Apibara
None of this works without a full Starknet node. Pathfinder was my choice: https://github.com/eqlabs/pathfinder

Once pathfinder is in sync then Apibara was needed for building the Starknet indexer: https://www.apibara.com/

Docker compose files are available in the apibara_dna directory for both apibara and pathfinder.

## Indexer
There were events from 4 different smart contracts that I needed to index. Of those 4 smart contracts, there were approximately 90 distinct events that needed to be indexed to maintain onchain game state. All indexed data was written to a MySQL database.

Indexer code is available in the indexer directory

## API
A Flask API server was built to return data to a web based dashboard. The API server included a method of validating the web user's wallet and providing analytics specific to that wallet.

The API code is available in the api directory.
