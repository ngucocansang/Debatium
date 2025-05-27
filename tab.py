import json
import os
from tabulate import tabulate

# Constants
TOURNAMENT_DB = "tournaments.json"

def load_tournaments():
    """Safely load tournament data from JSON file"""
    try:
        if os.path.exists(TOURNAMENT_DB):
            with open(TOURNAMENT_DB, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"❌ Error loading tournament data: {str(e)}")
        return []
    except Exception as e:
        print(f"❌ Unexpected error loading tournaments: {str(e)}")
        return []

def display_participants(tournament_id):
    """
    Display tournament participants in two formatted tables:
    - Judges table (shows nicknames and tournament IDs)
    - Debaters table (with team information, shows nicknames)
    """
    try:
        tournaments = load_tournaments()
        if not tournaments:
            print("📭 No tournaments available in the database")
            return

        # Find the specified tournament
        tournament = None
        for t in tournaments:
            if t.get('id') == tournament_id:
                tournament = t
                break

        if not tournament:
            print(f"❌ Tournament with ID '{tournament_id}' not found")
            return

        # Prepare data structures
        judges = []
        debaters = []
        teams = {team['team_id']: team for team in tournament.get('teams', [])}

        # Process participants
        for participant in tournament.get('participants', []):
            # Use tournament-specific participant ID instead of user ID
            participant_id = participant.get('id', 'N/A')
            nickname = participant.get('nickname', 'Unknown')
            institution = participant.get('institution', 'N/A')
            status = participant.get('status', 'confirmed')

            if participant.get('role') == 'judge':
                judges.append([
                    participant_id[-3:],  # Last 3 digits of participant ID
                    nickname,
                    institution,
                    status
                ])
            elif participant.get('role') == 'debater':
                team_info = teams.get(participant.get('team_id', ''), {})
                debaters.append([
                    participant_id[-3:],  # Last 3 digits of participant ID
                    nickname,
                    team_info.get('team_name', 'No team'),
                    institution,
                    status
                ])

        # Display the tables
        print("\n" + "="*50)
        print(f"PARTICIPANTS FOR TOURNAMENT: {tournament.get('name', 'Unnamed')} (ID: {tournament_id})")
        print("="*50)

        if judges:
            print("\n👨‍⚖️ JUDGES")
            print(tabulate(judges,
                         headers=["ID", "Nickname", "Institution", "Status"],
                         tablefmt="grid"))
        else:
            print("\nℹ️ No judges registered")

        if debaters:
            print("\n🎤 DEBATERS")
            print(tabulate(debaters,
                         headers=["ID", "Nickname", "Team", "Institution", "Status"],
                         tablefmt="grid"))
        else:
            print("\nℹ️ No debaters registered")

        # Summary statistics
        print("\n📊 SUMMARY STATISTICS")
        print(f"- Total Judges: {len(judges)}")
        print(f"- Total Debaters: {len(debaters)}")
        print(f"- Total Teams: {len(teams)}")
        print("="*50 + "\n")

    except Exception as e:
        print(f"\n❌ Error displaying participants: {str(e)}")
        print("Please check the tournament data format and try again\n")

# Example usage (for testing)
if __name__ == "__main__":
    print("Participant Display Module")
    test_id = input("Enter tournament ID to display participants: ").strip()
    display_participants(test_id)