import uuid
import json
import os
from utils import load_json, save_json
TOURNAMENT_DB = "tournaments.json"

def load_tournaments():
    if not os.path.exists(TOURNAMENT_DB):
        return []
    with open(TOURNAMENT_DB, "r") as f:
        try:
            data = f.read().strip()
            return json.loads(data) if data else []
        except json.JSONDecodeError:
            return []

def save_tournaments(tournaments):
    with open(TOURNAMENT_DB, "w") as f:
        json.dump(tournaments, f, indent=2)

def create_tournament(current_user):
    tournaments = load_json(TOURNAMENT_DB) or []

    while True:
        name = input("Enter tournament name: ").strip()
        if not name:
            print("❌ Tournament name cannot be empty. Please enter again.")
            continue

        # Kiểm tra tên đã tồn tại chưa (so sánh không phân biệt hoa thường)
        if any(tour["name"].lower() == name.lower() for tour in tournaments):
            print("❌ Tournament name already exists. Please enter a different name.")
            continue

        break  # Nếu hợp lệ thì thoát vòng lặp

    import uuid
    tournament_id = str(uuid.uuid4())[:8]

    new_tournament = {
        "id": tournament_id,
        "name": name,
        "organizer": {
            "id": current_user["id"],
            "username": current_user["username"],
            "nickname": current_user["nickname"],
            "full_name": current_user["full_name"]
        },
        "participants": [],
        "teams": [],
    }

    tournaments.append(new_tournament)
    save_json(TOURNAMENT_DB, tournaments)
    print(f"✅ Tournament '{name}' created with ID {tournament_id}")

    return tournament_id


def add_participant():
    tournaments = load_tournaments()
    tid = input("Enter tournament ID: ").strip()
    tournament = next((t for t in tournaments if t["id"] == tid), None)
    if not tournament:
        print("❌ Tournament not found.")
        return

    participant_id = input("Enter participant user ID: ").strip()
    tournament["participants"].append(participant_id)
    save_tournaments(tournaments)
    print(f"✅ Participant {participant_id} added to tournament {tid}.")

def add_post_conflict():
    tournaments = load_tournaments()
    tid = input("Enter tournament ID: ").strip()
    tournament = next((t for t in tournaments if t["id"] == tid), None)
    if not tournament:
        print("❌ Tournament not found.")
        return

    conflict_description = input("📝 Describe the post-tournament conflict: ").strip()
    tournament["conflicts"].append(conflict_description)
    save_tournaments(tournaments)
    print("✅ Conflict added.")

def list_tournaments():
    tournaments = load_json(TOURNAMENT_DB)
    if not tournaments:
        print("📭 No tournaments available.")
        return []

    print("\n📅 Coming Tournaments:")
    for i, tour in enumerate(tournaments, 1):
        organizer_username = tour.get('organizer', {}).get('username', 'N/A')
        organizer_insti = tour.get('organizer', {}).get('institution', 'N/A')
        print(f"{i}. {tour['name']} (ID: {tour['id']}) - 6Organizer: {organizer_username} - {organizer_insti}")
    return tournaments


def join_tournament(user):
    tournaments = list_tournaments()
    if not tournaments:
        return

    choice = input("🔢 Choose tournament number to join: ").strip()
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(tournaments):
        print("❌ Invalid choice.")
        return

    tournament = tournaments[int(choice) - 1]

    # Check if already joined
    for p in tournament["participants"]:
        if p["id"] == user["id"]:
            print("⚠️ You already joined this tournament.")
            return

    # Chọn private level
    print("\nChoose private level:")
    print("1. Public")
    print("2. Private")
    level_choice = input("Your choice (1-2): ").strip()
    if level_choice == "1":
        private_level = "public"
    elif level_choice == "2":
        private_level = "private"
    else:
        print("❌ Invalid choice for private level.")
        return

    # Chọn role
    print("\nChoose role:")
    print("1. Debater")
    print("2. Judge")
    print("3. Observer")
    role_choice = input("Your choice (1-3): ").strip()
    if role_choice == "1":
        role = "debater"
    elif role_choice == "2":
        role = "judge"
    elif role_choice == "3":
        role = "observer"
    else:
        print("❌ Invalid choice for role.")
        return

    team_id = None
    if role == "debater":
        # Quản lý team: tạo team mới hoặc join team có sẵn
        print("\nDebater role selected.")
        print("1. Create a new team")
        print("2. Join an existing team")
        team_choice = input("Choose (1 or 2): ").strip()

        if team_choice == "1":
            # Tạo team mới, team id tự tạo uuid
            import uuid
            team_id = str(uuid.uuid4())[:8]  # lấy 8 ký tự đầu
            team_name = input("Enter team name: ").strip()

            # Tạo team object và thêm vào tournament (nếu chưa có trường teams thì tạo)
            if "teams" not in tournament:
                tournament["teams"] = []

            # Thêm team mới
            tournament["teams"].append({
                "team_id": team_id,
                "team_name": team_name,
                "members": [{
                    "id": user["id"],
                    "username": user["username"],
                    "nickname": user["nickname"],
                    "full_name": user["full_name"]
                }]
            })

            print(f"✅ Created team '{team_name}' with id {team_id} and joined as a member.")

        elif team_choice == "2":
            if "teams" not in tournament or len(tournament["teams"]) == 0:
                print("⚠️ No teams available to join. Please create a new team.")
                return

            # Hiển thị danh sách team có trong tournament
            print("\nAvailable teams:")
            for t in tournament["teams"]:
                print(f"- {t['team_name']} (ID: {t['team_id']})")

            join_team_id = input("Enter the Team ID you want to join: ").strip()

            # Tìm team theo id
            team = next((t for t in tournament["teams"] if t["team_id"] == join_team_id), None)
            if not team:
                print("❌ Team ID not found.")
                return

            # Kiểm tra user đã có trong team chưa
            if any(m["id"] == user["id"] for m in team["members"]):
                print("⚠️ You are already a member of this team.")
                return

            # Thêm user vào team
            team["members"].append({
                "id": user["id"],
                "username": user["username"],
                "nickname": user["nickname"],
                "full_name": user["full_name"]
            })

            print(f"✅ Joined team '{team['team_name']}' successfully.")

        else:
            print("❌ Invalid choice for team option.")
            return

        # Cuối cùng, thêm participant role debater kèm team id
        tournament["participants"].append({
            "id": user["id"],
            "username": user["username"],
            "nickname": user["nickname"],
            "full_name": user["full_name"],
            "role": role,
            "private_level": private_level,
            "team_id": team_id if team_id else join_team_id
        })

    else:
        # Role judge hoặc observer không cần team
        tournament["participants"].append({
            "id": user["id"],
            "username": user["username"],
            "nickname": user["nickname"],
            "full_name": user["full_name"],
            "role": role,
            "private_level": private_level
        })

        print(f"✅ Joined tournament as {role}.")

    # Lưu thay đổi
    save_json(TOURNAMENT_DB, tournaments)
