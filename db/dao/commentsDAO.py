from ..couch_client import CouchClient
from typing import Dict, List, Optional, Tuple
from models.comment import Comment

class CommentsDAO:
    
        def __init__(self, db_name="comments") -> None:
            """
            Initialises the DAO with a CouchDBManager instance.
            """
            self.db_name = db_name
            self.manager = CouchClient()
    
        def create_comment(self, comment: Comment) -> Tuple[str, bool, str]|None:
            """
            Creates a new comment in the database.
            """
            comment_data = comment.to_dict()
            return self.manager.create_doc(self.db_name, comment_data)
    
        def get_comment_by_id(self, id: str) -> Optional[Comment]:
            """
            Retrieves a comment by its ID.
            """
            # Get comment do
            doc = self.manager.get_doc(self.db_name, id)
            return Comment.from_dict(doc) if doc else None
    
        def get_comments(self, query_params: Optional[Dict] = None) -> List[Comment]:
            """
            Retrieves comments based on optional query parameters.
            """
            query = {"selector": query_params or {}}
            results = self.manager.query_documents(self.db_name, query)
            return [Comment.from_dict(doc) for doc in results]
    
        def update_comment(self, comment: Comment) -> (Tuple[str, bool, str] | None):
            """
            Updates an existing comment in the database.
            """
            comment_data = comment.to_dict()
            return self.manager.update_doc(self.db_name, comment_data["id"], comment_data)
    
        def delete_comment(self, id: str) -> bool:
            """
            Deletes a comment from the database.
            """
            # Get comment doc ID
            comment_doc = self.manager.query_documents(self.db_name, {"id": id})[0]
            if not comment_doc:
                return False
            return self.manager.delete_doc(self.db_name, comment_doc["_id"])
    
        def get_comments_by_user_id(self, user_id: str) -> List[Comment]:
            """
            Retrieves comments by their user_id.
            """
            query = {"user_id": user_id}
            results = self.manager.query_documents(self.db_name, query)
            return [Comment.from_dict(doc) for doc in results]  
