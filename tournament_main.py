from tournament import create_tournament, add_participant, add_post_conflict, join_tournament

def tournament_dashboard(current_user):
    print("\n==== 🧑‍💼 Welcome to your profile ====")
    print(f"🔑 User ID: {current_user['id']}")
    print(f"🏷️  Nickname: {current_user['nickname']}")
    print(f"🪪 Full name: {current_user['full_name']}")
    print("")

    tournament_ids_created = []

    while True:
        print("\n🎯 Options:")
        print("1. Create a new Tournament")
        print("2. Join a Tournament")
        if tournament_ids_created:
            print("3. Add participant to my tournament")
            print("4. Add post-tournament conflict")
        print("0. Exit")

        choice = input("Choose action: ").strip()

        if choice == "1":
            tid = create_tournament(current_user)
            tournament_ids_created.append(tid)
        elif choice == "2":
            join_tournament(current_user)
        elif choice == "3" and tournament_ids_created:
            add_participant()
        elif choice == "4" and tournament_ids_created:
            add_post_conflict()
        elif choice == "0":
            print("👋 Exiting dashboard.")
            break        
        else:
            print("❌ Invalid option.")


