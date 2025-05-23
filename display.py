import os 
from tournament import load_tournaments

def display_participants():
    tournaments = load_tournaments()

    if not tournaments:
        print("No tournaments available.")
        return

    print("\n📋 Available Tournaments:")
    for t in tournaments:
        print(f"- ID: {t['id']} | Name: {t['name']}")

    tid = input("\nEnter the tournament ID to view participants: ").strip()
    tournament = next((t for t in tournaments if t["id"] == tid), None)

    if not tournament:
        print("❌ Tournament not found.")
        return

    participants = tournament.get("participants", [])
    if not participants:
        print("📭 No participants in this tournament.")
        return

    print(f"\n👥 Participants in '{tournament['name']}' (ID: {tournament['id']}):\n")
    for i, p in enumerate(participants, 1):
        team_info = f" - Team ID: {p['team_id']}" if p.get("team_id") else ""
        print(f"{i}. {p['full_name']} ({p['role'].capitalize()}){team_info}")
