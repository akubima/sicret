import bcrypt
import auth.user as auth_user

import database as db

def is_username_exist(username: str) -> bool:
    db.cur.execute('SELECT COUNT(*) from users WHERE username=?', (username, ))
    return db.cur.fetchone()[0] == 1

def is_user_exist(user_id: str) -> bool:
    db.cur.execute('SELECT COUNT(*) from users WHERE id=?', (user_id, ))
    return db.cur.fetchone()[0] == 1

def authenticate(username: str, password: str) -> bool:
    if not is_username_exist(username): return False
    db.cur.execute(f'SELECT * FROM users WHERE username=?', (username,))
    user_data = db.query_to_dict('users', db.cur.fetchone())
    auth_attempt = bcrypt.checkpw(password.encode('utf-8'), user_data['password'])
    auth_user.user = user_data if auth_attempt else None
    return True if auth_attempt else False

def refresh_auth()-> None:
    if auth_user.user is None: return
    auth_user.user = auth_user.get_user(auth_user.user['id'])

def is_authed() -> bool:
    return auth_user.user is not None and len(auth_user.user) > 0