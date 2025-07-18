def getLightTransport():
    components=[{"id": "166", "name": "light_transport_hull", "amount": "1"},
            {"id": "239","name": "terrain_interface_module", "amount": "4"},
            {"id": "240","name": "avionics_module", "amount": "1"},
            {"id": "241","name": "escape_module", "amount": "1"},
            {"id": "242","name": "attitude_control_module", "amount": "2"},
            {"id": "243","name": "power_module", "amount": "2"},
            {"id": "244","name": "thermal_module", "amount": "1"},
            {"id": "245","name": "propulsion_module", "amount": "2"},
            {"id": "148","name": "cargo_module", "amount": "6"}]
    return components

def getHeavyTransport():
    components=[{"id": "168", "name": "heavy_transport_hull", "amount": "1"},
            {"id": "240","name": "avionics_module", "amount": "3"},
            {"id": "241","name": "escape_module", "amount": "1"},
            {"id": "242","name": "attitude_control_module", "amount": "6"},
            {"id": "243","name": "power_module", "amount": "3"},
            {"id": "244","name": "thermal_module", "amount": "3"},
            {"id": "245","name": "propulsion_module", "amount": "9"},
            {"id": "148","name": "cargo_module", "amount": "36"}]
    return components


def getShuttle():
    components=[{"id": "165", "name": "shuttle_hull", "amount": "1"},
            {"id": "240","name": "avionics_module", "amount": "1"},
            {"id": "241","name": "escape_module", "amount": "3"},
            {"id": "242","name": "attitude_control_module", "amount": "1"},
            {"id": "243","name": "power_module", "amount": "1"},
            {"id": "244","name": "thermal_module", "amount": "1"},
            {"id": "245","name": "propulsion_module", "amount": "1"}]
    return components


def getRawMaterial(product_id, spectral_type):
    products=[{'id': '1', 'name': 'Water', 'mass': '1', 'quantized': False, 'type': 'C'},
            {'id': '2', 'name': 'Hydrogen', 'mass': '1', 'quantized': False, 'type': 'I'},
            {'id': '3', 'name': 'Ammonia', 'mass': '1', 'quantized': False, 'type': 'I'},
            {'id': '4', 'name': 'Nitrogen', 'mass': '1', 'quantized': False, 'type': 'I'},
            {'id': '5', 'name': 'Sulfur Dioxide', 'mass': '1', 'quantized': False, 'type': 'I'},
            {'id': '6', 'name': 'Carbon Dioxide', 'mass': '1', 'quantized': False, 'type': 'C'},
            {'id': '7', 'name': 'Carbon Monoxide', 'mass': '1', 'quantized': False, 'type': 'C'},
            {'id': '8', 'name': 'Methane', 'mass': '1', 'quantized': False, 'type': 'C'},
            {'id': '9', 'name': 'Apatite', 'mass': '1', 'quantized': False, 'type': 'C'},
            {'id': '10', 'name': 'Bitumen', 'mass': '1', 'quantized': False, 'type': 'C'},
            {'id': '11', 'name': 'Calcite', 'mass': '1', 'quantized': False, 'type': 'C'},
            {'id': '12', 'name': 'Feldspar', 'mass': '1', 'quantized': False, 'type': 'S'},
            {'id': '13', 'name': 'Olivine', 'mass': '1', 'quantized': False, 'type': 'S'},
            {'id': '14', 'name': 'Pyroxene', 'mass': '1', 'quantized': False, 'type': 'S'},
            {'id': '15', 'name': 'Coffinite', 'mass': '1', 'quantized': False, 'type': 'S'},
            {'id': '16', 'name': 'Merrillite', 'mass': '1', 'quantized': False, 'type': 'S'},
            {'id': '17', 'name': 'Xenotime', 'mass': '1', 'quantized': False, 'type': 'S'},
            {'id': '18', 'name': 'Rhabdite', 'mass': '1', 'quantized': False, 'type': 'M'},
            {'id': '19', 'name': 'Graphite', 'mass': '1', 'quantized': False, 'type': 'M'},
            {'id': '20', 'name': 'Taenite', 'mass': '1', 'quantized': False, 'type': 'M'},
            {'id': '21', 'name': 'Troilite', 'mass': '1', 'quantized': False, 'type': 'M'},
            {'id': '22', 'name': 'Uraninite', 'mass': '1', 'quantized': False, 'type': 'M'}]

    for row in products:
        if int(row['id']) == int(product_id):
            print(row)
            if row['type'] == spectral_type:
                return int(row['mass'])
            else:
                return None


