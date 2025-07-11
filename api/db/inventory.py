import sys
import os
import pymysql
import warnings
import traceback
import configparser
import time

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


def parseShipType(ship_type):

    if ship_type == 1:
        ship_type = "ESCAPE_MODULE"

    if ship_type == 2:
        ship_type = "LIGHT_TRANSPORT"

    if ship_type == 3:
        ship_type = "HEAVY_TRANSPORT"

    if ship_type == 4:
        ship_type = "SHUTTLE"

    return ship_type


def parseBuildingType(building_type):

    if building_type == 0:
        building_type = "EMPTY_LOT"

    if building_type == 1:
        building_type = "WAREHOUSE"

    if building_type == 2:
        building_type = "EXTRACTOR"

    if building_type == 3:
        building_type = "REFINERY"

    if building_type == 4:
        building_type = "BIOREACTOR"

    if building_type == 5:
        building_type = "FACTORY"

    if building_type == 6:
        building_type = "SHIPYARD"

    if building_type == 7:
        building_type = "SPACEPORT"

    if building_type == 8:
        building_type = "MARKETPLACE"

    if building_type == 9:
        building_type = "HABITAT"

    return building_type


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


def getBuildingData(con, building_id):

    asteroid_id = None
    lot_id = None
    caller_address = None
    crew_id = None

    sql = ("SELECT caller_address, crew_id, asteroid_id, lot_id FROM buildings WHERE building_id = %s" % building_id)
    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return caller_address, crew_id, asteroid_id, lot_id

    for row in rows:
        caller_address=row[0]
        crew_id=row[1]
        asteroid_id=row[2]
        lot_id=row[3]

    return caller_address, crew_id, asteroid_id, lot_id


def getBuildings(con, parameter1, parameter2, asteroid_id, lot_id):

    buildings = []
    if parameter1 == "wallet":
        if lot_id is None:
            sql = ("SELECT building_id, caller_address, crew_id, asteroid_id, lot_id, building_type FROM buildings WHERE caller_address = '%s' AND asteroid_id = %s AND status = 3" % (parameter2, asteroid_id))
        else:
            sql = ("SELECT building_id, caller_address, crew_id, asteroid_id, lot_id, building_type FROM buildings WHERE caller_address = '%s' AND asteroid_id = %s AND lot_id = %s AND status = 3" % (parameter2, asteroid_id, lot_id))
    elif parameter1 == "crew":
        if lot_id is None:
            sql = ("SELECT building_id, caller_address, crew_id, asteroid_id, lot_id, building_type FROM buildings WHERE crew_id = %s AND asteroid_id = %s AND status = 3" % (parameter2, asteroid_id))
        else:
            sql = ("SELECT building_id, caller_address, crew_id, asteroid_id, lot_id, building_type FROM buildings WHERE crew_id = %s AND asteroid_id = %s AND lot_id = %s AND status = 3" % (parameter2, asteroid_id, lot_id))

    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return buildings

    for row in rows:
        building_id=row[0]
        caller_address=row[1]
        crew_id=row[2]
        asteroid_id=row[3]
        lot_id=row[4]
        building_type=row[5]
        building_name=parseBuildingType(building_id)
        buildings.append({"building_id": building_id, "caller_address": caller_address, "crew_id": crew_id, "asteroid_id": asteroid_id, "lot_id": lot_id, "building_type": building_type, "building_name": building_name})

    return buildings


