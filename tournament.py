import uuid
import json
import os
from utils import load_json, save_json
TOURNAMENT_DB = "tournaments.json"
from datetime import datetime
#calendar 
def validate_date(date):
    try: 
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def to_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")
def dates_overlap(start1, end1, start2, ende)
    

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

    while True: 
        start_date = input("Enter the start date of the tournament: ").strip()

        if not validate_date(start_date):
            print("Invalid start date format. Please use YYYY-MM-DD")
            continue
        end_date = input("Enter the end date(Expected) of the tournament: ").strip()
        if not validate_date(end_date):
            print("Invalid end date. Please use YYYY-MM-DD")
            continue
        if end_date < start_date:
            print("End date cannot be earlier than start date")
            continue
        if any(tour.get("start_date") == start_date or tour.get("end_date") == end_date for tour in tournaments):
            print("the date already booked")
            continue
        break

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
        "start_date": start_date,
        "end_date": end_date,
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
        tour_date = tour.get('start_date')
        tour_end = tour.get('end_date')
        print(f"{i}. {tour_name} (ID: {tour_id})")
        print(f"   Language: {language} | Format: {rules}")
        print(f"   Time of event: {tour_date} - {tour_end} ")
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
    rules = tournament.get("rules", "WSDC")
    team_capacity = tournament.get("team_capacity", 16)
    tournament_id = tournament["id"]

    # Check if already joined
    for p in tournament["participants"]:
        if p["id"] == user["id"]:
            print("⚠️ You already joined this tournament.")
            return

    # Choose role
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

    # Generate participant ID based on role and tournament
    def generate_participant_id(role, tournament_id):
        prefix = "D" if role == "debater" else "J" if role == "judge" else "O"
        existing_ids = [p["id"] for p in tournament.get("participants", []) if p["id"].startswith(prefix)]
        next_num = len(existing_ids) + 1
        return f"{prefix}{tournament_id[:3].upper()}{next_num:03d}"

    participant_id = generate_participant_id(role, tournament_id)

    team_id = None
    status = "confirmed"
    
    if role == "debater":
        print("\nDebater role selected.")
        print("1. Create a new team")
        print("2. Join an existing team")
        team_choice = input("Choose (1 or 2): ").strip()

        if team_choice == "1":
            current_teams = len(tournament.get("teams", []))
            if current_teams >= team_capacity:
                print("⚠️ Tournament has reached maximum team capacity. Your team will be placed on reserve.")
                status = "reserved"

            team_id = str(uuid.uuid4())[:8]
            team_name = input("Enter team name: ").strip()

            if "teams" not in tournament:
                tournament["teams"] = []

            new_team = {
                "team_id": team_id,
                "team_name": team_name,
                "members": [{
                    "id": participant_id,
                    "user_id": user["id"],
                    "username": user["username"],
                    "nickname": user["nickname"],
                    "full_name": user["full_name"],
                    "institution": user["institution"],
                    "status": status
                }],
                "status": status
            }
            tournament["teams"].append(new_team)

            tournament["participants"].append({
                "id": participant_id,
                "user_id": user["id"],
                "username": user["username"],
                "nickname": user["nickname"],
                "full_name": user["full_name"],
                "institution": user["institution"],
                "role": role,
                "team_id": team_id,
                "status": status
            })

            save_json(TOURNAMENT_DB, tournaments)
            
            print(f"\n✅ Created team '{team_name}' (ID: {team_id})")
            print(f"Your participant ID: {participant_id}")
            print(f"Current teams: {len(tournament['teams'])}/{team_capacity}")
            if status == "reserved":
                print("ℹ️ Your team is on reserve list")

        elif team_choice == "2":
            if not tournament.get("teams"):
                print("⚠️ No teams available to join. Please create a new team.")
                return

            print("\nAvailable teams:")
            for i, t in enumerate(tournament["teams"], 1):
                print(f"{i}. {t['team_name']} (ID: {t['team_id']})")
                print(f"   Members: {len(t['members'])}/{get_max_members(rules)}")
                print(f"   Status: {t.get('status', 'confirmed')}\n")

            join_team_id = input("Enter the Team ID you want to join: ").strip()
            team = next((t for t in tournament["teams"] if t["team_id"] == join_team_id), None)
            
            if not team:
                print("❌ Team ID not found.")
                return

            if any(m["user_id"] == user["id"] for m in team["members"]):
                print("⚠️ You are already a member of this team.")
                return

            max_members = get_max_members(rules)
            if len(team["members"]) >= max_members:
                print(f"❌ Team is full (max {max_members} members for {rules} format)")
                return

            team["members"].append({
                "id": participant_id,
                "user_id": user["id"],
                "username": user["username"],
                "nickname": user["nickname"],
                "full_name": user["full_name"],
                "institution": user["institution"],
                "status": team.get("status", "confirmed")
            })

            tournament["participants"].append({
                "id": participant_id,
                "user_id": user["id"],
                "username": user["username"],
                "nickname": user["nickname"],
                "full_name": user["full_name"],
                "institution": user["institution"],
                "role": role,
                "team_id": join_team_id,
                "status": team.get("status", "confirmed")
            })

            save_json(TOURNAMENT_DB, tournaments)
            
            print(f"\n✅ Joined team '{team['team_name']}' successfully")
            print(f"Your participant ID: {participant_id}")
            print(f"Team now has {len(team['members'])} members")

        else:
            print("❌ Invalid choice")
            return
    else:
        tournament["participants"].append({
            "id": participant_id,
            "user_id": user["id"],
            "username": user["username"],
            "nickname": user["nickname"],
            "full_name": user["full_name"],
            "institution": user["institution"],
            "role": role,
            "status": "confirmed"
        })
        save_json(TOURNAMENT_DB, tournaments)
        print(f"\n✅ Joined tournament as {role}")
        print(f"Your participant ID: {participant_id}")
        
        check_calendar = ["participants"]
        if role in check_calendar:
            
   
     


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


