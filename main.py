from user_auth import UserAuthentication
from community_post import CommunityPost
from temp_data import TempDatabase
from chat_system import ChatSystem

def main():
    auth = UserAuthentication()
    community = CommunityPost()
    temp_db = TempDatabase()
    chat_system = ChatSystem(temp_db)

    while True:
        print("\n=== Welcome to the Community Platform ===")
        print("1. Create Profile & Register")
        print("2. Login")
        print("3. View All Users")
        print("4. View All Therapists")
        print("5. Exit")
        choice = input("\nEnter choice: ")

        if choice == "1":
            print("\n=== Registration ===")
            user_id = input("Enter User ID: ")
            username = input("Enter username: ")
            email = input("Enter email: ")
            password = input("Enter password: ")
            role = input("Enter role (patient/therapist): ").strip().lower()

            if role not in ["patient", "therapist"]:
                print("❌ Invalid role! Defaulting to 'patient'.")
                role = "patient"

            if auth.register(username, password, email, role):
                print("✅ Registration successful!")
            else:
                print("❌ Registration failed.")

        elif choice == "2":
            print("\n=== Login ===")
            username = input("Enter username: ")
            password = input("Enter password: ")
            result = auth.login(username, password)

            if result:
                user_id, user_role = result
                print(f"\n✅ Welcome back! You are logged in as: {user_role}")

                while True:
                    print("\n=== Main Menu ===")
                    print("1. Community Posts")
                    print("2. Messages")
                    print("3. Logout")
                    menu_choice = input("\nEnter choice: ")

                    if menu_choice == "1":
                        while True:
                            print("\n=== Community Posts ===")
                            print("1. Create Post")
                            print("2. View Posts")
                            print("3. Return to Main Menu")
                            post_choice = input("\nEnter choice: ")

                            if post_choice == "1":
                                content = input("\nEnter your post content: ")
                                community.create_post(user_id, content)
                                print("✅ Post created successfully!")
                            elif post_choice == "2":
                                community.display_posts()
                            elif post_choice == "3":
                                break

                    elif menu_choice == "2":
                        chat_system.start_chat(user_id, user_role)
                    
                    elif menu_choice == "3":
                        print("\n👋 Goodbye! You have been logged out.")
                        break

        elif choice == "3":
            print("\n=== All Users ===")
            users = temp_db.get_all_users()
            if users:
                for user in users:
                    print(f"Username: {user.username}, Role: {user.user_role}")
            else:
                print("No users found.")

        elif choice == "4":
            print("\n=== All Therapists ===")
            therapists = temp_db.get_all_therapists()
            if therapists:
                for therapist in therapists:
                    print(f"Dr. {therapist.username}")
            else:
                print("No therapists found.")

        elif choice == "5":
            print("\n👋 Thank you for using our platform. Goodbye!")
            break

        else:
            print("\n❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
