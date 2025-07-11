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


def getShipAssemblyState(con, parameter1, parameter2, state, start_block, end_block):

    assembly = []
    if state == "pending" or state == "finished":
        pre_sql="SELECT start_txn_id, start_block_number, finish_txn_id, finish_block_number, caller_address, crew_id, ship_id, ship_type, ship_type_name, dry_dock_label, dry_dock_id, dry_dock_slot, dry_dock_type, dry_dock_asteroid_id, dry_dock_lot_id, origin_label, origin_id, origin_slot, origin_type, origin_asteroid_id, origin_lot_id, destination_label, destination_type, destination_asteroid_id, destination_lot_id, finish_time "
        print(pre_sql)
        if state == "pending":
            status = 1
        elif state == "finished":
            status = 2
        if parameter1 == "wallet":
            from_sql=("FROM ship_assembly WHERE caller_address = '%s' AND status = %s AND start_block_number > %s" % (parameter2, status, start_block))
        elif parameter1 == "crew":
            from_sql=("FROM ship_assembly WHERE crew_id = %s AND status = %s AND start_block_number > %s" % (parameter2, status, start_block))
            print("from_sql: %s" % from_sql)
        if status == 2 and end_block > 0:
            finish_sql=(" AND finish_block_number <= %s ORDER BY start_block_number" % end_block)
        else:
            finish_sql=" ORDER BY start_block_number"

    elif state == "started":
        pre_sql="SELECT txn_id, block_number, NULL, NULL, caller_address, caller_crew_id, ship_id, ship_type, ship_type_name, dry_dock_label, dry_dock_id, dry_dock_slot, dry_dock_type, dry_dock_asteroid_id, dry_dock_lot_id, origin_label, origin_id, origin_slot, origin_type, origin_asteroid_id, origin_lot_id, NULL, NULL, NULL, NULL, finish_time "
        print(pre_sql)
        if parameter1 == "wallet":
            from_sql=("FROM dispatcher_ship_assembly_started_v1 WHERE caller_address = '%s' AND block_number > %s" % (parameter2, start_block))
        elif parameter1 == "crew":
            from_sql=("FROM dispatcher_material_processing_started_v1 WHERE caller_crew_id = %s AND block_number > %s" % (parameter2, start_block))
            print("from_sql: %s" % from_sql)
        if end_block > 0:
            finish_sql=(" AND block_number <= %s ORDER BY block_number" % end_block)
        else:
            finish_sql=" ORDER BY block_number"

    sql = pre_sql + from_sql + finish_sql

    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return assembly

    for row in rows:
        start_txn_id=row[0]
        start_block_number=row[1]
        finish_txn_id=row[2]
        finish_block_number=row[3]
        caller_address=row[4]
        crew_id=row[5]
        ship_id=row[6]
        ship_type=row[7]
        ship_type_name=row[8]
        dry_dock_label=row[9]
        dry_dock_id=row[10]
        dry_dock_slot=row[11]
        dry_dock_type=row[12]
        dry_dock_asteroid_id=row[13]
        dry_dock_lot_id=row[14]
        origin_label=row[15]
        origin_id=row[16]
        origin_slot=row[17]
        origin_type=row[18]
        origin_asteroid_id=row[19]
        origin_lot_id=row[20]
        destination_label=row[21]
        destination_type=row[22]
        destination_asteroid_id=row[23]
        destination_lot_id=row[24]
        finish_time=row[25]

        assembly.append({"start_txn_id": start_txn_id, "start_block_number": start_block_number, "finish_txn_id": finish_txn_id, "finish_block_number": finish_block_number, "caller_address": caller_address, "crew_id": crew_id, "ship_id": ship_id, "ship_type": ship_type, "ship_type_name": ship_type_name, "dry_dock_label": dry_dock_label, "dry_dock_id": dry_dock_id, "dry_dock_slot": dry_dock_slot, "dry_dock_type": dry_dock_type, "dry_dock_asteroid_id": dry_dock_asteroid_id, "dry_dock_lot_id": dry_dock_lot_id, "origin_label": origin_label, "origin_id": origin_id, "origin_slot": origin_slot, "origin_type": origin_type, "origin_asteroid_id": origin_asteroid_id, "origin_lot_id": origin_lot_id, "destination_label": destination_label, "destination_type": destination_type, "destination_asteroid_id": destination_asteroid_id, "destination_lot_id": destination_lot_id, "finish_time": finish_time})

    return assembly


