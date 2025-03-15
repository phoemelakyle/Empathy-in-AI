from temp_data import TempDatabase, User
import uuid

class UserAuthentication:
    def __init__(self):
        self.db = TempDatabase()  # Use temporary database

    def register(self, username, password, email, role):
        """Register a new user"""
        if self.db.get_user_by_email(email):
            print("Email already registered!")
            return False

        user = User(user_id=str(uuid.uuid4()), username=username, email=email, password=password, user_role=role)
        self.db.users[user.user_id] = user
        print("✅ Registration successful!")
        return True

    def login(self, username, password):
        """Authenticate user"""
        for user in self.db.users.values():
            if user.username == username and user.password == password:
                print(f"✅ Login successful! Welcome, {username}.")
                return user.user_id, user.user_role
        
        print("❌ Invalid credentials. Please try again.")
        return None
