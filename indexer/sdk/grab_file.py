import os
import requests

def snagAsteroid(asteroid_id, asteroids_storage, network):

    if network == "mainnet":
        #slug = "production"
        slug = "https://images.influenceth.io/v2/"
        # https://images.influenceth.io/v2/asteroids/1/image.png
    elif network == "testnet":
        slug = "https://images.influenceth.io/v2/"
    elif network == "sepolia":
        slug = "https://images-prerelease.influenceth.io/v2/"
        # https://images-prerelease.influenceth.io/v2/asteroids/68/image.png

    url = slug + "asteroids/" + str(asteroid_id) + "/image.png"
    print("getting %s" % url)
    destination_path = asteroids_storage + str(asteroid_id) + ".png"
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
