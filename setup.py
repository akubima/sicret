"""
This is a setup script that will set up all the things that are mandatory to execute this program.

*** RUN ONLY ONCE *** unless it is required to reset the database contents.
"""
import interface.print as iface_print
import interface.common as iface_common
import interface.error as iface_error
import random
import database as db
import database.schema as db_schema
import database.seed as db_seed
import os

try:
    iface_print.header()
    iface_print.warning(
        '\033[41m\033[4mATTENTION! This setup script will reset all database contents. BE CAREFUL!\033[0m')
    iface_print.separator()

    iface_print.info('Verification required!')
    verif_code = ''.join(str(random.randint(0, 9)) for _ in range(6))
    iface_print.info(f'Please type \033[44m\033[4m{verif_code}\033[0m to continue.')

    iface_print.separator()
    if iface_common.input_general('Insert verification code') != verif_code:
        iface_print.separator()
        iface_print.failed('Verification code mismatch.')
        iface_print.warning('Setup terminated.')
        exit()

    iface_print.separator()
    iface_print.info('Checking database file...')
    if not os.path.exists('database.db'):
        iface_print.info('Database file not found!')
        iface_print.info('Creating database.db file...')
        open('./database.db', 'a').close()
        iface_print.success('Database file created.')
    else:
        iface_print.success('Database file found.')

    iface_print.separator()
    if iface_common.input_general('Are you sure you want to reset all database contents? [y/N]') not in ['y', 'Y']:
        iface_print.warning('Setup terminated.')
        exit()

    iface_print.separator()
    iface_print.info('Migrating database...')
    for name, attributes in db_schema.schema.items():
        iface_print.info(f'Creating table {name}')
        db.create_table(name, attributes, drop_if_exists=True)
        iface_print.success(f'Created table {name}')
    iface_print.success('Migration completed.')

    iface_print.separator()
    iface_print.info('Seeding database...')

    for vehicle in db_seed.vehicles:
        db.cur.execute("INSERT INTO vehicles (name, emissions_gr_km) VALUES (?, ?)", (vehicle['name'], vehicle['emissions_gr_km']))
    for tree in db_seed.trees:
        db.cur.execute("INSERT INTO trees (name, scientific_name, carbon_absorption_gr_hr) VALUES (?, ?, ?)",
                           (tree['name'], tree['scientific_name'], tree['carbon_absorption_gr_hr']))

    db.conn.commit()

    iface_print.success('Seeding completed.')
except KeyboardInterrupt:
    iface_print.header()
    iface_print.warning('Sepertinya kamu telah menekan kombinasi tombol CTRL+C.')
    iface_print.warning('Program telah dihentikan dengan aman.')
except Exception as e:
    iface_error.handle_exception(e)