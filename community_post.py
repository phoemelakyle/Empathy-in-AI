from database_manager import DatabaseManager
from datetime import datetime
from typing import List, Tuple, Optional

class CommunityPost:
    """Manages community posts and integrates user data."""  # Abstraction

    def __init__(self, db: DatabaseManager):
        """Initialize with a database connection."""  # Encapsulation
        self._db = db  # Encapsulation

    def create_post(self, user_id: int, content: str) -> Optional[int]:
        """Creates a new community post and returns the post ID."""  # Abstraction
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = "INSERT INTO community_posts (user_id, content, timestamp) VALUES (?, ?, ?)"
        cursor = self._db.execute_query(query, (user_id, content, timestamp))
        return cursor.lastrowid if cursor else None

    def delete_post(self, post_id: int) -> bool:
        """Deletes a post by its ID if it exists."""  # Encapsulation
        existing_post = self.get_post_details(post_id)
        if existing_post[0]: 
            self._db.execute_query("DELETE FROM community_posts WHERE post_id = ?", (post_id,))
            return True
        return False  

    def edit_post(self, post_id: int, new_content: str) -> bool:
        """Updates an existing post's content if it exists."""  # Encapsulation
        existing_post = self.get_post_details(post_id)
        if existing_post[0]: 
            self._db.execute_query(
                "UPDATE community_posts SET content = ? WHERE post_id = ?", 
                (new_content, post_id)
            )
            return True
        return False  

    def fetch_all_posts(self) -> List[Tuple[int, str, str, str]]:
        """Fetches all community posts with user details, displaying user_id if username is not found."""  # Abstraction
        query = """
            SELECT c.post_id, 
                   COALESCE(u.username, CAST(c.user_id AS TEXT)) AS user_name, 
                   c.content, 
                   c.timestamp 
            FROM community_posts c
            LEFT JOIN users u ON c.user_id = u.user_id
            ORDER BY c.timestamp DESC
        """
        return self._db.fetch_all(query)

    def get_post_details(self, post_id: int) -> Tuple[int, str, str, str]:
        """Retrieves details of a specific post, displaying user_id if username is not found."""  # Reusability
        query = """
            SELECT c.post_id, 
                   COALESCE(u.username, CAST(c.user_id AS TEXT)) AS user_name, 
                   c.content, 
                   c.timestamp 
            FROM community_posts c 
            LEFT JOIN users u ON c.user_id = u.user_id 
            WHERE c.post_id = ?
        """
        result = self._db.fetch_one(query, (post_id,))
        return result if result else (0, "Unknown", "No Content", "")  # Encapsulation
