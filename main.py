from user_profile import signup, signin
from tournament_main import tournament_dashboard

def main():
    print("==== Debatium Login System ====")
    print("1. Sign up")
    print("2. Sign in")
    choice = input("Choose option (1 or 2): ").strip()

    if choice == "1":
        signup()
    elif choice == "2":
        user = signin()
        if user:
            print("\n1. Tournament dashboard")
            print("2. Let's Spar (Coming soon)")
            dash = input("Choose option: ").strip()
            if dash == "1":
                tournament_dashboard(user)
            else:
                print("👷 Feature coming soon.")
        else:
            print("⚠️ Sign-in failed.")
    else:
        print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
