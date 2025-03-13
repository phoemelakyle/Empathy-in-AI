import sqlite3 

class DatabaseManager:
    def __init__(self, db_name="user_profiles.db"):
        """Initialize database connection"""
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        """Create tables for user authentication, user profiles, and community posts"""
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS UserProfile (
                    user_id TEXT PRIMARY KEY, 
                    name TEXT, 
                    age INTEGER, 
                    gender TEXT, 
                    email TEXT,
                    user_role TEXT DEFAULT 'user'
                )
            """)
