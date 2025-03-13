from database_manager import UserDatabase

class UserAuthentication:
    def __init__(self):
        self.db = UserDatabase()  # Initialize database instance

    def register(self, username, password, email):
        """Register a new user"""
        if self.db.add_user(username, password, email):
            print("Registration successful!")
        else:
            print("Username already exists!")

    @staticmethod
    def login(username, password):
        """Authenticate user"""
        db = UserDatabase()
        user = db.get_user(username)

        if not user:
            print("User not found.")
            return False

        if user[1] == password:  # Ensure correct index for password
            print("Login successful! Proceeding to community post section...")
            return True

        print("Invalid credentials. Please try again.")
        return False

    @staticmethod
    def logout():
        """Logout user"""
        print("User logged out successfully!")
