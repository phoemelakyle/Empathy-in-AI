from user_auth import UserAuthentication
from user_profile import UserProfile
from community_post import CommunityPost

def main():
    auth = UserAuthentication()
    community = CommunityPost()
    
    while True:
        print("\nWelcome to the Community Platform")
        print("1. Create Profile & Register")
        print("2. Login")
        print("3. Update Email")
        print("4. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            print("\nStep 1: Create Your Profile")
            user_id = input("Enter User ID: ")  # This should be unique

            name = input("Enter your name: ")
            while True:
                try:
                    age = int(input("Enter your age: "))
                    if age <= 0:
                        print("Age must be a positive number. Try again.")
                        continue
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")

            gender = input("Enter your gender: ")
            email = input("Enter your email: ")

            user_profile = UserProfile(user_id, name, age, gender, email)
            if user_profile.save_to_db():  # Ensure profile creation was successful
                print("\nProfile created successfully! Now proceed to registration.")

                print("\nStep 2: Register Your Account")
                username = input("Enter username: ")
                password = input("Enter password: ")

                if auth.register(username, password, email):
                    print("\nRegistration successful! You can now log in.")
                else:
                    print("\nRegistration failed. Please try again.")
            else:
                print("\nProfile creation failed. Registration aborted.")

        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")

            user_id = auth.login(username, password)
            if user_id:
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
                        break

                    else:
                        print("Invalid choice! Try again.")

        elif choice == "3":
            user_id = input("Enter user ID to update email: ")
            new_email = input("Enter new email: ")

            user = UserProfile(user_id)
            current_email = user.get_email()

            if current_email:
                user.update_email(new_email)
            else:
                print("User not found.")

        elif choice == "4":
            print("Exiting system.")
            break

        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    main()
