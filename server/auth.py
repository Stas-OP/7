import json
import secrets
import time
import hashlib
from datetime import datetime

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

def add_request_to_history(user_id: int, request_type: str, endpoint: str):
    users = load_users()
    for user_data in users.values():
        if user_data["id"] == user_id:
            if "history" not in user_data:
                user_data["history"] = []
            user_data["history"].append({
                "timestamp": datetime.now().isoformat(),
                "request_type": request_type,
                "endpoint": endpoint
            })
            save_users(users)
            break

def get_user_history(user_id: int) -> list:
    users = load_users()
    for user_data in users.values():
        if user_data["id"] == user_id:
            return user_data.get("history", [])
    return []

def clear_user_history(user_id: int):
    users = load_users()
    for user_data in users.values():
        if user_data["id"] == user_id:
            user_data["history"] = []
            save_users(users)
            break 

def add_text(user_id: int, text: str) -> dict:
    users = load_users()
    for user_data in users.values():
        if user_data["id"] == user_id:
            if "texts" not in user_data:
                user_data["texts"] = []
            
            text_id = len(user_data["texts"]) + 1
            text_entry = {
                "id": text_id,
                "text": text,
                "timestamp": datetime.now().isoformat()
            }
            user_data["texts"].append(text_entry)
            save_users(users)
            return text_entry
    return None

def get_user_texts(user_id: int) -> list:
    users = load_users()
    for user_data in users.values():
        if user_data["id"] == user_id:
            return user_data.get("texts", [])
    return [] 

def get_text_by_id(user_id: int, text_id: int) -> dict:
    users = load_users()
    for user_data in users.values():
        if user_data["id"] == user_id:
            texts = user_data.get("texts", [])
            for text in texts:
                if text["id"] == text_id:
                    return text
    return None

def delete_text(user_id: int, text_id: int) -> bool:
    users = load_users()
    for user_data in users.values():
        if user_data["id"] == user_id:
            texts = user_data.get("texts", [])
            for i, text in enumerate(texts):
                if text["id"] == text_id:
                    texts.pop(i)
                    save_users(users)
                    return True
    return False 