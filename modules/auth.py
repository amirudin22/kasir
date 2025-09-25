import hashlib, uuid, datetime
from modules.db import execute

SECRET_SALT = 'CHANGE_THIS_TO_STRONG_SECRET'

def get_hwid():
    node = uuid.getnode()
    system_id = uuid.UUID(int=uuid.getnode()) if node else uuid.uuid4()
    base = f"{system_id}-{uuid.getnode()}"
    return hashlib.sha256(base.encode('utf-8')).hexdigest()

def generate_activation_code_from_hwid(hwid: str) -> str:
    merged = (hwid + SECRET_SALT).encode('utf-8')
    hashed = hashlib.sha256(merged).hexdigest()
    return (hashed[:2] + hashed[-4:]).upper()

def validate_activation(hwid: str, code_input: str) -> bool:
    return generate_activation_code_from_hwid(hwid) == code_input.strip().upper()

def register_user(username, password, activation_code, role='kasir'):
    hwid = get_hwid()
    if not validate_activation(hwid, activation_code):
        return False, 'Kode aktivasi tidak sesuai.'
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), SECRET_SALT.encode(), 100000).hex()
    now = datetime.datetime.utcnow().isoformat()
    try:
        execute('INSERT INTO users (username, password_hash, role, created_at) VALUES (?,?,?,?)',
                (username, pwd_hash, role, now))
    except Exception as e:
        return False, str(e)
    return True, 'Registrasi berhasil.'

def login(username, password):
    rows = execute('SELECT id, password_hash, role FROM users WHERE username=?', (username,), fetch=True)
    if not rows:
        return False, 'User tidak ditemukan.'
    uid, stored_hash, role = rows[0]
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), SECRET_SALT.encode(), 100000).hex()
    if pwd_hash == stored_hash:
        return True, {'id': uid, 'username': username, 'role': role}
    return False, 'Password salah.'
