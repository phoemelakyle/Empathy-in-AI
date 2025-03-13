from user_profile import UserProfile

class UserFactory:
    @staticmethod
    def create_user(user_id, name, age, gender, email, user_role):
        """
        Factory method to return the appropriate user type.

        Args:
            user_id (str): User ID
            name (str): Name of the user
            age (int): Age
            gender (str): Gender
            email (str): Email
            user_role (str): "user" or "therapist"

        Returns:
            UserProfile: An instance of UserProfile with the correct role
        """
        return UserProfile(user_id, name, age, gender, email, user_role)
