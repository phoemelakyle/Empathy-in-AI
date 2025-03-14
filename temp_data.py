import uuid
from datetime import datetime

class User:
    """Represents a regular user"""
    def __init__(self, user_id, username, email, password, user_role="patient"):
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

class Message:
    """Represents a chat message"""
    def __init__(self, sender_id, receiver_id, content, timestamp):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.message = content
        self.timestamp = timestamp

class TempDatabase:
    """Temporary database storing user data and posts in memory"""
    def __init__(self):
        self.users = {}
        self.therapists = {}
        self.posts = {}
        self.messages = []  # Store chat messages
        self.session_notes = []  # Store therapy session notes
        
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

    def save_user(self, user_id, username, password, email, role):
        user = User(user_id=user_id, username=username, email=email, password=password, user_role=role)
        self.users[user.user_id] = user
        return True

    def get_user_by_username(self, username):
        for user in self.users.values():
            if user.username == username:
                return user
        return None

    def save_message(self, patient_id, therapist_id, content, timestamp):
        """Save a chat message between a patient and therapist"""
        message = Message(
            sender_id=patient_id,
            receiver_id=therapist_id,
            content=content,
            timestamp=timestamp
        )
        self.messages.append(message)
        return True

    def get_chat_history(self, patient_id, therapist_id, limit=None):
        """Get chat history between a patient and therapist"""
        history = [
            msg for msg in self.messages 
            if (msg.sender_id == patient_id and msg.receiver_id == therapist_id) or
               (msg.sender_id == therapist_id and msg.receiver_id == patient_id)
        ]
        history.sort(key=lambda x: x.timestamp)
        if limit:
            return history[-limit:]
        return history

    def get_active_chats(self, therapist_id):
        """Get all active chats for a therapist"""
        active_chats = []
        seen_patients = set()

        # Sort messages by timestamp in reverse order
        sorted_messages = sorted(self.messages, key=lambda x: x.timestamp, reverse=True)

        for msg in sorted_messages:
            patient_id = msg.sender_id if msg.receiver_id == therapist_id else msg.receiver_id
            if patient_id not in seen_patients:
                patient = self.users.get(patient_id)
                if patient and patient.user_role == 'patient':
                    active_chats.append(patient)
                    seen_patients.add(patient_id)

        return active_chats

    def save_session_notes(self, therapist_id, patient_id, notes, timestamp):
        """Save therapy session notes"""
        session_note = {
            'therapist_id': therapist_id,
            'patient_id': patient_id,
            'notes': notes,
            'timestamp': timestamp
        }
        self.session_notes.append(session_note)
        return True

    def get_session_notes(self, therapist_id, patient_id):
        """Get all session notes for a specific patient"""
        notes = [
            note for note in self.session_notes
            if note['therapist_id'] == therapist_id and note['patient_id'] == patient_id
        ]
        return sorted(notes, key=lambda x: x['timestamp'], reverse=True)

    def get_user_chats(self, user_id):
        """Get all chat messages for a user"""
        user_chats = []
        user = self.users.get(user_id)
        
        if not user:
            return []

        for msg in self.messages:
            other_user = None
            if msg.sender_id == user_id:
                other_user = self.users.get(msg.receiver_id)
            elif msg.receiver_id == user_id:
                other_user = self.users.get(msg.sender_id)

            if other_user:
                chat = {
                    'sender_id': msg.sender_id,
                    'other_user': other_user.username,  
                    'message': msg.message,
                    'timestamp': msg.timestamp
                }
                user_chats.append(chat)

        return sorted(user_chats, key=lambda x: x['timestamp'], reverse=True)
