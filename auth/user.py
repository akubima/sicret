import bcrypt

import database as db
import database.schema as db_schema

user: dict|None = None

def user_query_to_dict(user_query_result: tuple) -> dict:
    column_count = 0
    user_dict = dict({})
    for key in db_schema.schema['users'].keys():
        user_query_column = user_query_result[column_count]
        user_dict[key] = user_query_column
        column_count += 1

    return user_dict

def register(name: str, username: str, password: str):
    hashed_password: str = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())
    db.cur.execute('INSERT INTO users (name, username, password) VALUES (?, ?, ?)', (name, username, hashed_password))
    db.conn.commit()

def get_user(user_id: int) -> dict|None:
    db.cur.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user_data = db.cur.fetchone()
    if user_data is None:
        return None
    return user_query_to_dict(user_data)

def logout() -> None:
    global user
    user = None