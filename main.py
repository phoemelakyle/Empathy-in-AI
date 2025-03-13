from user_auth import UserAuthentication
from community_post import CommunityPost
from temp_data import TempDatabase

def main():
    auth = UserAuthentication()
    community = CommunityPost()
    temp_db = TempDatabase()  # Use the temporary database

    while True:
        print("\nWelcome to the Community Platform")
        print("1. Create Profile & Register")
        print("2. Login")
        print("3. View All Users")
        print("4. View All Therapists")
        print("5. Exit")
        choice = input("Enter choice: ")

        # REGISTER
        if choice == "1":
            print("\nStep 1: Create Your Profile")
            user_id = input("Enter User ID: ")
            username = input("Enter username: ")
            email = input("Enter email: ")
            password = input("Enter password: ")
            role = input("Enter role (user/therapist): ").strip().lower()

            if role not in ["user", "therapist"]:
                print("❌ Invalid role! Defaulting to 'user'.")
                role = "user"

            if auth.register(username, password, email, role):
                print("✅ Registration successful!")
            else:
                print("❌ Registration failed.")

        # LOGIN
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            result = auth.login(username, password)

            if result:
                user_id, user_role = result
                print(f"Logged in as {user_role}.")

                while True:
                    print("\nCommunity Post Section")
                    print("1. Create Post")
                    print("2. View Posts")
                    print("3. Logout")
                    post_choice = input("Enter choice: ")

                    if post_choice == "1":
                        content = input("Enter your post content: ")
                        community.create_post(user_id, content)

                    elif post_choice == "2":
                        community.display_posts()

                    elif post_choice == "3":
                        print("Logged out.")
                        break  # Exit to main menu

                    else:
                        print("Invalid choice! Try again.")

        # VIEW USERS
        elif choice == "3":
            print("\n=== Users ===")
            for user in temp_db.get_all_users():
                print(user.to_dict())

        # VIEW THERAPISTS
        elif choice == "4":
            print("\n=== Therapists ===")
            for therapist in temp_db.get_all_therapists():
                print(therapist.to_dict())

        # EXIT
        elif choice == "5":
            print("Exiting system.")
            break

        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    main()
