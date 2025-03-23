from database_manager import TherapistRepository, DatabaseManager

class TherapistDescription:
    """Handles therapist descriptions and profile details."""
    def __init__(self, therapist_id: int, db: DatabaseManager):
        """Initialize with therapist ID and database instance."""
        self._therapist_id = self._validate_therapist_id(therapist_id)
        self._repo = TherapistRepository(db)

    @staticmethod
    def _validate_therapist_id(therapist_id):
        """Ensure therapist ID is an integer."""
        try:
            return int(therapist_id)
        except ValueError:
            print("❌ ERROR: Therapist ID must be an integer.")
            return None

    def add_or_update_description(self, name: str, specialization: str, experience: str, bio: str):
        """Add or update therapist description."""
        if not self._is_valid_therapist():
            return
        
        existing_therapist = self._repo.get_therapist_by_id(self._therapist_id)
        if existing_therapist:
            self._repo.update_therapist(self._therapist_id, name, specialization, experience, bio)
        else:
            self._repo.add_therapist(self._therapist_id, name, specialization, experience, bio)

    def get_therapist_details(self):
        """Retrieve therapist details from the database."""
        if not self._is_valid_therapist():
            return None
        result = self._repo.get_therapist_by_id(self._therapist_id)
        return self._format_therapist_details(result) if result else None

    def _is_valid_therapist(self):
        """Check if therapist ID is valid."""
        if self._therapist_id is None:
            print("❌ ERROR: Invalid Therapist ID.")
            return False
        return True

    @staticmethod
    def _format_therapist_details(result):
        """Format database result into a dictionary."""
        return {
            "user_id": result[0],
            "name": result[1],
            "specialization": result[2],
            "experience": result[3],
            "bio": result[4]
        }
