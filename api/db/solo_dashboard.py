import sys
import os
import pymysql
import warnings
import traceback
import configparser
import time
from datetime import datetime
import db.fix_address as fix_address
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


def parseBuildingType(building_type):

    if building_type == 1:
        building_type = 'warehouse'

    if building_type == 2:
        building_type = 'extractor'

    if building_type == 3:
        building_type = 'refinery'

    if building_type == 4:
        building_type = 'bioreactor'

    if building_type == 5:
        building_type = 'factory'

    if building_type == 6:
        building_type = 'shipyard'

    if building_type == 7:
        building_type = 'spaceport'

    if building_type == 8:
        building_type = 'marketplace'

    if building_type == 9:
        building_type = 'habitat'

    return building_type


def parseShipType(ship_type):

    if ship_type == 1:
        ship_type = 'Escape Module'

    if ship_type == 2:
        ship_type = 'Light Transport'

    if ship_type == 3:
        ship_type = 'Heavy Transport'

    if ship_type == 4:
        ship_type = 'Shuttle'

    return ship_type


def parseProductType(product_id):

    products=[{"id": 1, "name": "WATER"},
    {"id": 1, "name": "WATER"},
    {"id": 2, "name": "HYDROGEN"},
    {"id": 3, "name": "AMMONIA"},
    {"id": 4, "name": "NITROGEN"},
    {"id": 5, "name": "SULFUR_DIOXIDE"},
    {"id": 6, "name": "CARBON_DIOXIDE"},
    {"id": 7, "name": "CARBON_MONOXIDE"},
    {"id": 8, "name": "METHANE"},
    {"id": 9, "name": "APATITE"},
    {"id": 10, "name": "BITUMEN"},
    {"id": 11, "name": "CALCITE"},
    {"id": 12, "name": "FELDSPAR"},
    {"id": 13, "name": "OLIVINE"},
    {"id": 14, "name": "PYROXENE"},
    {"id": 15, "name": "COFFINITE"},
    {"id": 16, "name": "MERRILLITE"},
    {"id": 17, "name": "XENOTIME"},
    {"id": 18, "name": "RHABDITE"},
    {"id": 19, "name": "GRAPHITE"},
    {"id": 20, "name": "TAENITE"},
    {"id": 21, "name": "TROILITE"},
    {"id": 22, "name": "URANINITE"},
    {"id": 23, "name": "OXYGEN"},
    {"id": 24, "name": "DEIONIZED_WATER"},
    {"id": 25, "name": "SALTS"},
    {"id": 26, "name": "SILICA"},
    {"id": 27, "name": "NAPHTHA"},
    {"id": 28, "name": "SODIUM_BICARBONATE"},
    {"id": 29, "name": "IRON"},
    {"id": 30, "name": "COPPER"},
    {"id": 31, "name": "NICKEL"},
    {"id": 32, "name": "QUICKLIME"},
    {"id": 33, "name": "ACETYLENE"},
    {"id": 34, "name": "AMMONIUM_CARBONATE"},
    {"id": 35, "name": "TRIPLE_SUPERPHOSPHATE"},
    {"id": 36, "name": "PHOSPHATE_AND_SULFATE_SALTS"},
    {"id": 37, "name": "IRON_SULFIDE"},
    {"id": 38, "name": "LEAD_SULFIDE"},
    {"id": 39, "name": "TIN_SULFIDE"},
    {"id": 40, "name": "MOLYBDENUM_DISULFIDE"},
    {"id": 41, "name": "FUSED_QUARTZ"},
    {"id": 42, "name": "FIBERGLASS"},
    {"id": 43, "name": "BARE_COPPER_WIRE"},
    {"id": 44, "name": "CEMENT"},
    {"id": 45, "name": "SODIUM_CHLORIDE"},
    {"id": 46, "name": "POTASSIUM_CHLORIDE"},
    {"id": 47, "name": "BORAX"},
    {"id": 48, "name": "LITHIUM_CARBONATE"},
    {"id": 49, "name": "MAGNESIUM_CHLORIDE"},
    {"id": 50, "name": "PROPYLENE"},
    {"id": 51, "name": "SULFUR"},
    {"id": 52, "name": "STEEL"},
    {"id": 53, "name": "SILICON"},
    {"id": 54, "name": "NITRIC_ACID"},
    {"id": 55, "name": "SULFURIC_ACID"},
    {"id": 56, "name": "SOIL"},
    {"id": 57, "name": "FERROSILICON"},
    {"id": 58, "name": "WEATHERED_OLIVINE"},
    {"id": 59, "name": "OXALIC_ACID"},
    {"id": 60, "name": "SILVER"},
    {"id": 61, "name": "GOLD"},
    {"id": 62, "name": "TIN"},
    {"id": 63, "name": "IRON_OXIDE"},
    {"id": 64, "name": "SPIRULINA_AND_CHLORELLA_ALGAE"},
    {"id": 65, "name": "MOLYBDENUM_TRIOXIDE"},
    {"id": 66, "name": "SILICA_POWDER"},
    {"id": 67, "name": "SOLDER"},
    {"id": 68, "name": "FIBER_OPTIC_CABLE"},
    {"id": 69, "name": "STEEL_BEAM"},
    {"id": 70, "name": "STEEL_SHEET"},
    {"id": 71, "name": "STEEL_PIPE"},
    {"id": 72, "name": "STEEL_WIRE"},
    {"id": 73, "name": "ACRYLONITRILE"},
    {"id": 74, "name": "POLYPROPYLENE"},
    {"id": 75, "name": "MAGNESIUM"},
    {"id": 76, "name": "CHLORINE"},
    {"id": 77, "name": "SODIUM_CARBONATE"},
    {"id": 78, "name": "CALCIUM_CHLORIDE"},
    {"id": 79, "name": "BORIA"},
    {"id": 80, "name": "LITHIUM_SULFATE"},
    {"id": 81, "name": "HYDROCHLORIC_ACID"},
    {"id": 82, "name": "HYDROFLUORIC_ACID"},
    {"id": 83, "name": "PHOSPHORIC_ACID"},
    {"id": 84, "name": "BORIC_ACID"},
    {"id": 85, "name": "ZINC_OXIDE"},
    {"id": 86, "name": "NICKEL_OXIDE"},
    {"id": 87, "name": "MAGNESIA"},
    {"id": 88, "name": "ALUMINA"},
    {"id": 89, "name": "SODIUM_HYDROXIDE"},
    {"id": 90, "name": "POTASSIUM_HYDROXIDE"},
    {"id": 91, "name": "SOYBEANS"},
    {"id": 92, "name": "POTATOES"},
    {"id": 93, "name": "AMMONIUM_OXALATE"},
    {"id": 94, "name": "RARE_EARTH_SULFATES"},
    {"id": 95, "name": "FERROCHROMIUM"},
    {"id": 96, "name": "YELLOWCAKE"},
    {"id": 97, "name": "ALUMINA_CERAMIC"},
    {"id": 98, "name": "AUSTENITIC_NICHROME"},
    {"id": 99, "name": "COPPER_WIRE"},
    {"id": 100, "name": "SILICON_WAFER"},
    {"id": 101, "name": "STEEL_CABLE"},
    {"id": 102, "name": "POLYACRYLONITRILE"},
    {"id": 103, "name": "NATURAL_FLAVORINGS"},
    {"id": 104, "name": "PLATINUM"},
    {"id": 105, "name": "LITHIUM_CHLORIDE"},
    {"id": 106, "name": "ZINC"},
    {"id": 107, "name": "EPICHLOROHYDRIN"},
    {"id": 108, "name": "BISPHENOL_A"},
    {"id": 109, "name": "RARE_EARTH_OXIDES"},
    {"id": 110, "name": "AMMONIUM_CHLORIDE"},
    {"id": 111, "name": "ALUMINIUM"},
    {"id": 112, "name": "CALCIUM"},
    {"id": 113, "name": "SODIUM_CHROMATE"},
    {"id": 114, "name": "LEACHED_COFFINITE"},
    {"id": 115, "name": "URANYL_NITRATE"},
    {"id": 116, "name": "FLUORINE"},
    {"id": 117, "name": "SODIUM_TUNGSTATE"},
    {"id": 118, "name": "FERRITE"},
    {"id": 119, "name": "DIODE"},
    {"id": 120, "name": "LASER_DIODE"},
    {"id": 121, "name": "BALL_VALVE"},
    {"id": 122, "name": "ALUMINIUM_BEAM"},
    {"id": 123, "name": "ALUMINIUM_SHEET"},
    {"id": 124, "name": "ALUMINIUM_PIPE"},
    {"id": 125, "name": "POLYACRYLONITRILE_FABRIC"},
    {"id": 126, "name": "COLD_GAS_THRUSTER"},
    {"id": 127, "name": "COLD_GAS_TORQUE_THRUSTER"},
    {"id": 128, "name": "CARBON_FIBER"},
    {"id": 129, "name": "FOOD"},
    {"id": 130, "name": "SMALL_PROPELLANT_TANK"},
    {"id": 131, "name": "BOROSILICATE_GLASS"},
    {"id": 132, "name": "BALL_BEARING"},
    {"id": 133, "name": "LARGE_THRUST_BEARING"},
    {"id": 134, "name": "BORON"},
    {"id": 135, "name": "LITHIUM"},
    {"id": 136, "name": "EPOXY"},
    {"id": 137, "name": "NEODYMIUM_OXIDE"},
    {"id": 138, "name": "YTTRIA"},
    {"id": 139, "name": "SODIUM_DICHROMATE"},
    {"id": 140, "name": "NOVOLAK_PREPOLYMER_RESIN"},
    {"id": 141, "name": "FERROMOLYBDENUM"},
    {"id": 142, "name": "AMMONIUM_DIURANATE"},
    {"id": 143, "name": "AMMONIUM_PARATUNGSTATE"},
    {"id": 144, "name": "ENGINE_BELL"},
    {"id": 145, "name": "STEEL_TRUSS"},
    {"id": 146, "name": "ALUMINIUM_HULL_PLATE"},
    {"id": 147, "name": "ALUMINIUM_TRUSS"},
    {"id": 148, "name": "CARGO_MODULE"},
    {"id": 149, "name": "PRESSURE_VESSEL"},
    {"id": 150, "name": "PROPELLANT_TANK"},
    {"id": 151, "name": "STAINLESS_STEEL"},
    {"id": 152, "name": "BARE_CIRCUIT_BOARD"},
    {"id": 153, "name": "FERRITE_BEAD_INDUCTOR"},
    {"id": 154, "name": "CORE_DRILL_SAMPLER"},
    {"id": 155, "name": "CORE_DRILL_THRUSTER"},
    {"id": 156, "name": "PARABOLIC_DISH"},
    {"id": 157, "name": "PHOTOVOLTAIC_PANEL"},
    {"id": 158, "name": "LIPO_BATTERY"},
    {"id": 159, "name": "NEODYMIUM_TRICHLORIDE"},
    {"id": 161, "name": "CHROMIA"},
    {"id": 162, "name": "PHOTORESIST_EPOXY"},
    {"id": 163, "name": "URANIUM_DIOXIDE"},
    {"id": 164, "name": "TUNGSTEN"},
    {"id": 165, "name": "SHUTTLE_HULL"},
    {"id": 166, "name": "LIGHT_TRANSPORT_HULL"},
    {"id": 167, "name": "CARGO_RING"},
    {"id": 168, "name": "HEAVY_TRANSPORT_HULL"},
    {"id": 169, "name": "TUNGSTEN_POWDER"},
    {"id": 170, "name": "HYDROGEN_PROPELLANT"},
    {"id": 171, "name": "STAINLESS_STEEL_SHEET"},
    {"id": 172, "name": "STAINLESS_STEEL_PIPE"},
    {"id": 173, "name": "CCD"},
    {"id": 174, "name": "COMPUTER_CHIP"},
    {"id": 175, "name": "CORE_DRILL"},
    {"id": 176, "name": "NEODYMIUM"},
    {"id": 178, "name": "CHROMIUM"},
    {"id": 179, "name": "URANIUM_TETRAFLUORIDE"},
    {"id": 180, "name": "PURE_NITROGEN"},
    {"id": 181, "name": "ND_YAG_LASER_ROD"},
    {"id": 182, "name": "NICHROME"},
    {"id": 183, "name": "NEODYMIUM_MAGNET"},
    {"id": 184, "name": "UNENRICHED_URANIUM_HEXAFLUORIDE"},
    {"id": 185, "name": "HIGHLY_ENRICHED_URANIUM_HEXAFLUORIDE"},
    {"id": 186, "name": "ND_YAG_LASER"},
    {"id": 187, "name": "THIN_FILM_RESISTOR"},
    {"id": 188, "name": "HIGHLY_ENRICHED_URANIUM_POWDER"},
    {"id": 189, "name": "LEACHED_FELDSPAR"},
    {"id": 190, "name": "ROASTED_RHABDITE"},
    {"id": 191, "name": "RHABDITE_SLAG"},
    {"id": 192, "name": "POTASSIUM_CARBONATE"},
    {"id": 193, "name": "HYDROGEN_HEPTAFLUOROTANTALATE_AND_NIOBATE"},
    {"id": 194, "name": "LEAD"},
    {"id": 195, "name": "POTASSIUM_FLUORIDE"},
    {"id": 196, "name": "POTASSIUM_HEPTAFLUOROTANTALATE"},
    {"id": 197, "name": "DIEPOXY_PREPOLYMER_RESIN"},
    {"id": 199, "name": "TANTALUM"},
    {"id": 200, "name": "PEDOT"},
    {"id": 201, "name": "POLYMER_TANTALUM_CAPACITOR"},
    {"id": 202, "name": "SURFACE_MOUNT_DEVICE_REEL"},
    {"id": 203, "name": "CIRCUIT_BOARD"},
    {"id": 204, "name": "BRUSHLESS_MOTOR_STATOR"},
    {"id": 205, "name": "BRUSHLESS_MOTOR_ROTOR"},
    {"id": 206, "name": "BRUSHLESS_MOTOR"},
    {"id": 207, "name": "LANDING_LEG"},
    {"id": 208, "name": "LANDING_AUGER"},
    {"id": 209, "name": "PUMP"},
    {"id": 210, "name": "RADIO_ANTENNA"},
    {"id": 211, "name": "FIBER_OPTIC_GYROSCOPE"},
    {"id": 212, "name": "STAR_TRACKER"},
    {"id": 213, "name": "COMPUTER"},
    {"id": 214, "name": "CONTROL_MOMENT_GYROSCOPE"},
    {"id": 215, "name": "ROBOTIC_ARM"},
    {"id": 217, "name": "BERYLLIUM_CARBONATE"},
    {"id": 218, "name": "BERYLLIA"},
    {"id": 219, "name": "BERYLLIA_CERAMIC"},
    {"id": 220, "name": "NEON"},
    {"id": 221, "name": "HEAT_EXCHANGER"},
    {"id": 222, "name": "TURBOPUMP"},
    {"id": 224, "name": "NEON_FUEL_SEPARATOR_CENTRIFUGE"},
    {"id": 225, "name": "FUEL_MAKE_UP_TANK"},
    {"id": 226, "name": "NEON_MAKE_UP_TANK"},
    {"id": 227, "name": "LIGHTBULB_END_MODERATORS"},
    {"id": 229, "name": "FUSED_QUARTZ_LIGHTBULB_TUBE"},
    {"id": 230, "name": "REACTOR_PLUMBING_ASSEMBLY"},
    {"id": 231, "name": "FLOW_DIVIDER_MODERATOR"},
    {"id": 232, "name": "NUCLEAR_LIGHTBULB"},
    {"id": 233, "name": "COMPOSITE_OVERWRAPPED_REACTOR_SHELL"},
    {"id": 234, "name": "CLOSED_CYCLE_GAS_CORE_NUCLEAR_REACTOR_ENGINE"},
    {"id": 235, "name": "HABITATION_MODULE"},
    {"id": 236, "name": "MOBILITY_MODULE"},
    {"id": 237, "name": "FLUIDS_AUTOMATION_MODULE"},
    {"id": 238, "name": "SOLIDS_AUTOMATION_MODULE"},
    {"id": 239, "name": "TERRAIN_INTERFACE_MODULE"},
    {"id": 240, "name": "AVIONICS_MODULE"},
    {"id": 241, "name": "ESCAPE_MODULE"},
    {"id": 242, "name": "ATTITUDE_CONTROL_MODULE"},
    {"id": 243, "name": "POWER_MODULE"},
    {"id": 244, "name": "THERMAL_MODULE"},
    {"id": 245, "name": "PROPULSION_MODULE"}]

    for row in products:
        if row['id'] == product_id:
            product_type = row['name']

    return product_type


