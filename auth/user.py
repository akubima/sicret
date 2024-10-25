import bcrypt

import database as db

user: dict|None = None

def register(name: str, username: str, password: str):
    hashed_password: str = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())
    db.cur.execute('INSERT INTO users (name, username, password) VALUES (?, ?, ?)', (name, username, hashed_password))
    db.conn.commit()

def get_user(user_id: int) -> dict|None:
    db.cur.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user_data = db.cur.fetchone()
    if user_data is None:
        return None
    return db.query_to_dict('users', user_data)

def logout() -> None:
    global user
    user = None