def getShips(con, parameter1, parameter2, asteroid_id, lot_id):

    ships = []
    if parameter1 == "wallet":
        if lot_id is None:
            sql = ("SELECT b.ship_id, b.caller_address, b.crew_id, b.dock_type, b.dock_asteroid_id, b.dock_lot_id, c.ship_type, c.ship_type_name FROM ships_docked b, ships c WHERE b.caller_address = '%s' AND b.dock_asteroid_id = %s AND b.status = 1 AND b.ship_id = c.ship_id" % (parameter2, asteroid_id))
        else:
            sql = ("SELECT b.ship_id, b.caller_address, b.crew_id, b.dock_type, b.dock_asteroid_id, b.dock_lot_id, c.ship_type, c.ship_type_name FROM ships_docked b, ships c WHERE b.caller_address = '%s' AND b.dock_asteroid_id = %s AND b.dock_lot_id = %s AND b.status = 1 AND b.ship_id = c.ship_id" % (parameter2, asteroid_id, lot_id))
    elif parameter1 == "crew":
        if lot_id is None:
            sql = ("SELECT b.ship_id, b.caller_address, b.crew_id, b.dock_type, b.dock_asteroid_id, b.dock_lot_id, c.ship_type, c.ship_type_name FROM ships_docked b, ships c WHERE b.crew_id = %s AND b.dock_asteroid_id = %s AND b.status = 1 AND b.ship_id = c.ship_id" % (parameter2, asteroid_id))
        else:
            sql = ("SELECT b.ship_id, b.caller_address, b.crew_id, b.dock_type, b.dock_asteroid_id, b.dock_lot_id, c.ship_type, c.ship_type_name FROM ships_docked b, ships c WHERE b.crew_id = %s AND b.dock_asteroid_id = %s AND b.dock_lot_id = %s AND b.status = 1" % (parameter2, asteroid_id, lot_id))

    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return ships

    for row in rows:
        ship_id=row[0]
        caller_address=row[1]
        crew_id=row[2]
        dock_type=row[3]
        asteroid_id=row[4]
        lot_id=row[5]
        ship_type=row[6]
        ship_name=row[7]
        ships.append({"ship_id": ship_id, "caller_address": caller_address, "crew_id": crew_id, "dock_type": dock_type, "asteroid_id": asteroid_id, "lot_id": lot_id, "ship_type": ship_type, "ship_name": ship_name})

    return ships


def getShipData(con, ship_id):

    asteroid_id = None
    lot_id = None
    caller_address = None
    crew_id = None

    sql = ("SELECT caller_address, crew_id, dock_asteroid_id, dock_lot_id FROM ships_docked WHERE ship_id = %s" % ship_id)
    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return caller_address, crew_id, asteroid_id, lot_id

    for row in rows:
        caller_address=row[0]
        crew_id=row[1]
        asteroid_id=row[2]
        lot_id=row[3]

    return caller_address, crew_id, asteroid_id, lot_id


def getOutputs(con, txn_id):

    outputs = []
    sql = ("SELECT resource_id, resource_name, resource_amount FROM dispatcher_material_processing_started_outputs WHERE txn_id = '%s'" % txn_id)
    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return outputs

    for row in rows:
        output_id=row[0]
        output_name=row[1]
        output_amount=row[2]
        outputs.append({"resource_id": output_id, "resource_name": output_name, "resource_amount": output_amount})

    return outputs


def getInventoryAtEntity(con, entity_label, entity_id):

    inventory = []
    slot1 = []
    slot2 = []
    resources = []

    if entity_label == 5:
        caller_address, crew_id, asteroid_id, lot_id = getBuildingData(con, entity_id)
    elif entity_label == 6:
        caller_address, crew_id, asteroid_id, lot_id = getShipData(con, entity_id)

    sql=("SELECT inventory_label, inventory_type, inventory_id, inventory_slot, resource_id, inventory_amount FROM inventories WHERE inventory_label = %s AND inventory_id = %s AND inventory_amount > 0" % (entity_label, entity_id))
    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return inventory

    for row in rows:
        inventory_label=row[0]
        inventory_type=row[1]
        inventory_id=row[2]
        inventory_slot=row[3]
        resource_id=row[4]
        resource_amount=row[5]

        resource_name = parseProductType(resource_id)

        if entity_label == 5:
            inventory_name = parseBuildingType(inventory_type)
        elif entity_label == 6:
            inventory_name = parseShipType(inventory_type)
            if inventory_slot == 1:
                slot1.append({"resource_id": resource_id, "resource_name": resource_name, "resource_amount": resource_amount})
            elif inventory_slot == 2:
                slot2.append({"resource_id": resource_id, "resource_name": resource_name, "resource_amount": resource_amount})

        resources.append({"inventory_slot": inventory_slot, "resource_id": resource_id, "resource_name": resource_name, "resource_amount": resource_amount})

    if entity_label == 5:
        inventory.append({"inventory_label": inventory_label, "inventory_type": inventory_type, "inventory_id": inventory_id, "inventory_name": inventory_name, "asteroid_id": asteroid_id, "lot_id": lot_id, "caller_address": caller_address, "crew_id": crew_id, "resources": resources})
    if entity_label == 6:
        inventory.append({"inventory_label": inventory_label, "inventory_type": inventory_type, "inventory_id": inventory_id, "inventory_name": inventory_name, "asteroid_id": asteroid_id, "lot_id": lot_id, "caller_address": caller_address, "crew_id": crew_id, "slot_1": slot1, "slot_2": slot2})

    return inventory


