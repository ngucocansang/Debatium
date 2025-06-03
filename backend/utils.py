import json
import os
import bcrypt

def load_json(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        try:
            data = f.read().strip()
            return json.loads(data) if data else []
        except json.JSONDecodeError:
            return []

def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

def generate_user_id(users):
    return str(len(users) + 1)

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))