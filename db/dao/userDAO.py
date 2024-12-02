from typing import Optional, List, Dict, Tuple
from models.user import User
from ..couch_client import CouchClient


class UserDAO:

    def __init__(self):
        """
        Initializes the DAO with a CouchDBManager instance.
        """
        self.db_name = "users"
        self.manager = CouchClient()
        

    def create_user(self, user: User) -> Tuple[str, bool, str]|None:
        """
        Creates a new user in the database.
        """
        if self.get_user_by_email(user.email):
            raise ValueError("A user with this email already exists.")
        user_data = user.to_dict()
        return self.manager.create_doc(self.db_name, user_data)

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieves a user by their ID.
        """
        doc = self.manager.get_doc(self.db_name, user_id)
        return User.from_dict(doc) if doc else None

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieves a user by their email.
        """
        query = {"selector": {"email": email}}
        results = self.manager.query_documents(self.db_name, query)
        if results:
            return User.from_dict(results[0])
        return None

    def get_users(self, query_params: Optional[Dict] = None) -> List[User]:
        """
        Retrieves users based on optional query parameters.
        """
        query = {"selector": query_params or {}}
        results = self.manager.query_documents(self.db_name, query)
        return [User.from_dict(doc) for doc in results]

    def update_user(self, user_id: int, updated_data: Dict) -> bool:
        """
        Updates a user's information.
        """
        try:
            self.manager.update_doc(self.db_name, user_id, updated_data)
            return True
        except KeyError:
            raise ValueError("User not found.")
        except Exception as e:
            raise RuntimeError(f"Error updating user: {e}")

    def delete_user(self, user_id: int) -> bool:
        """
        Deletes a user by their ID.
        """
        try:
            return self.manager.delete_doc(self.db_name, user_id)
        except KeyError:
            raise ValueError("User not found.")
        except Exception as e:
            raise RuntimeError(f"Error deleting user: {e}")
