from temp_data import TempDatabase
from datetime import datetime
import uuid

class CommunityPost:
    """Manages community posts and integrates user data."""

    def __init__(self):
        """Initialize in-memory database"""
        self.db = TempDatabase()

    def create_post(self, user_id: str, content: str):
        """Creates a new community post"""
        # Ensure the user exists before allowing post creation
        user = self.db.get_user(user_id)
        if not user:
            print("❌ User not found. Cannot create post.")
            return

        # Generate a unique post ID
        post_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Store the new post in the database
        new_post = {
            "post_id": post_id,
            "user_id": user_id,
            "username": user.username,  # Store username for display
            "content": content,
            "timestamp": timestamp
        }

        self.db.posts[post_id] = new_post  # Add the new post to TempDatabase
        print(f"✅ Post created successfully! Post ID: {post_id}")

    def display_posts(self):
        """Displays all community posts"""
        posts = self.db.get_all_posts()
        if not posts:
            print("🚫 No posts available.")
            return

        print("\n===== 📢 Community Posts =====")
        for post in posts:
            print(f"\n🆔 [Post ID: {post['post_id']}] - 📅 {post['timestamp']}")
            print(f"👤 {post['username']}")
            print(f"📝 Content: {post['content']}")
            print("-" * 40)
