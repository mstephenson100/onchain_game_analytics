
# Pathfinder and Apibara Direct Node Access
# Overview
This repo includes the docker-compose configs needed to launch both a pathfinder full node and a Apibara DNA node. It's assumed that the user of this repo has basic Docker knowledge.

## Pathfinder
Pathfinder is a Starknet Full Node which can be used to access every block and every transaction in a block in the history of Starknet. It's also a json-rpc service which provides API access into Starknet. Here is the official documentation on how to get started with Pathfinder: https://github.com/eqlabs/pathfinder
#### Pathfinder Requirements
The basic requirements for running a Pathfinder full node is that you have access to an ethereum full node. The ethereum full node is needed to synchronize the Pathfinder full node for Starknet. You can either run your own ethereum full node or you can use Alchemy API's free tier to get enough access to keep your Pathfinder node in sync. The docket-compose files in this repo give both an example of using Alchemy or your own ethereum full node. Be prepared to wait a couple days for your node to fully sync. You could try using snapshots to decrease the sync time: https://github.com/zkLend/starknet-snapshots

The minimum server requirements to run a pathfinder full node on mainnet include:
-   CPU: 2+ cores
-   RAM: 4 GB
-   NVMe Disk: 600 GB
-   Connection Speed: 8 mbps/sec

As starknet grows in size then the disk requirements will also grow. Be prepared.

The final requirement is that you have docker installed.

## Apibara Direct Node Access
Apibara is an opensource tool that we will use to stream events from each block in Starknet (through Pathfinder) into an easily indexable format. You can read more about it here: https://www.apibara.com/docs

Apibara provides their own public DNA stream which you can freely access by obtaining an API key. This is probably the easiest approach to indexing events since then you wouldn't even need to run a local Pathfinder node but I want to run it and host it all myself. Running DNA locally has proven to be more fault tolerant and faster as a direct result. The full DNA database for mainnet is currently under 40G in size and testnet is similar so disk space won't really be an issue. The real resource hog here is Pathfinder.

DNA also requires Docker as the most basic requirement. 

## Launching Docker Stack
For this example we will be launching both Pathfinder and DNA from the same docker-compose.yml for Testnet. Your mileage may vary based on the fact that Pathfinder will take a very long time to sync up without using a snapshot.

Add the user you will be running docker as to the docker group in /etc/group
~~~
docker:x:998:bios
~~~
Assuming you've cloned this repo, set up in the repo testnet directory:
~~~
$ cd /home/bios/apibara_dna/testnet
~~~
Update the pathfinder-testnet-var.env config with the address of your ethereum full node (goerli testnet). You can use a free Alchemy API key for this:
~~~
$ vi pathfinder-testnet-var.env
PATHFINDER_ETHEREUM_API_URL=https://eth-goerli.g.alchemy.com/v2/<free_api_key_redacted>
~~~
The pathfinder_data and dna_data directories are placeholders for where docker-compose will write data to.

Let's take a quick look at a couple sections of docker-compose.yml before launching the stack:
~~~
services:
	testnet:
		ports:
			- 8545:9545
~~~
This maps the tcp port 9545 in the docker machine to tcp port 8545 so that you can access this service from localhost. Note that if you are running a firewall then you'll need to add a policy allowing tcp port 8545 from the internet to make Pathfinder in this container publicly accessible.

~~~
services:
	testnet:
		ports:
			- 7171:7171
~~~
This maps the tcp port 7171 in the docker machine to tcp port 7171 so that you can access this service from localhost. Note that if you are running a firewall then you'll need to add a policy allowing tcp port 7171 from the internet to make DNA in this container publicly accessible.

~~~
volumes:
	testnet:
		driver: local
		driver_opts:
			o: bind
			type: none
			device: /home/bios/apibara_dna/testnet/pathfinder_data
	apibara-data:
		driver: local
		driver_opts:
		o: bind
		type: none
		device: /home/bios/apibara_dna/testnet/dna_data
~~~
This maps the data volumes for both Pathfinder and DNA to the pathfinder_data and dna_data placeholders in the docker-compose.yml directory

### Launch docker-compose
You should be ready to launch the docker stack now.
~~~
$ docker-compose up --detach
~~~
Check to see the state of your docker instances:
~~~
$ docker ps

CONTAINER ID IMAGE COMMAND  CREATED STATUS PORTS NAMES

564f681a4e01 quay.io/apibara/starknet:8a5ff0593bc9eb561ade52535eaef489570eef08 "/nix/store/307fcyjm…" 9 days ago  Up 9 days  0.0.0.0:7171->7171/tcp, :::7171->7171/tcp dna_testnet_apibara_1

62d6c7b69818 eqlabs/pathfinder:latest  "/usr/bin/tini -- /u…" 9 days ago  Up 9 days  0.0.0.0:8545->9545/tcp, :::8545->9545/tcp dna_testnet_testnet_1
~~~
Hopefully both containers are healthy. You can tail the logs of both nodes to see how they're doing:
~~~
$ docker logs -f dna_testnet_apibara_1
$ docker logs -f dna_testnet_testnet_1
~~~
If you see errors then oopsie.
