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
                    email TEXT
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS Users (
                    username TEXT PRIMARY KEY, 
                    password TEXT, 
                    email TEXT
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS CommunityPost (
                    postId TEXT PRIMARY KEY,
                    userId TEXT,
                    content TEXT,
                    timestamp TEXT
                )
            """)

    def execute_query(self, query, params=()):
        """Execute a query with parameters and return cursor"""
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor

class UserDatabase:
    def __init__(self):
        self.db = DatabaseManager()

    def add_user(self, username, password, email):
        """Add a user to the database"""
        existing_user = self.db.execute_query("SELECT * FROM Users WHERE username = ?", (username,)).fetchone()
        if existing_user:
            return False  # User already exists
        
        self.db.execute_query("INSERT INTO Users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
        return True

    def get_user(self, username):
        """Retrieve a user from the database"""
        return self.db.execute_query("SELECT * FROM Users WHERE username = ?", (username,)).fetchone()
