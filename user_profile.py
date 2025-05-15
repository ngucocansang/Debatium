from tournament_main import tournament_dashboard
from tournament import create_tournament, add_participant, add_post_conflict

 
# register.py
from utils import load_json, save_json, generate_user_id, hash_password, verify_password
import os

DB_PATH = "users.json"

def username_exists(users, username):
    return any(user["username"] == username for user in users)

def get_user(users, username):
    for user in users:
        if user["username"] == username:
            return user
    return None

def signup():
    users = load_json(DB_PATH)

    while True: 
        username = input("📝 Enter new username: ").strip()

        if not username:
            print("User name cannot be emty. Please enter again.")
            continue 

        if username_exists(users, username):
            print("❌ Username already taken.")
            continue
        break

    while True:
        password = input("🔒 Enter password: ").strip()
        if not password:
            print("User name cannot be emty. Please enter again.")
            continue
        break

    user_id = generate_user_id(users)
    hashed_pw = hash_password(password)
    nickname = input("🏷️  Nickname: ").strip()
    full_name = input("🪪 Full name: ").strip()
    institution = input("Institution: ").strip()

    new_user = {
        "id": user_id,
        "username": username,
        "password": hashed_pw,
        "conflicts": [],
        "nickname": nickname,
        "full_name": full_name,
        "institution": institution,
    }

    users.append(new_user)
    save_json(DB_PATH, users)
    print(f"✅ Signup successful! Your user ID is: {user_id}")

def signin():
    users = load_json(DB_PATH)
    username = input("👤 Username: ").strip()
    password = input("🔒 Password: ").strip()

    user = get_user(users, username)
    if not user:
        print("❌ Username not found.")
        return None

    if verify_password(password, user["password"]):
        print(f"✅ Welcome back, {username}!")
        print(f"🔑 Your User ID: {user['id']}")
        print(f"🏷️  Nickname: {user['nickname']}")
        print(f"🪪 Full name: {user['full_name']}")
        print(f"institution: {user['institution']}")
        print(f"⚔️  Conflicts: {user['conflicts']}")
        return user

    else:
        print("❌ Incorrect password.")
