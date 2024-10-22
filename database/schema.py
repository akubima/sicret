schema: dict = {
    'users': {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'name': 'TEXT NOT NULL',
        'username': 'TEXT UNIQUE NOT NULL',
        'password': 'BLOB NOT NULL',
        'total_carbon_gr': 'DECIMAL(17, 2) DEFAULT 0',
        'total_distance_m': 'DECIMAL(17, 2) DEFAULT 0'
    },
    'trees': {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'name': 'TEXT NOT NULL',
        'scientific_name': 'TEXT',
        'carbon_absorption_gr_hr': 'DECIMAL(17, 2) DEFAULT 0',
    },
    'vehicles': {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'name': 'TEXT NOT NULL',
        'model': 'TEXT',
        'emissions_gr_km': 'DECIMAL(17, 2) DEFAULT 0',
    }
}