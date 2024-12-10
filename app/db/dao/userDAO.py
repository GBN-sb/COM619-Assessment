from typing import Optional
from models.user import User
from ..couch_client import CouchClient


class UserDAO:

    def __init__(self, db_name="users") -> None:
        """
        Initialises the DAO with a CouchDBManager instance.
        """
        self.db_name = db_name
        self.client = CouchClient()
        

    def add_user(self, user: User) -> bool:
        """
        Adds a user to the database.
        """
        user_dict = user.to_dict()
        try:
            result = self.client.create_doc(self.db_name, user_dict)
            if result:
                return result[1]
            return False
        except Exception as e:
            raise e
        
    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email.
        """
        query = {"email": email}
        try:
            result = self.client.query_documents(self.db_name, query)
            if result:
                return User.from_dict(result[0])
            return None
        except Exception as e:
            print(f"Error fetching user by email: {e}")
            return None
        
    def update_user_role(self, user_id: int, new_role: str) -> bool:
        """
        Update a user's role by their ID.
        """
        try:
            # Find the user document by ID
            user_doc = self.client.query_documents(self.db_name, {"id": user_id})[0]
            if not user_doc:
                print(f"User with ID {user_id} not found.")
                return False

            user_doc["role"] = new_role
            doc_id = user_doc["_id"]
            result = self.client.update_doc(self.db_name, doc_id, user_doc)
            return result[1]
        except Exception as e:
            print(f"Error updating user role: {e}")
            return False
        
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieve a user by their ID.
        """
        user_doc = self.client.get_doc(self.db_name, str(user_id))
        if not user_doc:
            return None
        return User.from_dict(user_doc)
    
    def get_all_users(self) -> list[User]:
        """
        Retrieve all users from the database.
        """
        try:
            docs = self.client.get_all_docs(self.db_name)
            #print(docs)

            users = [User.from_dict(doc) for doc in docs]
            return users
        except Exception as e:
            print(f"Error fetching all users: {e}")
            return []

    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user by their ID.
        """
        try:
            # Find the user document by ID
            user_doc = self.client.query_documents(self.db_name, {"id": user_id})[0]
            if not user_doc:
                print(f"User with ID {user_id} not found.")
                return False
            doc_id = user_doc["_id"]
            result = self.client.delete_doc(self.db_name, doc_id)
            return result
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