def getInventoryOnAsteroid(con, parameter1, parameter2, asteroid_id):

    lot_id = None
    ship_inventory = []
    building_inventory = []
    inventory = []
    slot1 = []
    slot2 = []
    resources = []

    buildings=getBuildings(con, parameter1, parameter2, asteroid_id, lot_id)
    ships=getShips(con, parameter1, parameter2, asteroid_id, lot_id)

    for ship in ships:
        ship_resources = []
        ship_id = ship['ship_id']
        caller_address = ship['caller_address']
        crew_id = ship['crew_id']
        dock_asteroid_id = ship['asteroid_id']
        dock_lot_id = ship['lot_id']
        ship_type = ship['ship_type']
        ship_name = ship['ship_name']
        sql=("SELECT inventory_label, inventory_type, inventory_id, inventory_slot, resource_id, inventory_amount FROM inventories WHERE inventory_label = 6 AND inventory_id = %s" % ship_id)
        print(sql)
        with con:
            cur = con.cursor()
            cur.execute("%s" % sql)
            ship_rows = cur.fetchall()
            cur.close()

        for ship_row in ship_rows:
            inventory_label=ship_row[0]
            inventory_type=ship_row[1]
            inventory_id=ship_row[2]
            inventory_slot=ship_row[3]
            resource_id=ship_row[4]
            resource_amount=ship_row[5]

            resource_name = parseProductType(resource_id)
            ship_resources.append({"inventory_slot": inventory_slot, "resource_id": resource_id, "resource_name": resource_name, "resource_amount": resource_amount})

        ship_inventory.append({"ship_id": ship_id, "caller_address": caller_address, "crew_id": crew_id, "asteroid_id": dock_asteroid_id, "lot_id": dock_lot_id, "ship_type": ship_type, "ship_name": ship_name, "inventory": ship_resources})


    for building in buildings:
        building_resources = []
        building_id = building['building_id']
        caller_address = building['caller_address']
        crew_id = building['crew_id']
        building_asteroid_id = building['asteroid_id']
        building_lot_id = building['lot_id']
        building_type = building['building_type']
        building_name = building['building_name']
        sql=("SELECT inventory_label, inventory_type, inventory_id, inventory_slot, resource_id, inventory_amount FROM inventories WHERE inventory_label = 5 AND inventory_id = %s" % building_id)
        print(sql)
        with con:
            cur = con.cursor()
            cur.execute("%s" % sql)
            building_rows = cur.fetchall()
            cur.close()

        for building_row in building_rows:
            inventory_label=building_row[0]
            inventory_type=building_row[1]
            inventory_id=building_row[2]
            inventory_slot=building_row[3]
            resource_id=building_row[4]
            resource_amount=building_row[5]

            resource_name = parseProductType(resource_id)
            building_resources.append({"inventory_slot": inventory_slot, "resource_id": resource_id, "resource_name": resource_name, "resource_amount": resource_amount})

        building_inventory.append({"building_id": building_id, "caller_address": caller_address, "crew_id": crew_id, "asteroid_id": building_asteroid_id, "lot_id": building_lot_id, "building_type": building_type, "building_name": building_name, "inventory": building_resources})

    inventory.append({"buildings": building_inventory, "ships": ship_inventory})

    return inventory


