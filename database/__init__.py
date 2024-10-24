"""
https://docs.python.org/3/library/sqlite3.html
"""
import sqlite3

import auth
import interface.print as iface_print
import database.schema as db_schema
import auth.user as auth_user

conn = sqlite3.connect('../database.db')
cur = conn.cursor()

def create_table(table_name: str, attributes: dict, drop_if_exists: bool = False) -> None:
    columns = ', '.join([f"{col} {dtype}" for col, dtype in attributes.items()])
    if drop_if_exists: cur.execute(f'DROP TABLE IF EXISTS {table_name};')
    cur.execute(f'CREATE TABLE {table_name} ({columns})')
    conn.commit()

def check_table(table_name: str) -> bool:
    cur.execute(f'SELECT name FROM sqlite_master WHERE type="table" AND name=?', (table_name, ))
    return cur.fetchone() is not None

def validate_tables(must_all_checked: bool = True, verbose: bool = True) -> bool | None:
    iface_print.info("Running database validation...") if verbose else None

    all_checked: bool = True

    for table in db_schema.schema:
        if not check_table(table):
            all_checked = False
            iface_print.warning(f"Table {table} not found!") if verbose else None
        else:
            iface_print.success(f"Table {table} found!") if verbose else None

    if all_checked:
        iface_print.success('Database validated.')
    elif must_all_checked and not all_checked:
        iface_print.failed('Database validation failed, one or more table can not be found.')
        iface_print.warning('Program terminated!')
        exit()

    return True if all_checked else False

def query_to_dict(database_schema: str, query_result: tuple) -> dict:
    column_count = 0
    result = dict({})
    for key in db_schema.schema[database_schema].keys():
        query_column = query_result[column_count]
        result[key] = query_column
        column_count += 1

    return result

def get_vehicles() -> list:
    cur.execute('SELECT * FROM vehicles')
    query = cur.fetchall()

    return [query_to_dict('vehicles', query[i]) for i in range(len(query))]

def increment_user_carbon(increment_by: float) -> None:
    if not auth.is_authed(): raise Exception("Authentication required")
    cur.execute('UPDATE users SET total_carbon_gr = total_carbon_gr + ? WHERE id = ?', (increment_by, auth_user.user['id']))
    conn.commit()

def increment_user_distance(increment_by: float) -> None:
    if not auth.is_authed(): raise Exception("Authentication required")
    cur.execute('UPDATE users SET total_distance_m = total_distance_m + ? WHERE id = ?', (increment_by, auth_user.user['id']))
    conn.commit()