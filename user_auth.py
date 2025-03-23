import bcrypt
import uuid
from database_manager import DatabaseManager

class PasswordManager:
    """Handles password hashing and verification."""
    
    # Encapsulation
    @staticmethod
    def hash_password(password):
        """Hash a password before storing it."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    # Encapsulation
    @staticmethod
    def verify_password(plain_password, hashed_password):
        """Verify the entered password against the stored hashed password."""
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

class UserAuthentication:
    """Manages user registration and authentication."""
    
    # Encapsulation, Abstraction, Dependency Injection
    def __init__(self):
        self.db = DatabaseManager()

    # Encapsulation, Abstraction, Single Responsibility Principle
    def register(self, username, password, email, role):
        """Register a new user with hashed password."""
        existing_user = self.db.fetch_one("SELECT email FROM users WHERE email = ?", (email,))
        if existing_user:
            print("❌ Email already registered!")
            return False

        # Encapsulation
        hashed_password = PasswordManager.hash_password(password)
        query = """
            INSERT INTO users (username, email, password, role)
            VALUES (?, ?, ?, ?)
        """
        # Abstraction
        self.db.execute_query(query, (username, email, hashed_password, role))
        print("✅ Registration successful!")
        return True

    # Encapsulation, Abstraction
    def login(self, username, password):
        """Authenticate user with password verification."""
        query = "SELECT user_id, username, password, role FROM users WHERE username = ?"
        user = self.db.fetch_one(query, (username,))

        # Encapsulation
        if user and PasswordManager.verify_password(password, user[2]):
            print(f"✅ Login successful! Welcome, {username}.")
            return user[0], user[3]

        print("❌ Invalid credentials. Please try again.")
        return None
