from tournament import load_tournaments
def display_participants():
    tournaments = load_tournaments()
    if not tournaments:
        print("No tournaments available.")
        return
    print("\n Available Tournaments:")
    for i, t in enumerate(tournaments, 1):
        print(f"{i}. {t['name']} (ID: {t['id']})")
    try:
        choice = int(input("\nEnter the tournament number to view participants: ").strip())
        if choice < 1 or choice > len(tournaments):
            print("Invalid tournament number.")
            return
    except ValueError:
        print(" Please enter a valid number.")
        return

    tournament = tournaments[choice - 1]
    participants = tournament.get("participants", [])

    if not participants:
        print(" No participants in this tournament.")
        return

    print(f"\n Participants in '{tournament['name']}' (ID: {tournament['id']}):\n")
    for i, p in enumerate(participants, 1):
        team_info = f" - Team ID: {p['team_id']}" if p.get("team_id") else ""
        print(f"{i}. {p['full_name']} ({p['role'].capitalize()}){team_info}")
