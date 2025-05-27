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

        # Input for debate format/rules
    print("\nSelect debate format/rules:")
    print("1. WSDC (World Schools Debate Championship)")
    print("2. BP (British Parliamentary)")
    print("3. WSC (World Scholar's Cup)")
    print("4. AP (Asian Parliamentary)")
    
    while True:
        rules_choice = input("Enter your choice (1-4): ").strip()
        if rules_choice == "1":
            rules = "WSDC"
            break
        elif rules_choice == "2":
            rules = "BP"
            break
        elif rules_choice == "3":
            rules = "WSC"
            break
        elif rules_choice == "4":
            rules = "AP"
            break
        else:
            print("❌ Invalid choice. Please enter a number between 1-4.")
    
    #input team capacity
    while True:
        try:
            team_capacity = int(input("Enter team capacity: ").strip())
            if team_capacity < 2:
                print("❌ Team capacity must be at least 2.")
                continue
            break
        except ValueError:
            print("❌ Please enter a valid number.")
    
    #input language
    print ("Select tournament language")
    print ("1. Vietnamese")
    print ("2. English")

    while True:
        language_choice = input("Enter your choice (1-2): ").strip()
        if language_choice == "1":
            language = "Vietnamese"
            break
        elif language_choice == "2":
            language = "English"
            break
        else:
            print("❌ Invalid choice. Please enter a number between 1-2.")


    tournament_id = str(uuid.uuid4())[:8]

    new_tournament = {
        "id": tournament_id,
        "name": name,
        "rules": rules,
        "team_capacity": team_capacity,
        "language": language,
        "organizer": {
            "id": current_user["id"],
            "username": current_user["username"],
            "nickname": current_user["nickname"],
            "full_name": current_user["full_name"],
            "institution": current_user["institution"]
        },
        "participants": [],
        "teams": [],
    }


    tournaments.append(new_tournament)
    save_json(TOURNAMENT_DB, tournaments)
    print(f"✅ Tournament '{name}' created with ID {tournament_id}")
    print(f"   Debate Format: {rules}")
    print(f"   Team Capacity: {team_capacity} team")

    return tournament_id


def add_participant():
    tournaments = load_tournaments()
    tid = input("Enter tournament ID: ").strip()
    tournament = next((t for t in tournaments if t["id"] == tid), None)
    while True:
        tid = input("Enter tournament ID: ").strip()
        tournament = next((t for t in tournaments if t["id"] == tid), None)
        
        if not tournament:
            print("❌ Tournament not found. Please try again.")
            continue  # This will make the loop repeat
        else:
            break  # Exit the loop if tournament is found
    

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
        # Safely get organizer info with defaults
        organizer = tour.get('organizer', {})
        organizer_username = organizer.get('username', 'N/A')
        organizer_insti = organizer.get('institution', 'N/A')
        
        # Safely get tournament details with defaults
        tour_name = tour.get('name', 'Unnamed Tournament')
        tour_id = tour.get('id', 'N/A')
        language = tour.get('language', 'Not specified')
        rules = tour.get('rules', 'Not specified')
        team_capacity = tour.get('team_capacity', 'Not specified')
        current_teams = len(tour.get('teams', []))
        
        print(f"{i}. {tour_name} (ID: {tour_id})")
        print(f"   Language: {language} | Format: {rules}")
        print(f"   Teams: {current_teams}/{team_capacity} | Organizer: {organizer_username} ({organizer_insti})")
        print("-" * 50)  # Separator between tournaments
    
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
    rules = tournament.get("rules", "WSDC")  # Get the tournament's rules format
    team_capacity = tournament.get("team_capacity", 16)  # Get the tournament's team capacity

    # Check if already joined
    for p in tournament["participants"]:
        if p["id"] == user["id"]:
            print("⚠️ You already joined this tournament.")
            return

    # # Chọn private level
    # print("\nChoose private level:")
    # print("1. Public")
    # print("2. Private")
    # level_choice = input("Your choice (1-2): ").strip()
    # if level_choice == "1":
    #     private_level = "public"
    # elif level_choice == "2":
    #     private_level = "private"
    # else:
    #     print("❌ Invalid choice for private level.")
    #     return

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
    status = "confirmed" #default status
    if role == "debater":
        # Quản lý team: tạo team mới hoặc join team có sẵn
        print("\nDebater role selected.")
        print("1. Create a new team")
        print("2. Join an existing team")
        team_choice = input("Choose (1 or 2): ").strip()

        if team_choice == "1":
            #check if tournament has reached team capacity
            current_teams = len(tournament.get("teams", []))
            if current_teams >= team_capacity:
                print("⚠️ Tournament has reached maximum team capacity. Your team will be placed on reserve.")
                status = "reserved"

            # Tạo team mới, team id tự tạo uuid
            # import uuid
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
                    "full_name": user["full_name"],
                    "status": status
                }],
                "status": status
            })

            print(f"✅ Created team '{team_name}' with id {team_id} and joined as a member.")
            if status == "reserved":
                print("ℹ️ Your team is on reserve list and will be automatically promoted if a spot becomes available.")
        
        elif team_choice == "2":
            if "teams" not in tournament or len(tournament["teams"]) == 0:
                print("⚠️ No teams available to join. Please create a new team.")
                return

            # Hiển thị danh sách team có trong tournament
            print("\nAvailable teams:")
            for t in tournament["teams"]:
                print(f"- {t['team_name']} (ID: {t['team_id']}) [Members: {len(t['members'])}/{get_max_members(rules)}] [Status: {t.get('status', 'confirmed')}]")
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

            # Kiểm tra số lượng thành viên trong team
            max_members = get_max_members(rules)
            if len(team["members"]) >= max_members:
                print(f"❌ This team already has the maximum number of members ({max_members}) for {rules} format.")

            # Thêm user vào team
            team["members"].append({
                "id": user["id"],
                "username": user["username"],
                "nickname": user["nickname"],
                "full_name": user["full_name"],
                "status": team.get("status", "confirmed")
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
            # "private_level": private_level,
            "team_id": team_id if team_id else join_team_id,
            "status": status
        })

    else:
        # Role judge hoặc observer không cần team
        tournament["participants"].append({
            "id": user["id"],
            "username": user["username"],
            "nickname": user["nickname"],
            "full_name": user["full_name"],
            "role": role,
            "status": "confirmed"
            # "private_level": private_level
        })

        print(f"✅ Joined tournament as {role}.")

