import json
import secrets
import time
import hashlib

def get_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return get_password_hash(plain_password) == hashed_password

def generate_token() -> str:
    return secrets.token_urlsafe(16)

def generate_id() -> int:
    return int(time.time())

def load_users() -> dict:
    try:
        with open("server/database.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users: dict):
    with open("server/database.json", "w") as f:
        json.dump(users, f, indent=4) 