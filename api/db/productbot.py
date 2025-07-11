import sys
import os
import pymysql
import warnings
import traceback
import configparser
import time
import json

sys.path.insert(0,'../')
import db.get_types as inf
import db.fix_address as fix_address

filename = __file__
config_path = filename.split('/')[3]
config_file = "/home/bios/" + config_path + "/api.conf"

if os.path.exists(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    db_user = config.get('credentials', 'db_user')
    db_password = config.get('credentials', 'db_password')
    db = config.get('credentials', 'db')
    production_chain = config.get('production', 'json')
    base_url = config.get('url', 'base_url')

else:
    raise Exception(config_file)


def getAllProducts():


    products = [{'id': 1, 'name': 'Water'}, {'id': 2, 'name': 'Hydrogen'}, {'id': 3, 'name': 'Ammonia'}, {'id': 4, 'name': 'Nitrogen'}, {'id': 5, 'name': 'Sulfur Dioxide'}, {'id': 6, 'name': 'Carbon Dioxide'}, {'id': 7, 'name': 'Carbon Monoxide'}, {'id': 8, 'name': 'Methane'}, {'id': 9, 'name': 'Apatite'}, {'id': 10, 'name': 'Bitumen'}, {'id': 11, 'name': 'Calcite'}, {'id': 12, 'name': 'Feldspar'}, {'id': 13, 'name': 'Olivine'}, {'id': 14, 'name': 'Pyroxene'}, {'id': 15, 'name': 'Coffinite'}, {'id': 16, 'name': 'Merrillite'}, {'id': 17, 'name': 'Xenotime'}, {'id': 18, 'name': 'Rhabdite'}, {'id': 19, 'name': 'Graphite'}, {'id': 20, 'name': 'Taenite'}, {'id': 21, 'name': 'Troilite'}, {'id': 22, 'name': 'Uraninite'}, {'id': 23, 'name': 'Oxygen'}, {'id': 24, 'name': 'Deionized Water'}, {'id': 25, 'name': 'Raw Salts'}, {'id': 26, 'name': 'Silica'}, {'id': 27, 'name': 'Naphtha'}, {'id': 28, 'name': 'Sodium Bicarbonate'}, {'id': 29, 'name': 'Iron'}, {'id': 30, 'name': 'Copper'}, {'id': 31, 'name': 'Nickel'}, {'id': 32, 'name': 'Quicklime'}, {'id': 33, 'name': 'Acetylene'}, {'id': 34, 'name': 'Ammonium Carbonate'}, {'id': 35, 'name': 'Triple Superphosphate'}, {'id': 36, 'name': 'Phosphate And Sulfate Salts'}, {'id': 37, 'name': 'Iron Sulfide'}, {'id': 38, 'name': 'Lead Sulfide'}, {'id': 39, 'name': 'Tin Sulfide'}, {'id': 40, 'name': 'Molybdenum Disulfide'}, {'id': 41, 'name': 'Fused Quartz'}, {'id': 42, 'name': 'Fiberglass'}, {'id': 43, 'name': 'Bare Copper Wire'}, {'id': 44, 'name': 'Cement'}, {'id': 45, 'name': 'Sodium Chloride'}, {'id': 46, 'name': 'Potassium Chloride'}, {'id': 47, 'name': 'Borax'}, {'id': 48, 'name': 'Lithium Carbonate'}, {'id': 49, 'name': 'Magnesium Chloride'}, {'id': 50, 'name': 'Propylene'}, {'id': 51, 'name': 'Sulfur'}, {'id': 52, 'name': 'Steel'}, {'id': 53, 'name': 'Silicon'}, {'id': 54, 'name': 'Nitric Acid'}, {'id': 55, 'name': 'Sulfuric Acid'}, {'id': 56, 'name': 'Soil'}, {'id': 57, 'name': 'Ferrosilicon'}, {'id': 58, 'name': 'Weathered Olivine'}, {'id': 59, 'name': 'Oxalic Acid'}, {'id': 60, 'name': 'Silver'}, {'id': 61, 'name': 'Gold'}, {'id': 62, 'name': 'Tin'}, {'id': 63, 'name': 'Iron Oxide'}, {'id': 64, 'name': 'Spirulina And Chlorella Algae'}, {'id': 65, 'name': 'Molybdenum Trioxide'}, {'id': 66, 'name': 'Silica Powder'}, {'id': 67, 'name': 'Solder'}, {'id': 68, 'name': 'Fiber Optic Cable'}, {'id': 69, 'name': 'Steel Beam'}, {'id': 70, 'name': 'Steel Sheet'}, {'id': 71, 'name': 'Steel Pipe'}, {'id': 72, 'name': 'Steel Wire'}, {'id': 73, 'name': 'Acrylonitrile'}, {'id': 74, 'name': 'Polypropylene'}, {'id': 75, 'name': 'Magnesium'}, {'id': 76, 'name': 'Chlorine'}, {'id': 77, 'name': 'Sodium Carbonate'}, {'id': 78, 'name': 'Calcium Chloride'}, {'id': 79, 'name': 'Boria'}, {'id': 80, 'name': 'Lithium Sulfate'}, {'id': 81, 'name': 'Hydrochloric Acid'}, {'id': 82, 'name': 'Hydrofluoric Acid'}, {'id': 83, 'name': 'Phosphoric Acid'}, {'id': 84, 'name': 'Boric Acid'}, {'id': 85, 'name': 'Zinc Oxide'}, {'id': 86, 'name': 'Nickel Oxide'}, {'id': 87, 'name': 'Magnesia'}, {'id': 88, 'name': 'Alumina'}, {'id': 89, 'name': 'Sodium Hydroxide'}, {'id': 90, 'name': 'Potassium Hydroxide'}, {'id': 91, 'name': 'Soybeans'}, {'id': 92, 'name': 'Potatoes'}, {'id': 93, 'name': 'Ammonium Oxalate'}, {'id': 94, 'name': 'Rare Earth Sulfates'}, {'id': 95, 'name': 'Ferrochromium'}, {'id': 96, 'name': 'Yellowcake'}, {'id': 97, 'name': 'Alumina Ceramic'}, {'id': 98, 'name': 'Austenitic Nichrome'}, {'id': 99, 'name': 'Copper Wire'}, {'id': 100, 'name': 'Silicon Wafer'}, {'id': 101, 'name': 'Steel Cable'}, {'id': 102, 'name': 'Polyacrylonitrile'}, {'id': 103, 'name': 'Natural Flavorings'}, {'id': 104, 'name': 'Platinum'}, {'id': 105, 'name': 'Lithium Chloride'}, {'id': 106, 'name': 'Zinc'}, {'id': 107, 'name': 'Epichlorohydrin'}, {'id': 108, 'name': 'Bisphenol A'}, {'id': 109, 'name': 'Rare Earth Oxides'}, {'id': 110, 'name': 'Ammonium Chloride'}, {'id': 111, 'name': 'Aluminium'}, {'id': 112, 'name': 'Calcium'}, {'id': 113, 'name': 'Sodium Chromate'}, {'id': 114, 'name': 'Leached Coffinite'}, {'id': 115, 'name': 'Uranyl Nitrate'}, {'id': 116, 'name': 'Fluorine'}, {'id': 117, 'name': 'Sodium Tungstate'}, {'id': 118, 'name': 'Ferrite'}, {'id': 119, 'name': 'Diode'}, {'id': 120, 'name': 'Laser Diode'}, {'id': 121, 'name': 'Ball Valve'}, {'id': 122, 'name': 'Aluminium Beam'}, {'id': 123, 'name': 'Aluminium Sheet'}, {'id': 124, 'name': 'Aluminium Pipe'}, {'id': 125, 'name': 'Polyacrylonitrile Fabric'}, {'id': 126, 'name': 'Cold Gas Thruster'}, {'id': 127, 'name': 'Cold Gas Torque Thruster'}, {'id': 128, 'name': 'Carbon Fiber'}, {'id': 129, 'name': 'Food'}, {'id': 130, 'name': 'Small Propellant Tank'}, {'id': 131, 'name': 'Borosilicate Glass'}, {'id': 132, 'name': 'Ball Bearing'}, {'id': 133, 'name': 'Large Thrust Bearing'}, {'id': 134, 'name': 'Boron'}, {'id': 135, 'name': 'Lithium'}, {'id': 136, 'name': 'Epoxy'}, {'id': 137, 'name': 'Neodymium Oxide'}, {'id': 138, 'name': 'Yttria'}, {'id': 139, 'name': 'Sodium Dichromate'}, {'id': 140, 'name': 'Novolak Prepolymer Resin'}, {'id': 141, 'name': 'Ferromolybdenum'}, {'id': 142, 'name': 'Ammonium Diuranate'}, {'id': 143, 'name': 'Ammonium Paratungstate'}, {'id': 144, 'name': 'Engine Bell'}, {'id': 145, 'name': 'Steel Truss'}, {'id': 146, 'name': 'Aluminium Hull Plate'}, {'id': 147, 'name': 'Aluminium Truss'}, {'id': 148, 'name': 'Cargo Module'}, {'id': 149, 'name': 'Pressure Vessel'}, {'id': 150, 'name': 'Propellant Tank'}, {'id': 151, 'name': 'Stainless Steel'}, {'id': 152, 'name': 'Bare Circuit Board'}, {'id': 153, 'name': 'Ferrite Bead Inductor'}, {'id': 154, 'name': 'Core Drill Bit'}, {'id': 155, 'name': 'Core Drill Thruster'}, {'id': 156, 'name': 'Parabolic Dish'}, {'id': 157, 'name': 'Photovoltaic Panel'}, {'id': 158, 'name': 'Lipo Battery'}, {'id': 159, 'name': 'Neodymium Trichloride'}, {'id': 161, 'name': 'Chromia'}, {'id': 162, 'name': 'Photoresist Epoxy'}, {'id': 163, 'name': 'Uranium Dioxide'}, {'id': 164, 'name': 'Tungsten'}, {'id': 165, 'name': 'Shuttle Hull'}, {'id': 166, 'name': 'Light Transport Hull'}, {'id': 167, 'name': 'Cargo Ring'}, {'id': 168, 'name': 'Heavy Transport Hull'}, {'id': 169, 'name': 'Tungsten Powder'}, {'id': 170, 'name': 'Hydrogen Propellant'}, {'id': 171, 'name': 'Stainless Steel Sheet'}, {'id': 172, 'name': 'Stainless Steel Pipe'}, {'id': 173, 'name': 'Ccd'}, {'id': 174, 'name': 'Computer Chip'}, {'id': 175, 'name': 'Core Drill'}, {'id': 176, 'name': 'Neodymium'}, {'id': 178, 'name': 'Chromium'}, {'id': 179, 'name': 'Uranium Tetrafluoride'}, {'id': 180, 'name': 'Pure Nitrogen'}, {'id': 181, 'name': 'Nd Yag Laser Rod'}, {'id': 182, 'name': 'Nichrome'}, {'id': 183, 'name': 'Neodymium Magnet'}, {'id': 184, 'name': 'Unenriched Uranium Hexafluoride'}, {'id': 185, 'name': 'Highly Enriched Uranium Hexafluoride'}, {'id': 186, 'name': 'Nd Yag Laser'}, {'id': 187, 'name': 'Thin Film Resistor'}, {'id': 188, 'name': 'Highly Enriched Uranium Powder'}, {'id': 189, 'name': 'Leached Feldspar'}, {'id': 190, 'name': 'Roasted Rhabdite'}, {'id': 191, 'name': 'Rhabdite Slag'}, {'id': 192, 'name': 'Potassium Carbonate'}, {'id': 193, 'name': 'Hydrogen Heptafluorotantalate And Niobate'}, {'id': 194, 'name': 'Lead'}, {'id': 195, 'name': 'Potassium Fluoride'}, {'id': 196, 'name': 'Potassium Heptafluorotantalate'}, {'id': 197, 'name': 'Diepoxy Prepolymer Resin'}, {'id': 199, 'name': 'Tantalum'}, {'id': 200, 'name': 'Pedot'}, {'id': 201, 'name': 'Polymer Tantalum Capacitor'}, {'id': 202, 'name': 'Surface Mount Device Reel'}, {'id': 203, 'name': 'Circuit Board'}, {'id': 204, 'name': 'Brushless Motor Stator'}, {'id': 205, 'name': 'Brushless Motor Rotor'}, {'id': 206, 'name': 'Brushless Motor'}, {'id': 207, 'name': 'Landing Leg'}, {'id': 208, 'name': 'Landing Auger'}, {'id': 209, 'name': 'Pump'}, {'id': 210, 'name': 'Radio Antenna'}, {'id': 211, 'name': 'Fiber Optic Gyroscope'}, {'id': 212, 'name': 'Star Tracker'}, {'id': 213, 'name': 'Computer'}, {'id': 214, 'name': 'Control Moment Gyroscope'}, {'id': 215, 'name': 'Robotic Arm'}, {'id': 217, 'name': 'Beryllium Carbonate'}, {'id': 218, 'name': 'Beryllia'}, {'id': 219, 'name': 'Beryllia Ceramic'}, {'id': 220, 'name': 'Neon'}, {'id': 221, 'name': 'Heat Exchanger'}, {'id': 222, 'name': 'Turbopump'}, {'id': 224, 'name': 'Neon Fuel Separator Centrifuge'}, {'id': 225, 'name': 'Fuel Make Up Tank'}, {'id': 226, 'name': 'Neon Make Up Tank'}, {'id': 227, 'name': 'Lightbulb End Moderators'}, {'id': 229, 'name': 'Fused Quartz Lightbulb Tube'}, {'id': 230, 'name': 'Reactor Plumbing Assembly'}, {'id': 231, 'name': 'Flow Divider Moderator'}, {'id': 232, 'name': 'Nuclear Lightbulb'}, {'id': 233, 'name': 'Composite Overwrapped Reactor Shell'}, {'id': 234, 'name': 'Closed Cycle Gas Core Nuclear Reactor Engine'}, {'id': 235, 'name': 'Habitation Module'}, {'id': 236, 'name': 'Mobility Module'}, {'id': 237, 'name': 'Fluids Automation Module'}, {'id': 238, 'name': 'Solids Automation Module'}, {'id': 239, 'name': 'Terrain Interface Module'}, {'id': 240, 'name': 'Avionics Module'}, {'id': 241, 'name': 'Escape Module'}, {'id': 242, 'name': 'Attitude Control Module'}, {'id': 243, 'name': 'Power Module'}, {'id': 244, 'name': 'Thermal Module'}, {'id': 245, 'name': 'Propulsion Module'}, {'id': 'B1', 'name': 'Warehouse'}, {'id': 'B2', 'name': 'Extractor'}, {'id': 'B3', 'name': 'Refinery'}, {'id': 'B4', 'name': 'Bioreactor'}, {'id': 'B5', 'name': 'Factory'}, {'id': 'B6', 'name': 'Shipyard'}, {'id': 'B7', 'name': 'Spaceport'}, {'id': 'B8', 'name': 'Marketplace'}, {'id': 'B9', 'name': 'Habitat'}, {'id': 'S1', 'name': 'Light Transport'}, {'id': 'S2', 'name': 'Heavy Transport'}, {'id': 'S3', 'name': 'Shuttle'}]

    return products


def getProductionChain(con, product_id):

    result=[]
    product_data, finalized_production_chains = getComponents(product_id)
    exchange_asteroid_id, exchange_lot_id, price, amount, complexity, new_finalized_production_chains, product_mass, product_volume, product_category, processes = getPrices(con, product_data, finalized_production_chains, product_id)
    new_product_data=addUrl(product_data, exchange_asteroid_id, exchange_lot_id, price, amount, complexity, new_finalized_production_chains, product_mass, product_volume, product_category, processes)
    result.append({"product_data": new_product_data})
    return result
    

def addUrl(product_dict, exchange_asteroid_id, exchange_lot_id, price, amount, complexity, new_finalized_production_chains, product_mass, product_volume, product_category, processes):

    product_name = product_dict['product_name']
    product_type = product_dict['product_type']
    category = product_dict['category']
    mass = product_dict['weight']
    volume = product_dict['volume']
    quantized = product_dict['quantized']
    squeezed_spaces = product_name.replace(" ", "")
    image = squeezed_spaces + ".v1.png"
    image_url = base_url + image

    if product_volume == 0:
        product_volume = None

    new_product_dict = {'product_name': product_name, 'product_type': product_type, 'category': category, 'mass': product_mass, 'volume': product_volume, 'quantized': quantized, "asteroid_id": exchange_asteroid_id, "lot_id": exchange_lot_id, "exchange_price": price, "complexity": complexity, "image_url": image_url, "production_chains": processes}

    return new_product_dict


def getPrices(con, new_product_data, finalized_production_chains, product_id):

    if 'B' in product_id or 'S' in product_id:
        exchange_asteroid_id = None
        exchange_lot_id = None
        price = None
        amount = None
    else:
        exchange_asteroid_id, exchange_lot_id, price, amount = getFloor(con, product_id)

    complexity = 0
    build_your_own_price = 0
    processes = []
    for row in finalized_production_chains:
        process_id = row['process_id']
        process_name = row['process_name']
        building_id = row['building_id']
        building_name = row['building_name']
        mAdalianHoursPerSR = row['mAdalianHoursPerSR']
        bAdalianHoursPerAction = row['bAdalianHoursPerAction']
        process_score = row['process_score']
        inputs = row['inputs']
        outputs = row['outputs']

        new_finalized_production_chains = []
        for output_product in outputs:
            if output_product['product_id'] == product_id:
                product_type = output_product['product_type']
                if building_name == 'Extractor':
                    product_units_per_sr = 1
                else:
                    product_units_per_sr = int(output_product['unitsPerSR'])

                product_mass = output_product['weight']
                product_volume = output_product['volume']
                product_category = output_product['product_category']

                new_inputs = []
                for input_row in inputs:
                    new_input_row = []
                    input_asteroid_id = None
                    input_lot_id = None
                    input_price = None
                    input_amount = None
                    input_id = input_row['product_id']
                    input_name = input_row['product_name']
                    input_type = input_row['product_type']
                    input_category = input_row['product_category']
                    input_mass = input_row['product_weight']
                    input_volume = input_row['product_volume']
                    input_score = input_row['product_score']
                    complexity+=input_score
                    input_unitsPerSR = int(input_row['unitsPerSR'])
                    input_quantized = input_row['product_quantized']
                    input_asteroid_id, input_lot_id, input_price, input_amount = getFloor(con, input_id)
                    cost_for_materials = round(((input_unitsPerSR * input_price) / product_units_per_sr),3)
                    build_your_own_price+=cost_for_materials
                    squeezed_spaces = input_name.replace(" ", "")
                    image = squeezed_spaces + ".v1.png"
                    image_url = base_url + image
                    new_input_row = {"product_id": input_id, "product_name": input_name, "product_type": input_type, "product_category": input_category, "product_mass": input_mass, "product_volume": input_volume, "complexity": input_score, "unitsPerSR": input_unitsPerSR, "product_quantized": input_quantized, "asteroid_id": input_asteroid_id, "lot_id": input_lot_id, "floor_price_per_unit": input_price, "total_price": cost_for_materials, "image_url": image_url}
                    new_inputs.append(new_input_row)
                    new_finalized_production_chains.append(new_input_row)

                processes.append({"process_id": process_id, "process_name": process_name, "product_units_per_sr": product_units_per_sr, "build_your_own_price": build_your_own_price, "exchange_price": price, "inputs": new_inputs})

    return exchange_asteroid_id, exchange_lot_id, price, amount, complexity, new_finalized_production_chains, product_mass, product_volume, product_category, processes


def getFloor(con, product_id):

    exchange_asteroid_id = None
    exchange_lot_id = None
    price = 0
    amount = 0

    sql = ("SELECT exchange_asteroid_id, exchange_lot_id, price, amount FROM sell_orders WHERE product_id = %s AND amount > 0 ORDER BY price LIMIT 1" % product_id)
    print(sql)
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


def getBuildingScore(input_id, product_data):

    extractor_score = int(0)
    refinery_score = int(1)
    factory_score = int(1)
    shipyard_score = int(1)
    bioreactor_score = int(1)
    spaceport_score = int(0)
    marketplace_score = int(0)
    habitat_score = int(0)

    if product_data['product_type'] == 'Raw Material':
        building_score = extractor_score
    elif product_data['product_type'] == 'Refined Material':
        building_score = refinery_score
    elif product_data['product_type'] == 'Refined Metal':
        building_score = refinery_score
    elif product_data['product_type'] == 'Component':
        building_score = factory_score
    elif product_data['product_type'] == 'Ship Component':
        building_score = shipyard_score
    elif product_data['product_type'] == 'Finished Good':
        building_score = factory_score
    elif product_data['product_type'] == 'Ship':
        building_score = shipyard_score
    elif product_data['product_type'] == 'Building':
        building_score = 0


    return building_score


def getBuildingScore2(building_name):

    if building_name == "Extractor":
        building_score = int(0)
    elif building_name == "Refinery":
        building_score = int(1)
    elif building_name == "Factory":
        building_score = int(1)
    elif building_name == "Shipyard":
        building_score = int(1)
    elif building_name == "Bioreactor":
        building_score = int(1)
    else:
        building_score = int(0)

    return building_score


def processScore(missed_materials, finished_materials, product_scores, sorted_list, product_type):

    for row in sorted_list:
        if row['product_type'] == product_type:
            product_id = row['product_id']
            product_name = row['product_name']
            product_type = row['product_type']
            building_score = row['building_score']
            product_score = building_score
            inputs = row['inputs']
            count = 0
            for input_row in inputs:
                input_id = input_row['input_id']
                input_name = input_row['input_name']
                input_type = input_row['input_type']
                if input_id in product_scores:
                    product_score+=product_scores[input_id]
                else:
                    count+=1
                    missed_materials.append(input_id)

            if count == 0:
                if product_id not in product_scores:
                    product_scores.update({product_id: product_score})
                    finished_materials.append(product_id)
                    if product_id == missed_materials:
                        missed_materials.remove(product_id)

            else:
                missed_materials.append(product_id)

    return missed_materials, finished_materials, product_scores


def getProducts(category_id):

    if int(category_id) == 1:
        category_name = 'Raw Material'
    elif int(category_id) == 2:
        category_name = 'Refined Material'
    elif int(category_id) == 3:
        category_name = 'Refined Metal'
    elif int(category_id) == 4:
        category_name = 'Component'
    elif int(category_id) == 5:
        category_name = 'Ship Component'
    elif int(category_id) == 6:
        category_name = 'Finished Good'
    elif int(category_id) == 7:
        category_name = 'Ship'
    elif int(category_id) == 8:
        category_name = 'Building'

    f = open('production_chains.json')
    data = json.load(f)
    for key, value in data.items():
        if key == "buildings":
            buildings = value
        elif key == "products":
            products = value
        else:
            processes = value

    building_list = []
    for row in buildings:
        building_id = row['id']
        building_name = row['name']
        score = 0
        if building_name == 'Refinery':
            score = int(1)
        elif building_name == 'Factory':
            score = int(2)
        elif building_name == 'Shipyard':
            score = int(2)
        elif building_name == 'Bioreactor':
            score = int(2)

        building_list.append({"building_id": building_id, "building_name": building_name, "building_score": score})

    input_weights = {}
    product_list = []

    for row in products:
        if row['type'] == category_name:
            product_id = row['id']
            product_name = row['name']
            product_category = row['category']
            product_list.append({"product_id": product_id, "product_name": product_name, "category": product_category})

    return product_list


def getProductName(product_id):

    product_name = None
    f = open('production_chains.json')
    data = json.load(f)
    for key, value in data.items():
        if key == "products":
            products = value

    for row in products:
        if row['id'] == product_id:
            product_name = row['name']

    return product_name


def searchProducts(search_str):

    f = open('production_chains.json')
    data = json.load(f)
    for key, value in data.items():
        if key == "products":
            products = value

    search_str = search_str.lower()
    product_list = []
    for row in products:
        product_name = row['name']
        product_id = row['id']
        product_category = row['category']
        massKilogramsPerUnit = row['massKilogramsPerUnit']
        volumeLitersPerUnit = row['volumeLitersPerUnit']
        quantized = row['quantized']
        lower_product_name = product_name.lower()
        if search_str in lower_product_name:
            product_list.append({"product_id": product_id, "product_name": product_name, "category": product_category, "weight": massKilogramsPerUnit, "volume": volumeLitersPerUnit, "quantized": quantized})

    return product_list


def findProducts(search_input_id):

    f = open('production_chains.json')
    data = json.load(f)
    for key, value in data.items():
        if key == "buildings":
            buildings = value
        elif key == "products":
            products = value
        elif key == "processes":
            processes = value

    u_dict = {}
    u_list = []
    master_product_list, product_process_list, product_dict, product_list, unrefined_processes = getMasterLists()
    for row in master_product_list:
        if row['product_id'] == search_input_id:
            product_record = row
            used_in = row['used_in']
            for u_row in used_in:
                u_product_id = u_row['product_id']
                u_product_name = u_row['product_name']
                u_product_type = u_row['product_type']
                u_product_category = u_row['category']
                u_massKilogramsPerUnit = u_row['massKilogramsPerUnit']
                u_volumeLitersPerUnit = u_row['volumeLitersPerUnit']
                u_quantized = u_row['quantized']
                u_dict = {"product_id": u_product_id, "product_name": u_product_name, "product_type": u_product_type, "category": u_product_category, "weight": u_massKilogramsPerUnit, "volume": u_volumeLitersPerUnit, "quantized": u_quantized}
                u_list.append(u_dict)

    product_dupes = []
    return_dict = {}
    return_list = []
    for row in u_list:
        product_id = row['product_id']
        product_name = row['product_name']
        product_type = row['product_type']
        product_category = row['category']
        massKilogramsPerUnit = row['weight']
        volumeLitersPerUnit = row['volume']
        quantized = row['quantized']

        for record in master_product_list:
            if record['product_id'] == product_id:
                product_score = record['product_score']

        return_dict = {"product_id": product_id, "product_name": product_name, "product_type": product_type, "product_score": product_score, "category": product_category, "weight": massKilogramsPerUnit, "volume": volumeLitersPerUnit, "quantized": quantized}

        if product_id not in product_dupes:
            return_list.append(return_dict)
            product_dupes.append(product_id)

    sorted_return_list = sorted(return_list, key = lambda i: i['product_id'])
    return sorted_return_list


def getComponents(component_id):

    master_product_list, product_process_list, product_dict, product_list, unrefined_processes = getMasterLists()

    for key, value in product_dict.items():
        if key == component_id:
            processes = value['processes']

    for i_row in product_list:
        for i_key, i_value in i_row.items():
            if i_key == component_id:
                product_data = i_value

    revised_process_list = []
    for process_row in processes:
        p_inputs_list = []
        process_dict = {}
        process_id = process_row['process_id']
        process_name = process_row['process_name']
        mAdalianHoursPerSR = process_row['mAdalianHoursPerSR']
        bAdalianHoursPerAction = process_row['bAdalianHoursPerAction']
        process_dupes = []
        for pp_row in product_process_list:
            if pp_row['process_id'] == process_id:
                if process_id not in process_dupes:
                    process_dupes.append(process_id)
                    revised_process_list.append(pp_row)

    finalized_production_chains = []
    for row in revised_process_list:
        r_process_name = row['process_name']
        r_process_id = row['process_id']
        r_building_id = row['building_id']
        r_building_name = row['building_name']
        r_mAdalianHoursPerSR = row['mAdalianHoursPerSR']
        r_bAdalianHoursPerAction = row['bAdalianHoursPerAction']
        inputs = row['inputs']
        process_inputs = []
        process_score = 0
        for input_row in inputs:
            mp_dupes = []
            r_input_id = input_row['input_id']
            r_input_name = input_row['input_name']
            r_input_type = input_row['input_type']
            r_input_category = input_row['category']
            r_input_weight = input_row['weight']
            r_input_volume = input_row['volume']
            r_input_quantized = input_row['quantized']
            r_input_unitsPerSR = input_row['unitsPerSR']

            for mp_row in master_product_list:
                if mp_row['product_id'] == r_input_id:
                    mp_product_score = mp_row['product_score']
                    mp_dupes.append({"product_id": r_input_id, "product_score": mp_product_score})

            sorted_mp_dupes = sorted(mp_dupes, key = lambda i: i['product_score'])
            r_product_score = sorted_mp_dupes[0]['product_score']
            process_score+=r_product_score
            process_inputs.append({"product_id": r_input_id, "product_name": r_input_name, "product_type": r_input_type, "product_category": r_input_category, "product_weight": r_input_weight, "product_volume": r_input_volume, "product_score": sorted_mp_dupes[0]['product_score'], "unitsPerSR": r_input_unitsPerSR, "product_quantized": r_input_quantized })

        for u_row in unrefined_processes:
            if u_row['id'] == r_process_id:
                add_outputs = []
                additional_outputs = u_row['outputs']
                for add_output_row in additional_outputs:
                    add_output_id = add_output_row['productId']
                    add_unitsPerSR = add_output_row['unitsPerSR']
                    for add_product_row in product_list:
                        for add_key, add_value in add_product_row.items():
                            if add_key == add_output_id:
                                add_product_name = add_value['product_name']
                                add_product_type = add_value['product_type']
                                add_product_category = add_value['category']
                                add_product_weight = add_value['weight']
                                add_product_volume = add_value['volume']
                                add_outputs.append({"product_id": add_output_id, "product_name": add_product_name, "product_type": add_product_type, "weight": add_product_weight, "volume": add_product_volume, "unitsPerSR": add_unitsPerSR, "product_category": add_product_category})

        finalized_production_chains.append({"process_id": r_process_id, "process_name": r_process_name, "building_id": r_building_id, "building_name": r_building_name, "mAdalianHoursPerSR": r_mAdalianHoursPerSR, "bAdalianHoursPerAction": r_bAdalianHoursPerAction, "process_score": process_score, "inputs": process_inputs, "outputs": add_outputs})

    return product_data, finalized_production_chains


def updateProductDict(product_dict, processes_per_product):

    new_product_dict={}
    for key, value in product_dict.items():
        product_id = key
        product_name = value['product_name']
        product_type = value['product_type']
        meh_process_id = value['process_id']
        meh_process_name = value['process_name']
        building_id = value['building_id']
        building_name = value['building_name']
        inputs = value['inputs']
        meh_mAdalianHoursPerSR = value['mAdalianHoursPerSR']
        meh_bAdalianHoursPerAction = value['bAdalianHoursPerAction']
        components = value['components']
        processes = []
        for row in processes_per_product:
            if row['product_id'] == product_id:
                process_id = row['process_id']
                process_name = row['process_name']
                building_id = row['building_id']
                building_name = row['building_name']
                mAdalianHoursPerSR = row['mAdalianHoursPerSR']
                bAdalianHoursPerAction = row['bAdalianHoursPerAction']
                processes.append({"process_id": process_id, "process_name": process_name, "building_id": building_id, "building_name": building_name, "mAdalianHoursPerSR": mAdalianHoursPerSR, "bAdalianHoursPerAction": bAdalianHoursPerAction})

        new_product_dict[product_id] = {"product_id": product_id, "product_name": product_name, "product_type": product_type, "process_id": meh_process_id, "process_name": meh_process_name, "building_id": building_id, "building_name": building_name, "inputs": inputs, "mAdalianHoursPerSR": meh_mAdalianHoursPerSR, "bAdalianHoursPerAction": meh_bAdalianHoursPerAction, "components": components, "processes": processes}

    return new_product_dict


def getMasterLists():

    f = open(production_chain)
    data = json.load(f)
    for key, value in data.items():
        if key == "buildings":
            buildings = value
        elif key == "products":
            products = value
        elif key == "processes":
            processes = value

    category_dict = {}
    kilo_dict = {}
    liter_dict = {}
    quantized_dict = {}
    building_list = []
    for row in buildings:
        building_id = row['id']
        building_name = row['name']
        building_list.append({"building_id": building_id, "building_name": building_name})

    product_list = []
    for row in products:
        product_id = row['id']
        product_name = row['name']
        product_type = row['type']
        product_category = row['category']
        massKilogramsPerUnit = row['massKilogramsPerUnit']
        volumeLitersPerUnit = row['volumeLitersPerUnit']
        quantized = row['quantized']
        product_list.append({product_id: {"product_name": product_name, "product_type": product_type, "category": product_category, "weight": massKilogramsPerUnit, "volume": volumeLitersPerUnit, "quantized": quantized}})

        category_dict.update({product_id: product_category})
        kilo_dict.update({product_id: massKilogramsPerUnit})
        liter_dict.update({product_id: volumeLitersPerUnit})
        quantized_dict.update({product_id: quantized})

    process_list = []
    product_process_list = []
    product_dict = {}
    output_dupes = {}
    disco_list = []
    process_id = None
    process_name = None
    for row in processes:
        process_id = row['id']
        process_name = row['name']
        building_id = row['buildingId']
        mAdalianHoursPerSR = row['mAdalianHoursPerSR']
        bAdalianHoursPerAction =row['bAdalianHoursPerAction']
        inputs = row['inputs']
        outputs = row['outputs']

        for building in building_list:
            if building['building_id'] == building_id:
                building_name = building['building_name']

        input_list=[]
        output_list=[]
        for product_input in inputs:
            input_id=product_input['productId']
            product_score = int(0)
            unitsPerSR = product_input['unitsPerSR']
            for product_row in product_list:
                for key, value in product_row.items():
                    if key == input_id:
                        building_score=int(getBuildingScore(input_id, value))
                        input_category = category_dict[input_id]
                        input_massKilogramsPerUnit = kilo_dict[input_id]
                        input_volumeLitersPerUnit = liter_dict[input_id]
                        input_quantized = quantized_dict[input_id]
                        input_list.append({"input_id": input_id, "input_name": value['product_name'], "input_type": value['product_type'], "building_score": building_score, "product_score": product_score, "category": input_category, "weight": input_massKilogramsPerUnit, "volume": input_volumeLitersPerUnit, "quantized": input_quantized, "unitsPerSR": unitsPerSR})

        for product_output in outputs:
            output_id = product_output['productId']
            unitsPerSR = product_output['unitsPerSR']
            for product_row in product_list:
                for key, value in product_row.items():
                    if key == output_id:
                        if output_id in output_dupes:
                            output_dupes[output_id]+=1
                        else:
                            output_dupes.update({output_id: 1})

                        output_category = category_dict[output_id]
                        output_massKilogramsPerUnit = kilo_dict[output_id]
                        output_volumeLitersPerUnit = liter_dict[output_id]
                        output_quantized = quantized_dict[output_id]
                        output_list.append({"output_id": output_id, "output_name": value['product_name'], "output_type": value['product_type'], "category": output_category, "weight": output_massKilogramsPerUnit, "volume": output_volumeLitersPerUnit, "quantized": output_quantized, "unitsPerSR": unitsPerSR})

        output_id = None
        for row in output_list:
            output_id = row['output_id']
            building_score=getBuildingScore2(building_name)
            process_list.append({row['output_id']: {"product_id": row['output_id'], "product_name": row['output_name'], "product_type": row['output_type'], "process_id": process_id, "process_name": process_name, "building_id": building_id, "building_name": building_name, "inputs": input_list, "outputs": output_list, "mAdalianHoursPerSR": mAdalianHoursPerSR, "bAdalianHoursPerAction": bAdalianHoursPerAction}})
            disco_list.append({"output_id": row['output_id'], "product_id": row['output_id'], "product_name": row['output_name'], "product_type": row['output_type'], "process_id": process_id, "process_name": process_name, "building_id": building_id, "building_name": building_name, "building_score": building_score, "inputs": input_list, "mAdalianHoursPerSR": mAdalianHoursPerSR, "bAdalianHoursPerAction": bAdalianHoursPerAction})
            product_dict[output_id] = {"product_id": row['output_id'], "product_name": row['output_name'], "product_type": row['output_type'], "process_id": process_id, "process_name": process_name, "building_id": building_id, "building_name": building_name, "inputs": input_list, "mAdalianHoursPerSR": mAdalianHoursPerSR, "bAdalianHoursPerAction": bAdalianHoursPerAction}
            product_dict[output_id]['components'] = {}
            product_process_list.append(product_dict[output_id])


    processes_per_product = []
    for product_row in products:
        product_id = product_row['id']
        product_name = product_row['name']
        for row in process_list:
            for process_key, process_value in row.items():
                if process_value['product_id'] == product_id:
                    ex_process_id = process_value['process_id']
                    ex_process_name = process_value['process_name']
                    ex_product_type = process_value['product_type']
                    ex_building_id = process_value['building_id']
                    ex_building_name = process_value['building_name']
                    ex_mAdalianHoursPerSR = process_value['mAdalianHoursPerSR']
                    ex_bAdalianHoursPerAction = process_value['bAdalianHoursPerAction']
                    processes_per_product.append({"product_id": product_id, "process_id": ex_process_id, "process_name": ex_process_name, "building_id": ex_building_id, "building_name": ex_building_name, "mAdalianHoursPerSR": ex_mAdalianHoursPerSR, "bAdalianHoursPerAction": ex_bAdalianHoursPerAction})

    product_dict = updateProductDict(product_dict, processes_per_product)
    finished_materials = []
    product_scores = {}
    process_scores = {}
    sorted_disco_list = sorted(disco_list, key = lambda i: i['output_id'])
    for row in sorted_disco_list:
        process_id = row['process_id']
        if row['product_type'] == 'Raw Material':
            product_id = row['product_id']
            building_score = row['building_score']
            if product_id not in product_scores:
                product_scores.update({product_id: (building_score + 1)})
                finished_materials.append(product_id)

    missed_materials = []

    # process refined materials
    missed_materials, finished_materials, product_score = processScore(missed_materials, finished_materials, product_scores, sorted_disco_list, 'Refined Material')
    missed_materials, finished_materials, product_score = processScore(missed_materials, finished_materials, product_scores, sorted_disco_list, 'Refined Material')
    missed_materials, finished_materials, product_score = processScore(missed_materials, finished_materials, product_scores, sorted_disco_list, 'Refined Material')
    missed_materials, finished_materials, product_score = processScore(missed_materials, finished_materials, product_scores, sorted_disco_list, 'Refined Material')
    missed_materials, finished_materials, product_score = processScore(missed_materials, finished_materials, product_scores, sorted_disco_list, 'Refined Material')

    # process refined metals
    missed_materials = []
    missed_materials, finished_materials, product_score = processScore(missed_materials, finished_materials, product_scores, sorted_disco_list, 'Refined Metal')
    missed_materials, finished_materials, product_score = processScore(missed_materials, finished_materials, product_scores, sorted_disco_list, 'Refined Metal')

    # process components
    missed_materials = []
    missed_materials, finished_materials, product_score = processScore(missed_materials, finished_materials, product_scores, sorted_disco_list, 'Component')
    missed_materials, finished_materials, product_score = processScore(missed_materials, finished_materials, product_scores, sorted_disco_list, 'Component')
    missed_materials, finished_materials, product_score = processScore(missed_materials, finished_materials, product_scores, sorted_disco_list, 'Component')
    missed_materials, finished_materials, product_score = processScore(missed_materials, finished_materials, product_scores, sorted_disco_list, 'Component')

    # process ship components
    missed_materials, finished_materials, product_score = processScore(missed_materials, finished_materials, product_scores, sorted_disco_list, 'Ship Component')
    missed_materials, finished_materials, product_score = processScore(missed_materials, finished_materials, product_scores, sorted_disco_list, 'Ship Component')

    # process ships
    missed_materials, finished_materials, product_score = processScore(missed_materials, finished_materials, product_scores, sorted_disco_list, 'Ship')
    missed_materials, finished_materials, product_score = processScore(missed_materials, finished_materials, product_scores, sorted_disco_list, 'Ship')

    # process finished goods
    missed_materials, finished_materials, product_score = processScore(missed_materials, finished_materials, product_scores, sorted_disco_list, 'Finished Good')
    missed_materials, finished_materials, product_score = processScore(missed_materials, finished_materials, product_scores, sorted_disco_list, 'Finished Good')

    # process buildings
    missed_materials, finished_materials, product_score = processScore(missed_materials, finished_materials, product_scores, sorted_disco_list, 'Building')
    missed_materials, finished_materials, product_score = processScore(missed_materials, finished_materials, product_scores, sorted_disco_list, 'Building')

    # one more pass
    missed_materials, finished_materials, product_score = processScore(missed_materials, finished_materials, product_scores, sorted_disco_list, 'Refined Material')
    missed_materials, finished_materials, product_score = processScore(missed_materials, finished_materials, product_scores, sorted_disco_list, 'Refined Metal')
    missed_materials, finished_materials, product_score = processScore(missed_materials, finished_materials, product_scores, sorted_disco_list, 'Component')
    missed_materials, finished_materials, product_score = processScore(missed_materials, finished_materials, product_scores, sorted_disco_list, 'Ship Component')
    missed_materials, finished_materials, product_score = processScore(missed_materials, finished_materials, product_scores, sorted_disco_list, 'Ship')
    missed_materials, finished_materials, product_score = processScore(missed_materials, finished_materials, product_scores, sorted_disco_list, 'Finished Good')
    missed_materials, finished_materials, product_score = processScore(missed_materials, finished_materials, product_scores, sorted_disco_list, 'Building')


    master_process_dict = {}
    for row in process_list:
        process_id = None
        process_name = None
        for key, value in row.items():
            input_dict = {}
            output_dict = {}
            output_list = []
            input_list = []
            output_dupes = []
            total_input_score = 0
            total_output_score = 0
            product_id = value['product_id']
            product_name = value['product_name']
            product_type = value['product_type']
            process_id = value['process_id']
            process_name = value['process_name']
            building_name = value['building_name']
            building_id = value['building_id']
            mAdalianHoursPerSR = value['mAdalianHoursPerSR']
            bAdalianHoursPerAction = value['bAdalianHoursPerAction']
            inputs = value['inputs']
            outputs = value['outputs']
            for input_data in inputs:
                input_id = input_data['input_id']
                input_name = input_data['input_name']
                input_type = input_data['input_type']
                input_category = input_data['category']
                input_massKilogramsPerUnit = input_data['weight']
                input_volumeLitersPerUnit = input_data['volume']
                input_quantized = input_data['quantized']
                input_unitsPerSR = input_data['unitsPerSR']
                input_score = product_scores[input_id]
                total_input_score+=input_score
                input_dict = {"input_id": input_id, "input_name": input_name, "input_type": input_type, "input_score": int(input_score), "input_category": input_category, "input_massKilogramsPerUnit": input_massKilogramsPerUnit, "input_volumeLitersPerUnit": input_volumeLitersPerUnit, "input_quantized": input_quantized, "input_unitsPerSR": input_unitsPerSR}
                input_list.append(input_dict)
                input_dict = {}
            for output_data in outputs:
                output_id = output_data['output_id']
                output_name = output_data['output_name']
                output_type = output_data['output_type']
                output_category = output_data['category']
                output_massKilogramsPerUnit = output_data['weight']
                output_volumeLitersPerUnit = output_data['volume']
                output_quantized = output_data['quantized']
                output_unitsPerSR = output_data['unitsPerSR']
                output_score = product_scores[output_id]
                if output_id not in output_dupes:
                    total_output_score+=output_score
                    output_dupes.append(output_id)
                output_dict = {"output_id": output_id, "output_name": output_name, "input_type": output_type, "output_score": int(output_score), "output_category": output_category, "output_massKilogramsPerUnit": output_massKilogramsPerUnit, "output_volumeLitersPerUnit": output_volumeLitersPerUnit, "output_quantized": output_quantized, "output_unitsPerSR": output_unitsPerSR}
                output_list.append(output_dict)
                output_dict = {}

        master_process_dict[process_id] = {"process_id": process_id, "process_name": process_name, "building_name": building_name, "building_id": int(building_id), "input_score": int(total_input_score), "inputs": input_list, "outputs": output_list, "mAdalianHoursPerSR": mAdalianHoursPerSR, "bAdalianHoursPerAction": bAdalianHoursPerAction}

    master_product_dict = {}
    master_product_list = []

    for row in sorted_disco_list:
        input_dict = {}
        input_list = []
        input_score = 0
        total_score = 0
        product_id = row['output_id']
        product_name = row['product_name']
        product_type = row['product_type']
        process_id = row['process_id']
        process_name = row['process_name']
        building_id = row['building_id']
        building_name = row['building_name']
        building_score = row['building_score']
        mAdalianHoursPerSR = row['mAdalianHoursPerSR']
        bAdalianHoursPerAction = row['bAdalianHoursPerAction']
        inputs = row['inputs']
        for input_data in inputs:
            input_id = input_data['input_id']
            input_name = input_data['input_name']
            input_type = input_data['input_type']
            input_category = input_data['category']
            input_massKilogramsPerUnit = input_data['weight']
            input_volumeLitersPerUnit = input_data['volume']
            input_quantized = input_data['quantized']
            input_unitsPerSR = input_data['unitsPerSR']
            input_score = product_scores[input_id]
            total_score+=input_score
            input_dict = {"input_id": input_id, "input_name": input_name, "input_type": input_type, "input_score": int(input_score), "input_category": input_category, "input_massKilogramsPerUnit": input_massKilogramsPerUnit, "input_volumeLitersPerUnit": input_volumeLitersPerUnit, "input_quantized": input_quantized, "input_unitsPerSR": input_unitsPerSR}
            input_list.append(input_dict)

        total_score+=building_score


        full_products = []
        full_products_list = []
        full_products_dict = {}
        for process_row in processes:
            process_id = process_row['id']
            process_name = process_row['name']
            building_id = process_row['buildingId']
            inputs = process_row['inputs']
            outputs = process_row['outputs']
            mAdalianHoursPerSR = process_row['mAdalianHoursPerSR']
            bAdalianHoursPerAction = process_row['bAdalianHoursPerAction']

            output_list=[]
            for product_input in inputs:
                input_id=product_input['productId']
                if input_id == product_id:
                    for product_output in outputs:
                        output_id=product_output['productId']
                        for product_row in product_list:
                            for key, value in product_row.items():
                                if key == output_id:
                                    product_origin_dict = value

                        p_product_type = product_origin_dict['product_type']
                        p_product_name = product_origin_dict['product_name']
                        p_category = product_origin_dict['category']
                        p_massKilogramsPerUnit = product_origin_dict['weight']
                        p_volumeLitersPerUnit = product_origin_dict['volume']
                        p_quantized = product_origin_dict['quantized']

                        full_products_list.append({"product_id": output_id, "product_name": p_product_name, "product_type": p_product_type, "category": p_category, "massKilogramsPerUnit": p_massKilogramsPerUnit, "volumeLitersPerUnit": p_volumeLitersPerUnit, "quantized": p_quantized})

        full_products_len=len(full_products_list)
        master_product_list.append({"product_id": product_id, "product_name": product_name, "product_type": product_type, "process_id": int(process_id), "process_name": process_name, "building_id": int(building_id), "building_name": building_name, "product_score": int(total_score), "usage_count": int(full_products_len), "inputs": input_list, "used_in": full_products_list})

    return master_product_list, product_process_list, product_dict, product_list, processes


def allProducts():

    result = []
    result = getAllProducts()
    return result


def productsByCategory(category_id):

    result = []
    result = getProducts(category_id)
    return result


def getChain(product_id):
    result = []
    con = pymysql.connect("127.0.0.1", db_user, db_password, db)
    result = getProductionChain(con, product_id)
    con.close()
    return result
