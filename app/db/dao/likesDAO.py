from ..couch_client import CouchClient
from typing import List, Optional, Tuple
from models.like import Like

class LikesDAO:
    def __init__(self, db_name="likes") -> None:
        """
        Initialises the DAO with a CouchDBManager instance and sets the db name.
        """
        self.db_name = db_name
        self.manager = CouchClient()

    def create_like(self, like: Like) -> Tuple[str, bool, str]|None:
        """
        Creates a new like in the database.
        """
        like_data = like.to_dict()
        return self.manager.create_doc(self.db_name, like_data)
    
    def delete_like(self, id: int) -> bool:
        """
        Deletes a like from the database.
        """
        # Get like doc ID
        like_doc = self.manager.query_documents(self.db_name, {"id": id})[0]
        if not like_doc:
            return False
        return self.manager.delete_doc(self.db_name, like_doc["_id"])
    
    def get_like_by_id(self, id: int) -> Optional[Like]:
        """
        Retrieves a like by its ID.
        """
        doc = self.manager.query_documents(self.db_name, {"id": id})[0]
        return Like.from_dict(doc) if doc else None
    
    def get_like_count(self, recipe_id: int) -> int:
        """
        Retrieves the number of likes for a recipe.
        """
        query = {"recipe_id": recipe_id}
        results = self.manager.query_documents(self.db_name, query)
        return len(results)
    
    def get_likes_by_user(self, user_id: int) -> List[Like]:
        """
        Retrieves likes by user.
        """
        query = {"user_id": user_id}
        results = self.manager.query_documents(self.db_name, query)
        return [Like.from_dict(doc) for doc in results]