def getMass(product_id):
    products=[{'id': '1', 'name': 'Water', 'mass': '1', 'quantized': False},
    {'id': '2', 'name': 'Hydrogen', 'mass': '1', 'quantized': False},
    {'id': '3', 'name': 'Ammonia', 'mass': '1', 'quantized': False},
    {'id': '4', 'name': 'Nitrogen', 'mass': '1', 'quantized': False},
    {'id': '5', 'name': 'Sulfur Dioxide', 'mass': '1', 'quantized': False},
    {'id': '6', 'name': 'Carbon Dioxide', 'mass': '1', 'quantized': False},
    {'id': '7', 'name': 'Carbon Monoxide', 'mass': '1', 'quantized': False},
    {'id': '8', 'name': 'Methane', 'mass': '1', 'quantized': False},
    {'id': '9', 'name': 'Apatite', 'mass': '1', 'quantized': False},
    {'id': '10', 'name': 'Bitumen', 'mass': '1', 'quantized': False},
    {'id': '11', 'name': 'Calcite', 'mass': '1', 'quantized': False},
    {'id': '12', 'name': 'Feldspar', 'mass': '1', 'quantized': False},
    {'id': '13', 'name': 'Olivine', 'mass': '1', 'quantized': False},
    {'id': '14', 'name': 'Pyroxene', 'mass': '1', 'quantized': False},
    {'id': '15', 'name': 'Coffinite', 'mass': '1', 'quantized': False},
    {'id': '16', 'name': 'Merrillite', 'mass': '1', 'quantized': False},
    {'id': '17', 'name': 'Xenotime', 'mass': '1', 'quantized': False},
    {'id': '18', 'name': 'Rhabdite', 'mass': '1', 'quantized': False},
    {'id': '19', 'name': 'Graphite', 'mass': '1', 'quantized': False},
    {'id': '20', 'name': 'Taenite', 'mass': '1', 'quantized': False},
    {'id': '21', 'name': 'Troilite', 'mass': '1', 'quantized': False},
    {'id': '22', 'name': 'Uraninite', 'mass': '1', 'quantized': False},
    {'id': '23', 'name': 'Oxygen', 'mass': '1', 'quantized': False},
    {'id': '24', 'name': 'Deionized Water', 'mass': '1', 'quantized': False},
    {'id': '25', 'name': 'Salts', 'mass': '1', 'quantized': False},
    {'id': '26', 'name': 'Silica', 'mass': '1', 'quantized': False},
    {'id': '27', 'name': 'Naphtha', 'mass': '1', 'quantized': False},
    {'id': '28', 'name': 'Sodium Bicarbonate', 'mass': '1', 'quantized': False},
    {'id': '29', 'name': 'Iron', 'mass': '1', 'quantized': False},
    {'id': '30', 'name': 'Copper', 'mass': '1', 'quantized': False},
    {'id': '31', 'name': 'Nickel', 'mass': '1', 'quantized': False},
    {'id': '32', 'name': 'Quicklime', 'mass': '1', 'quantized': False},
    {'id': '33', 'name': 'Acetylene', 'mass': '1', 'quantized': False},
    {'id': '34', 'name': 'Ammonium Carbonate', 'mass': '1', 'quantized': False},
    {'id': '35', 'name': 'Triple Superphosphate', 'mass': '1', 'quantized': False},
    {'id': '36', 'name': 'Phosphate and Sulfate Salts', 'mass': '1', 'quantized': False},
    {'id': '37', 'name': 'Iron Sulfide', 'mass': '1', 'quantized': False},
    {'id': '38', 'name': 'Lead Sulfide', 'mass': '1', 'quantized': False},
    {'id': '39', 'name': 'Tin Sulfide', 'mass': '1', 'quantized': False},
    {'id': '40', 'name': 'Molybdenum Disulfide', 'mass': '1', 'quantized': False},
    {'id': '41', 'name': 'Fused Quartz', 'mass': '1', 'quantized': False},
    {'id': '42', 'name': 'Fiberglass', 'mass': '1', 'quantized': False},
    {'id': '43', 'name': 'Bare Copper Wire', 'mass': '1', 'quantized': False},
    {'id': '44', 'name': 'Cement', 'mass': '1', 'quantized': False},
    {'id': '45', 'name': 'Sodium Chloride', 'mass': '1', 'quantized': False},
    {'id': '46', 'name': 'Potassium Chloride', 'mass': '1', 'quantized': False},
    {'id': '47', 'name': 'Borax', 'mass': '1', 'quantized': False},
    {'id': '48', 'name': 'Lithium Carbonate', 'mass': '1', 'quantized': False},
    {'id': '49', 'name': 'Magnesium Chloride', 'mass': '1', 'quantized': False},
    {'id': '50', 'name': 'Propylene', 'mass': '1', 'quantized': False},
    {'id': '51', 'name': 'Sulfur', 'mass': '1', 'quantized': False},
    {'id': '52', 'name': 'Steel', 'mass': '1', 'quantized': False},
    {'id': '53', 'name': 'Silicon', 'mass': '1', 'quantized': False},
    {'id': '54', 'name': 'Nitric Acid', 'mass': '1', 'quantized': False},
    {'id': '55', 'name': 'Sulfuric Acid', 'mass': '1', 'quantized': False},
    {'id': '56', 'name': 'Soil', 'mass': '1', 'quantized': False},
    {'id': '57', 'name': 'Ferrosilicon', 'mass': '1', 'quantized': False},
    {'id': '58', 'name': 'Weathered Olivine', 'mass': '1', 'quantized': False},
    {'id': '59', 'name': 'Oxalic Acid', 'mass': '1', 'quantized': False},
    {'id': '60', 'name': 'Silver', 'mass': '1', 'quantized': False},
    {'id': '61', 'name': 'Gold', 'mass': '1', 'quantized': False},
    {'id': '62', 'name': 'Tin', 'mass': '1', 'quantized': False},
    {'id': '63', 'name': 'Iron Oxide', 'mass': '1', 'quantized': False},
    {'id': '64', 'name': 'Spirulina and Chlorella Algae', 'mass': '1', 'quantized': False},
    {'id': '65', 'name': 'Molybdenum Trioxide', 'mass': '1', 'quantized': False},
    {'id': '66', 'name': 'Silica Powder', 'mass': '1', 'quantized': False},
    {'id': '67', 'name': 'Solder', 'mass': '1', 'quantized': False},
    {'id': '68', 'name': 'Fiber Optic Cable', 'mass': '1', 'quantized': False},
    {'id': '69', 'name': 'Steel Beam', 'mass': '1', 'quantized': False},
    {'id': '70', 'name': 'Steel Sheet', 'mass': '1', 'quantized': False},
    {'id': '71', 'name': 'Steel Pipe', 'mass': '1', 'quantized': False},
    {'id': '72', 'name': 'Steel Wire', 'mass': '1', 'quantized': False},
    {'id': '73', 'name': 'Acrylonitrile', 'mass': '1', 'quantized': False},
    {'id': '74', 'name': 'Polypropylene', 'mass': '1', 'quantized': False},
    {'id': '75', 'name': 'Magnesium', 'mass': '1', 'quantized': False},
    {'id': '76', 'name': 'Chlorine', 'mass': '1', 'quantized': False},
    {'id': '77', 'name': 'Sodium Carbonate', 'mass': '1', 'quantized': False},
    {'id': '78', 'name': 'Calcium Chloride', 'mass': '1', 'quantized': False},
    {'id': '79', 'name': 'Boria', 'mass': '1', 'quantized': False},
    {'id': '80', 'name': 'Lithium Sulfate', 'mass': '1', 'quantized': False},
    {'id': '81', 'name': 'Hydrochloric Acid', 'mass': '1', 'quantized': False},
    {'id': '82', 'name': 'Hydrofluoric Acid', 'mass': '1', 'quantized': False},
    {'id': '83', 'name': 'Phosphoric Acid', 'mass': '1', 'quantized': False},
    {'id': '84', 'name': 'Boric Acid', 'mass': '1', 'quantized': False},
    {'id': '85', 'name': 'Zinc Oxide', 'mass': '1', 'quantized': False},
    {'id': '86', 'name': 'Nickel Oxide', 'mass': '1', 'quantized': False},
    {'id': '87', 'name': 'Magnesia', 'mass': '1', 'quantized': False},
    {'id': '88', 'name': 'Alumina', 'mass': '1', 'quantized': False},
    {'id': '89', 'name': 'Sodium Hydroxide', 'mass': '1', 'quantized': False},
    {'id': '90', 'name': 'Potassium Hydroxide', 'mass': '1', 'quantized': False},
    {'id': '91', 'name': 'Soybeans', 'mass': '1', 'quantized': False},
    {'id': '92', 'name': 'Potatoes', 'mass': '1', 'quantized': False},
    {'id': '93', 'name': 'Ammonium Oxalate', 'mass': '1', 'quantized': False},
    {'id': '94', 'name': 'Rare Earth Sulfates', 'mass': '1', 'quantized': False},
    {'id': '95', 'name': 'Ferrochromium', 'mass': '1', 'quantized': False},
    {'id': '96', 'name': 'Yellowcake', 'mass': '1', 'quantized': False},
    {'id': '97', 'name': 'Alumina Ceramic', 'mass': '1', 'quantized': False},
    {'id': '98', 'name': 'Austenitic Nichrome', 'mass': '1', 'quantized': False},
    {'id': '99', 'name': 'Copper Wire', 'mass': '1', 'quantized': False},
    {'id': '100', 'name': 'Silicon Wafer', 'mass': '1', 'quantized': False},
    {'id': '101', 'name': 'Steel Cable', 'mass': '1', 'quantized': False},
    {'id': '102', 'name': 'Polyacrylonitrile', 'mass': '1', 'quantized': False},
    {'id': '103', 'name': 'Natural Flavorings', 'mass': '1', 'quantized': False},
    {'id': '104', 'name': 'Platinum', 'mass': '1', 'quantized': False},
    {'id': '105', 'name': 'Lithium Chloride', 'mass': '1', 'quantized': False},
    {'id': '106', 'name': 'Zinc', 'mass': '1', 'quantized': False},
    {'id': '107', 'name': 'Epichlorohydrin', 'mass': '1', 'quantized': False},
    {'id': '108', 'name': 'Bisphenol A', 'mass': '1', 'quantized': False},
    {'id': '109', 'name': 'Rare Earth Oxides', 'mass': '1', 'quantized': False},
    {'id': '110', 'name': 'Ammonium Chloride', 'mass': '1', 'quantized': False},
    {'id': '111', 'name': 'Aluminium', 'mass': '1', 'quantized': False},
    {'id': '112', 'name': 'Calcium', 'mass': '1', 'quantized': False},
    {'id': '113', 'name': 'Sodium Chromate', 'mass': '1', 'quantized': False},
    {'id': '114', 'name': 'Leached Coffinite', 'mass': '1', 'quantized': False},
    {'id': '115', 'name': 'Uranyl Nitrate', 'mass': '1', 'quantized': False},
    {'id': '116', 'name': 'Fluorine', 'mass': '1', 'quantized': False},
    {'id': '117', 'name': 'Sodium Tungstate', 'mass': '1', 'quantized': False},
    {'id': '118', 'name': 'Ferrite', 'mass': '1', 'quantized': False},
    {'id': '119', 'name': 'Diode', 'mass': '1', 'quantized': False},
    {'id': '120', 'name': 'Laser Diode', 'mass': '1', 'quantized': False},
    {'id': '121', 'name': 'Ball Valve', 'mass': '1', 'quantized': False},
    {'id': '122', 'name': 'Aluminium Beam', 'mass': '1', 'quantized': False},
    {'id': '123', 'name': 'Aluminium Sheet', 'mass': '1', 'quantized': False},
    {'id': '124', 'name': 'Aluminium Pipe', 'mass': '1', 'quantized': False},
    {'id': '125', 'name': 'Polyacrylonitrile Fabric', 'mass': '1', 'quantized': False},
    {'id': '126', 'name': 'Cold Gas Thruster', 'mass': '3', 'quantized': True},
    {'id': '127', 'name': 'Cold Gas Torque Thruster', 'mass': '3', 'quantized': True},
    {'id': '128', 'name': 'Carbon Fiber', 'mass': '1', 'quantized': False},
    {'id': '129', 'name': 'Food', 'mass': '1', 'quantized': False},
    {'id': '130', 'name': 'Small Propellant Tank', 'mass': '6', 'quantized': True},
    {'id': '131', 'name': 'Borosilicate Glass', 'mass': '1', 'quantized': False},
    {'id': '132', 'name': 'Ball Bearing', 'mass': '1', 'quantized': False},
    {'id': '133', 'name': 'Large Thrust Bearing', 'mass': '2000', 'quantized': True},
    {'id': '134', 'name': 'Boron', 'mass': '1', 'quantized': False},
    {'id': '135', 'name': 'Lithium', 'mass': '1', 'quantized': False},
    {'id': '136', 'name': 'Epoxy', 'mass': '1', 'quantized': False},
    {'id': '137', 'name': 'Neodymium Oxide', 'mass': '1', 'quantized': False},
    {'id': '138', 'name': 'Yttria', 'mass': '1', 'quantized': False},
    {'id': '139', 'name': 'Sodium Dichromate', 'mass': '1', 'quantized': False},
    {'id': '140', 'name': 'Novolak Prepolymer Resin', 'mass': '1', 'quantized': False},
    {'id': '141', 'name': 'Ferromolybdenum', 'mass': '1', 'quantized': False},
    {'id': '142', 'name': 'Ammonium Diuranate', 'mass': '1', 'quantized': False},
    {'id': '143', 'name': 'Ammonium Paratungstate', 'mass': '1', 'quantized': False},
    {'id': '144', 'name': 'Engine Bell', 'mass': '300', 'quantized': True},
    {'id': '145', 'name': 'Steel Truss', 'mass': '1500', 'quantized': True},
    {'id': '146', 'name': 'Aluminium Hull Plate', 'mass': '600', 'quantized': True},
    {'id': '147', 'name': 'Aluminium Truss', 'mass': '1000', 'quantized': True},
    {'id': '148', 'name': 'Cargo Module', 'mass': '5000', 'quantized': True},
    {'id': '149', 'name': 'Pressure Vessel', 'mass': '1850', 'quantized': True},
    {'id': '150', 'name': 'Propellant Tank', 'mass': '3500', 'quantized': True},
    {'id': '151', 'name': 'Stainless Steel', 'mass': '1', 'quantized': False},
    {'id': '152', 'name': 'Bare Circuit Board', 'mass': '1', 'quantized': False},
    {'id': '153', 'name': 'Ferrite-bead Inductor', 'mass': '1', 'quantized': False},
    {'id': '154', 'name': 'Core Drill Sampler', 'mass': '2', 'quantized': True},
    {'id': '155', 'name': 'Core Drill Thruster', 'mass': '10', 'quantized': True},
    {'id': '156', 'name': 'Parabolic Dish', 'mass': '72', 'quantized': True},
    {'id': '157', 'name': 'Photovoltaic Panel', 'mass': '8', 'quantized': True},
    {'id': '158', 'name': 'LiPo Battery', 'mass': '5', 'quantized': True},
    {'id': '159', 'name': 'Neodymium Trichloride', 'mass': '1', 'quantized': False},
    {'id': '161', 'name': 'Chromia', 'mass': '1', 'quantized': False},
    {'id': '162', 'name': 'Photoresist Epoxy', 'mass': '1', 'quantized': False},
    {'id': '163', 'name': 'Uranium Dioxide', 'mass': '1', 'quantized': False},
    {'id': '164', 'name': 'Tungsten', 'mass': '1', 'quantized': False},
    {'id': '165', 'name': 'Shuttle Hull', 'mass': '44600', 'quantized': True},
    {'id': '166', 'name': 'Light Transport Hull', 'mass': '74200', 'quantized': True},
    {'id': '167', 'name': 'Cargo Ring', 'mass': '10000', 'quantized': True},
    {'id': '168', 'name': 'Heavy Transport Hull', 'mass': '480400', 'quantized': True},
    {'id': '169', 'name': 'Tungsten Powder', 'mass': '1', 'quantized': False},
    {'id': '170', 'name': 'Hydrogen Propellant', 'mass': '1', 'quantized': False},
    {'id': '171', 'name': 'Stainless Steel Sheet', 'mass': '1', 'quantized': False},
    {'id': '172', 'name': 'Stainless Steel Pipe', 'mass': '1', 'quantized': False},
    {'id': '173', 'name': 'CCD', 'mass': '1', 'quantized': False},
    {'id': '174', 'name': 'Computer Chip', 'mass': '1', 'quantized': False},
    {'id': '175', 'name': 'Core Drill', 'mass': '30', 'quantized': True},
    {'id': '176', 'name': 'Neodymium', 'mass': '1', 'quantized': False},
    {'id': '178', 'name': 'Chromium', 'mass': '1', 'quantized': False},
    {'id': '179', 'name': 'Uranium Tetrafluoride', 'mass': '1', 'quantized': False},
    {'id': '180', 'name': 'Pure Nitrogen', 'mass': '1', 'quantized': False},
    {'id': '181', 'name': 'Nd:YAG Laser Rod', 'mass': '1', 'quantized': False},
    {'id': '182', 'name': 'Nichrome', 'mass': '1', 'quantized': False},
    {'id': '183', 'name': 'Neodymium Magnet', 'mass': '1', 'quantized': False},
    {'id': '184', 'name': 'Unenriched Uranium Hexafluoride', 'mass': '1', 'quantized': False},
    {'id': '185', 'name': 'Highly Enriched Uranium Hexafluoride', 'mass': '1', 'quantized': False},
    {'id': '186', 'name': 'Nd:YAG Laser', 'mass': '1', 'quantized': False},
    {'id': '187', 'name': 'Thin-film Resistor', 'mass': '1', 'quantized': False},
    {'id': '188', 'name': 'Highly Enriched Uranium Powder', 'mass': '1', 'quantized': False},
    {'id': '189', 'name': 'Leached Feldspar', 'mass': '1', 'quantized': False},
    {'id': '190', 'name': 'Roasted Rhabdite', 'mass': '1', 'quantized': False},
    {'id': '191', 'name': 'Rhabdite Slag', 'mass': '1', 'quantized': False},
    {'id': '192', 'name': 'Potassium Carbonate', 'mass': '1', 'quantized': False},
    {'id': '193', 'name': 'Hydrogen Heptafluorotantalate and Niobate', 'mass': '1', 'quantized': False},
    {'id': '194', 'name': 'Lead', 'mass': '1', 'quantized': False},
    {'id': '195', 'name': 'Potassium Fluoride', 'mass': '1', 'quantized': False},
    {'id': '196', 'name': 'Potassium Heptafluorotantalate', 'mass': '1', 'quantized': False},
    {'id': '197', 'name': 'Diepoxy Prepolymer Resin', 'mass': '1', 'quantized': False},
    {'id': '199', 'name': 'Tantalum', 'mass': '1', 'quantized': False},
    {'id': '200', 'name': 'PEDOT', 'mass': '1', 'quantized': False},
    {'id': '201', 'name': 'Polymer Tantalum Capacitor', 'mass': '1', 'quantized': False},
    {'id': '202', 'name': 'Surface Mount Device Reel', 'mass': '5', 'quantized': True},
    {'id': '203', 'name': 'Circuit Board', 'mass': '1', 'quantized': False},
    {'id': '204', 'name': 'Brushless Motor Stator', 'mass': '3', 'quantized': True},
    {'id': '205', 'name': 'Brushless Motor Rotor', 'mass': '3', 'quantized': True},
    {'id': '206', 'name': 'Brushless Motor', 'mass': '6', 'quantized': True},
    {'id': '207', 'name': 'Landing Leg', 'mass': '816', 'quantized': True},
    {'id': '208', 'name': 'Landing Auger', 'mass': '144', 'quantized': True},
    {'id': '209', 'name': 'Pump', 'mass': '8', 'quantized': True},
    {'id': '210', 'name': 'Radio Antenna', 'mass': '75', 'quantized': True},
    {'id': '211', 'name': 'Fiber Optic Gyroscope', 'mass': '2', 'quantized': True},
    {'id': '212', 'name': 'Star Tracker', 'mass': '2', 'quantized': True},
    {'id': '213', 'name': 'Computer', 'mass': '1', 'quantized': False},
    {'id': '214', 'name': 'Control Moment Gyroscope', 'mass': '160', 'quantized': True},
    {'id': '215', 'name': 'Robotic Arm', 'mass': '300', 'quantized': True},
    {'id': '217', 'name': 'Beryllium Carbonate', 'mass': '1', 'quantized': False},
    {'id': '218', 'name': 'Beryllia', 'mass': '1', 'quantized': False},
    {'id': '219', 'name': 'Beryllia Ceramic', 'mass': '1', 'quantized': False},
    {'id': '220', 'name': 'Neon', 'mass': '1', 'quantized': False},
    {'id': '221', 'name': 'Heat Exchanger', 'mass': '40', 'quantized': True},
    {'id': '222', 'name': 'Turbopump', 'mass': '290', 'quantized': True},
    {'id': '224', 'name': 'Neon/Fuel Separator Centrifuge', 'mass': '190', 'quantized': True},
    {'id': '225', 'name': 'Fuel Make-up Tank', 'mass': '100', 'quantized': True},
    {'id': '226', 'name': 'Neon Make-up Tank', 'mass': '250', 'quantized': True},
    {'id': '227', 'name': 'Lightbulb End Moderators', 'mass': '130', 'quantized': True},
    {'id': '229', 'name': 'Fused Quartz Lightbulb Tube', 'mass': '50', 'quantized': True},
    {'id': '230', 'name': 'Reactor Plumbing Assembly', 'mass': '1942', 'quantized': True},
    {'id': '231', 'name': 'Flow Divider Moderator', 'mass': '18700', 'quantized': True},
    {'id': '232', 'name': 'Nuclear Lightbulb', 'mass': '180', 'quantized': True},
    {'id': '233', 'name': 'Composite-overwrapped Reactor Shell', 'mass': '6000', 'quantized': True},
    {'id': '234', 'name': 'Closed-cycle Gas Core Nuclear Reactor Engine', 'mass': '30000', 'quantized': True},
    {'id': '235', 'name': 'Habitation Module', 'mass': '2200', 'quantized': True},
    {'id': '236', 'name': 'Mobility Module', 'mass': '2000', 'quantized': True},
    {'id': '237', 'name': 'Fluids Automation Module', 'mass': '3600', 'quantized': True},
    {'id': '238', 'name': 'Solids Automation Module', 'mass': '3600', 'quantized': True},
    {'id': '239', 'name': 'Terrain Interface Module', 'mass': '960', 'quantized': True},
    {'id': '240', 'name': 'Avionics Module', 'mass': '500', 'quantized': True},
    {'id': '241', 'name': 'Escape Module', 'mass': '6665', 'quantized': True},
    {'id': '242', 'name': 'Attitude Control Module', 'mass': '660', 'quantized': True},
    {'id': '243', 'name': 'Power Module', 'mass': '2000', 'quantized': True},
    {'id': '244', 'name': 'Thermal Module', 'mass': '1000', 'quantized': True},
    {'id': '245', 'name': 'Propulsion Module', 'mass': '32000', 'quantized': True},
    {'id': 'S1', 'name': 'Shuttle', 'mass': '100755', 'quantized': True},
    {'id': 'S2', 'name': 'Light Transport', 'mass': '185525', 'quantized': True},
    {'id': 'S3', 'name': 'Heavy Transport', 'mass': '969525', 'quantized': True},
    {'id': 'B1', 'name': 'Warehouse', 'mass': '1800000', 'quantized': True},
    {'id': 'B2', 'name': 'Extractor', 'mass': '1531900', 'quantized': True},
    {'id': 'B3', 'name': 'Refinery', 'mass': '2766900', 'quantized': True},
    {'id': 'B4', 'name': 'Bioreactor', 'mass': '7590700', 'quantized': True},
    {'id': 'B5', 'name': 'Factory', 'mass': '0', 'quantized': True},
    {'id': 'B6', 'name': 'Shipyard', 'mass': '0', 'quantized': True},
    {'id': 'B7', 'name': 'Spaceport', 'mass': '0', 'quantized': True},
    {'id': 'B8', 'name': 'Marketplace', 'mass': '0', 'quantized': True},
    {'id': 'B9', 'name': 'Habitat', 'mass': '0', 'quantized': True}]

    for row in products:
        if int(row['id']) == int(product_id):
            return int(row['mass'])

