import uuid

class User:
    """Represents a regular user"""
    def __init__(self, user_id, username, email, password, user_role="user"):
        self.user_id = user_id or str(uuid.uuid4())
        self.username = username
        self.email = email
        self.password = password  # In production, this should be hashed
        self.user_role = user_role

    def to_dict(self):
        """Convert user data to a dictionary"""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "user_role": self.user_role
        }

class Therapist(User):
    """Represents a therapist, which is a specialized user"""
    def __init__(self, user_id, username, email, password, specialization=None, bio=""):
        super().__init__(user_id, username, email, password, user_role="therapist")
        self.specialization = specialization or []
        self.bio = bio

    def to_dict(self):
        """Convert therapist data to a dictionary"""
        base_dict = super().to_dict()
        base_dict.update({
            "specialization": self.specialization,
            "bio": self.bio
        })
        return base_dict


class TempDatabase:
    """Temporary database storing user data and posts in memory"""
    def __init__(self):
        self.users = {}
        self.therapists = {}
        self.posts = {}

        # Preload mock data
        self.load_mock_data()

    def load_mock_data(self):
        """Loads temporary users, a therapist, and mock posts into memory"""
        # Create mock users
        user1 = User(user_id="user_001", username="alice", email="alice@example.com", password="password123")
        user2 = User(user_id="user_002", username="bob", email="bob@example.com", password="password123")
        user3 = User(user_id="user_003", username="charlie", email="charlie@example.com", password="password123")
        
        # Create mock therapist
        therapist = Therapist(
            user_id="therapist_001",
            username="dr_smith",
            email="drsmith@example.com",
            password="securepass",
            specialization=["Anxiety", "Depression"],
            bio="Licensed therapist with 10 years of experience in mental health support."
        )

        # Store users and therapist in the database
        self.users[user1.user_id] = user1
        self.users[user2.user_id] = user2
        self.users[user3.user_id] = user3
        self.therapists[therapist.user_id] = therapist
        self.users[therapist.user_id] = therapist  # Include therapist in users

        # Create mock posts
        self.posts["post_001"] = {
            "post_id": "post_001",
            "user_id": user1.user_id,
            "username": user1.username,
            "content": "Feeling a bit anxious today. Any advice?",
            "timestamp": "2024-03-13 10:15:00"
        }

        self.posts["post_002"] = {
            "post_id": "post_002",
            "user_id": user2.user_id,
            "username": user2.username,
            "content": "I just started practicing meditation, and it’s been helpful. Anyone else tried it?",
            "timestamp": "2024-03-13 12:30:00"
        }

        self.posts["post_003"] = {
            "post_id": "post_003",
            "user_id": therapist.user_id,
            "username": therapist.username,
            "content": "Remember, managing anxiety takes time. Small steps matter!",
            "timestamp": "2024-03-13 15:45:00"
        }

    def get_user(self, user_id):
        """Retrieve a user by ID"""
        return self.users.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve a user by email"""
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    def get_all_users(self):
        """Retrieve all users"""
        return list(self.users.values())

    def get_all_therapists(self):
        """Retrieve all therapists"""
        return list(self.therapists.values())

    def get_all_posts(self):
        """Retrieve all posts"""
        return list(self.posts.values())

