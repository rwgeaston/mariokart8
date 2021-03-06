spec_order = {'speed': 0, 'acceleration': 1, 'weight': 2, 'handling': 3, 'grip': 4}

character_classes = {
    'babyweight': [2.25, 3.25, 2.25, 4.75, 4.5],
    'featherweight': [2.75, 3.00, 2.75, 4.25, 4.25],
    'sub-lightweight': [3.25, 3, 3, 3.75, 4.00],
    'lightweight': [3.25, 2.75, 3.25, 3.75, 4.00],
    'sub-midweight': [3.75, 2.75, 3.5, 3.25, 3.75],
    'midweight': [3.75, 2.50, 3.75, 3.25, 3.75],
    'cruiserweight': [4.25, 2.25, 4.25, 2.75, 3.50],
    'metalweight': [4.25, 2.00, 4.75, 2.75, 3.25],
    'heavyweight': [4.75, 2.00, 4.75, 2.25, 3.25]
}

characters = {
    'Baby Mario': 'babyweight',
    'Baby Luigi': 'babyweight',
    'Baby Peach': 'babyweight',
    'Baby Daisy': 'babyweight',
    'Baby Rosalina': 'babyweight',
    'Lemmy': 'babyweight',
    'Toad': 'featherweight',
    'Koopa Troopa': 'featherweight',
    'Shy Guy': 'featherweight',
    'Lakitu': 'featherweight',
    'Toadette': 'featherweight',
    'Larry': 'featherweight',
    'Wendy': 'featherweight',
    'Isabelle': 'featherweight',
    'Cat Peach': 'sub-lightweight',
    'Villager (female)': 'sub-lightweight',
    'Peach': 'lightweight',
    'Daisy': 'lightweight',
    'Yoshi': 'lightweight',
    'Mario': 'midweight',
    'Tanooki Mario': 'sub-midweight',
    'Villager (male)': 'sub-midweight',
    'Luigi': 'midweight',
    'Ludwig': 'midweight',
    'Iggy': 'midweight',
    'Donkey Kong': 'cruiserweight',
    'Waluigi': 'cruiserweight',
    'Rosalina': 'cruiserweight',
    'Roy': 'cruiserweight',
    'Link': 'cruiserweight',
    'Metal Mario': 'metalweight',
    'Pink Gold Peach': 'metalweight',
    'Bowser': 'heavyweight',
    'Wario': 'heavyweight',
    'Morton': 'heavyweight',
    'Dry Bowser': 'heavyweight',
}

vehicles = {
    'Standard Kart': [+0.00, +0.00, +0.00, +0.00, +0.00],
    'Cat Cruiser': [+0.00, +0.00, +0.00, +0.00, +0.00],
    'Prancer': [+0.00, +0.00, +0.00, +0.00, +0.00],
    'Bounder': [+0.00, +0.00, +0.00, +0.00, +0.00],
    'Mach 8': [+0.50, -0.25, +0.25, +0.00, -1.00],
    'Sports Coupe': [+0.50, -0.25, +0.25, +0.00, -1.00],
    'Badwagon': [+0.00, -0.50, +0.50, -0.50, +0.50],
    'Tri-Speeder': [+0.00, -0.50, +0.50, -0.50, +0.50],
    'Buggybud': [-0.75, +1.25, -0.50, +0.50, -0.25],
    'Landship': [-0.75, +1.25, -0.50, +0.50, -0.25],
    'Circuit Special': [+0.50, -0.25, +0.25, +0.00, -1.00],
    'Pipe Frame': [+0.00, +0.25, -0.25, +0.50, -0.50],
    'Steel Driver': [+0.00, -0.50, +0.50, -0.50, +0.50],
    'Gold Standard': [+0.50, -0.25, +0.25, +0.00, -1.00],
    'Standard Bike': [+0.00, +0.25, -0.25, +0.50, -0.50],
    'Sport Bike': [+0.00, +0.75, -0.25, +0.75, -1.25],
    'Yoshi Bike': [+0.00, +0.75, -0.25, +0.75, -1.25],
    'Jet Bike': [+0.00, +0.75, -0.25, +0.75, -1.25],
    'Comet': [+0.00, +0.75, -0.25, +0.75, -1.25],
    'Varmint': [+0.00, +0.25, -0.25, +0.50, -0.50],
    'Flame Rider': [+0.00, +0.25, -0.25, +0.50, -0.50],
    'Mr. Scooty': [-0.75, +1.25, -0.50, +0.50, -0.25],
    'The Duke': [+0.00, +0.00, +0.00, +0.00, +0.00],
    'Standard Quad': [+0.00, -0.50, +0.50, -0.50, +0.50],
    'Teddy Buggy': [+0.00, +0.00, +0.00, +0.00, +0.00],
    'Wild Wiggler': [+0.00, +0.25, -0.25, +0.50, -0.50],
    'Mercedes GLA': [+0.00, -0.50, +0.50, -0.50, +0.50],
    'Mercedes W 25 Silver Arrow': [+0.00, +0.25, -0.25, +0.50, -0.50],
    'Mercedes 300 SL Roadster': [+0.00, +0.00, +0.00, +0.00, +0.00],
    'Blue Falcon': [+0.25, +0.25, -0.25, 0, -0.5],
    'Tanooki Kart': [0, -0.25, +0.25, -0.25, +0.25],
    'B Dasher': [+0.5, -0.25, +0.25, 0, -1],
    'Master Cycle': [0.25, 0, 0, 0.5, -0.75],
    'Streetle': [+0.25, +0.25, -0.25, 0, -0.5],
    'P-Wing': [+0.5, -0.25, +0.25, 0, -1],
    'City Tripper': [+0.00, +0.25, -0.25, +0.50, -0.50],
    'Bone Rattler': [+0.00, -0.50, +0.50, -0.50, +0.50],
}