def getOwnedShips(con, parameter1, parameter2, asteroid_id):

    ships=[]
    if parameter1 == "wallet":
        pre_sql = ("SELECT b.ship_id, b.caller_address, b.crew_id, b.ship_type, b.ship_type_name, b.emergency, c.dock_label, c.dock_type, c.dock_asteroid_id, c.dock_lot_id FROM ships b, ships_docked c WHERE b.caller_address = '%s' AND b.ship_id = c.ship_id" % (parameter2))
    elif parameter1 == "crew":
        pre_sql = ("SELECT b.ship_id, b.caller_address, b.crew_id, b.ship_type, b.ship_type_name, b.emergency, c.dock_label, c.dock_type, c.dock_asteroid_id, c.dock_lot_id FROM ships b, ships_docked c WHERE b.crew_id = %s AND b.ship_id = c.ship_id" % (parameter2))

    if asteroid_id is not None:
        post_sql = (" AND c.dock_asteroid_id = %s" % asteroid_id)
    else:
        post_sql = ""

    sql = pre_sql + post_sql
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
        ship_type=row[3]
        ship_type_name=row[4]
        emergency=row[5]
        dock_label=row[6]
        dock_type=row[7]
        dock_asteroid_id=row[8]
        dock_lot_id=row[9]

        ships.append({"caller_address": caller_address, "crew_id": crew_id, "ship_id": ship_id, "ship_type": ship_type, "ship_type_name": ship_type_name, "emergency": emergency, "dock_label": dock_label, "dock_type": dock_type, "dock_asteroid_id": dock_asteroid_id, "dock_lot_id": dock_lot_id})

    return ships


def getShipStatus(con, ship_id):

    ship_state=[]
    ship=[]
    inventory=[]
    slot1=[]
    slot2=[]
    resources=[]

    sql=("SELECT b.ship_id, b.caller_address, b.crew_id, b.ship_type, b.ship_type_name, b.emergency, c.dock_label, c.dock_type, c.dock_asteroid_id, c.dock_lot_id FROM ships b, ships_docked c WHERE b.ship_id = %s AND b.ship_id = c.ship_id" % (ship_id))
    print(sql)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql)
        rows = cur.fetchall()
        cur.close()

    if rows == None:
        return ship

    for row in rows:
        ship_id=row[0]
        caller_address=row[1]
        crew_id=row[2]
        ship_type=row[3]
        ship_type_name=row[4]
        emergency=row[5]
        dock_label=row[6]
        dock_type=row[7]
        dock_asteroid_id=row[8]
        dock_lot_id=row[9]

        ship_state.append({"caller_address": caller_address, "crew_id": crew_id, "ship_id": ship_id, "ship_type": ship_type, "ship_type_name": ship_type_name, "emergency": emergency, "dock_label": dock_label, "dock_type": dock_type, "dock_asteroid_id": dock_asteroid_id, "dock_lot_id": dock_lot_id})

    sql2=("SELECT inventory_label, inventory_type, inventory_id, inventory_slot, resource_id, inventory_amount FROM inventories WHERE inventory_label = 6 AND inventory_id = %s" % ship_id)
    print(sql2)
    with con:
        cur = con.cursor()
        cur.execute("%s" % sql2)
        inventory_rows = cur.fetchall()
        cur.close()

    for inventory_row in inventory_rows:
        inventory_label=inventory_row[0]
        inventory_type=inventory_row[1]
        inventory_id=inventory_row[2]
        inventory_slot=inventory_row[3]
        resource_id=inventory_row[4]
        resource_amount=inventory_row[5]
        resource_name = parseProductType(resource_id)

        if inventory_slot == 1:
            slot1.append({"resource_id": resource_id, "resource_name": resource_name, "resource_amount": resource_amount})
        elif inventory_slot == 2:
            slot2.append({"resource_id": resource_id, "resource_name": resource_name, "resource_amount": resource_amount})


    resources.append({"slot_1": slot1, "slot_2": slot2})
    ship.append({"caller_address": caller_address, "crew_id": crew_id, "ship_id": ship_id, "ship_type": ship_type, "ship_type_name": ship_type_name, "emergency": emergency, "dock_label": dock_label, "dock_type": dock_type, "dock_asteroid_id": dock_asteroid_id, "dock_lot_id": dock_lot_id, "inventory": resources})

    return ship


def shipAssemblyState(parameter1, parameter2, state, start_block, end_block):

    assembly = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    assembly = getShipAssemblyState(con, parameter1, parameter2, state, start_block, end_block)
    con.close()
    return assembly


def ownedShips(parameter1, parameter2):

    owned_ships = None
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    asteroid_id = None
    owned_ships = getOwnedShips(con, parameter1, parameter2, asteroid_id)
    con.close()
    return owned_ships


def ownedShipsOnAsteroid(parameter1, parameter2, asteroid_id):

    owned_ships = None
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    owned_ships = getOwnedShips(con, parameter1, parameter2, asteroid_id)
    con.close()
    return owned_ships


def shipStatus(ship_id):

    ship = None
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    ship = getShipStatus(con, ship_id)
    con.close()
    return ship

