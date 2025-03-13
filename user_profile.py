from database_manager import DatabaseManager

class UserProfile:
    def __init__(self, user_id, name=None, age=None, gender=None, email=None, user_role="user"):
        """Initialize user profile attributes"""
        self._db = DatabaseManager()
        self.user_id = user_id
        self.name = name
        self.age = age
        self.gender = gender
        self.email = email
        self.user_role = user_role  # New field

    def save_to_db(self):
        """Store user profile in the database, preventing duplicate user IDs"""
        try:
            existing_user = self._db.execute_query(
                "SELECT user_id FROM UserProfile WHERE user_id=?", (self.user_id,)
            ).fetchone()

            if existing_user:
                print("❌ Error: User already exists in the database.")
                return False

            self._db.execute_query(
                "INSERT INTO UserProfile (user_id, name, age, gender, email, user_role) VALUES (?, ?, ?, ?, ?, ?)", 
                (self.user_id, self.name, self.age, self.gender, self.email, self.user_role)
            )
            print(f"✅ UserProfile for {self.name} created successfully.")
            return True

        except Exception as e:
            print(f"❌ Database error while saving user: {e}")
            return False

    def get_user_role(self):
        """Retrieve user role from database"""
        try:
            result = self._db.execute_query(
                "SELECT user_role FROM UserProfile WHERE user_id=?", 
                (self.user_id,)
            ).fetchone()

            return result[0] if result else None

        except Exception as e:
            print(f"❌ Database error while retrieving user role: {e}")
            return None
