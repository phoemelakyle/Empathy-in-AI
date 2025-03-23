import getpass
from user_auth import UserAuthentication
from community_post import CommunityPost
from chat_system import ChatSystem
from database_manager import DatabaseManager
from therapist_description import TherapistDescription

def main():
    auth = UserAuthentication()
    db = DatabaseManager()
    community = CommunityPost(db)
    chat_system = ChatSystem(db)

    while True:
        print("\n=== Welcome to Empathy in AI ===")
        print("1. Create Profile & Register")
        print("2. Login")
        print("3. Exit")
        choice = input("\nEnter choice: ")

        if choice == "1":
            print("\n=== Registration ===")
            username = input("Enter username: ")
            email = input("Enter email: ")
            password = getpass.getpass("Enter password: ")  
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
            password = getpass.getpass("Enter password: ")  
            result = auth.login(username, password)

            if result:
                user_id, user_role = result
                print(f"\n✅ Welcome back! You are logged in as: {user_role}")

                if user_role == "therapist":
                    therapist_desc = TherapistDescription(user_id, db)

                    while True:
                        print("\n=== Therapist Menu ===")
                        print("1. Add/Update Description")
                        print("2. View Description")
                        print("3. Edit Description")
                        print("4. View Messages")  
                        print("5. Go to Main Menu")
                        therapist_choice = input("\nEnter choice: ")

                        if therapist_choice == "1":
                            name = input("Enter your name: ")
                            specialization = input("Enter specialization: ")
                            experience = input("Enter years of experience: ")
                            bio = input("Enter a brief bio: ")

                            therapist_desc.add_or_update_description(name, specialization, experience, bio)
                            print("✅ Description and Therapist ID updated successfully!")

                        elif therapist_choice == "2":
                            details = therapist_desc.get_therapist_details()
                            if details:
                                print(f"\n👨‍⚕️ Name: {details['name']}")
                                print(f"🔹 Specialization: {details['specialization']}")
                                print(f"📆 Experience: {details['experience']} years")
                                print(f"📖 Bio: {details['bio']}")
                            else:
                                print("❌ No description found. Please add one.")

                        elif therapist_choice == "3":
                            name = input("Enter your updated name: ")
                            specialization = input("Enter updated specialization: ")
                            experience = input("Enter updated years of experience: ")
                            bio = input("Enter updated bio: ")

                            therapist_desc.add_or_update_description(name, specialization, experience, bio)
                            print("✅ Description updated successfully!")

                        elif therapist_choice == "4":  
                            chat_system.view_messages(user_id)

                        elif therapist_choice == "5":
                            break

                if user_role == "patient":
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
                                print("3. Edit Post")
                                print("4. Delete Post")
                                print("5. Return to Main Menu")
                                post_choice = input("\nEnter choice: ")

                                if post_choice == "1":
                                    content = input("\nEnter your post content: ")
                                    community.create_post(user_id, content)
                                    print("✅ Post created successfully!")

                                elif post_choice == "2":
                                    posts = community.fetch_all_posts()
                                    if posts:
                                        print("\n=== Community Posts ===")
                                        for post in posts:
                                            print(f"\n🆔 {post[0]}\n👤 {post[1]}\n📅 {post[3]}\n💬 {post[2]}\n")
                                    else:
                                        print("No posts available.")

                                elif post_choice == "3":
                                    post_id = input("\nEnter Post ID to edit: ")
                                    new_content = input("Enter new content: ")
                                    if community.edit_post(post_id, new_content):
                                        print("✅ Post updated successfully!")
                                    else:
                                        print("❌ Post not found!")

                                elif post_choice == "4":
                                    post_id = input("\nEnter Post ID to delete: ")
                                    if community.delete_post(post_id):
                                        print("✅ Post deleted successfully!")
                                    else:
                                        print("❌ Post not found!")

                                elif post_choice == "5":
                                    break

                        elif menu_choice == "2":
                            chat_system.start_chat(user_id, user_role)

                        elif menu_choice == "3":
                            print("\n👋 Goodbye! You have been logged out.")
                            break

        elif choice == "3":
            print("\n👋 Thank you for using our platform. Goodbye!")
            break

        else:
            print("\n❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
