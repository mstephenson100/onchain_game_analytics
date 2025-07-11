#!/usr/bin/python3

IDS = {
    'CREW': 1,
    'CREWMATE': 2,
    'ASTEROID': 3,
    'LOT': 4,
    'BUILDING': 5,
    'SHIP': 6,
    'DEPOSIT': 7,
    'ORDER': 8,
    'DELIVERY': 9
}

TYPES = {
    IDS['CREW']: {'label': 'CREW'},
    IDS['CREWMATE']: {'label': 'CREWMATE'},
    IDS['ASTEROID']: {'label': 'ASTEROID'},
    IDS['LOT']: {'label': 'LOT'},
    IDS['BUILDING']: {'label': 'BUILDING'},
    IDS['SHIP']: {'label': 'SHIP'},
    IDS['DEPOSIT']: {'label': 'DEPOSIT'},
    IDS['ORDER']: {'label': 'ORDER'},
    IDS['DELIVERY']: {'label': 'DELIVERY'}
}

def unpackLot(entity_id):
    entity = format_entity(entity_id)
    if entity['label'] != IDS['LOT']:
        raise ValueError('Invalid entity label')

    split = 2 ** 32

    return {
        'asteroidId': entity['id'] % split,
        'lotIndex': entity['id'] // split
    }

def format_entity(entity_id):
    # Implement the logic to format the entity if needed
    # For now, assuming it's a dictionary
    return {'id': entity_id, 'label': IDS['LOT']}
    #return entity_id, IDS['LOT']

