import sys
import os
import pymysql
import warnings
import traceback
import configparser
import time
from . import get_types

filename = __file__
config_path = filename.split('/')[3]
config_file = "/home/bios/" + config_path + "/api.conf"

if os.path.exists(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    db_user = config.get('credentials', 'db_user')
    db_password = config.get('credentials', 'db_password')
    db = config.get('credentials', 'db')
else:
    raise Exception(config_file)


def getCrewmateOwner(con, crewmate_id):

    crewmate_owner = {}
    sql = ("SELECT crewmate_owner, crew_id FROM crewmates WHERE crewmate_id = %s" % crewmate_id)
    print(sql)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        crewmate_owner=result[0]
        crew_id=result[1]
        cur.close()

    crewmate_owner = {"crewmate_id": crewmate_id, "owner": crewmate_owner, "crew_id": crew_id}
    return crewmate_owner


def getCrewmateTraits(con, crewmate_id):

    traits = []
    sql = ("SELECT trait_id FROM crewmate_traits_set WHERE crewmate_id = %s" % crewmate_id)
    print(sql)

    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return traits

    for row in rows:
        trait_id=row[0]
        trait_name = get_types.getCrewTraitTypes(int(trait_id))
        traits.append(trait_name)

    return traits


def getCrewOwner(con, crew_id):

    owner = None
    sql = ("SELECT crew_owner FROM crews WHERE crew_id = %s" % crew_id)
    print(sql)

    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        cur.close()

    if result == None:
        return None
    else:
        owner=result[0]

    return owner


def getCrewmateName(con, crewmate_id):

    name = None
    sql = ("SELECT name FROM crewmates WHERE crewmate_id = %s ORDER BY block_number DESC LIMIT 1" % crewmate_id)
    print(sql)

    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        result = cur.fetchone()
        cur.close()

    if result == None:
        return None
    else:
        name=result[0]

    return name


def getOwnedCrewmates(con, wallet):

    crewmates=[]
    sql = ("SELECT crewmate_id, crewmate_owner, name, collection, class, title, crew_id, impactful_1, impactful_2, impactful_3, impactful_4, impactful_5, impactful_6 FROM crewmates WHERE crewmate_owner = '%s'" % (wallet))
    print(sql)

    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return crewmates

    for row in rows:
        crewmate_id=row[0]
        owner=row[1]
        name = row[2]
        collection = row[3]
        collection = get_types.getCrewCollectionTypes(collection)
        class_name = row[4]
        class_name = get_types.getClassTypes(class_name)
        title = row[5]
        title = get_types.getTitleTypes(title)
        crew_id = row[6]
        traits=(row[7], row[8], row[9], row[10], row[11], row[12])
        traits = resolveTraits(traits)
        crewmates.append({"crewmate_id": crewmate_id, "owner": owner, "name": name, "collection": collection, "class": class_name, "title": title, "crew_id": crew_id, "traits": traits})

    return crewmates


def getCrewmates(con, crew_id):

    crewmates=[]
    sql = ("SELECT crewmate_id, crewmate_owner, name, collection, class, title, impactful_1, impactful_2, impactful_3, impactful_4, impactful_5, impactful_6 FROM crewmates WHERE crew_id = %s" % (crew_id))
    print(sql)

    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return crewmates

    for row in rows:
        crewmate_id=row[0]
        owner=row[1]
        name=row[2]
        collection=row[3]
        collection = get_types.getCrewCollectionTypes(collection)
        class_name=row[4]
        class_name=get_types.getClassTypes(class_name)
        title=row[5]
        title = get_types.getTitleTypes(title)
        traits=(row[6], row[7], row[8], row[9], row[10], row[11])
        traits = resolveTraits(traits)
        crewmates.append({"crewmate_id": crewmate_id, "owner": owner, "name": name, "collection": collection, "class": class_name, "title": title, "traits": traits})

    return crewmates


def resolveTraits(traits):

    traits_arr = []
    for element in traits:
        if element is not None:
            trait_name = get_types.getCrewTraitTypes(element)
            traits_arr.append(trait_name)
        else:
            trait_name = None

    return traits_arr


def getOwnedCrew(con, wallet):

    crew=[]
    sql = ("SELECT crew_id, name, crew_owner FROM crews WHERE crew_owner = '%s'" % (wallet))
    print(sql)

    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return crew

    for row in rows:
        crew_id=row[0]
        crew_name=row[1]
        crew_owner=row[2]
        crewmates = getCrewmates(con, crew_id)
        crew.append({"crew_id": crew_id, "crew_name": crew_name, "crewmates": crewmates})

    return crew


def getCrew(con, crew_id):

    sql = ("SELECT name, crew_owner FROM crews WHERE crew_id = %s" % crew_id)
    print(sql)

    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return None, None

    for row in rows:
        crew_name=row[0]
        crew_owner=row[1]

    return crew_name, crew_owner


def getCrewmate(con, crewmate_id):

    crewmate = {}

    sql = ("SELECT crewmate_id, crewmate_owner, name, collection, class, title, crew_id, impactful_1, impactful_2, impactful_3, impactful_4, impactful_5, impactful_6 FROM crewmates WHERE crewmate_id = %s" % (crewmate_id))
    print(sql)

    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return crewmate

    for row in rows:
        print(row)
        crewmate_id=row[0]
        owner=row[1]
        name=row[2]
        collection=row[3]
        collection = get_types.getCrewCollectionTypes(collection)
        class_name=row[4]
        class_name=get_types.getClassTypes(class_name)
        title=row[5]
        title = get_types.getTitleTypes(title)
        crew_id=row[6]
        traits=(row[7], row[8], row[9], row[10], row[11], row[12])
        traits = resolveTraits(traits)

        crewmate = {"crewmate_id": crewmate_id, "owner": owner, "name": name, "collection": collection, "class": class_name, "title": title, "crew_id": crew_id, "traits": traits}

    return crewmate


def crewComposition(crew_id):

    crew=[]
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    crew_name, crew_owner = getCrew(con, crew_id)
    crewmates = getCrewmates(con, crew_id)
    crew.append({"crew_id": crew_id, "crew_name": crew_name, "crew_owner": crew_owner, "crewmates": crewmates})
    con.close()
    return crew


def crewOwner(crew_id):

    crew_owner = None
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    crew_owner = getCrewOwner(con, crew_id)
    con.close()
    return crew_owner


def crewmateOwner(crewmate_id):

    crewmate_owner = None
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    crewmate_owner = getCrewmateOwner(con, crewmate_id)
    con.close()
    return crewmate_owner


def ownedCrewmates(wallet):

    owned_crewmates = None
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    owned_crewmates = getOwnedCrewmates(con, wallet)
    con.close()
    return owned_crewmates


def ownedCrew(wallet):

    owned_crew = None
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    owned_crew = getOwnedCrew(con, wallet)
    con.close()
    return owned_crew


def crewmate(crewmate_id):

    crewmate = {}
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    crewmate = getCrewmate(con, crewmate_id)
    con.close()
    return crewmate


def crew(crew_id):

    crew = {}
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    crew = getCrew(con, crew_id)
    con.close()
    return crew

