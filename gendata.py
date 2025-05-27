import uuid
import json
import random

# Danh sách trường
institutions = [
    "Xando", "VinSchool", "Hanoi Amsterdam", "Le Quy Don",
    "FPT High", "Nguyen Hue", "Chu Van An", "Marie Curie"
]

# Hàm tạo user ngẫu nhiên
def create_user(idx):
    return {
        "username": str(idx),
        "nickname": f"nick{idx}",
        "full_name": f"User {idx}",
        "institution": random.choice(institutions)
    }

# Tạo dữ liệu giải đấu
tournament_data = {
    "id": str(uuid.uuid4())[:8],
    "name": "nsdc-wsdc",
    "rules": "WSDC",
    "team_capacity": 32,
    "language": "Vietnamese",
    "organizer": {
        "id": "000000001",
        "username": "org",
        "nickname": "organizer",
        "full_name": "Tournament Org",
        "institution": "Xando"
    },
    "participants": [],
    "teams": []
}

participant_counter = 10  # ID người dùng bắt đầu từ đây

# Tạo 32 đội
for i in range(1, 33):
    team_id = str(uuid.uuid4())[:8]
    team_name = f"Team{i:02d}"
    team_members = []

    for j in range(3):  # 3 debaters per team
        user = create_user(participant_counter)
        participant_id = f"{participant_counter:09d}"

        # Thêm vào participants
        tournament_data["participants"].append({
            "id": participant_id,
            "username": user["username"],
            "nickname": user["nickname"],
            "full_name": user["full_name"],
            "institution": user["institution"],
            "role": "debater",
            "team_id": team_id,
            "status": "confirmed"
        })

        # Thêm vào danh sách team
        team_members.append({
            "id": participant_id,
            "username": user["username"],
            "nickname": user["nickname"],
            "full_name": user["full_name"],
            "institution": user["institution"],
            "status": "confirmed"
        })

        participant_counter += 1

    tournament_data["teams"].append({
        "team_id": team_id,
        "team_name": team_name,
        "members": team_members,
        "status": "confirmed"
    })

# Tạo 10 Judges
for _ in range(10):
    user = create_user(participant_counter)
    participant_id = f"{participant_counter:09d}"
    tournament_data["participants"].append({
        "id": participant_id,
        "username": user["username"],
        "nickname": user["nickname"],
        "full_name": user["full_name"],
        "institution": user["institution"],
        "role": "judge",
        "team_id": None,
        "status": "confirmed"
    })
    participant_counter += 1

# Tạo 5 Observers
for _ in range(5):
    user = create_user(participant_counter)
    participant_id = f"{participant_counter:09d}"
    tournament_data["participants"].append({
        "id": participant_id,
        "username": user["username"],
        "nickname": user["nickname"],
        "full_name": user["full_name"],
        "institution": user["institution"],
        "role": "observer",
        "team_id": None,
        "status": "confirmed"
    })
    participant_counter += 1

# Lưu ra file JSON
with open("tournaments.json", "w", encoding="utf-8") as f:
    json.dump(tournament_data, f, ensure_ascii=False, indent=2)

print("✅ File 'tournaments.json' đã được tạo thành công.")
