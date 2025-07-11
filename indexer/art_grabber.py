#!/home/bios/.pyenv/shims/python3

import os
import sys
import requests
import asyncio
import time
import configparser
import db.artgrab_db as artgrab_db

async def log_loop(poll_interval, network, asteroids_storage, crewmates_storage):

    while True:

        asteroid_type = 1
        asteroids = artgrab_db.getToGrab(asteroid_type)
        print(asteroids)
        for asteroid_id in asteroids:
            snagAsteroid(asteroid_id, asteroids_storage, network)
            artgrab_db.markDone(asteroid_type, asteroid_id)
            time.sleep(2)


        crewmate_type = 2
        crewmates = artgrab_db.getToGrab(crewmate_type)
        print(crewmates)
        for crewmate_id in crewmates:
            snagCrewmate(crewmate_id, crewmates_storage, network)
            artgrab_db.markDone(crewmate_type, crewmate_id)
            time.sleep(2)

        await asyncio.sleep(poll_interval)


def snagAsteroid(asteroid_id, asteroids_storage, network):

    if network == "mainnet":
        slug = "https://images.influenceth.io/v2/"
    elif network == "testnet":
        slug = "https://images.influenceth.io/v2/"
    elif network == "sepolia":
        slug = "https://images-prerelease.influenceth.io/v2/"

    url = slug + "asteroids/" + str(asteroid_id) + "/image.png"
    print("getting %s" % url)
    destination_path = asteroids_storage + str(asteroid_id) + ".png"
    print("writing to %s" % destination_path)
    response = requests.get(url)

    if response.status_code == 200:
        with open(destination_path, "wb") as file:
            file.write(response.content)
        print(f"File downloaded to {destination_path}")
    else:
        print(f"Failed to download the file. Err {response.status_code}")


def snagCrewmate(crewmate_id, crewmates_storage, network):

    if network == "mainnet":
        slug = "https://images.influenceth.io/v2/"
    elif network == "testnet":
        slug = "https://images.influenceth.io/v2/"
    elif network == "sepolia":
        slug = "https://images-prerelease.influenceth.io/v2/"

    url = slug + "crewmates/" + str(crewmate_id) + "/image.png"
    print("getting %s" % url)
    destination_path = crewmates_storage + str(crewmate_id) + ".png"
    if os.path.exists(destination_path):
        print(f"The file already exists at: {destination_path}")
    else:
        print("writing to %s" % destination_path)
        response = requests.get(url)

        if response.status_code == 200:
            with open(destination_path, "wb") as file:
                file.write(response.content)
            print(f"File downloaded to {destination_path}")
        else:
            print(f"Failed to download the file. Err {response.status_code}")


def main():

    global network
    global asteroids_storage
    global crewmates_storage


    filename = __file__
    config_path = filename.split('/')[3]
    phase = config_path.split('_')[1]
    config_file = "/home/bios/" + config_path + "/indexer.conf"

    if os.path.exists(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        network = config.get('blockchain', 'network')
        asteroids_storage = config.get('storage', 'asteroids')
        crewmates_storage = config.get('storage', 'crewmates')

    else:
        raise Exception(config_file)

    poll_interval=60
    loop = asyncio.get_event_loop()
    try:
        print("*** Starting art grabber")
        loop.run_until_complete(
            asyncio.gather(
                log_loop(poll_interval, network, asteroids_storage, crewmates_storage)))
    finally:
        loop.close()


if __name__ == "__main__" : main()