def get_max_members(rules):
    """Returns the maximum number of members allowed per team based on debate format"""
    rules_member_limits = {
        "WSDC": 5,   # WSDC allows 3-5 members
        "BP": 2,     # BP is 2 members per team
        "WSC": 3,    # WSC is 3 members
        "AP": 3      # AP is 3 members
    }
    return rules_member_limits.get(rules, 3)  # Default to 3 if format not found

def leave_tournament(user):
    """Function to handle participants leaving the tournament"""
    tournaments = load_json(TOURNAMENT_DB)
    if not tournaments:
        print("📭 No tournaments available.")
        return

    # List tournaments the user has joined
    user_tournaments = []
    for i, tour in enumerate(tournaments, 1):
        for p in tour.get("participants", []):
            if p["id"] == user["id"]:
                user_tournaments.append((i, tour))
                break

    if not user_tournaments:
        print("⚠️ You haven't joined any tournaments yet.")
        return

    print("\n📅 Your Tournaments:")
    for i, tour in user_tournaments:
        print(f"{i}. {tour['name']} (ID: {tour['id']})")

    choice = input("🔢 Choose tournament number to leave: ").strip()
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(user_tournaments):
        print("❌ Invalid choice.")
        return

    tournament = user_tournaments[int(choice)-1][1]
    
    # Remove from participants
    tournament["participants"] = [p for p in tournament["participants"] if p["id"] != user["id"]]
    
    # If debater, remove from team and check if team becomes empty
    for team in tournament.get("teams", []):
        team["members"] = [m for m in team["members"] if m["id"] != user["id"]]
        
        # If team is now empty, remove it
        if not team["members"]:
            tournament["teams"].remove(team)
            print(f"ℹ️ Team '{team['team_name']}' has been removed as it became empty.")
        else:
            # Promote first reserved member if any
            reserved_members = [m for m in team["members"] if m.get("status") == "reserved"]
            if reserved_members:
                promoted = reserved_members[0]
                promoted["status"] = "confirmed"
                print(f"ℹ️ Member {promoted['username']} has been promoted from reserved to confirmed status.")
    
    # Check if we can promote any reserved teams
    confirmed_teams = [t for t in tournament.get("teams", []) if t.get("status") == "confirmed"]
    if len(confirmed_teams) < tournament.get("team_capacity", 16):
        reserved_teams = [t for t in tournament.get("teams", []) if t.get("status") == "reserved"]
        if reserved_teams:
            promoted_team = reserved_teams[0]
            promoted_team["status"] = "confirmed"
            for member in promoted_team["members"]:
                member["status"] = "confirmed"
            print(f"ℹ️ Team '{promoted_team['team_name']}' has been promoted from reserved to confirmed status.")

    # Lưu thay đổi
    save_json(TOURNAMENT_DB, tournaments)
    print("✅ You have left the tournament successfully.")  # Add this line