def getInventoryOnLot(con, parameter1, parameter2, asteroid_id, lot_id):

    ship_inventory = []
    building_inventory = []
    inventory = []
    slot1 = []
    slot2 = []
    resources = []

    buildings=getBuildings(con, parameter1, parameter2, asteroid_id, lot_id)
    ships=getShips(con, parameter1, parameter2, asteroid_id, lot_id)

    for ship in ships:
        ship_resources = []
        ship_id = ship['ship_id']
        caller_address = ship['caller_address']
        crew_id = ship['crew_id']
        dock_asteroid_id = ship['asteroid_id']
        dock_lot_id = ship['lot_id']
        ship_type = ship['ship_type']
        ship_name = ship['ship_name']
        sql=("SELECT inventory_label, inventory_type, inventory_id, inventory_slot, resource_id, inventory_amount FROM inventories WHERE inventory_label = 6 AND inventory_id = %s" % ship_id)
        print(sql)
        with con:
            cur = con.cursor()
            cur.execute("%s" % sql)
            ship_rows = cur.fetchall()
            cur.close()

        for ship_row in ship_rows:
            inventory_label=ship_row[0]
            inventory_type=ship_row[1]
            inventory_id=ship_row[2]
            inventory_slot=ship_row[3]
            resource_id=ship_row[4]
            resource_amount=ship_row[5]

            resource_name = parseProductType(resource_id)
            ship_resources.append({"inventory_slot": inventory_slot, "resource_id": resource_id, "resource_name": resource_name, "resource_amount": resource_amount})

        ship_inventory.append({"ship_id": ship_id, "caller_address": caller_address, "crew_id": crew_id, "asteroid_id": dock_asteroid_id, "lot_id": dock_lot_id, "ship_type": ship_type, "ship_name": ship_name, "inventory": ship_resources})

    for building in buildings:
        building_resources = []
        building_id = building['building_id']
        caller_address = building['caller_address']
        crew_id = building['crew_id']
        building_asteroid_id = building['asteroid_id']
        building_lot_id = building['lot_id']
        building_type = building['building_type']
        building_name = building['building_name']
        sql=("SELECT inventory_label, inventory_type, inventory_id, inventory_slot, resource_id, inventory_amount FROM inventories WHERE inventory_label = 5 AND inventory_id = %s" % building_id)
        print(sql)
        with con:
            cur = con.cursor()
            cur.execute("%s" % sql)
            building_rows = cur.fetchall()
            cur.close()

        for building_row in building_rows:
            inventory_label=building_row[0]
            inventory_type=building_row[1]
            inventory_id=building_row[2]
            inventory_slot=building_row[3]
            resource_id=building_row[4]
            resource_amount=building_row[5]

            resource_name = parseProductType(resource_id)
            building_resources.append({"inventory_slot": inventory_slot, "resource_id": resource_id, "resource_name": resource_name, "resource_amount": resource_amount})

        building_inventory.append({"building_id": building_id, "caller_address": caller_address, "crew_id": crew_id, "asteroid_id": building_asteroid_id, "lot_id": building_lot_id, "building_type": building_type, "building_name": building_name, "inventory": building_resources})

    inventory.append({"buildings": building_inventory, "ships": ship_inventory})
    return inventory


def inventoryAtEntity(inventory_type, inventory_id):

    inventory = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    inventory = getInventoryAtEntity(con, inventory_type, inventory_id)
    con.close()
    return inventory


def inventoryOnAsteroid(asteroid_id, parameter1, parameter2):

    inventory = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    inventory = getInventoryOnAsteroid(con, parameter1, parameter2, asteroid_id)
    con.close()
    return inventory


def inventoryOnLot(asteroid_id, lot_id, parameter1, parameter2):

    inventory = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    inventory = getInventoryOnLot(con, parameter1, parameter2, asteroid_id, lot_id)
    con.close()
    return inventory