vehicle_classes = {
    'Standard Kart': 'Kart',
    'Cat Cruiser': 'Kart',
    'Prancer': 'Kart',
    'Bounder': 'Kart',
    'Mach 8': 'Kart',
    'Sports Coupe': 'Kart',
    'Badwagon': 'Kart',
    'Tri-Speeder': 'Kart',
    'Buggybud': 'Kart',
    'Landship': 'Kart',
    'Circuit Special': 'Kart',
    'Pipe Frame': 'Kart',
    'Steel Driver': 'Kart',
    'Gold Standard': 'Kart',
    'Standard Bike': 'Bike',
    'Sport Bike': 'Bike (in)',
    'Yoshi Bike': 'Bike (in)',
    'Jet Bike': 'Bike (in)',
    'Comet': 'Bike (in)',
    'Varmint': 'Bike',
    'Flame Rider': 'Bike',
    'Mr. Scooty': 'Bike',
    'The Duke': 'Bike',
    'Standard Quad': 'Quad',
    'Teddy Buggy': 'Quad',
    'Wild Wiggler': 'Quad',
    'Mercedes GLA': 'Kart',
    'Mercedes W 25 Silver Arrow': 'Kart', 
    'Mercedes 300 SL Roadster': 'Kart',
    'Blue Falcon': 'Kart',
    'Tanooki Kart': 'Kart',
    'B Dasher': 'Kart',
    'Master Cycle': 'Bike (in)',
    'Streetle': 'Kart',
    'P-Wing': 'Kart',
    'City Tripper': 'Bike',
    'Bone Rattler': 'Quad',
}

tyres = {
    'Normal Tyres': [+0.00, +0.00, +0.00, +0.00, +0.00],
    'Normal Blue': [+0.00, +0.00, +0.00, +0.00, +0.00],
    'Monster': [+0.00, -0.50, +0.50, -0.75, +0.75],
    'Funky Monster': [+0.00, -0.50, +0.50, -0.75, +0.75],
    'Slick': [+0.50, -0.25, +0.25, +0.00, -1.00],
    'Cyber Slick': [+0.50, -0.25, +0.25, +0.00, -1.00],
    'Roller': [-0.50, +1.00, -0.50, +0.25, -0.25],
    'Azure Roller': [-0.50, +1.00, -0.50, +0.25, -0.25],
    'Button': [-0.50, +1.00, -0.50, +0.25, -0.25],
    'Slim': [+0.25, -0.25, +0.00, +0.25, -0.50],
    'Crimson Slim': [+0.25, -0.25, +0.00, +0.25, -0.50],
    'Offroad': [+0.00, +0.00, +0.00, +0.00, +0.00],
    'Retro Off-road': [+0.00, +0.00, +0.00, +0.00, +0.00],
    'Wooden': [-0.25, +0.25, -0.25, -0.25, +0.50],
    'Sponge': [-0.25, +0.25, -0.25, -0.25, +0.50],
    'Cushion': [-0.25, +0.25, -0.25, -0.25, +0.50],
    'Metal': [+0.25, -0.50, +0.50, +0.00, -0.50],
    'Gold Tyres': [+0.25, -0.50, +0.50, +0.00, -0.50],
    'GLA Tyres': [+0.00, +0.00, +0.00, +0.00, +0.00],
    'TriForce Tyres': [0.25, -0.25, 0, 0.25, -0.5],
    'Leaf Tyres': [-0.50, +1.00, -0.50, +0.25, -0.25],
}

gliders = {
    'Super Glider': [+0.00, +0.00, +0.00, +0.00, +0.00],
    'Wario Wing': [+0.00, +0.00, +0.00, +0.00, +0.00],
    'Waddle Wing': [+0.00, +0.00, +0.00, +0.00, +0.00],
    'Plane Glider': [+0.00, +0.00, +0.00, +0.00, +0.00],
    'Cloud Glider': [+0.00, +0.25, -0.25, +0.00, +0.00],
    'Flower Glider': [+0.00, +0.25, -0.25, +0.00, +0.00],
    'Bowser Kite': [+0.00, +0.25, -0.25, +0.00, +0.00],
    'Parafoil': [+0.00, +0.25, -0.25, +0.00, +0.00],
    'MKTV Parafoil': [+0.00, +0.25, -0.25, +0.00, +0.00],
    'Peach Parasol': [+0.00, +0.25, -0.25, +0.00, +0.00],
    'Parachute': [+0.00, +0.25, -0.25, +0.00, +0.00],
    'Gold Glider': [+0.00, +0.00, +0.00, +0.00, +0.00],
    'Hylian Kite': [0, 0.25, -0.25, 0, 0],
    'Paper Glider': [+0.00, +0.00, +0.00, +0.00, +0.00],
}
