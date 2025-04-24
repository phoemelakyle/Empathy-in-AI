import sqlite3 
import uuid

class DatabaseManager:
    def __init__(self, db_name="user_profiles.db"):
        """Initialize database connection"""
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_tables()
    
    def fetch_one(self, query, params=()):
        """Execute a SELECT query and return a single result."""
        cursor = self.conn.execute(query, params)
        return cursor.fetchone()


    def get_all_therapists(self):
        query = "SELECT user_id, username FROM users WHERE role = 'therapist'"
        return self.fetch_all(query)
    
    def get_chat_history(self, user1_id, user2_id, limit=None):
        query = """
            SELECT sender_id, receiver_id, message, timestamp
            FROM messages
            WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)
            ORDER BY timestamp ASC
        """
        params = (user1_id, user2_id, user2_id, user1_id)
        results = self.fetch_all(query, params)
        return results[-limit:] if limit else results
    
    def save_message(self, sender_id, receiver_id, message, timestamp):
        query = """
            INSERT INTO messages (message_id, sender_id, receiver_id, message, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """
        self.execute_query(query, (str(uuid.uuid4()), sender_id, receiver_id, message, timestamp))

    
    def execute_query(self, query, params=()):
        """Execute a write query like INSERT, UPDATE, DELETE."""
        with self.conn:
            cursor = self.conn.execute(query, params)
            return cursor

    def create_tables(self):
        """Create tables for user authentication, user profiles, posts, messages, and session notes"""
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY, 
                    username TEXT, 
                    email TEXT, 
                    password TEXT,
                    role TEXT
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS community_posts (
                    post_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    content TEXT,
                    timestamp TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    message_id TEXT PRIMARY KEY,
                    sender_id TEXT,
                    receiver_id TEXT,
                    message TEXT,
                    timestamp TEXT
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS session_notes (
                    note_id TEXT PRIMARY KEY,
                    therapist_id TEXT,
                    patient_id TEXT,
                    notes TEXT,
                    timestamp TEXT
                )
            """)


class TherapistRepository:
    """Handles database operations related to therapists."""
    def __init__(self, db: DatabaseManager):
        self.db = db

    def get_therapist_by_id(self, therapist_id):
        query = "SELECT user_id, name, specialization, experience, bio FROM UserProfile WHERE user_id = ?"
        return self.db.fetch_one(query, (therapist_id,))

    def add_therapist(self, user_id, name, specialization, experience, bio):
        query = """
            INSERT INTO UserProfile (user_id, name, gender, age, email, user_role)
            VALUES (?, ?, '', 0, '', 'therapist')
        """
        self.db.execute_query(query, (user_id, name))

        # Add description data
        query = """
            UPDATE UserProfile SET 
                name = ?, 
                specialization = ?, 
                experience = ?, 
                bio = ?
            WHERE user_id = ?
        """
        self.db.execute_query(query, (name, specialization, experience, bio, user_id))

    def update_therapist(self, user_id, name, specialization, experience, bio):
        query = """
            UPDATE UserProfile SET 
                name = ?, 
                specialization = ?, 
                experience = ?, 
                bio = ?
            WHERE user_id = ?
        """
        self.db.execute_query(query, (name, specialization, experience, bio, user_id))
