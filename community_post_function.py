from database_manager import DatabaseManager
from datetime import datetime

class CommunityPost:
    """Manages community posts and integrates user data."""

    def __init__(self):
        """Initialize database connection"""
        self.db = DatabaseManager()

    def create_post(self, user_id: str, content: str):
        """Creates a new community post and immediately displays updated posts"""
        post_id = f"post_{datetime.now().strftime('%Y%m%d%H%M%S')}"  # Unique post ID
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Store the new post in the database
        self.db.execute_query(
            "INSERT INTO CommunityPost (postId, userId, content, timestamp) VALUES (?, ?, ?, ?)", 
            (post_id, user_id, content, timestamp)
        )
        print(f"✅ Post created successfully! Post ID: {post_id}")

        # Automatically display updated posts
        self.display_posts()

    def delete_post(self, post_id: str):
        """Deletes a post by its ID and refreshes the post list"""
        self.db.execute_query("DELETE FROM CommunityPost WHERE postId = ?", (post_id,))
        print(f"🗑️ Post {post_id} deleted successfully!")

        # Refresh the view
        self.display_posts()

    def edit_post(self, post_id: str, new_content: str):
        """Edits an existing post and refreshes the post list"""
        self.db.execute_query(
            "UPDATE CommunityPost SET content = ? WHERE postId = ?", 
            (new_content, post_id)
        )
        print(f"✏️ Post {post_id} updated successfully!")

        # Refresh the view
        self.display_posts()

    def fetch_all_posts(self):
        """Fetches all community posts with user details"""
        return self.db.execute_query("""
            SELECT c.postId, COALESCE(u.name, 'userId') AS user_name, c.content, c.timestamp 
            FROM CommunityPost c
            LEFT JOIN UserProfile u ON c.userId = u.user_id
        """).fetchall()

    def display_posts(self):
        """Displays all community posts with user details"""
        posts = self.fetch_all_posts()
        if not posts:
            print("🚫 No posts available.")
            return

        print("\n===== 📢 Community Posts =====")
        for post in posts:
            post_id, user_name, content, timestamp = post

            print(f"\n🆔 [Post ID: {post_id}] - 📅 {timestamp}")
            print(f"👤 {user_name}")  # Show user name instead of user ID
            print(f"📝 Content: {content}")
            print("-" * 40)
