import os
import sys
import pymysql
import warnings
import traceback
import configparser
import time

from flask import Flask, Response, request, jsonify
from flask_cors import CORS, cross_origin
import jwt
from jsonrpcserver import method, Result, Success, dispatch, Error
from blueprint_auth import authentication
from auth_utils import utils
from functools import wraps

import db.buildings as buildings_db
import db.crew as crew_db
import db.asteroids as asteroids_db
import db.coresamples as coresamples_db
import db.construction as construction_db
import db.extraction as extraction_db
import db.buildings as buildings_db
import db.deliveries as deliveries_db
import db.processing as processing_db
import db.inventory as inventory_db
import db.ships as ships_db
import db.transit as transit_db
import db.txn as txn_db
import db.propellant as propellant_db
import db.food as food_db
import db.marketplace as marketplace_db
import db.kpi as kpi_db
import db.global_metrics as global_db
import db.solo_metrics as solo_db
import db.solo_metrics_v2 as solo_db_v2
import db.community_metrics as community_db
import db.policies as policies_db
import db.productbot as productbot_db
import db.solo_dashboard as solo_dashboard_db
import db.ship_dashboard as ship_dashboard_db
import db.colonization_metrics as colonization_db

filename = __file__
config_path = filename.split('/')[3]
phase = config_path.split('_')[1]
config_file = "/home/bios/" + config_path + "/api.conf"

