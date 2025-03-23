from database_manager import DatabaseManager, UserProfileRepository

class UserProfile:
    # Encapsulation, Abstraction
    def __init__(self, user_id, name=None, age=None, gender=None, email=None, user_role="user"):
        """Initialize user profile attributes"""
        self.user_id = user_id
        self.name = name
        self.age = age
        self.gender = gender
        self.email = email
        self.user_role = user_role
        self._repo = UserProfileRepository(DatabaseManager())  # Dependency Injection

    # Encapsulation, Abstraction
    def save_to_db(self):
        """Save user profile using the repository"""
        return self._repo.save_user(self.user_id, self.name, self.age, self.gender, self.email, self.user_role)

    # Encapsulation, Abstraction
    def get_user_role(self):
        """Retrieve user role using the repository"""
        return self._repo.get_user_role(self.user_id)
