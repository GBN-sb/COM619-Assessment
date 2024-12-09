import bcrypt
import re
import uuid
from typing import Optional


class User:
    """
    User class implementing schema with secure password handling, role validation, and unique ID management.
    """

    _id_counter = 1

    def __init__(
        self,
        name: str,
        email: str,
        password: str,
        profile_picture: Optional[str] = None,
        role: Optional[str] = "user",
        bio: Optional[str] = None,
        id: str = None,
    ):
        self.id = id if id != None else str(uuid.uuid4())
        self.name = name
        self.email = email
        self.password_hash = self.hash_password(password)
        self.profile_picture = profile_picture
        self.role = role
        self.bio = bio

        self.validate()

    @classmethod
    def _generate_id(cls) -> int:
        """
        Generates a unique, sequential integer ID.
        """
        id_value = cls._id_counter
        cls._id_counter += 1
        return id_value

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashes the password securely using bcrypt.
        """
        if not password:
            raise ValueError("Password cannot be empty.")
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifies a plaintext password against the hashed password.
        """
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    def validate(self):
        """
        Validates the user's fields against the schema.
        """
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Name must be a non-empty string.")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise ValueError("Invalid email format.")
        if not self.password_hash or len(self.password_hash) < 60:
            raise ValueError("Password hash is invalid.")
        valid_roles = ["user", "admin", "moderator"]
        if self.role not in valid_roles:
            raise ValueError(f"Role must be one of {valid_roles}.")

    def to_dict(self) -> dict:
        """
        Converts the User object to a dictionary for serialization.
        """
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "passwordHash": self.password_hash,
            "profilePicture": self.profile_picture,
            "role": self.role,
            "bio": self.bio,
        }

    @staticmethod
    def from_dict(data: dict) -> "User":
        """
        Reconstructs a User object from a dictionary.
        """
        required_fields = {"id", "name", "email", "passwordHash", "profilePicture", "role", "bio"}
        if not required_fields.issubset(data.keys()):
            raise ValueError(f"Missing required fields: {required_fields - data.keys()}")

        user = User(
            id=data["id"],
            name=data["name"],
            email=data["email"],
            password="placeholder",
            profile_picture=data.get("profilePicture"),
            role=data.get("role", "user"),
            bio=data.get("bio"),
        )
        user.password_hash = data["passwordHash"] 
        return user