if os.path.exists(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    db_user = config.get('credentials', 'db_user')
    db_password = config.get('credentials', 'db_password')
    db = config.get('credentials', 'db')
    jwt_secret_key = config.get('authentication', 'jwt_secret_key')
else:
    raise Exception(config_file)

app = Flask(__name__)
cors = CORS(app)

app.config['SECRET_KEY'] = jwt_secret_key
app.config['CORS_HEADERS'] = 'Content-Type'
app.register_blueprint(authentication, url_prefix="/api/auth")

# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print(request.headers)
        token = None
        if 'X-Access-Token' in request.headers:
            token = request.headers['X-Access-Token']
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401

        try:
            data = jwt.decode(token, jwt_secret_key, algorithms="HS256")
            wallet = utils.getWallet(data['id'])
        except:
            return jsonify({'message' : 'Token is invalid !!'}), 401

        return  f(*args, **kwargs)

    return decorated


@method
def owned_asteroids(**kwargs):
    print(kwargs)
    if 'wallet' not in kwargs:
        return Error(-852, "wallet is required")

    if not kwargs['wallet'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = asteroids_db.ownedAsteroids(kwargs['wallet'])
    return (Success({"results_len": len(result), "result": result}))


@method
def managed_asteroids(**kwargs):
    print(kwargs)
    parameter1 = None
    parameter2 = None
    if 'wallet' in kwargs:
        parameter1 = 'wallet'
        parameter2 = kwargs['wallet']
    elif 'crew_id' in kwargs:
        parameter1 = 'crew'
        parameter2 = kwargs['crew_id']

    if parameter1 is None:
        return Error(-852, "either wallet or crew_id is required")

    if not parameter2.isalnum():
        return Error(-1679, "illegal parameter value")

    result = asteroids_db.managedAsteroids(parameter1, parameter2)
    return (Success({"results_len": len(result), "result": result}))


@method
def unmanaged_asteroids(**kwargs):
    print(kwargs)
    if 'wallet' not in kwargs:
        return Error(-852, "wallet is required")

    if not kwargs['wallet'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = asteroids_db.unmanagedAsteroids(kwargs['wallet'])
    return (Success({"results_len": len(result), "result": result}))


@method
def scanned_asteroids(**kwargs):
    print(kwargs)
    parameter1 = None
    parameter2 = None
    if 'wallet' in kwargs:
        parameter1 = 'wallet'
        parameter2 = kwargs['wallet']
    elif 'crew_id' in kwargs:
        parameter1 = 'crew'
        parameter2 = kwargs['crew_id']

    if parameter1 is None:
        return Error(-852, "either wallet or crew_id is required")

    if not parameter2.isalnum():
        return Error(-1679, "illegal parameter value")

    result = asteroids_db.scannedAsteroids(parameter1, parameter2)
    return (Success({"results_len": len(result), "result": result}))


@method
def asteroid(**kwargs):
    print(kwargs)
    if 'asteroid_id' not in kwargs:
        return Error(-852, "asteroid_id is required")

    if not kwargs['asteroid_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = asteroids_db.asteroid(int(kwargs['asteroid_id']))

    if result is None:
        results_len = 0
    else:
        results_len = 1

    return (Success({"results_len": results_len, "result": result}))


@method
def asteroid_owner(**kwargs):
    print(kwargs)
    if 'asteroid_id' not in kwargs:
        return Error(-852, "asteroid_id is required")

    if not kwargs['asteroid_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = asteroids_db.asteroidOwner(int(kwargs['asteroid_id']))

    if result is None:
        results_len = 0
    else:
        results_len = 1

    return (Success({"results_len": results_len, "result": result}))


@method
def owned_crewmates(**kwargs):
    print(kwargs)
    if 'wallet' not in kwargs:
        return Error(-852, "wallet is required")

    if not kwargs['wallet'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = crew_db.ownedCrewmates(kwargs['wallet'])
    return (Success({"results_len": len(result), "result": result}))


@method
def owned_crew(**kwargs):
    print(kwargs)
    if 'wallet' not in kwargs:
        return Error(-852, "wallet is required")

    if not kwargs['wallet'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = crew_db.ownedCrew(kwargs['wallet'])
    return (Success({"results_len": len(result), "result": result}))


@method
def crew_composition(**kwargs):
    print(kwargs)
    if 'crew_id' not in kwargs:
        return Error(-852, "crew_id is required")

    if not kwargs['crew_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = crew_db.crewComposition(int(kwargs['crew_id']))
    return (Success({"results_len": len(result), "result": result}))


@method
def crew_owner(**kwargs):
    print(kwargs)
    if 'crew_id' not in kwargs:
        return Error(-852, "crew_id is required")


    if not kwargs['crew_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = crew_db.crewOwner(int(kwargs['crew_id']))

    if result is None: 
        results_len = 0
    else:
        results_len = 1

    return (Success({"results_len": results_len, "result": result}))


@method
def crewmate_owner(**kwargs):
    print(kwargs)
    if 'crewmate_id' not in kwargs:
        return Error(-852, "crewmate_id is required")

    if not kwargs['crewmate_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = crew_db.crewmateOwner(int(kwargs['crewmate_id']))

    if result is None:
        results_len = 0
    else:
        results_len = 1

    return (Success({"results_len": results_len, "result": result}))


@method
def crewmate(**kwargs):
    print(kwargs)
    if 'crewmate_id' not in kwargs:
        return Error(-852, "crewmate_id is required")

    if not kwargs['crewmate_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = crew_db.crewmate(int(kwargs['crewmate_id']))

    if result is None:
        results_len = 0
    else:
        results_len = 1

    return (Success({"results_len": results_len, "result": result}))


@method
def crew(**kwargs):
    print(kwargs)
    if 'crew_id' not in kwargs:
        return Error(-852, "crew_id is required")

    if not kwargs['crew_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = crew_db.crewComposition(int(kwargs['crew_id']))

    if result is None:
        results_len = 0
    else:
        results_len = 1

    return (Success({"results_len": results_len, "result": result}))


@method
def policies_applied_by(**kwargs):
    print(kwargs)
    parameter1 = None
    parameter2 = None
    if 'wallet' in kwargs:
        parameter1 = 'wallet'
        parameter2 = kwargs['wallet']
    elif 'crew_id' in kwargs:
        parameter1 = 'crew'
        parameter2 = kwargs['crew_id']

    if parameter1 is None:
        return Error(-852, "either wallet or crew_id is required")

    if not parameter2.isalnum():
        return Error(-1679, "illegal parameter value")

    result = asteroids_db.policiesAppliedBy(parameter1, parameter2)
    return (Success({"results_len": len(result), "result": result}))


@method
def coresamples_state(**kwargs):
    print(kwargs)
    parameter1 = None
    parameter2 = None
    if 'wallet' in kwargs:
        parameter1 = 'wallet'
        parameter2 = kwargs['wallet']
    elif 'crew_id' in kwargs:
        parameter1 = 'crew'
        parameter2 = kwargs['crew_id']

    if 'state' not in kwargs:
        return Error(-852, "state is required")

    if 'start_block' not in kwargs:
        start_block = 1
    else:
        start_block = kwargs['start_block']

    if 'end_block' not in kwargs:
        end_block = 0
    else:
        end_block = kwargs['end_block']

    if parameter1 is None:
        return Error(-852, "either wallet or crew_id is required")

    if not parameter2.isalnum():
        return Error(-1679, "illegal parameter value")

    result = coresamples_db.coresamplesState(kwargs['state'], parameter1, parameter2, int(start_block), int(end_block))
    return (Success({"results_len": len(result), "coresamples": result}))


@method
def coresamples_depleted(**kwargs):
    print(kwargs)
    parameter1 = None
    parameter2 = None
    if 'wallet' in kwargs:
        parameter1 = 'wallet'
        parameter2 = kwargs['wallet']
    elif 'crew_id' in kwargs:
        parameter1 = 'crew'
        parameter2 = kwargs['crew_id']

    if parameter1 is None:
        return Error(-852, "either wallet or crew_id is required")

    if not parameter2.isalnum():
        return Error(-1679, "illegal parameter value")

    result = coresamples_db.depletedCoresamples(parameter1, parameter2)
    return (Success({"results_len": len(result), "coresamples": result}))


@method
def coresamples_at_lot(**kwargs):
    print(kwargs)
    if 'lot_id' not in kwargs:
        return Error(-852, "lot_id is required")

    if 'asteroid_id' not in kwargs:
        return Error(-852, "asteroid_id is required")

    if not kwargs['lot_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    if not kwargs['asteroid_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = coresamples_db.coresamplesAtLot(int(kwargs['asteroid_id']), int(kwargs['lot_id']))
    return (Success({"results_len": len(result), "coresamples": result}))


@method
def coresamples_owned_at_lot(**kwargs):
    print(kwargs)
    parameter1 = None
    parameter2 = None
    if 'wallet' in kwargs:
        parameter1 = 'wallet'
        parameter2 = kwargs['wallet']
    elif 'crew_id' in kwargs:
        parameter1 = 'crew'
        parameter2 = kwargs['crew_id']

    if parameter1 is None:
        return Error(-852, "either wallet or crew_id is required")

    if 'lot_id' not in kwargs:
        return Error(-852, "lot_id is required")

    if 'asteroid_id' not in kwargs:
        return Error(-852, "asteroid_id is required")

    if not parameter2.isalnum():
        return Error(-1679, "illegal parameter value")

    if not kwargs['lot_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    if not kwargs['asteroid_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = coresamples_db.coresamplesOwnedAtLot(int(kwargs['asteroid_id']), int(kwargs['lot_id']), parameter1, parameter2)
    return (Success({"results_len": len(result), "coresamples": result}))


@method
def coresamples_owned_on_asteroid(**kwargs):
    print(kwargs)
    parameter1 = None
    parameter2 = None
    if 'wallet' in kwargs:
        parameter1 = 'wallet'
        parameter2 = kwargs['wallet']
    elif 'crew_id' in kwargs:
        parameter1 = 'crew'
        parameter2 = kwargs['crew_id']

    if parameter1 is None:
        return Error(-852, "either wallet or crew_id is required")

    if 'asteroid_id' not in kwargs:
        return Error(-852, "asteroid_id is required")

    if not parameter2.isalnum():
        return Error(-1679, "illegal parameter value")

    if not kwargs['asteroid_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = coresamples_db.coresamplesOwnedOnAsteroid(int(kwargs['asteroid_id']), parameter1, parameter2)
    return (Success({"results_len": len(result), "coresamples": result}))


@method
def coresamples_owned(**kwargs):
    print(kwargs)
    parameter1 = None
    parameter2 = None
    if 'wallet' in kwargs:
        parameter1 = 'wallet'
        parameter2 = kwargs['wallet']
    elif 'crew_id' in kwargs:
        parameter1 = 'crew'
        parameter2 = kwargs['crew_id']

    if parameter1 is None:
        return Error(-852, "either wallet or crew_id is required")

    if not parameter2.isalnum():
        return Error(-1679, "illegal parameter value")

    result = coresamples_db.coresamplesOwned(parameter1, parameter2)
    return (Success({"results_len": len(result), "coresamples": result}))


@method
def coresamples_on_asteroid(**kwargs):
    print(kwargs)
    if 'asteroid_id' not in kwargs:
        return Error(-852, "asteroid_id is required")

    if not kwargs['asteroid_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = coresamples_db.coresamplesOnAsteroid(int(kwargs['asteroid_id']))
    return (Success({"results_len": len(result), "coresamples": result}))


@method
def coresample_details(**kwargs):
    print(kwargs)
    if 'deposit_id' not in kwargs:
        return Error(-852, "deposit_id is required")

    if not kwargs['deposit_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = coresamples_db.coresampleDetails(int(kwargs['deposit_id']))
    return (Success({"results_len": len(result), "coresample": result}))


@method
def construction_state(**kwargs):
    print(kwargs)
    parameter1 = None
    parameter2 = None
    if 'wallet' in kwargs:
        parameter1 = 'wallet'
        parameter2 = kwargs['wallet']
    elif 'crew_id' in kwargs:
        parameter1 = 'crew'
        parameter2 = kwargs['crew_id']

    if parameter1 is None:
        return Error(-852, "either wallet or crew_id is required")

    if 'building_type' not in kwargs:
        return Error(-852, "building_type is required")

    if 'state' not in kwargs:
        return Error(-852, "state is required")

    if 'start_block' not in kwargs:
        start_block = 1
    else:
        start_block = kwargs['start_block']

    if 'end_block' not in kwargs:
        end_block = 0
    else:
        end_block = kwargs['end_block']

    if kwargs['building_type'] not in ['warehouse', 'extractor', 'refinery', 'bioreactor', 'factory', 'shipyard', 'spaceport', 'marketplace', 'habitat']:
        return Error(-852, "invalid building_type")

    if not parameter2.isalnum():
        return Error(-1679, "illegal parameter value")

    result = construction_db.constructionState(kwargs['building_type'], parameter1, parameter2, kwargs['state'], start_block, end_block)
    return (Success({"results_len": len(result), "construction": result}))


@method
def owned_buildings(**kwargs):
    print(kwargs)
    parameter1 = None
    parameter2 = None
    if 'wallet' in kwargs:
        parameter1 = 'wallet'
        parameter2 = kwargs['wallet']
    elif 'crew_id' in kwargs:
        parameter1 = 'crew'
        parameter2 = kwargs['crew_id']

    if parameter1 is None:
        return Error(-852, "either wallet or crew_id is required")

    if 'building_type' not in kwargs:
        return Error(-852, "building_type is required")

    if kwargs['building_type'] not in ['warehouse', 'extractor', 'refinery', 'bioreactor', 'factory', 'shipyard', 'spaceport', 'marketplace', 'habitat']:
        return Error(-852, "invalid building_type")

    if not parameter2.isalnum():
        return Error(-1679, "illegal parameter value")

    result = buildings_db.ownedBuildings(kwargs['building_type'], parameter1, parameter2)
    return (Success({"results_len": len(result), "buildings": result}))


@method
def owned_buildings_on_asteroid(**kwargs):
    print(kwargs)
    parameter1 = None
    parameter2 = None
    if 'wallet' in kwargs:
        parameter1 = 'wallet'
        parameter2 = kwargs['wallet']
    elif 'crew_id' in kwargs:
        parameter1 = 'crew'
        parameter2 = kwargs['crew_id']

    if parameter1 is None:
        return Error(-852, "either wallet or crew_id is required")

    if 'asteroid_id' not in kwargs:
        return Error(-852, "asteroid_id is required")

    if not parameter2.isalnum():
        return Error(-1679, "illegal parameter value")

    if not kwargs['asteroid_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = buildings_db.ownedBuildingsOnAsteroid(parameter1, parameter2, int(kwargs['asteroid_id']))
    return (Success({"results_len": len(result), "buildings": result}))


@method
def owned_buildings_on_lot(**kwargs):
    print(kwargs)
    parameter1 = None
    parameter2 = None
    if 'wallet' in kwargs:
        parameter1 = 'wallet'
        parameter2 = kwargs['wallet']
    elif 'crew_id' in kwargs:
        parameter1 = 'crew'
        parameter2 = kwargs['crew_id']

    if parameter1 is None:
        return Error(-852, "either wallet or crew_id is required")

    if 'asteroid_id' not in kwargs:
        return Error(-852, "asteroid_id is required")

    if 'lot_id' not in kwargs:
        return Error(-852, "lot_id is required")

    if not parameter2.isalnum():
        return Error(-1679, "illegal parameter value")

    if not kwargs['asteroid_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    if not kwargs['lot_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = buildings_db.ownedBuildingsOnLot(parameter1, parameter2, int(kwargs['asteroid_id']), int(kwargs['lot_id']))
    return (Success({"results_len": len(result), "buildings": result}))


@method
def building_state(**kwargs):
    print(kwargs)
    if 'building_id' not in kwargs:
        return Error(-852, "building_id is required")

    if not kwargs['building_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = buildings_db.buildingState(int(kwargs['building_id']))
    return (Success({"results_len": len(result), "buildings": result}))


@method
def extraction_state(**kwargs):
    print(kwargs)
    parameter1 = None
    parameter2 = None
    if 'wallet' in kwargs:
        parameter1 = 'wallet'
        parameter2 = kwargs['wallet']
    elif 'crew_id' in kwargs:
        parameter1 = 'crew'
        parameter2 = kwargs['crew_id']

    if kwargs['state'] not in ['started', 'pending', 'finished']:
        return Error(-852, "invalid state")

    if 'start_block' not in kwargs:
        start_block = 1
    else:
        start_block = kwargs['start_block']

    if 'end_block' not in kwargs:
        end_block = 0
    else:
        end_block = kwargs['end_block']

    if parameter1 is None:
        return Error(-852, "either wallet or crew_id is required")

    if not parameter2.isalnum():
        return Error(-1679, "illegal parameter value")

    result = extraction_db.extractionState(parameter1, parameter2, kwargs['state'], start_block, end_block)
    return (Success({"results_len": len(result), "extractions": result}))


@method
def extraction_on_asteroid(**kwargs):
    print(kwargs)
    parameter1 = None
    parameter2 = None
    if 'wallet' in kwargs:
        parameter1 = 'wallet'
        parameter2 = kwargs['wallet']
    elif 'crew_id' in kwargs:
        parameter1 = 'crew'
        parameter2 = kwargs['crew_id']

    if kwargs['state'] not in ['started', 'pending', 'finished']:
        return Error(-852, "invalid state")

    if 'start_block' not in kwargs:
        start_block = 1
    else:
        start_block = kwargs['start_block']

    if 'end_block' not in kwargs:
        end_block = 0
    else:
        end_block = kwargs['end_block']

    if 'asteroid_id' not in kwargs:
        return Error(-852, "asteroid_id is required")

    if not kwargs['asteroid_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    if parameter1 is None:
        return Error(-852, "either wallet or crew_id is required")

    if not parameter2.isalnum():
        return Error(-1679, "illegal parameter value")

    result = extraction_db.extractionOnAsteroid(parameter1, parameter2, kwargs['state'], kwargs['asteroid_id'], start_block, end_block)
    return (Success({"results_len": len(result), "extractions": result}))


@method
def extraction_on_lot(**kwargs):
    print(kwargs)
    parameter1 = None
    parameter2 = None
    if 'wallet' in kwargs:
        parameter1 = 'wallet'
        parameter2 = kwargs['wallet']
    elif 'crew_id' in kwargs:
        parameter1 = 'crew'
        parameter2 = kwargs['crew_id']

    if kwargs['state'] not in ['started', 'pending', 'finished']:
        return Error(-852, "invalid state")

    if 'start_block' not in kwargs:
        start_block = 1
    else:
        start_block = kwargs['start_block']

    if 'end_block' not in kwargs:
        end_block = 0
    else:
        end_block = kwargs['end_block']

    if 'asteroid_id' not in kwargs:
        return Error(-852, "asteroid_id is required")

    if not kwargs['asteroid_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    if 'lot_id' not in kwargs:
        return Error(-852, "lot_id is required")

    if not kwargs['lot_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    if parameter1 is None:
        return Error(-852, "either wallet or crew_id is required")

    if not parameter2.isalnum():
        return Error(-1679, "illegal parameter value")

    result = extraction_db.extractionOnLot(parameter1, parameter2, kwargs['state'], kwargs['asteroid_id'], kwargs['lot_id'], start_block, end_block)
    return (Success({"results_len": len(result), "extractions": result}))


@method
def extracted_resources(**kwargs):
    print(kwargs)
    parameter1 = None
    parameter2 = None
    if 'wallet' in kwargs:
        parameter1 = 'wallet'
        parameter2 = kwargs['wallet']
    elif 'crew_id' in kwargs:
        parameter1 = 'crew'
        parameter2 = kwargs['crew_id']

    if parameter1 is None:
        return Error(-852, "either wallet or crew_id is required")

    if not parameter2.isalnum():
        return Error(-1679, "illegal parameter value")

    if not kwargs['resource_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = extraction_db.extractedByResource(int(kwargs['resource_id']), parameter1, parameter2)
    return (Success({"results_len": len(result), "extracted_resources": result}))


@method
def extracted_resources_all(**kwargs):
    print(kwargs)
    parameter1 = None
    parameter2 = None
    if 'wallet' in kwargs:
        parameter1 = 'wallet'
        parameter2 = kwargs['wallet']
    elif 'crew_id' in kwargs:
        parameter1 = 'crew'
        parameter2 = kwargs['crew_id']

    if parameter1 is None:
        return Error(-852, "either wallet or crew_id is required")

    if not parameter2.isalnum():
        return Error(-1679, "illegal parameter value")

    result = extraction_db.extractedResourcesAll(parameter1, parameter2)
    return (Success({"results_len": len(result), "extracted_resources": result}))


@method
def deliveries_state(**kwargs):
    print(kwargs)
    parameter1 = None
    parameter2 = None
    if 'wallet' in kwargs:
        parameter1 = 'wallet'
        parameter2 = kwargs['wallet']
    elif 'crew_id' in kwargs:
        parameter1 = 'crew'
        parameter2 = kwargs['crew_id']

    if 'state' not in kwargs:
        return Error(-852, "state is required")

    if kwargs['state'] not in ['started', 'pending', 'finished']:
        return Error(-852, "invalid state")

    if 'start_block' not in kwargs:
        start_block = 1
    else:
        start_block = kwargs['start_block']

    if 'end_block' not in kwargs:
        end_block = 0
    else:
        end_block = kwargs['end_block']

    if not start_block.isalnum():
        return Error(-1679, "illegal parameter value")

    if not end_block.isalnum():
        return Error(-1679, "illegal parameter value")

    if parameter1 is None:
        return Error(-852, "either wallet or crew_id is required")

    if not parameter2.isalnum():
        return Error(-1679, "illegal parameter value")

    result = deliveries_db.allDeliveries(parameter1, parameter2, kwargs['state'], int(start_block), int(end_block))
    return (Success({"results_len": len(result), "deliveries": result}))


@method
def deliveries_on_asteroid(**kwargs):
    print(kwargs)
    parameter1 = None
    parameter2 = None
    if 'wallet' in kwargs:
        parameter1 = 'wallet'
        parameter2 = kwargs['wallet']
    elif 'crew_id' in kwargs:
        parameter1 = 'crew'
        parameter2 = kwargs['crew_id']

    if 'state' not in kwargs:
        return Error(-852, "state is required")

    if kwargs['state'] not in ['started', 'pending', 'finished']:
        return Error(-852, "invalid state")

    if 'start_block' not in kwargs:
        start_block = 1
    else:
        start_block = kwargs['start_block']

    if 'end_block' not in kwargs:
        end_block = 0
    else:
        end_block = kwargs['end_block']

    if not start_block.isalnum():
        return Error(-1679, "illegal parameter value")

    if not end_block.isalnum():
        return Error(-1679, "illegal parameter value")

    if parameter1 is None:
        return Error(-852, "either wallet or crew_id is required")

    if not parameter2.isalnum():
        return Error(-1679, "illegal parameter value")

    if 'asteroid_id' not in kwargs:
        return Error(-852, "asteroid_id is required")

    if not kwargs['asteroid_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = deliveries_db.deliveriesOnAsteroid(int(kwargs['asteroid_id']), parameter1, parameter2, kwargs['state'], int(start_block), int(end_block))
    return (Success({"results_len": len(result), "deliveries": result}))


@method
def deliveries_from_lot(**kwargs):
    print(kwargs)
    parameter1 = None
    parameter2 = None
    if 'wallet' in kwargs:
        parameter1 = 'wallet'
        parameter2 = kwargs['wallet']
    elif 'crew_id' in kwargs:
        parameter1 = 'crew'
        parameter2 = kwargs['crew_id']

    if 'state' not in kwargs:
        return Error(-852, "state is required")

    if kwargs['state'] not in ['started', 'pending', 'finished']:
        return Error(-852, "invalid state")

    if 'start_block' not in kwargs:
        start_block = 1
    else:
        start_block = kwargs['start_block']

    if 'end_block' not in kwargs:
        end_block = 0
    else:
        end_block = kwargs['end_block']

    if not start_block.isalnum():
        return Error(-1679, "illegal parameter value")

    if not end_block.isalnum():
        return Error(-1679, "illegal parameter value")

    if parameter1 is None:
        return Error(-852, "either wallet or crew_id is required")

    if not parameter2.isalnum():
        return Error(-1679, "illegal parameter value")

    if 'asteroid_id' not in kwargs:
        return Error(-852, "asteroid_id is required")

    if 'lot_id' not in kwargs:
        return Error(-852, "lot_id is required")

    if not kwargs['asteroid_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    if not kwargs['lot_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = deliveries_db.deliveriesFromLot(int(kwargs['asteroid_id']), int(kwargs['lot_id']), parameter1, parameter2, kwargs['state'], int(start_block), int(end_block))
    return (Success({"results_len": len(result), "deliveries": result}))


@method
def deliveries_to_lot(**kwargs):
    print(kwargs)
    parameter1 = None
    parameter2 = None
    if 'wallet' in kwargs:
        parameter1 = 'wallet'
        parameter2 = kwargs['wallet']
    elif 'crew_id' in kwargs:
        parameter1 = 'crew'
        parameter2 = kwargs['crew_id']

    if parameter1 is None:
        return Error(-852, "either wallet or crew_id is required")

    if not parameter2.isalnum():
        return Error(-1679, "illegal parameter value")

    if 'state' not in kwargs:
        return Error(-852, "state is required")

    if kwargs['state'] not in ['started', 'pending', 'finished']:
        return Error(-852, "invalid state")

    if 'start_block' not in kwargs:
        start_block = 1
    else:
        start_block = kwargs['start_block']

    if 'end_block' not in kwargs:
        end_block = 0
    else:
        end_block = kwargs['end_block']

    if not start_block.isalnum():
        return Error(-1679, "illegal parameter value")

    if not end_block.isalnum():
        return Error(-1679, "illegal parameter value")

    if 'asteroid_id' not in kwargs:
        return Error(-852, "asteroid_id is required")

    if 'lot_id' not in kwargs:
        return Error(-852, "lot_id is required")

    if not kwargs['asteroid_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    if not kwargs['lot_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = deliveries_db.deliveriesToLot(int(kwargs['asteroid_id']), int(kwargs['lot_id']), parameter1, parameter2, kwargs['state'], int(start_block), int(end_block))
    return (Success({"results_len": len(result), "deliveries": result}))


@method
def processing_state(**kwargs):
    print(kwargs)
    parameter1 = None
    parameter2 = None
    if 'wallet' in kwargs:
        parameter1 = 'wallet'
        parameter2 = kwargs['wallet']
    elif 'crew_id' in kwargs:
        parameter1 = 'crew'
        parameter2 = kwargs['crew_id']

    if 'state' not in kwargs:
        return Error(-852, "state is required")

    if kwargs['state'] not in ['started', 'pending', 'finished']:
        return Error(-852, "invalid state")

    if 'processor' not in kwargs:
        return Error(-852, "processor is required")

    if kwargs['processor'] not in ['refinery', 'factory', 'bioreactor', 'shipyard']:
        return Error(-852, "invalid processor")

    if 'start_block' not in kwargs:
        start_block = 1
    else:
        start_block = kwargs['start_block']

    if 'end_block' not in kwargs:
        end_block = 0
    else:
        end_block = kwargs['end_block']

    if not start_block.isalnum():
        return Error(-1679, "illegal parameter value")

    if not end_block.isalnum():
        return Error(-1679, "illegal parameter value")

    if parameter1 is None:
        return Error(-852, "either wallet or crew_id is required")

    if not parameter2.isalnum():
        return Error(-1679, "illegal parameter value")

    result = processing_db.processingState(parameter1, parameter2, kwargs['state'], kwargs['processor'], int(start_block), int(end_block))
    return (Success({"results_len": len(result), "processing": result}))


@method
def processing_on_asteroid(**kwargs):
    print(kwargs)
    parameter1 = None
    parameter2 = None
    if 'wallet' in kwargs:
        parameter1 = 'wallet'
        parameter2 = kwargs['wallet']
    elif 'crew_id' in kwargs:
        parameter1 = 'crew'
        parameter2 = kwargs['crew_id']

    if 'state' not in kwargs:
        return Error(-852, "state is required")

    if kwargs['state'] not in ['started', 'pending', 'finished']:
        return Error(-852, "invalid state")

    if 'processor' not in kwargs:
        return Error(-852, "processor is required")

    if kwargs['processor'] not in ['refinery', 'factory', 'bioreactor', 'shipyard']:
        return Error(-852, "invalid processor")

    if 'start_block' not in kwargs:
        start_block = 1
    else:
        start_block = kwargs['start_block']

    if 'end_block' not in kwargs:
        end_block = 0
    else:
        end_block = kwargs['end_block']

    if not start_block.isalnum():
        return Error(-1679, "illegal parameter value")

    if not end_block.isalnum():
        return Error(-1679, "illegal parameter value")

    if parameter1 is None:
        return Error(-852, "either wallet or crew_id is required")

    if not parameter2.isalnum():
        return Error(-1679, "illegal parameter value")

    if 'asteroid_id' not in kwargs:
        return Error(-852, "asteroid_id is required")

    if not kwargs['asteroid_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = processing_db.processingOnAsteroid(int(kwargs['asteroid_id']), parameter1, parameter2, kwargs['state'], kwargs['processor'], int(start_block), int(end_block))
    return (Success({"results_len": len(result), "processing": result}))


@method
def processing_on_lot(**kwargs):
    print(kwargs)
    parameter1 = None
    parameter2 = None
    if 'wallet' in kwargs:
        parameter1 = 'wallet'
        parameter2 = kwargs['wallet']
    elif 'crew_id' in kwargs:
        parameter1 = 'crew'
        parameter2 = kwargs['crew_id']

    if 'state' not in kwargs:
        return Error(-852, "state is required")

    if kwargs['state'] not in ['started', 'pending', 'finished']:
        return Error(-852, "invalid state")

    if 'processor' not in kwargs:
        return Error(-852, "processor is required")

    if kwargs['processor'] not in ['refinery', 'factory', 'bioreactor', 'shipyard']:
        return Error(-852, "invalid processor")

    if 'start_block' not in kwargs:
        start_block = 1
    else:
        start_block = kwargs['start_block']

    if 'end_block' not in kwargs:
        end_block = 0
    else:
        end_block = kwargs['end_block']

    if not start_block.isalnum():
        return Error(-1679, "illegal parameter value")

    if not end_block.isalnum():
        return Error(-1679, "illegal parameter value")

    if parameter1 is None:
        return Error(-852, "either wallet or crew_id is required")

    if not parameter2.isalnum():
        return Error(-1679, "illegal parameter value")

    if 'asteroid_id' not in kwargs:
        return Error(-852, "asteroid_id is required")

    if 'lot_id' not in kwargs:
        return Error(-852, "lot_id is required")

    if not kwargs['asteroid_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    if not kwargs['lot_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = processing_db.processingOnLot(int(kwargs['asteroid_id']), int(kwargs['lot_id']), parameter1, parameter2, kwargs['state'], kwargs['processor'], int(start_block), int(end_block))
    return (Success({"results_len": len(result), "processing": result}))


@method
def processing_search_component(**kwargs):
    print(kwargs)
    parameter1 = None
    parameter2 = None
    parameter3 = None
    parameter4 = None
    if 'wallet' in kwargs:
        parameter1 = 'wallet'
        parameter2 = kwargs['wallet']
    elif 'crew_id' in kwargs:
        parameter1 = 'crew'
        parameter2 = kwargs['crew_id']

    if 'input_id' in kwargs:
        parameter3 = "inputs"
        parameter4 = kwargs['input_id']
    elif 'output_id' in kwargs:
        parameter3 = "outputs"
        parameter4 = kwargs['output_id']

    if 'processor' not in kwargs:
        processor = None
    else:
        if kwargs['processor'] not in ['refinery', 'factory', 'bioreactor', 'shipyard']:
            return Error(-852, "invalid processor")

    if 'start_block' not in kwargs:
        start_block = 1
    else:
        start_block = kwargs['start_block']

    if 'end_block' not in kwargs:
        end_block = 0
    else:
        end_block = kwargs['end_block']

    if not start_block.isalnum():
        return Error(-1679, "illegal parameter value")

    if not end_block.isalnum():
        return Error(-1679, "illegal parameter value")

    if parameter1 is None:
        return Error(-852, "either wallet or crew_id is required")

    if not parameter2.isalnum():
        return Error(-1679, "illegal parameter value")

    if parameter3 is None:
        return Error(-852, "either input_id or output_id is required")

    if not parameter4.isalnum():
        return Error(-1679, "illegal parameter value")

    result = processing_db.processingSearchComponent(parameter1, parameter2, parameter3, parameter4, processor, int(start_block), int(end_block))
    return (Success({"results_len": len(result), "processing": result}))


@method
def inventory_at_entity(**kwargs):
    print(kwargs)
    if 'inventory_type' not in kwargs:
        return Error(-852, "inventory_type is required")

    if 'inventory_id' not in kwargs:
        return Error(-852, "inventory_id is required")

    if not kwargs['inventory_type'].isalnum():
        return Error(-1679, "illegal parameter value")

    if not kwargs['inventory_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = inventory_db.inventoryAtEntity(int(kwargs['inventory_type']), int(kwargs['inventory_id']))
    return (Success({"results_len": len(result), "inventory": result}))


@method
def inventory_on_asteroid(**kwargs):
    print(kwargs)
    parameter1 = None
    parameter2 = None
    if 'wallet' in kwargs:
        parameter1 = 'wallet'
        parameter2 = kwargs['wallet']
    elif 'crew_id' in kwargs:
        parameter1 = 'crew'
        parameter2 = kwargs['crew_id']

    if parameter1 is None:
        return Error(-852, "either wallet or crew_id is required")

    if not parameter2.isalnum():
        return Error(-1679, "illegal parameter value")

    if 'asteroid_id' not in kwargs:
        return Error(-852, "asteroid_id is required")

    if not kwargs['asteroid_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = inventory_db.inventoryOnAsteroid(int(kwargs['asteroid_id']), parameter1, parameter2)
    return (Success({"results_len": len(result), "inventory": result}))


@method
def inventory_on_lot(**kwargs):
    print(kwargs)
    parameter1 = None
    parameter2 = None
    if 'wallet' in kwargs:
        parameter1 = 'wallet'
        parameter2 = kwargs['wallet']
    elif 'crew_id' in kwargs:
        parameter1 = 'crew'
        parameter2 = kwargs['crew_id']

    if parameter1 is None:
        return Error(-852, "either wallet or crew_id is required")

    if not parameter2.isalnum():
        return Error(-1679, "illegal parameter value")

    if 'asteroid_id' not in kwargs:
        return Error(-852, "asteroid_id is required")

    if 'lot_id' not in kwargs:
        return Error(-852, "lot_id is required")

    if not kwargs['asteroid_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    if not kwargs['lot_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = inventory_db.inventoryOnLot(int(kwargs['asteroid_id']), int(kwargs['lot_id']), parameter1, parameter2)
    return (Success({"results_len": len(result), "inventory": result}))


@method
def ship_assembly_state(**kwargs):
    print(kwargs)
    parameter1 = None
    parameter2 = None
    if 'wallet' in kwargs:
        parameter1 = 'wallet'
        parameter2 = kwargs['wallet']
    elif 'crew_id' in kwargs:
        parameter1 = 'crew'
        parameter2 = kwargs['crew_id']

    if 'state' not in kwargs:
        return Error(-852, "state is required")

    if kwargs['state'] not in ['started', 'pending', 'finished']:
        return Error(-852, "invalid state")

    if 'start_block' not in kwargs:
        start_block = 1
    else:
        start_block = kwargs['start_block']

    if 'end_block' not in kwargs:
        end_block = 0
    else:
        end_block = kwargs['end_block']

    if not start_block.isalnum():
        return Error(-1679, "illegal parameter value")

    if not end_block.isalnum():
        return Error(-1679, "illegal parameter value")

    if parameter1 is None:
        return Error(-852, "either wallet or crew_id is required")

    if not parameter2.isalnum():
        return Error(-1679, "illegal parameter value")

    result = ships_db.shipAssemblyState(parameter1, parameter2, kwargs['state'], int(start_block), int(end_block))
    return (Success({"results_len": len(result), "ship_assembly": result}))


@method
def owned_ships(**kwargs):
    print(kwargs)
    parameter1 = None
    parameter2 = None
    if 'wallet' in kwargs:
        parameter1 = 'wallet'
        parameter2 = kwargs['wallet']
    elif 'crew_id' in kwargs:
        parameter1 = 'crew'
        parameter2 = kwargs['crew_id']

    if parameter1 is None:
        return Error(-852, "either wallet or crew_id is required")

    if not parameter2.isalnum():
        return Error(-1679, "illegal parameter value")

    result = ships_db.ownedShips(parameter1, parameter2)
    return (Success({"results_len": len(result), "ships": result}))


@method
def owned_ships_on_asteroid(**kwargs):
    print(kwargs)
    parameter1 = None
    parameter2 = None
    if 'wallet' in kwargs:
        parameter1 = 'wallet'
        parameter2 = kwargs['wallet']
    elif 'crew_id' in kwargs:
        parameter1 = 'crew'
        parameter2 = kwargs['crew_id']

    if parameter1 is None:
        return Error(-852, "either wallet or crew_id is required")

    if not parameter2.isalnum():
        return Error(-1679, "illegal parameter value")

    if 'asteroid_id' not in kwargs:
        return Error(-852, "asteroid_id is required")

    if not kwargs['asteroid_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = ships_db.ownedShipsOnAsteroid(parameter1, parameter2, kwargs['asteroid_id'])
    return (Success({"results_len": len(result), "ships": result}))


@method
def ship(**kwargs):
    print(kwargs)
    if 'ship_id' not in kwargs:
        return Error(-852, "ship_id is required")

    if not kwargs['ship_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = ships_db.shipStatus(kwargs['ship_id'])
    return (Success({"results_len": len(result), "ship": result}))


@method
def transit_state(**kwargs):
    print(kwargs)
    parameter1 = None
    parameter2 = None
    if 'wallet' in kwargs:
        parameter1 = 'wallet'
        parameter2 = kwargs['wallet']
    elif 'crew_id' in kwargs:
        parameter1 = 'crew'
        parameter2 = kwargs['crew_id']

    if 'state' not in kwargs:
        return Error(-852, "state is required")

    if kwargs['state'] not in ['started', 'pending', 'finished']:
        return Error(-852, "invalid state")

    if 'start_block' not in kwargs:
        start_block = 1
    else:
        start_block = kwargs['start_block']

    if 'end_block' not in kwargs:
        end_block = 0
    else:
        end_block = kwargs['end_block']

    if 'hours' not in kwargs:
        hours = None
    else:
        hours = kwargs['hours']

    if hours is not None:
        if not hours.isalnum():
            return Error(-1679, "illegal parameter value")

    if not start_block.isalnum():
        return Error(-1679, "illegal parameter value")

    if not end_block.isalnum():
        return Error(-1679, "illegal parameter value")

    if parameter1 is None:
        return Error(-852, "either wallet or crew_id is required")

    if not parameter2.isalnum():
        return Error(-1679, "illegal parameter value")

    result = transit_db.transitState(parameter1, parameter2, kwargs['state'], int(start_block), int(end_block), hours)
    print(result)
    return (Success({"results_len": len(result), "transit": result}))


@method
def transit_state_ship(**kwargs):
    print(kwargs)

    if 'ship_id' not in kwargs:
        return Error(-852, "ship_id is required")

    if 'state' not in kwargs:
        return Error(-852, "state is required")

    if kwargs['state'] not in ['started', 'pending', 'finished']:
        return Error(-852, "invalid state")

    if 'start_block' not in kwargs:
        start_block = 1
    else:
        start_block = kwargs['start_block']

    if 'end_block' not in kwargs:
        end_block = 0
    else:
        end_block = kwargs['end_block']

    if 'hours' not in kwargs:
        hours = None
    else:
        hours = kwargs['hours']

    if hours is not None:
        if not hours.isalnum():
            return Error(-1679, "illegal parameter value")

    if not start_block.isalnum():
        return Error(-1679, "illegal parameter value")

    if not end_block.isalnum():
        return Error(-1679, "illegal parameter value")

    if not kwargs['ship_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = transit_db.transitStateShip(kwargs['ship_id'], kwargs['state'], int(start_block), int(end_block), hours)
    return (Success({"results_len": len(result), "transit": result}))


@method
def transit_from_asteroid(**kwargs):
    print(kwargs)

    if 'asteroid_id' not in kwargs:
        return Error(-852, "asteroid_id is required")

    if 'state' not in kwargs:
        return Error(-852, "state is required")

    if kwargs['state'] not in ['started', 'pending', 'finished']:
        return Error(-852, "invalid state")

    if 'start_block' not in kwargs:
        start_block = 1
    else:
        start_block = kwargs['start_block']

    if 'end_block' not in kwargs:
        end_block = 0
    else:
        end_block = kwargs['end_block']

    if 'hours' not in kwargs:
        hours = None
    else:
        hours = kwargs['hours']

    if hours is not None:
        if not hours.isalnum():
            return Error(-1679, "illegal parameter value")

    if not start_block.isalnum():
        return Error(-1679, "illegal parameter value")

    if not end_block.isalnum():
        return Error(-1679, "illegal parameter value")

    if not kwargs['asteroid_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = transit_db.transitFromAsteroid(kwargs['asteroid_id'], kwargs['state'], int(start_block), int(end_block), hours)
    return (Success({"results_len": len(result), "transit": result}))


@method
def transit_to_asteroid(**kwargs):
    print(kwargs)

    if 'asteroid_id' not in kwargs:
        return Error(-852, "asteroid_id is required")

    if 'state' not in kwargs:
        return Error(-852, "state is required")

    if kwargs['state'] not in ['started', 'pending', 'finished']:
        return Error(-852, "invalid state")

    if 'start_block' not in kwargs:
        start_block = 1
    else:
        start_block = kwargs['start_block']

    if 'end_block' not in kwargs:
        end_block = 0
    else:
        end_block = kwargs['end_block']

    if 'hours' not in kwargs:
        hours = None
    else:
        hours = kwargs['hours']

    if hours is not None:
        if not hours.isalnum():
            return Error(-1679, "illegal parameter value")

    if not start_block.isalnum():
        return Error(-1679, "illegal parameter value")

    if not end_block.isalnum():
        return Error(-1679, "illegal parameter value")

    if not kwargs['asteroid_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = transit_db.transitToAsteroid(kwargs['asteroid_id'], kwargs['state'], int(start_block), int(end_block), hours)
    return (Success({"results_len": len(result), "transit": result}))


@method
@token_required
def transit_state_all(**kwargs):
    print(kwargs)

    if 'state' not in kwargs:
        return Error(-852, "state is required")

    if kwargs['state'] not in ['started', 'pending', 'finished']:
        return Error(-852, "invalid state")

    if 'start_block' not in kwargs:
        start_block = 1
    else:
        start_block = kwargs['start_block']

    if 'end_block' not in kwargs:
        end_block = 0
    else:
        end_block = kwargs['end_block']

    if 'hours' not in kwargs:
        hours = None
    else:
        hours = kwargs['hours']

    if hours is not None:
        if not hours.isalnum():
            return Error(-1679, "illegal parameter value")

    if not start_block.isalnum():
        return Error(-1679, "illegal parameter value")

    if not end_block.isalnum():
        return Error(-1679, "illegal parameter value")

    result = transit_db.transitStateAll(kwargs['state'], int(start_block), int(end_block), hours)
    return (Success({"results_len": len(result), "transit": result}))


@method
def buy_orders(**kwargs):
    print(kwargs)

    if 'asteroid_id' not in kwargs:
        asteroid_id = None
    else:
        if not kwargs['asteroid_id'].isalnum():
            return Error(-1679, "illegal parameter value")
        else:
            asteroid_id = kwargs['asteroid_id']

    if 'hours' not in kwargs:
        hours = None
    else:
        if not kwargs['hours'].isalnum():
            return Error(-1679, "illegal parameter value")
        else:
            hours = kwargs['hours']

    if 'state' not in kwargs:
        return Error(-852, "state is required")

    if kwargs['state'] not in ['open', 'filled']:
        return Error(-852, "invalid state")
    else:
        state = kwargs['state']

    result = marketplace_db.buyOrders(asteroid_id, state, hours)
    return (Success({"results_len": len(result), "buy_orders": result}))


@method
def product_buy_orders(**kwargs):
    print(kwargs)

    if 'product_id' not in kwargs:
        return Error(-852, "product_id is required")
    else:
        if not kwargs['product_id'].isalnum():
            return Error(-1679, "illegal parameter value")
        else:
            product_id = kwargs['product_id']

    if 'asteroid_id' not in kwargs:
        asteroid_id = None
    else:
        if not kwargs['asteroid_id'].isalnum():
            return Error(-1679, "illegal parameter value")
        else:
            asteroid_id = kwargs['asteroid_id']

    if 'hours' not in kwargs:
        hours = None
    else:
        if not kwargs['hours'].isalnum():
            return Error(-1679, "illegal parameter value")
        else:
            hours = kwargs['hours']

    if 'state' not in kwargs:
        return Error(-852, "state is required")

    if kwargs['state'] not in ['open', 'filled']:
        return Error(-852, "invalid state")
    else:
        state = kwargs['state']

    result = marketplace_db.productBuyOrders(asteroid_id, state, hours, product_id)
    return (Success({"results_len": len(result), "buy_orders": result}))


@method
def sell_orders(**kwargs):
    print(kwargs)

    if 'asteroid_id' not in kwargs:
        asteroid_id = None
    else:
        if not kwargs['asteroid_id'].isalnum():
            return Error(-1679, "illegal parameter value")
        else:
            asteroid_id = kwargs['asteroid_id']

    if 'hours' not in kwargs:
        hours = None
    else:
        if not kwargs['hours'].isalnum():
            return Error(-1679, "illegal parameter value")
        else:
            hours = kwargs['hours']

    if 'state' not in kwargs:
        return Error(-852, "state is required")

    if kwargs['state'] not in ['open', 'filled']:
        return Error(-852, "invalid state")
    else:
        state = kwargs['state']

    result = marketplace_db.sellOrders(asteroid_id, state, hours)
    return (Success({"results_len": len(result), "sell_orders": result}))


@method
def product_sell_orders(**kwargs):
    print(kwargs)

    if 'product_id' not in kwargs:
        return Error(-852, "product_id is required")
    else:
        if not kwargs['product_id'].isalnum():
            return Error(-1679, "illegal parameter value")
        else:
            product_id = kwargs['product_id']

    if 'asteroid_id' not in kwargs:
        asteroid_id = None
    else:
        if not kwargs['asteroid_id'].isalnum():
            return Error(-1679, "illegal parameter value")
        else:
            asteroid_id = kwargs['asteroid_id']

    if 'hours' not in kwargs:
        hours = None
    else:
        if not kwargs['hours'].isalnum():
            return Error(-1679, "illegal parameter value")
        else:
            hours = kwargs['hours']

    if 'state' not in kwargs:
        return Error(-852, "state is required")

    if kwargs['state'] not in ['open', 'filled']:
        return Error(-852, "invalid state")
    else:
        state = kwargs['state']

    result = marketplace_db.productSellOrders(asteroid_id, state, hours, product_id)
    return (Success({"results_len": len(result), "sell_orders": result}))


@method
@token_required
def propellant_report(**kwargs):
    print(kwargs)

    if 'start_time' not in kwargs or 'end_time' not in kwargs:
        if 'hours' not in kwargs:
            return Error(-852, "hours is required when start_time and end_time are not passed")
        else:
            start_time = None
            end_time = None
            hours = kwargs['hours']
    else:
        start_time = kwargs['start_time']
        end_time = kwargs['end_time']
        hours = None

    if hours is not None:
        if not hours.isalnum():
            return Error(-1679, "illegal parameter value")

    result = propellant_db.propellantReport(start_time, end_time, hours)
    return (Success({"results_len": len(result), "propellant": result}))


@method
@token_required
def food_report(**kwargs):
    print(kwargs)

    if 'start_time' not in kwargs or 'end_time' not in kwargs:
        if 'hours' not in kwargs:
            return Error(-852, "hours is required when start_time and end_time are not passed")
        else:
            start_time = None
            end_time = None
            hours = kwargs['hours']
    else:
        start_time = kwargs['start_time']
        end_time = kwargs['end_time']
        hours = None

    if hours is not None:
        if not hours.isalnum():
            return Error(-1679, "illegal parameter value")

    result = food_db.foodReport(start_time, end_time, hours)
    return (Success({"results_len": len(result), "food": result}))


@method
def propellant_consumed(**kwargs):
    print(kwargs)

    if 'start_time' not in kwargs or 'end_time' not in kwargs:
        if 'hours' not in kwargs:
            return Error(-852, "hours is required when start_time and end_time are not passed")
        else:
            start_time = None
            end_time = None
            hours = kwargs['hours']
    else:
        start_time = kwargs['start_time']
        end_time = kwargs['end_time']
        hours = None

    if hours is not None:
        if not hours.isalnum():
            return Error(-1679, "illegal parameter value")

    result = propellant_db.propellantConsumed(start_time, end_time, hours)
    return (Success({"results_len": len(result), "propellant_consumed": result}))


@method
def food_consumed(**kwargs):
    print(kwargs)

    if 'start_time' not in kwargs or 'end_time' not in kwargs:
        if 'hours' not in kwargs:
            return Error(-852, "hours is required when start_time and end_time are not passed")
        else:
            start_time = None
            end_time = None
            hours = kwargs['hours']
    else:
        start_time = kwargs['start_time']
        end_time = kwargs['end_time']
        hours = None

    if hours is not None:
        if not hours.isalnum():
            return Error(-1679, "illegal parameter value")

    result = food_db.foodConsumed(start_time, end_time, hours)
    return (Success({"results_len": len(result), "food_consumed": result}))


@method
@token_required
def txn_fees(**kwargs):
    print(kwargs)

    if 'start_time' not in kwargs or 'end_time' not in kwargs:
        if 'hours' not in kwargs:
            return Error(-852, "hours is required when start_time and end_time are not passed")
        else:
            start_time = None
            end_time = None
            hours = kwargs['hours']
    else:
        start_time = kwargs['start_time']
        end_time = kwargs['end_time']
        hours = None

    if hours is not None:
        if not hours.isalnum():
            return Error(-1679, "illegal parameter value")

    if 'all' in kwargs:
        if kwargs['all'].lower() == 'true':
            all_contracts = True
        else:
            all_contracts = False
    else:
        all_contracts = True

    result = txn_db.feesConsumed(start_time, end_time, hours, all_contracts)
    return (Success({"results_len": len(result), "fees": result}))


@method
def general_usage(**kwargs):
    print(kwargs)

    if 'start_time' not in kwargs or 'end_time' not in kwargs:
        if 'hours' not in kwargs:
            return Error(-852, "hours is required when start_time and end_time are not passed")
        else:
            start_time = None
            end_time = None
            hours = kwargs['hours']
    else:
        start_time = kwargs['start_time']
        end_time = kwargs['end_time']
        hours = None

    if hours is not None:
        if not hours.isalnum():
            return Error(-1679, "illegal parameter value")

    result = txn_db.generalUsage(start_time, end_time, hours)
    return (Success({"results_len": len(result), "usage": result}))


@method
@token_required
def txns_by_contract(**kwargs):
    print(kwargs)

    if 'start_time' not in kwargs or 'end_time' not in kwargs:
        if 'hours' not in kwargs:
            return Error(-852, "hours is required when start_time and end_time are not passed")
        else:
            start_time = None
            end_time = None
            hours = kwargs['hours']
    else:
        start_time = kwargs['start_time']
        end_time = kwargs['end_time']
        hours = None

    if hours is not None:
        if not hours.isalnum():
            return Error(-1679, "illegal parameter value")

    result = txn_db.txnsByContract(start_time, end_time, hours)
    return (Success({"results_len": len(result), "txns": result}))


@method
def txns_between_times_v2(**kwargs):
    print(kwargs)

    if 'start_time' not in kwargs or 'end_time' not in kwargs:
        if 'hours' not in kwargs:
            return Error(-852, "hours is required when start_time and end_time are not passed")
        else:
            start_time = None
            end_time = None
            hours = kwargs['hours']
    else:
        start_time = kwargs['start_time']
        end_time = kwargs['end_time']
        hours = None

    if hours is not None:
        if not hours.isalnum():
            return Error(-1679, "illegal parameter value")

    result = txn_db.txnsBetweenTimes(start_time, end_time, hours)
    return (Success({"results_len": len(result), "txns": result}))


@method
@token_required
def txns_between_times(**kwargs):
    print(kwargs)

    if 'start_time' not in kwargs or 'end_time' not in kwargs:
        if 'hours' not in kwargs:
            return Error(-852, "hours is required when start_time and end_time are not passed")
        else:
            start_time = None
            end_time = None
            hours = kwargs['hours']
    else:
        start_time = kwargs['start_time']
        end_time = kwargs['end_time']
        hours = None

    if hours is not None:
        if not hours.isalnum():
            return Error(-1679, "illegal parameter value")

    result = txn_db.txnsBetweenTimes(start_time, end_time, hours)
    return (Success({"results_len": len(result), "txns": result}))


@method
def crewmates_recruited(**kwargs):
    print(kwargs)

    if 'start_time' not in kwargs or 'end_time' not in kwargs:
        if 'hours' not in kwargs:
            return Error(-852, "hours is required when start_time and end_time are not passed")
        else:
            start_time = None
            end_time = None
            hours = kwargs['hours']
    else:
        start_time = kwargs['start_time']
        end_time = kwargs['end_time']
        hours = None

    if hours is not None:
        if not hours.isalnum():
            return Error(-1679, "illegal parameter value")

    result = kpi_db.crewmatesRecruited(start_time, end_time, hours)
    return (Success({"results_len": len(result), "crewmates": result}))


@method
def crews_minted(**kwargs):
    print(kwargs)

    if 'start_time' not in kwargs or 'end_time' not in kwargs:
        if 'hours' not in kwargs:
            return Error(-852, "hours is required when start_time and end_time are not passed")
        else:
            start_time = None
            end_time = None
            hours = kwargs['hours']
    else:
        start_time = kwargs['start_time']
        end_time = kwargs['end_time']
        hours = None

    if hours is not None:
        if not hours.isalnum():
            return Error(-1679, "illegal parameter value")

    result = kpi_db.crewsMinted(start_time, end_time, hours)
    return (Success({"results_len": len(result), "crews": result}))


@method
@token_required
def resources_extracted(**kwargs):
    print(kwargs)

    if 'start_time' not in kwargs or 'end_time' not in kwargs:
        if 'hours' not in kwargs:
            return Error(-852, "hours is required when start_time and end_time are not passed")
        else:
            start_time = None
            end_time = None
            hours = kwargs['hours']
    else:
        start_time = kwargs['start_time']
        end_time = kwargs['end_time']
        hours = None

    if hours is not None:
        if not hours.isalnum():
            return Error(-1679, "illegal parameter value")

    result = kpi_db.resourcesExtracted(start_time, end_time, hours)
    return (Success({"results_len": len(result), "resources": result}))


@method
@token_required
def products_produced(**kwargs):
    print(kwargs)

    if 'start_time' not in kwargs or 'end_time' not in kwargs:
        if 'hours' not in kwargs:
            return Error(-852, "hours is required when start_time and end_time are not passed")
        else:
            start_time = None
            end_time = None
            hours = kwargs['hours']
    else:
        start_time = kwargs['start_time']
        end_time = kwargs['end_time']
        hours = None

    if hours is not None:
        if not hours.isalnum():
            return Error(-1679, "illegal parameter value")

    result = kpi_db.productsProduced(start_time, end_time, hours)
    return (Success({"results_len": len(result), "products": result}))


@method
@token_required
def products_consumed(**kwargs):
    print(kwargs)

    if 'start_time' not in kwargs or 'end_time' not in kwargs:
        if 'hours' not in kwargs:
            return Error(-852, "hours is required when start_time and end_time are not passed")
        else:
            start_time = None
            end_time = None
            hours = kwargs['hours']
    else:
        start_time = kwargs['start_time']
        end_time = kwargs['end_time']
        hours = None

    if hours is not None:
        if not hours.isalnum():
            return Error(-1679, "illegal parameter value")

    result = kpi_db.productsConsumed(start_time, end_time, hours)
    return (Success({"results_len": len(result), "products": result}))


@method
def global_crews_per_asteroid(**kwargs):
    print(kwargs)
    result = global_db.globalCrewsPerAsteroid()
    return (Success({"results_len": len(result), "global": result}))


@method
def global_buildings(**kwargs):
    print(kwargs)
    result = global_db.globalBuildings()
    return (Success({"results_len": len(result), "global": result}))


@method
def global_ships_assembled(**kwargs):
    print(kwargs)
    result = global_db.globalShipsAssembled()
    return (Success({"results_len": len(result), "global": result}))


@method
def global_tonnes_extracted(**kwargs):
    print(kwargs)
    result = global_db.globalTonnesExtracted()
    return (Success({"results_len": len(result), "global": result}))


@method
def global_crews_composed(**kwargs):
    print(kwargs)
    result = global_db.globalCrewsComposed()
    return (Success({"results_len": len(result), "global": result}))

@method
def global_core_samples(**kwargs):
    print(kwargs)
    result = global_db.globalCoreSamples()
    return (Success({"results_len": len(result), "global": result}))


@method
def global_propellant_produced(**kwargs):
    print(kwargs)
    result = global_db.globalPropellant()
    return (Success({"results_len": len(result), "global": result}))


@method
def global_food_produced(**kwargs):
    print(kwargs)
    result = global_db.globalFood()
    return (Success({"results_len": len(result), "global": result}))


@method
def global_buildings_on_asteroid(**kwargs):
    print(kwargs)

    if 'asteroid_id' not in kwargs:
        return Error(-852, "asteroid_id is required")

    if not kwargs['asteroid_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = global_db.globalBuildingsOnAsteroid(kwargs['asteroid_id'])
    return (Success({"results_len": len(result), "global": result}))


@method
@token_required
def solo_missions(**kwargs):
    print(kwargs)
    if 'wallet' not in kwargs:
        return Error(-852, "wallet is required")

    result = solo_db.soloMissionsSummary(kwargs['wallet'])
    return (Success({"results_len": len(result), "result": result}))


@method
@token_required
def solo_missions_v2(**kwargs):
    print(kwargs)
    if 'wallet' not in kwargs:
        return Error(-852, "wallet is required")

    result = solo_db_v2.soloMissionsSummary(kwargs['wallet'])
    return (Success({"results_len": len(result), "result": result}))


@method
@token_required
def community_missions(**kwargs):
    print(kwargs)
    if 'wallet' not in kwargs:
        return Error(-852, "wallet is required")

    result = community_db.communityMissionsSummary(kwargs['wallet'])
    return (Success({"results_len": len(result), "result": result}))


@method
def colonization_missions(**kwargs):
    print(kwargs)
    if 'wallet' not in kwargs:
        return Error(-852, "wallet is required")

    result = colonization_db.colonizationMissionsSummary(kwargs['wallet'])
    return (Success({"results_len": len(result), "result": result}))


@method
def colonization_report(**kwargs):
    print(kwargs)
    result = colonization_db.colonizationGlobalReport()
    return (Success({"results_len": len(result), "result": result}))


@method
def colonization_asteroid_status(**kwargs):
    print(kwargs)
    if 'asteroid_id' not in kwargs:
        return Error(-852, "asteroid_id is required")

    result = colonization_db.colonizationAsteroidStatus(kwargs['asteroid_id'])
    return (Success({"results_len": len(result), "result": result}))


@method
@token_required
def wallet_leases(**kwargs):
    print(kwargs)
    if 'wallet' not in kwargs:
        return Error(-852, "wallet is required")

    result = policies_db.walletLeases(kwargs['wallet'])
    return (Success({"results_len": len(result), "result": result}))


@method
@token_required
def all_products(**kwargs):
    print(kwargs)
    result = productbot_db.allProducts()
    return (Success({"results_len": len(result), "result": result}))


@method
@token_required
def product_categories(**kwargs):
    print(kwargs)
    result=({"id": 1, "category_name": "Raw Materials"}, {"id": 2, "category_name": "Refined Materials"}, {"id": 3, "category_name": "Refined Metals"}, {"id": 4, "category_name": "Components"}, {"id": 5, "category_name": "Ship Components"}, {"id": 6, "category_name": "Finished Goods"}, {"id": 7, "category_name": "Ships"}, {"id": 8, "category_name": "Buildings"})
    return (Success({"results_len": len(result), "result": result}))


@method
@token_required
def products_by_category(**kwargs):
    print(kwargs)
    if 'category_id' not in kwargs:
        return Error(-852, "category_id is required")

    if not kwargs['category_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = productbot_db.productsByCategory(kwargs['category_id'])
    return (Success({"results_len": len(result), "result": result}))


@method
@token_required
def get_chain(**kwargs):
    print(kwargs)
    if 'product_id' not in kwargs:
        return Error(-852, "product_id is required")

    if not kwargs['product_id'].isalnum():
        return Error(-1679, "illegal parameter value")

    result = productbot_db.getChain(kwargs['product_id'])
    return (Success({"results_len": len(result), "result": result}))


@method
@token_required
def solo_dashboard(**kwargs):
    print(kwargs)
    if 'wallet' not in kwargs:
        return Error(-852, "wallet is required")

    result = solo_dashboard_db.walletState(kwargs['wallet'])
    return (Success({"results_len": len(result), "result": result}))


@method
@token_required
def ship_dashboard(**kwargs):
    print(kwargs)
    result = ship_dashboard_db.shipDashboard()
    return (Success({"results_len": len(result), "result": result}))


@method
@token_required
def solo_crew(**kwargs):
    print(kwargs)
    if 'wallet' not in kwargs:
        return Error(-852, "wallet is required")

    result = solo_dashboard_db.crew(kwargs['wallet'])
    return (Success({"results_len": len(result), "result": result}))


@method
@token_required
def solo_pending_actions(**kwargs):
    print(kwargs)
    if 'wallet' not in kwargs:
        return Error(-852, "wallet is required")

    result = solo_dashboard_db.crewPendingActions(kwargs['wallet'])
    return (Success({"results_len": len(result), "result": result}))


@method
@token_required
def solo_pending_extractions(**kwargs):
    print(kwargs)
    if 'wallet' not in kwargs:
        return Error(-852, "wallet is required")

    result = solo_dashboard_db.crewPendingExtractions(kwargs['wallet'])
    return (Success({"results_len": len(result), "result": result}))


@method
@token_required
def solo_pending_processing(**kwargs):
    print(kwargs)
    if 'wallet' not in kwargs:
        return Error(-852, "wallet is required")

    result = solo_dashboard_db.crewPendingProcessing(kwargs['wallet'])
    return (Success({"results_len": len(result), "result": result}))


@method
@token_required
def solo_pending_deliveries(**kwargs):
    print(kwargs)
    if 'wallet' not in kwargs:
        return Error(-852, "wallet is required")

    result = solo_dashboard_db.crewPendingDeliveries(kwargs['wallet'])
    return (Success({"results_len": len(result), "result": result}))


@method
@token_required
def solo_pending_samples(**kwargs):
    print(kwargs)
    if 'wallet' not in kwargs:
        return Error(-852, "wallet is required")

    result = solo_dashboard_db.crewPendingSamples(kwargs['wallet'])
    return (Success({"results_len": len(result), "result": result}))


@method
@token_required
def solo_pending_construction(**kwargs):
    print(kwargs)
    if 'wallet' not in kwargs:
        return Error(-852, "wallet is required")

    result = solo_dashboard_db.crewPendingConstruction(kwargs['wallet'])
    return (Success({"results_len": len(result), "result": result}))


@method
@token_required
def solo_pending_transit(**kwargs):
    print(kwargs)
    if 'wallet' not in kwargs:
        return Error(-852, "wallet is required")

    result = solo_dashboard_db.crewPendingTransit(kwargs['wallet'])
    return (Success({"results_len": len(result), "result": result}))


@method
@token_required
def solo_pending_ship_assembly(**kwargs):
    print(kwargs)
    if 'wallet' not in kwargs:
        return Error(-852, "wallet is required")

    result = solo_dashboard_db.crewPendingShipAssembly(kwargs['wallet'])
    return (Success({"results_len": len(result), "result": result}))


@method
@token_required
def solo_completed_actions(**kwargs):
    print(kwargs)
    if 'wallet' not in kwargs:
        return Error(-852, "wallet is required")

    result = solo_dashboard_db.crewCompletedActions(kwargs['wallet'])
    return (Success({"results_len": len(result), "result": result}))


@method
@token_required
def solo_buildings(**kwargs):
    print(kwargs)
    if 'wallet' not in kwargs:
        return Error(-852, "wallet is required")

    result = solo_dashboard_db.crewBuildings(kwargs['wallet'])
    return (Success({"results_len": len(result), "result": result}))


@method
@token_required
def solo_ships(**kwargs):
    print(kwargs)
    if 'wallet' not in kwargs:
        return Error(-852, "wallet is required")

    result = solo_dashboard_db.crewShips(kwargs['wallet'])
    return (Success({"results_len": len(result), "result": result}))


@method
@token_required
def solo_marketplace(**kwargs):
    print(kwargs)
    if 'wallet' not in kwargs:
        return Error(-852, "wallet is required")

    result = solo_dashboard_db.marketplace(kwargs['wallet'])
    return (Success({"results_len": len(result), "result": result}))


@app.route("/", methods=["POST","OPTIONS"])
def index():
    return Response(
        dispatch(request.get_data().decode()), content_type="application/json"
    )


if __name__ == "__main__":
    app.run()