def getPendingCrew(con, wallet):

    crews = []
    crew_list = []
    crew_sql = ("SELECT b.crew_id, b.name, b.station_id, b.station_label, c.asteroid_id, c.lot_id FROM crews b, stations c WHERE b.station_id = c.station_id AND b.station_label = c.station_label AND b.delegated_address = '%s'" % wallet)

    with con:
        cur = con.cursor()
        cur.execute("%s" % crew_sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return None

    for row in rows:
        crew_id=row[0]
        crew_name=row[1]
        station_id=row[2]
        station_label=row[3]
        asteroid_id=row[4]
        lot_id=row[5]
        crews.append({"crew_id": crew_id, "crew_name": crew_name, "station_id": station_id, "station_label": station_label, "asteroid_id": asteroid_id, "lot_id": lot_id})
        if crew_id not in crew_list:
            crew_list.append(crew_id)

    return crews, crew_list


def getInventoryAtEntity(con, inventory_label, inventory_id, inventory_type):

    inventory = []
    slot1 = []
    slot2 = []
    resources = []

    sql=("SELECT inventory_slot, resource_id, inventory_amount FROM inventories WHERE inventory_label = %s AND inventory_id = %s AND inventory_amount > 0" % (inventory_label, inventory_id))
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return inventory

    slot_1_value = 0
    slot_2_value = 0
    for row in rows:
        inventory_slot=row[0]
        resource_id=row[1]
        resource_amount=row[2]

        resource_name = parseProductType(resource_id)
        exchange_asteroid_id, exchange_lot_id, price, amount = floor_price = getFloor(con, resource_id)
        resource_value = (resource_amount * price)

        if inventory_label == 6:
            if inventory_slot == 1:
                slot_1_value+=resource_value
                slot1.append({"resource_id": resource_id, "resource_name": resource_name, "resource_amount": resource_amount, "resource_floor_price": price, "resource_value": round(resource_value, 3)})
            elif inventory_slot == 2:
                slot_2_value+=resource_value
                slot2.append({"resource_id": resource_id, "resource_name": resource_name, "resource_amount": resource_amount, "resource_floor_price": price, "resource_value": round(resource_value, 3)})
        else:
            slot_2_value+=resource_value
            slot2.append({"resource_id": resource_id, "resource_name": resource_name, "resource_amount": resource_amount, "resource_floor_price": price, "resource_value": round(resource_value, 2)})


        #resource_name = parseProductType(resource_id)
        #if inventory_label == 5:
        #    resources.append({"resource_id": resource_id, "resource_name": resource_name, "resource_amount": resource_amount})

    if inventory_label == 5:
        inventory.append({"inventory_label": inventory_label, "inventory_type": inventory_type, "inventory_id": inventory_id, "slot_2_value": round(slot_2_value, 2), "slot_2": slot2})
    if inventory_label == 6:
        inventory.append({"inventory_label": inventory_label, "inventory_type": inventory_type, "inventory_id": inventory_id, "slot_1_value": round(slot_1_value, 2), "slot_1": slot1, "slot_2_value": round(slot_2_value, 2), "slot_2": slot2})

    return inventory


#    transit = []
#    transit_sql = ("SELECT start_txn_id, ship_id, ship_type, origin_id, destination_id, departure, arrival, finish_time FROM transit WHERE status = 1 AND crew_id = %s" % crew_id)
#    #print(transit_sql)
#    with con:
#        cur = con.cursor()
#        cur.execute("%s" % transit_sql)
#        rows = cur.fetchall()
#        cur.close()
#
#    if len(rows) == 0:
#        transit = []
#
#    for row in rows:
#        start_txn_id=row[0]
#        ship_id=row[1]
#        ship_type=row[2]
#        origin_id=row[3]
#        destination_id=row[4]
#        departure=row[5]
#        arrival=row[6]
#        finish_time=row[7]
#        transit.append({"start_txn_id": start_txn_id, "ship_id": ship_id, "ship_type": ship_type, "origin_id": origin_id, "destination_id": destination_id, "departure": departure, "arrival": arrival, "finish_time": finish_time})


def getShipTransit(con, ship_id):

    transit = []
    transit_sql = ("SELECT start_txn_id, ship_id, ship_type, origin_id, destination_id, departure, arrival, finish_time FROM transit WHERE status = 1 AND ship_id = %s" % ship_id)
    #print(transit_sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % transit_sql)
        rows = cur.fetchall()
        cur.close()

    if len(rows) == 0:
        transit = []

    for row in rows:
        start_txn_id=row[0]
        ship_id=row[1]
        ship_type=row[2]
        origin_id=row[3]
        destination_id=row[4]
        departure=row[5]
        arrival=row[6]
        finish_time=row[7]
        converted_finish_time = convertFinishTime(finish_time)
        transit.append({"start_txn_id": start_txn_id, "ship_id": ship_id, "ship_type": ship_type, "origin_id": origin_id, "destination_id": destination_id, "departure": departure, "arrival": arrival, "finish_time": finish_time, "remaining_time": converted_finish_time})

    return transit


def getDockedShips(con, crew_id):

    ships=[]

    ship_sql = ("SELECT b.ship_id, b.caller_address, b.ship_type, b.ship_type_name, b.emergency, b.name, c.dock_label, c.dock_type, c.dock_asteroid_id, c.dock_lot_id FROM ships b, ships_docked c WHERE b.crew_id = %s AND b.ship_id = c.ship_id" % crew_id)
    #print(ship_sql)

    with con:
        cur = con.cursor()
        cur.execute("%s" % ship_sql)
        rows = cur.fetchall()
        cur.close()

    #if rows == None:
    #    return ships

    for row in rows:
        #print(row)
        ship_id=row[0]
        owner_address=row[1]
        ship_type=row[2]
        ship_type_name=row[3]
        emergency=row[4]
        ship_name=row[5]
        dock_label=row[6]
        dock_type=row[7]
        dock_asteroid_id=row[8]
        dock_lot_id=row[9]
        ship_label = 6
        inventory = getInventoryAtEntity(con, ship_label, ship_id, ship_type)

        ships.append({"ship_id": ship_id, "ship_name": ship_name, "ship_type": ship_type, "ship_description": ship_type_name, "emergency": emergency, "dock_label": dock_label, "dock_type": dock_type, "dock_asteroid_id": dock_asteroid_id, "dock_lot_id": dock_lot_id, "inventory": inventory})

    return ships


def getTransitShips(con, crew_id):

    ships=[]

    ship_sql = ("SELECT ship_id, caller_address, ship_type, ship_type_name, emergency, name FROM ships WHERE crew_id = %s" % crew_id)
    #print(ship_sql)

    with con:
        cur = con.cursor()
        cur.execute("%s" % ship_sql)
        rows = cur.fetchall()
        cur.close()

    #if rows == None:
    #    return ships

    for row in rows:
        #print(row)
        ship_id=row[0]
        owner_address=row[1]
        ship_type=row[2]
        ship_type_name=row[3]
        emergency=row[4]
        ship_name=row[5]
        ship_label = 6
        #print("working on %s" % ship_id)
        transit = getShipTransit(con, ship_id)
        inventory = getInventoryAtEntity(con, ship_label, ship_id, ship_type)

        ships.append({"ship_id": ship_id, "ship_name": ship_name, "ship_type": ship_type, "ship_description": ship_type_name, "emergency": emergency, "transit_state": transit, "inventory": inventory})

    return ships


def getCrewmateTraits(con, crewmate_id):

    traits = []
    sql = ("SELECT trait_id FROM crewmate_traits_set WHERE crewmate_id = %s" % crewmate_id)
    #print(sql)

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


def getCrewmateName(con, crewmate_id):

    name = None
    sql = ("SELECT name FROM crewmates WHERE crewmate_id = %s ORDER BY block_number DESC LIMIT 1" % crewmate_id)
    #print(sql)

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


def getCrewmates(con, crew_id):

    crewmates=[]
    sql = ("SELECT crewmate_id, crewmate_owner, name, collection, class, title, impactful_1, impactful_2, impactful_3, impactful_4, impactful_5, impactful_6 FROM crewmates WHERE crew_id = %s" % (crew_id))

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
        #traits = resolveTraits(row[6], row[7], row[8], row[9], row[10], row[11])
        traits = resolveTraits(traits)
        #crewmate_name = getCrewmateName(crewmate_id)
        #traits = getCrewmateTraits(con, crewmate_id)
        #name = getCrewmateName(con, crewmate_id)
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


def getCrewPendingActions(con, wallet):

    crew_data = []
    crew_sql = ("SELECT b.crew_id, b.name, b.station_id, b.station_label, c.asteroid_id, c.lot_id FROM crews b, stations c WHERE b.station_id = c.station_id AND b.station_label = c.station_label AND b.delegated_address = '%s'" % wallet)

    with con:
        cur = con.cursor()
        cur.execute("%s" % crew_sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return None

    for row in rows:
        crew_id=row[0]
        crew_name=row[1]
        station_id=row[2]
        station_label=row[3]
        asteroid_id=row[4]
        lot_id=row[5]
        pending_extractions, pending_processing, pending_sampling, pending_delivering, pending_construction, pending_transit, pending_ship_assembly = getPendingActions(con, crew_id)
        pending_actions = {"extractions": pending_extractions, "processing": pending_processing, "sampling": pending_sampling, "deliveries": pending_delivering, "construction": pending_construction, "transit": pending_transit, "ship_assembly": pending_ship_assembly}
        crew_data.append({"crew_id": crew_id, "crew_name": crew_name, "station_id": station_id, "station_label": station_label, "asteroid_id": asteroid_id, "lot_id": lot_id, "pending_actions": pending_actions})

    return crew_data


def getCrewPendingExtractions(con, wallet):

    crew_data = []
    crew_sql = ("SELECT b.crew_id, b.name, b.station_id, b.station_label, c.asteroid_id, c.lot_id FROM crews b, stations c WHERE b.station_id = c.station_id AND b.station_label = c.station_label AND b.delegated_address = '%s'" % wallet)

    with con:
        cur = con.cursor()
        cur.execute("%s" % crew_sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return None

    for row in rows:
        crew_id=row[0]
        crew_name=row[1]
        station_id=row[2]
        station_label=row[3]
        asteroid_id=row[4]
        lot_id=row[5]
        crew_data.append({"crew_id": crew_id, "crew_name": crew_name, "station_id": station_id, "station_label": station_label, "asteroid_id": asteroid_id, "lot_id": lot_id, "pending_extractions": pending_extractions})

    return crew_data



def getFloor(con, product_id):

    exchange_asteroid_id = None
    exchange_lot_id = None
    price = 0
    amount = 0

    sql = ("SELECT exchange_asteroid_id, exchange_lot_id, price, amount FROM sell_orders WHERE product_id = %s AND amount > 0 AND exchange_asteroid_id = 1 ORDER BY price LIMIT 1" % product_id)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    for row in rows:
        exchange_asteroid_id=row[0]
        exchange_lot_id=row[1]
        price=(row[2] / 1000000)
        amount=row[3]

    return exchange_asteroid_id, exchange_lot_id, price, amount


def getCrewCompletedActions(con, wallet):

    crew_data = []
    crew_sql = ("SELECT b.crew_id, b.name, b.station_id, b.station_label, c.asteroid_id, c.lot_id FROM crews b, stations c WHERE b.station_id = c.station_id AND b.station_label = c.station_label AND b.delegated_address = '%s'" % wallet)

    with con:
        cur = con.cursor()
        cur.execute("%s" % crew_sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return None

    for row in rows:
        crew_id=row[0]
        crew_name=row[1]
        station_id=row[2]
        station_label=row[3]
        asteroid_id=row[4]
        lot_id=row[5]
        completed_extractions, completed_processing, completed_sampling, completed_delivering, completed_construction, completed_transit = getCompletedActions(con, crew_id)
        completed_actions = {"extractions": completed_extractions, "processing": completed_processing, "sampling": completed_sampling, "deliveries": completed_delivering, "construction": completed_construction, "transit": completed_transit}
        crew_data.append({"crew_id": crew_id, "crew_name": crew_name, "station_id": station_id, "station_label": station_label, "asteroid_id": asteroid_id, "lot_id": lot_id, "completed_actions": completed_actions})

    return crew_data


def getCrewBuildings(con, wallet):

    crew_data = []
    crew_sql = ("SELECT b.crew_id, b.name, b.station_id, b.station_label, c.asteroid_id, c.lot_id FROM crews b, stations c WHERE b.station_id = c.station_id AND b.station_label = c.station_label AND b.delegated_address = '%s'" % wallet)

    with con:
        cur = con.cursor()
        cur.execute("%s" % crew_sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return None

    for row in rows:
        crew_id=row[0]
        crew_name=row[1]
        station_id=row[2]
        station_label=row[3]
        asteroid_id=row[4]
        lot_id=row[5]
        buildings = getOwnedBuildings(con, crew_id)
        crew_data.append({"crew_id": crew_id, "crew_name": crew_name, "station_id": station_id, "station_label": station_label, "asteroid_id": asteroid_id, "lot_id": lot_id, "buildings": buildings})

    return crew_data


def getCrewMarketplace(con, wallet):

    marketplace_data = []
    concatenated_filled_sell_orders = []
    concatenated_filled_buy_orders = []
    total_sway_earned = 0
    total_sway_spent = 0
    crew_sql = ("SELECT b.crew_id, b.name, b.station_id, b.station_label, c.asteroid_id, c.lot_id FROM crews b, stations c WHERE b.station_id = c.station_id AND b.station_label = c.station_label AND b.delegated_address = '%s'" % wallet)

    with con:
        cur = con.cursor()
        cur.execute("%s" % crew_sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return None

    for row in rows:
        crew_id=row[0]
        crew_name=row[1]
        station_id=row[2]
        station_label=row[3]
        asteroid_id=row[4]
        lot_id=row[5]
        filled_sell_orders, filled_buy_orders = getFilledOrders(con, crew_id)
        for sell_orders in filled_sell_orders:
            total_sway_earned+=sell_orders['total']
            concatenated_filled_sell_orders.append(sell_orders)

        for buy_orders in filled_buy_orders:
            total_sway_spent+=buy_orders['total']
            concatenated_filled_buy_orders.append(buy_orders)

    open_sell_orders, open_buy_orders = getOpenOrders(con, wallet)

    marketplace_data.append({"sway_spent": round(total_sway_spent), "sway_earned": round(total_sway_earned), "filled_sell_orders": concatenated_filled_sell_orders, "filled_buy_orders": concatenated_filled_buy_orders, "open_sell_orders": open_sell_orders, "open_buy_orders": open_buy_orders})

    return marketplace_data


def getCrewShips(con, wallet):

    crew_data = []
    crew_sql = ("SELECT b.crew_id, b.name, b.station_id, b.station_label, c.asteroid_id, c.lot_id FROM crews b, stations c WHERE b.station_id = c.station_id AND b.station_label = c.station_label AND b.delegated_address = '%s'" % wallet)

    with con:
        cur = con.cursor()
        cur.execute("%s" % crew_sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return None

    for row in rows:
        crew_id=row[0]
        crew_name=row[1]
        station_id=row[2]
        station_label=row[3]
        asteroid_id=row[4]
        lot_id=row[5]
        docked_ships = getDockedShips(con, crew_id)
        transit_ships = getTransitShips(con, crew_id)
        crew_data.append({"crew_id": crew_id, "crew_name": crew_name, "station_id": station_id, "station_label": station_label, "asteroid_id": asteroid_id, "lot_id": lot_id, "docked_ships": docked_ships, "in_transit": transit_ships})

    return crew_data


def getFilledOrders(con, crew_id):

    filled_sold_orders = getProductsSold(con, crew_id)
    filled_buy_orders = getProductsPurchased(con, crew_id)

    return filled_sold_orders, filled_buy_orders


def getOpenOrders(con, wallet):

    open_sell_orders = getOpenSellOrders(con, wallet)
    open_buy_orders = getOpenBuyOrders(con, wallet)

    return open_sell_orders, open_buy_orders


def getCrew(con, wallet):

    crew_data = []
    asteroid_list = getAsteroidNames(con)
    crew_sql = ("SELECT b.crew_id, b.name, b.station_id, b.station_label, b.origin_asteroid_id, c.asteroid_id, c.lot_id FROM crews b, stations c WHERE b.station_id = c.station_id AND b.station_label = c.station_label AND b.delegated_address = '%s'" % wallet)

    with con:
        cur = con.cursor()
        cur.execute("%s" % crew_sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return None

    for row in rows:
        crew_id=row[0]
        crew_name=row[1]
        station_id=row[2]
        station_label=row[3]
        origin_asteroid_id=row[4]
        asteroid_id=row[5]
        lot_id=row[6]
        crewmates = getCrewmates(con, crew_id)

        for asteroid_row in asteroid_list:
            if asteroid_row['asteroid_id'] == asteroid_id:
                asteroid_name = asteroid_row['asteroid_name']

        for asteroid_row in asteroid_list:
            if asteroid_row['asteroid_id'] == origin_asteroid_id:
                origin_asteroid_name = asteroid_row['asteroid_name']

        if station_label == 5:
            station_description, station_name = getBuildingStationType(con, station_label, station_id)
        elif station_label == 6:
            station_description, station_name = getShipStationType(con, station_label, station_id)


        crew_data.append({"crew_id": crew_id, "crew_name": crew_name, "station_id": station_id, "station_label": station_label, "station_description": station_description, "station_name": station_name, "lot_id": lot_id, "asteroid_id": asteroid_id, "asteroid_name": asteroid_name, "origin_asteroid_id": origin_asteroid_id, "origin_asteroid_name": origin_asteroid_name, "composition": crewmates})

    return crew_data


def getShipStationType(con, station_label, station_id):

    station_desription = None
    station_name = None
    sql = ("SELECT ship_type, name FROM ships WHERE ship_id = %s" % station_id)
    print(sql)

    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return station_desription, station_name

    for row in rows:
        station_type=row[0]
        station_name=row[1]

    station_description = parseShipType(station_type)
    return station_description, station_name


def getBuildingStationType(con, station_label, station_id):

    station_desription = None
    station_name = None
    sql = ("SELECT building_type, name FROM buildings WHERE building_label = %s AND building_id = %s" % (station_label, station_id))
    print(sql)

    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return station_desription, station_name

    for row in rows:
        station_type=row[0]
        station_name=row[1]

    station_description = parseBuildingType(station_type)
    return station_description, station_name


def getOwnedBuildings(con, crew_id):

    owned_buildings = []
    sql = ("SELECT txn_id, block_number, caller_address, asteroid_id, lot_id, crew_id, building_id, building_type, building_label, name FROM buildings WHERE crew_id = %s AND status = 3" % crew_id)
    #print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return owned_buildings

    for row in rows:
        inventory = []
        txn_id=row[0]
        block_number=row[1]
        owner_address=row[2]
        asteroid_id=row[3]
        lot_id=row[4]
        crew_id=row[5]
        building_id=row[6]
        building_type=row[7]
        building_label=row[8]
        building_name=row[9]
        building_description = parseBuildingType(building_type)
        if building_type == 1:
            inventory = getInventoryAtEntity(con, building_label, building_id, building_type)

        owned_buildings.append({"building_id": building_id, "building_type": building_description, "building_name": building_name, "asteroid_id": asteroid_id, "lot_id": lot_id, "crew_id": crew_id, "wallet": owner_address, "txn_id": txn_id, "block_number": block_number, "inventory": inventory})

    return owned_buildings


def getCompletedActions(con, crew_id):

    extraction_sql = ("SELECT finish_txn_id, resource_name, resource_yield, extractor_id, extractor_asteroid_id, extractor_lot_id, destination_label, destination_type, destination_id, destination_asteroid_id, destination_lot_id, finish_time FROM extractions WHERE status = 2 AND crew_id = %s ORDER BY finish_block_number DESC LIMIT 10" % crew_id)
    extractions = []
    with con:
        cur = con.cursor()
        cur.execute("%s" % extraction_sql)
        rows = cur.fetchall()
        cur.close()

    if len(rows) == 0:
        extractions = []

    for row in rows:
        finish_txn_id=row[0]
        resource_name=row[1]
        resource_yield=round((row[2] / 1000))
        extractor_id=row[3]
        asteroid_id=row[4]
        lot_id=row[5]
        destination_label=row[6]
        destination_type=row[7]
        destination_id=row[8]
        destination_asteroid_id=row[9]
        destination_lot_id=row[10]

        if destination_label == 5:
            destination_description = parseBuildingType(destination_type)
        elif destination_label == 6:
            destination_description = parseShipType(destination_type)

        extractions.append({"finish_txn_id": finish_txn_id, "resource_name": resource_name, "resource_yield": resource_yield, "extractor_id": extractor_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "destination_label": destination_label, "destination_description": destination_description, "destination_id": destination_id, "destination_asteroid_id": destination_asteroid_id, "destination_lot_id": destination_lot_id})

    processing = []
    processing_sql = ("SELECT finish_txn_id, process_name, processor_id, processor_type, processor_asteroid_id, processor_lot_id, destination_id, destination_asteroid_id, destination_lot_id, destination_label, destination_type, finish_time FROM processing_actions WHERE status = 2 AND crew_id = %s ORDER BY finish_block_number DESC LIMIT 10" % crew_id)
    with con:
        cur = con.cursor()
        cur.execute("%s" % processing_sql)
        rows = cur.fetchall()
        cur.close()

    if len(rows) == 0:
        extractions = []

    for row in rows:
        finish_txn_id=row[0]
        process_name=row[1]
        processor_id=row[2]
        processor_type=row[3]
        processor_asteroid_id=row[4]
        processor_lot_id=row[5]
        destination_id=row[6]
        destination_asteroid_id=row[7]
        destination_lot_id=row[8]
        destination_label=row[9]
        destination_type=row[10]
        finish_time=row[10]

        processor_description = parseBuildingType(processor_type)

        if destination_label == 5:
            destination_description = parseBuildingType(destination_type)
        elif destination_label == 6:
            destination_description = parseShipType(destination_type)

        processing.append({"finish_txn_id": finish_txn_id, "process_name": process_name, "processor_id": processor_id, "processor_type": processor_type, "processor_description": processor_description, "processor_asteroid_id": processor_asteroid_id, "processor_lot_id": processor_lot_id, "destination_id": destination_id, "destination_asteroid_id": destination_asteroid_id, "destination_lot_id": destination_lot_id, "destination_label": destination_label, "destination_description": destination_description})


    sampling = []
    sampling_sql = ("SELECT finish_txn_id, deposit_id, asteroid_id, lot_id, resource_name, finish_time, initial_yield FROM core_samples WHERE status = 2 AND crew_id = %s ORDER BY finish_block_number DESC LIMIT 10" % crew_id)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sampling_sql)
        rows = cur.fetchall()
        cur.close()

    if len(rows) == 0:
        sampling = []

    for row in rows:
        finish_txn_id=row[0]
        deposit_id=row[1]
        asteroid_id=row[2]
        lot_id=row[3]
        resource_name=row[4]
        finish_time=row[5]
        initial_yield=row[6]
        sampling.append({"finish_txn_id": finish_txn_id, "deposit_id": deposit_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "resource_name": resource_name, "initial_yield": initial_yield})


    delivering = []
    delivering_sql = ("SELECT finish_txn_id, origin_id, origin_label, origin_type, origin_asteroid_id, origin_lot_id, dest_id, dest_label, dest_type, dest_asteroid_id, dest_lot_id, finish_time, product_name, product_amount FROM deliveries WHERE status = 2 AND crew_id = %s ORDER BY finish_block_number DESC LIMIT 10" % crew_id)
    with con:
        cur = con.cursor()
        cur.execute("%s" % delivering_sql)
        rows = cur.fetchall()
        cur.close()

    if len(rows) == 0:
        delivering = []

    for row in rows:
        finish_txn_id=row[0]
        origin_id=row[1]
        origin_label=row[2]
        origin_type=row[3]
        origin_asteroid_id=row[4]
        origin_lot_id=row[5]
        dest_id=row[6]
        dest_label=row[7]
        dest_type=row[8]
        dest_asteroid_id=row[9]
        dest_lot_id=row[10]
        finish_time=row[11]
        product_name=row[12]
        product_amount=row[13]

        if origin_label == 5:
            origin_description = parseBuildingType(origin_type)
        elif origin_label == 6:
            origin_description = parseShipType(origin_type)

        if dest_label == 5:
            dest_description = parseBuildingType(dest_type)
        elif dest_label == 6:
            dest_description = parseShipType(dest_type)

        delivering.append({"finish_txn_id": finish_txn_id, "origin_id": origin_id, "origin_label": origin_label, "origin_description": origin_description, "origin_asteroid_id": origin_asteroid_id, "origin_lot_id": origin_lot_id, "destination_id": dest_id, "destination_label": dest_label, "destination_description": dest_description, "destination_asteroid_id": dest_asteroid_id, "destination_lot_id": dest_lot_id, "product_name": product_name, "product_amount": product_amount})


    construction = []
    construction_sql = ("SELECT finish_txn_id, building_type, building_id, asteroid_id, lot_id, finish_time FROM construction WHERE status = 2 AND crew_id = %s ORDER BY finish_block_number DESC LIMIT 10" % crew_id)
    with con:
        cur = con.cursor()
        cur.execute("%s" % construction_sql)
        rows = cur.fetchall()
        cur.close()

    if len(rows) == 0:
        construction = []

    for row in rows:
        finish_txn_id=row[0]
        building_type=row[1]
        building_id=row[2]
        asteroid_id=row[3]
        lot_id=row[4]
        finish_time=row[5]

        building_description = parseBuildingType(building_type)

        construction.append({"finish_txn_id": finish_txn_id, "building_type": building_type, "building_description": building_description, "building_id": building_id, "asteroid_id": asteroid_id, "lot_id": lot_id})


    transit = []
    transit_sql = ("SELECT finish_txn_id, ship_id, ship_type, origin_id, destination_id, departure, arrival, finish_time FROM transit WHERE status = 2 AND crew_id = %s ORDER BY finish_block_number DESC LIMIT 10" % crew_id)
    with con:
        cur = con.cursor()
        cur.execute("%s" % transit_sql)
        rows = cur.fetchall()
        cur.close()

    if len(rows) == 0:
        transit = []

    for row in rows:
        finish_txn_id=row[0]
        ship_id=row[1]
        ship_type=row[2]
        origin_id=row[3]
        destination_id=row[4]
        departure=row[5]
        arrival=row[6]
        finish_time=row[7]
        transit.append({"finish_txn_id": finish_txn_id, "ship_id": ship_id, "ship_type": ship_type, "origin_id": origin_id, "destination_id": destination_id, "departure": departure, "arrival": arrival})

    return extractions, processing, sampling, delivering, construction, transit


def getPendingExtractions(con, wallet):

    crews, crew_list = getPendingCrew(con, wallet)
    extractions_crew = []
    extractions = []
    for crew_row in crews:
        crew_id = crew_row['crew_id']
        crew_name = crew_row['crew_name']
        station_id = crew_row['station_id']
        station_label = crew_row['station_label']
        asteroid_id = crew_row['asteroid_id']
        lot_id = crew_row['lot_id']

        extraction_sql = ("SELECT start_txn_id, start_timestamp, resource_name, resource_yield, extractor_id, extractor_asteroid_id, extractor_lot_id, destination_label, destination_type, destination_id, destination_asteroid_id, destination_lot_id, finish_time FROM extractions WHERE status = 1 AND crew_id = %s ORDER BY finish_time" % crew_id)
        print(extraction_sql)

        with con:
            cur = con.cursor()
            cur.execute("%s" % extraction_sql)
            rows = cur.fetchall()
            cur.close()

        if len(rows) == 0:
            extractions = []

        for row in rows:
            start_txn_id=row[0]
            start_timestamp=row[1]
            resource_name=row[2]
            resource_yield=round((row[3] / 1000))
            extractor_id=row[4]
            asteroid_id=row[5]
            lot_id=row[6]
            destination_label=row[7]
            destination_type=row[8]
            destination_id=row[9]
            destination_asteroid_id=row[10]
            destination_lot_id=row[11]
            finish_time=row[12]

            if destination_label == 5:
                dest_description = parseBuildingType(destination_type)
            elif destination_label == 6:
                dest_description = parseShipType(destination_type)

            converted_finish_time = convertFinishTime(finish_time)
            extractions.append({"start_txn_id": start_txn_id, "start_timestamp": str(start_timestamp), "resource_name": resource_name, "resource_yield": resource_yield, "extractor_id": extractor_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "destination_label": destination_label, "destination_id": destination_id, "destination_description": dest_description, "destination_asteroid_id": destination_asteroid_id, "destination_lot_id": destination_lot_id, "finish_time": finish_time, "remaining_time": converted_finish_time})
        extractions_crew.append({"crew_id": crew_id, "crew_name": crew_name, "station_id": station_id, "station_label": station_label, "asteroid_id": asteroid_id, "lot_id": lot_id, "pending": extractions})

    return extractions_crew


def getPendingProcessing(con, wallet):

    crews, crew_list = getPendingCrew(con, wallet)
    processed_crew = []
    processing = []
    for crew_row in crews:
        crew_id = crew_row['crew_id']
        crew_name = crew_row['crew_name']
        station_id = crew_row['station_id']
        station_label = crew_row['station_label']
        asteroid_id = crew_row['asteroid_id']
        lot_id = crew_row['lot_id']

        processing_sql = ("SELECT start_txn_id, start_timestamp, process_name, processor_id, processor_type, processor_asteroid_id, processor_lot_id, destination_id, destination_asteroid_id, destination_lot_id, destination_label, destination_type, finish_time FROM processing_actions WHERE status = 1 AND crew_id = %s ORDER BY finish_time" % crew_id)
        print(processing_sql)
        with con:
            cur = con.cursor()
            cur.execute("%s" % processing_sql)
            rows = cur.fetchall()
            cur.close()

        if len(rows) == 0:
            processing = []

        for row in rows:
            start_txn_id=row[0]
            start_timestamp=row[1]
            process_name=row[2]
            processor_id=row[3]
            processor_type=row[4]
            processor_asteroid_id=row[5]
            processor_lot_id=row[6]
            processor_description = parseBuildingType(processor_type)
            destination_id=row[7]
            destination_asteroid_id=row[8]
            destination_lot_id=row[9]
            destination_label=row[10]
            destination_type=row[11]
            finish_time=row[12]
            converted_finish_time = convertFinishTime(finish_time)

            if destination_label == 5:
                dest_description = parseBuildingType(destination_type)
            elif destination_label == 6:
                dest_description = parseShipType(destination_type)

            processing.append({"start_txn_id": start_txn_id, "start_timestamp": str(start_timestamp), "process_name": process_name, "processor_id": processor_id, "processor_type": processor_type, "processor_description": processor_description, "processor_asteroid_id": processor_asteroid_id, "processor_lot_id": processor_lot_id, "destination_id": destination_id, "destination_asteroid_id": destination_asteroid_id, "destination_lot_id": destination_lot_id, "destination_label": destination_label, "destination_description": dest_description, "finish_time": finish_time, "remaining_time": converted_finish_time})

        processed_crew.append({"crew_id": crew_id, "crew_name": crew_name, "station_id": station_id, "station_label": station_label, "asteroid_id": asteroid_id, "lot_id": lot_id, "pending": processing})

    return processed_crew


def getPendingSamples(con, wallet):

    crews, crew_list = getPendingCrew(con, wallet)
    sampling_crew = []
    sampling = []

    for crew_row in crews:
        sampling = []
        crew_id = crew_row['crew_id']
        crew_name = crew_row['crew_name']
        station_id = crew_row['station_id']
        station_label = crew_row['station_label']
        asteroid_id = crew_row['asteroid_id']
        lot_id = crew_row['lot_id']

        sampling_sql = ("SELECT start_txn_id, start_timestamp, deposit_id, asteroid_id, lot_id, resource_name, finish_time, initial_yield FROM core_samples WHERE status = 1 AND crew_id = %s" % crew_id)
        with con:
            cur = con.cursor()
            cur.execute("%s" % sampling_sql)
            rows = cur.fetchall()
            cur.close()

        if len(rows) == 0:
            sampling = []

        for row in rows:
            start_txn_id=row[0]
            start_timestamp=row[1]
            deposit_id=row[2]
            asteroid_id=row[3]
            lot_id=row[4]
            resource_name=row[5]
            finish_time=row[6]
            converted_finish_time = convertFinishTime(finish_time)
            initial_yield=row[7]
            sampling.append({"start_txn_id": start_txn_id, "start_timestamp": str(start_timestamp), "deposit_id": deposit_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "resource_name": resource_name, "finish_time": finish_time, "remaining_time": converted_finish_time, "initial_yield": initial_yield})

        sampling_crew.append({"crew_id": crew_id, "crew_name": crew_name, "station_id": station_id, "station_label": station_label, "asteroid_id": asteroid_id, "lot_id": lot_id, "pending": sampling})

    return sampling_crew


def getPendingDeliveries(con, wallet):

    crews, crew_list = getPendingCrew(con, wallet)
    delivering_crews = []
    delivering = []

    for crew_row in crews:
        delivering = []
        crew_id = crew_row['crew_id']
        crew_name = crew_row['crew_name']
        station_id = crew_row['station_id']
        station_label = crew_row['station_label']
        asteroid_id = crew_row['asteroid_id']
        lot_id = crew_row['lot_id']

        delivering_sql = ("SELECT start_txn_id, start_timestamp, origin_id, origin_label, origin_type, origin_asteroid_id, origin_lot_id, dest_id, dest_label, dest_type, dest_asteroid_id, dest_lot_id, finish_time, product_name, product_amount FROM deliveries WHERE status = 1 AND crew_id = %s" % crew_id)
        print(delivering_sql)

        with con:
            cur = con.cursor()
            cur.execute("%s" % delivering_sql)
            rows = cur.fetchall()
            cur.close()

        if len(rows) == 0:
            delivering = []

        for row in rows:
            start_txn_id=row[0]
            start_timestamp=row[1]
            origin_id=row[2]
            origin_label=row[3]
            origin_type=row[4]
            origin_asteroid_id=row[5]
            origin_lot_id=row[6]
            dest_id=row[7]
            dest_label=row[8]
            dest_type=row[9]
            dest_asteroid_id=row[10]
            dest_lot_id=row[11]
            finish_time=row[12]
            converted_finish_time = convertFinishTime(finish_time)
            product_name=row[13]
            product_amount=row[14]

            if origin_label == 5:
                origin_description = parseBuildingType(origin_type)
            elif origin_label == 6:
                origin_description = parseShipType(origin_type)

            if dest_label == 5:
                dest_description = parseBuildingType(dest_type)
            elif dest_label == 6:
                dest_description = parseShipType(dest_type)

            delivering.append({"start_txn_id": start_txn_id, "start_timestamp": str(start_timestamp), "origin_id": origin_id, "origin_label": origin_label, "origin_description": origin_description, "origin_asteroid_id": origin_asteroid_id, "origin_lot_id": origin_lot_id, "dest_id": dest_id, "dest_label": dest_label, "dest_description": dest_description, "dest_asteroid_id": dest_asteroid_id, "dest_lot_id": dest_lot_id, "finish_time": finish_time, "remaining_time": converted_finish_time, "product_name": product_name, "product_amount": product_amount})

        delivering_crews.append({"crew_id": crew_id, "crew_name": crew_name, "station_id": station_id, "station_label": station_label, "asteroid_id": asteroid_id, "lot_id": lot_id, "pending": delivering})

    return delivering_crews


def getPendingConstruction(con, wallet):

    crews, crew_list = getPendingCrew(con, wallet)
    construction_crews = []
    construction = []

    for crew_row in crews:
        construction = []
        crew_id = crew_row['crew_id']
        crew_name = crew_row['crew_name']
        station_id = crew_row['station_id']
        station_label = crew_row['station_label']
        asteroid_id = crew_row['asteroid_id']
        lot_id = crew_row['lot_id']

        construction_sql = ("SELECT start_txn_id, start_timestamp, building_type, building_id, asteroid_id, lot_id, finish_time FROM construction WHERE status = 1 AND crew_id = %s" % crew_id)
        with con:
            cur = con.cursor()
            cur.execute("%s" % construction_sql)
            rows = cur.fetchall()
            cur.close()

        if len(rows) == 0:
            construction = []

        for row in rows:
            start_txn_id=row[0]
            start_timestamp=row[1]
            building_type=row[2]
            building_id=row[3]
            asteroid_id=row[4]
            lot_id=row[5]
            finish_time=row[6]
            converted_finish_time = convertFinishTime(finish_time)
            building_description = parseBuildingType(building_type)

            construction.append({"start_txn_id": start_txn_id, "start_timestamp": str(start_timestamp), "building_type": building_type, "building_id": building_id, "building_description": building_description, "asteroid_id": asteroid_id, "lot_id": lot_id, "finish_time": finish_time, "remaining_time": converted_finish_time})

        construction_crews.append({"crew_id": crew_id, "crew_name": crew_name, "station_id": station_id, "station_label": station_label, "asteroid_id": asteroid_id, "lot_id": lot_id, "pending": construction})

    return construction_crews


def getPendingTransit(con, wallet):

    crews, crew_list = getPendingCrew(con, wallet)
    transit_crews = []
    transit = []

    for crew_row in crews:
        transit = []
        crew_id = crew_row['crew_id']
        crew_name = crew_row['crew_name']
        station_id = crew_row['station_id']
        station_label = crew_row['station_label']
        asteroid_id = crew_row['asteroid_id']
        lot_id = crew_row['lot_id']

        transit_sql = ("SELECT start_txn_id, start_timestamp, ship_id, ship_type, origin_id, destination_id, departure, arrival, finish_time FROM transit WHERE status = 1 AND crew_id = %s" % crew_id)
        with con:
            cur = con.cursor()
            cur.execute("%s" % transit_sql)
            rows = cur.fetchall()
            cur.close()

        if len(rows) == 0:
            transit = []

        for row in rows:
            start_txn_id=row[0]
            start_timestamp=row[1]
            ship_id=row[2]
            ship_type=row[3]
            origin_id=row[4]
            destination_id=row[5]
            departure=row[6]
            arrival=row[7]
            finish_time=row[8]
            converted_finish_time = convertFinishTime(finish_time)
            transit.append({"start_txn_id": start_txn_id, "start_timestamp": str(start_timestamp), "ship_id": ship_id, "ship_type": ship_type, "origin_id": origin_id, "destination_id": destination_id, "departure": departure, "arrival": arrival, "finish_time": finish_time, "remaining_time": converted_finish_time})

        transit_crews.append({"crew_id": crew_id, "crew_name": crew_name, "station_id": station_id, "station_label": station_label, "asteroid_id": asteroid_id, "lot_id": lot_id, "pending": transit})

    return transit_crews


def getPendingShipAssembly(con, wallet):

    crews, crew_list = getPendingCrew(con, wallet)
    ship_assembly_crews = []
    ship_assembly = []

    for crew_row in crews:
        ship_assembly = []
        crew_id = crew_row['crew_id']
        crew_name = crew_row['crew_name']
        station_id = crew_row['station_id']
        station_label = crew_row['station_label']
        asteroid_id = crew_row['asteroid_id']
        lot_id = crew_row['lot_id']

        ship_assembly_sql = ("SELECT start_txn_id, start_timestamp, ship_id, ship_type, dry_dock_id, dry_dock_asteroid_id, dry_dock_lot_id, finish_time FROM ship_assembly WHERE status = 1 AND crew_id = %s" % crew_id)
        with con:
            cur = con.cursor()
            cur.execute("%s" % ship_assembly_sql)
            rows = cur.fetchall()
            cur.close()

        if len(rows) == 0:
            delivering = []

        for row in rows:
            start_txn_id=row[0]
            start_timestamp=row[1]
            ship_id=row[2]
            ship_type=row[3]
            shipyard_id=row[4]
            shipyard_asteroid_id=row[5]
            shipyard_lot_id=row[6]
            finish_time=row[7]
            converted_finish_time = convertFinishTime(finish_time)

            ship_assembly.append({"start_txn_id": start_txn_id, "start_timestamp": str(start_timestamp), "ship_id": ship_id, "ship_type": ship_type, "shipyard_id": shipyard_id, "shipyard_asteroid_id": shipyard_asteroid_id, "finish_time": finish_time, "remaining_time": converted_finish_time})

        ship_assembly_crews.append({"crew_id": crew_id, "crew_name": crew_name, "station_id": station_id, "station_label": station_label, "asteroid_id": asteroid_id, "lot_id": lot_id, "pending": ship_assembly})

    return ship_assembly_crews


def getPendingActions(con, crew_id):

    extraction_sql = ("SELECT start_txn_id, start_timestamp, resource_name, resource_yield, extractor_id, extractor_asteroid_id, extractor_lot_id, destination_label, destination_type, destination_id, destination_asteroid_id, destination_lot_id, finish_time FROM extractions WHERE status = 1 AND crew_id = %s ORDER BY finish_time" % crew_id)
    extractions = []
    with con:
        cur = con.cursor()
        cur.execute("%s" % extraction_sql)
        rows = cur.fetchall()
        cur.close()

    if len(rows) == 0:
        extractions = []

    for row in rows:
        start_txn_id=row[0]
        start_timestamp=row[1]
        resource_name=row[2]
        resource_yield=round((row[3] / 1000))
        extractor_id=row[4]
        asteroid_id=row[5]
        lot_id=row[6]
        destination_label=row[7]
        destination_type=row[8]
        destination_id=row[9]
        destination_asteroid_id=row[10]
        destination_lot_id=row[11]
        finish_time=row[12]

        if destination_label == 5:
            dest_description = parseBuildingType(destination_type)
        elif destination_label == 6:
            dest_description = parseShipType(destination_type)


        converted_finish_time = convertFinishTime(finish_time)
        extractions.append({"start_txn_id": start_txn_id, "start_timestamp": str(start_timestamp), "resource_name": resource_name, "resource_yield": resource_yield, "extractor_id": extractor_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "destination_label": destination_label, "destination_id": destination_id, "destination_description": dest_description, "destination_asteroid_id": destination_asteroid_id, "destination_lot_id": destination_lot_id, "finish_time": finish_time, "remaining_time": converted_finish_time})

    processing = []
    processing_sql = ("SELECT start_txn_id, start_timestamp, process_name, processor_id, processor_type, processor_asteroid_id, processor_lot_id, destination_id, destination_asteroid_id, destination_lot_id, destination_label, destination_type, finish_time FROM processing_actions WHERE status = 1 AND crew_id = %s ORDER BY finish_time" % crew_id)
    with con:
        cur = con.cursor()
        cur.execute("%s" % processing_sql)
        rows = cur.fetchall()
        cur.close()

    if len(rows) == 0:
        extractions = []

    for row in rows:
        start_txn_id=row[0]
        start_timestamp=row[1]
        process_name=row[2]
        processor_id=row[3]
        processor_type=row[4]
        processor_asteroid_id=row[5]
        processor_lot_id=row[6]
        processor_description = parseBuildingType(processor_type)
        destination_id=row[7]
        destination_asteroid_id=row[8]
        destination_lot_id=row[9]
        destination_label=row[10]
        destination_type=row[11]
        finish_time=row[12]
        converted_finish_time = convertFinishTime(finish_time)

        if destination_label == 5:
            dest_description = parseBuildingType(destination_type)
        elif destination_label == 6:
            dest_description = parseShipType(destination_type)

        processing.append({"start_txn_id": start_txn_id, "start_timestamp": str(start_timestamp), "process_name": process_name, "processor_id": processor_id, "processor_type": processor_type, "processor_description": processor_description, "processor_asteroid_id": processor_asteroid_id, "processor_lot_id": processor_lot_id, "destination_id": destination_id, "destination_asteroid_id": destination_asteroid_id, "destination_lot_id": destination_lot_id, "destination_label": destination_label, "destination_description": dest_description, "finish_time": finish_time, "remaining_time": converted_finish_time})


    sampling = []
    sampling_sql = ("SELECT start_txn_id, start_timestamp, deposit_id, asteroid_id, lot_id, resource_name, finish_time, initial_yield FROM core_samples WHERE status = 1 AND crew_id = %s" % crew_id)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sampling_sql)
        rows = cur.fetchall()
        cur.close()

    if len(rows) == 0:
        sampling = []

    for row in rows:
        start_txn_id=row[0]
        start_timestamp=row[1]
        deposit_id=row[2]
        asteroid_id=row[3]
        lot_id=row[4]
        resource_name=row[5]
        finish_time=row[6]
        converted_finish_time = convertFinishTime(finish_time)
        initial_yield=row[7]
        sampling.append({"start_txn_id": start_txn_id, "start_timestamp": str(start_timestamp), "deposit_id": deposit_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "resource_name": resource_name, "finish_time": finish_time, "remaining_time": converted_finish_time, "initial_yield": initial_yield})


    delivering = []
    delivering_sql = ("SELECT start_txn_id, start_timestamp, origin_id, origin_label, origin_type, origin_asteroid_id, origin_lot_id, dest_id, dest_label, dest_type, dest_asteroid_id, dest_lot_id, finish_time, product_name, product_amount FROM deliveries WHERE status = 1 AND crew_id = %s" % crew_id)
    with con:
        cur = con.cursor()
        cur.execute("%s" % delivering_sql)
        rows = cur.fetchall()
        cur.close()

    if len(rows) == 0:
        delivering = []

    for row in rows:
        start_txn_id=row[0]
        start_timestamp=row[1]
        origin_id=row[2]
        origin_label=row[3]
        origin_type=row[4]
        origin_asteroid_id=row[5]
        origin_lot_id=row[6]
        dest_id=row[7]
        dest_label=row[8]
        dest_type=row[9]
        dest_asteroid_id=row[10]
        dest_lot_id=row[11]
        finish_time=row[12]
        converted_finish_time = convertFinishTime(finish_time)
        product_name=row[13]
        product_amount=row[14]

        if origin_label == 5:
            origin_description = parseBuildingType(origin_type)
        elif origin_label == 6:
            origin_description = parseShipType(origin_type)

        if dest_label == 5:
            dest_description = parseBuildingType(dest_type)
        elif dest_label == 6:
            dest_description = parseShipType(dest_type)

        delivering.append({"start_txn_id": start_txn_id, "start_timestamp": str(start_timestamp), "origin_id": origin_id, "origin_label": origin_label, "origin_description": origin_description, "origin_asteroid_id": origin_asteroid_id, "origin_lot_id": origin_lot_id, "dest_id": dest_id, "dest_label": dest_label, "dest_description": dest_description, "dest_asteroid_id": dest_asteroid_id, "dest_lot_id": dest_lot_id, "finish_time": finish_time, "remaining_time": converted_finish_time, "product_name": product_name, "product_amount": product_amount})


    construction = []
    construction_sql = ("SELECT start_txn_id, start_timestamp, building_type, building_id, asteroid_id, lot_id, finish_time FROM construction WHERE status = 1 AND crew_id = %s" % crew_id)
    with con:
        cur = con.cursor()
        cur.execute("%s" % construction_sql)
        rows = cur.fetchall()
        cur.close()

    if len(rows) == 0:
        construction = []

    for row in rows:
        start_txn_id=row[0]
        start_timestamp=row[1]
        building_type=row[2]
        building_id=row[3]
        asteroid_id=row[4]
        lot_id=row[5]
        finish_time=row[6]
        converted_finish_time = convertFinishTime(finish_time)
        building_description = parseBuildingType(building_type)

        construction.append({"start_txn_id": start_txn_id, "start_timestamp": str(start_timestamp), "building_type": building_type, "building_id": building_id, "building_description": building_description, "asteroid_id": asteroid_id, "lot_id": lot_id, "finish_time": finish_time, "remaining_time": converted_finish_time})


    transit = []
    transit_sql = ("SELECT start_txn_id, start_timestamp, ship_id, ship_type, origin_id, destination_id, departure, arrival, finish_time FROM transit WHERE status = 1 AND crew_id = %s" % crew_id)
    with con:
        cur = con.cursor()
        cur.execute("%s" % transit_sql)
        rows = cur.fetchall()
        cur.close()

    if len(rows) == 0:
        transit = []

    for row in rows:
        start_txn_id=row[0]
        start_timestamp=row[1]
        ship_id=row[2]
        ship_type=row[3]
        origin_id=row[4]
        destination_id=row[5]
        departure=row[6]
        arrival=row[7]
        finish_time=row[8]
        converted_finish_time = convertFinishTime(finish_time)
        transit.append({"start_txn_id": start_txn_id, "start_timestamp": str(start_timestamp), "ship_id": ship_id, "ship_type": ship_type, "origin_id": origin_id, "destination_id": destination_id, "departure": departure, "arrival": arrival, "finish_time": finish_time, "remaining_time": converted_finish_time})


    ship_assembly = []
    ship_assembly_sql = ("SELECT start_txn_id, start_timestamp, ship_id, ship_type, dry_dock_id, dry_dock_asteroid_id, dry_dock_lot_id, finish_time FROM ship_assembly WHERE status = 1 AND crew_id = %s" % crew_id)
    with con:
        cur = con.cursor()
        cur.execute("%s" % delivering_sql)
        rows = cur.fetchall()
        cur.close()

    if len(rows) == 0:
        delivering = []

    for row in rows:
        start_txn_id=row[0]
        start_timestamp=row[1]
        ship_id=row[2]
        ship_type=row[3]
        shipyard_id=row[4]
        shipyard_asteroid_id=row[5]
        shipyard_lot_id=row[6]
        finish_time=row[7]
        converted_finish_time = convertFinishTime(finish_time)

        ship_assembly.append({"start_txn_id": start_txn_id, "start_timestamp": str(start_timestamp), "ship_id": ship_id, "ship_type": ship_type, "shipyard_id": shipyard_id, "shipyard_asteroid_id": shipyard_asteroid_id, "finish_time": finish_time, "remaining_time": converted_finish_time})


    return extractions, processing, sampling, delivering, construction, transit, ship_assembly


def getProductsSold(con, crew_id):

    orders = []
    sell_filled_sql = ("SELECT exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price, timestamp FROM dispatcher_sell_order_filled WHERE seller_crew_id = %s ORDER BY timestamp DESC" % crew_id)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sell_filled_sql)
        rows = cur.fetchall()
        cur.close()

    for row in rows:
        exchange_id=row[0]
        asteroid_id=row[1]
        lot_id=row[2]
        product_id=row[3]
        product_name=row[4]
        amount=row[5]
        price=(row[6] / 1000000)
        total = round((amount * price), 3)
        timestamp=row[7]
        orders.append({"exchange_id": exchange_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "product_id": product_id, "product_name": product_name, "amount": amount, "price": price, "total": total, "timestamp": str(timestamp)})

    buy_filled_sql = ("SELECT exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price, timestamp FROM dispatcher_buy_order_filled WHERE caller_crew_id = %s ORDER BY timestamp DESC" % crew_id)
    with con:
        cur = con.cursor()
        cur.execute("%s" % buy_filled_sql)
        rows = cur.fetchall()
        cur.close()

    for row in rows:
        exchange_id=row[0]
        asteroid_id=row[1]
        lot_id=row[2]
        product_id=row[3]
        product_name=row[4]
        amount=row[5]
        price=(row[6] / 1000000)
        total = round((amount * price), 3)
        timestamp=row[7]
        orders.append({"exchange_id": exchange_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "product_id": product_id, "product_name": product_name, "amount": amount, "price": price, "total": total, "timestamp": str(timestamp)})

    return orders


def getProductsPurchased(con, crew_id):

    orders = []
    buy_filled_sql = ("SELECT exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price, timestamp FROM dispatcher_buy_order_filled WHERE buyer_crew_id = %s ORDER BY TIMESTAMP DESC" % crew_id)
    with con:
        cur = con.cursor()
        cur.execute("%s" % buy_filled_sql)
        rows = cur.fetchall()
        cur.close()

    for row in rows:
        exchange_id=row[0]
        asteroid_id=row[1]
        lot_id=row[2]
        product_id=row[3]
        product_name=row[4]
        amount=row[5]
        price=(row[6] / 1000000)
        total = round((amount * price), 3)
        timestamp=row[7]
        orders.append({"exchange_id": exchange_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "product_id": product_id, "product_name": product_name, "amount": amount, "price": price, "total": total, "timestamp": str(timestamp)})


    sell_filled_sql = ("SELECT exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price, timestamp FROM dispatcher_sell_order_filled WHERE caller_crew_id = %s ORDER BY TIMESTAMP DESC" % crew_id)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sell_filled_sql)
        rows = cur.fetchall()
        cur.close()

    for row in rows:
        exchange_id=row[0]
        asteroid_id=row[1]
        lot_id=row[2]
        product_id=row[3]
        product_name=row[4]
        amount=row[5]
        price=(row[6] / 1000000)
        total = round((amount * price), 3)
        timestamp=row[7]
        orders.append({"exchange_id": exchange_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "product_id": product_id, "product_name": product_name, "amount": amount, "price": price, "total": total, "timestamp": str(timestamp)})

    return orders


def getOpenBuyOrders(con, wallet):

    orders = []
    sql = ("SELECT exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price, maker_fee, valid_time FROM wallet_buy_orders WHERE caller_address = '%s' ORDER BY valid_time ASC" % wallet)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return orders

    for row in rows:
        exchange_id=row[0]
        asteroid_id=row[1]
        lot_id=row[2]
        product_id=row[3]
        product_name=row[4]
        amount=row[5]
        price=(row[6] / 1000000)
        maker_fee=row[7]
        valid_time=row[8]
        dt_object = datetime.utcfromtimestamp(valid_time)
        dt_string = dt_object.strftime('%Y-%m-%d %H:%M:%S')
        orders.append({"exchange_id": exchange_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "product_id": product_id, "product_name": product_name, "amount": amount, "price": price, "valid_time": str(dt_string)})

    return orders


def getOpenSellOrders(con, wallet):

    orders = []
    sql = ("SELECT exchange_id, exchange_asteroid_id, exchange_lot_id, product_id, product_name, amount, price, maker_fee, valid_time FROM wallet_sell_orders WHERE caller_address = '%s' ORDER BY valid_time ASC" % wallet)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return orders

    for row in rows:
        exchange_id=row[0]
        asteroid_id=row[1]
        lot_id=row[2]
        product_id=row[3]
        product_name=row[4]
        amount=row[5]
        price=(row[6] / 1000000)
        maker_fee=row[7]
        valid_time=row[8]
        dt_object = datetime.utcfromtimestamp(valid_time)
        dt_string = dt_object.strftime('%Y-%m-%d %H:%M:%S')
        orders.append({"exchange_id": exchange_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "product_id": product_id, "product_name": product_name, "amount": amount, "price": price, "maker_fee": maker_fee, "valid_time": str(dt_string)})

    return orders


def getAsteroidNames(con):

    asteroid_list = []
    sql = "SELECT DISTINCT b.asteroid_id, c.name FROM buildings b, asteroids c WHERE b.asteroid_id = c.asteroid_id"
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    for row in rows:
        asteroid_id=row[0]
        asteroid_name=row[1]
        asteroid_list.append({"asteroid_id": asteroid_id, "asteroid_name": asteroid_name})

    return asteroid_list


def convertFinishTime(finish_time):

    current_epoch_seconds = datetime.utcnow().timestamp()
    seconds_difference = (current_epoch_seconds - finish_time)
    seconds_difference = (finish_time - current_epoch_seconds)
    if seconds_difference > 0:
        days = seconds_difference // (60 * 60 * 24)
        hours = (seconds_difference % (60 * 60 * 24)) // (60 * 60)
        minutes = (seconds_difference % (60 * 60)) // 60
        seconds = seconds_difference % 60
        days = int(days)
        hours = int(hours)
        minutes = int(minutes)
        seconds = int(seconds)
        duration_string = f"{days} days, {hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        duration_string = "0 days, 00:00:00"

    return duration_string


def walletState(wallet):

    result = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    wallet = fix_address.padAddress(wallet)
    result = getWalletState(con, wallet)
    con.close()
    return result


def crew(wallet):

    crew=[]
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    wallet = fix_address.padAddress(wallet)
    result = getCrew(con, wallet)
    con.close()
    return result


def crewPendingActions(wallet):

    crew=[]
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    wallet = fix_address.padAddress(wallet)
    result = getCrewPendingActions(con, wallet)
    con.close()
    return result


def crewCompletedActions(wallet):

    crew=[]
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    wallet = fix_address.padAddress(wallet)
    result = getCrewCompletedActions(con, wallet)
    con.close()
    return result


def crewBuildings(wallet):

    crew=[]
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    wallet = fix_address.padAddress(wallet)
    result = getCrewBuildings(con, wallet)
    con.close()
    return result


def crewShips(wallet):

    crew=[]
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    wallet = fix_address.padAddress(wallet)
    result = getCrewShips(con, wallet)
    con.close()
    return result


def marketplace(wallet):

    result=[]
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    wallet = fix_address.padAddress(wallet)
    result = getCrewMarketplace(con, wallet)
    con.close()
    return result

def crewPendingProcessing(wallet):

    result=[]
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    wallet = fix_address.padAddress(wallet)
    result = getPendingProcessing(con, wallet)
    con.close()
    return result

def crewPendingDeliveries(wallet):

    result=[]
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    wallet = fix_address.padAddress(wallet)
    result = getPendingDeliveries(con, wallet)
    con.close()
    return result

def crewPendingExtractions(wallet):

    result=[]
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    wallet = fix_address.padAddress(wallet)
    result = getPendingExtractions(con, wallet)
    con.close()
    return result

def crewPendingSamples(wallet):

    result=[]
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    wallet = fix_address.padAddress(wallet)
    result = getPendingSamples(con, wallet)
    con.close()
    return result

def crewPendingConstruction(wallet):

    result=[]
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    wallet = fix_address.padAddress(wallet)
    result = getPendingConstruction(con, wallet)
    con.close()
    return result

def crewPendingTransit(wallet):

    result=[]
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    wallet = fix_address.padAddress(wallet)
    result = getPendingTransit(con, wallet)
    con.close()
    return result

def crewPendingShipAssembly(wallet):

    result=[]
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    wallet = fix_address.padAddress(wallet)
    result = getPendingShipAssembly(con, wallet)
    con.close()
    return result

