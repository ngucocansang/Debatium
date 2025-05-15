# utils.py
import json
import os
import uuid
import bcrypt

def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        try:
            data = f.read().strip()
            return json.loads(data) if data else []
        except json.JSONDecodeError:
            print(f"⚠️ JSON Error in {path}, returning empty list.")
            return []

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def generate_user_id(users):
    return f"{len(users) + 1:09d}"

def generate_id(prefix):
    return f"{prefix}-{uuid.uuid4().hex[:6]}"

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())
