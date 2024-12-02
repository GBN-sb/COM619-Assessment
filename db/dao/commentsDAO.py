from ..couch_client import CouchClient
from typing import Dict, List, Optional, Tuple
from models.comment import Comment

class CommentsDAO:
    
        def __init__(self, db_name: str):
            """
            Initializes the DAO with a CouchDBManager instance.
            """
            self.db_name = db_name
            self.manager = CouchClient()
    
        def create_comment(self, comment: Comment) -> Tuple[str, bool, str]|None:
            """
            Creates a new comment in the database.
            """
            comment_data = comment.to_dict()
            return self.manager.create_doc(self.db_name, comment_data)
    
        def get_comment_by_id(self, comment_id: str) -> Optional[Comment]:
            """
            Retrieves a comment by its ID.
            """
            doc = self.manager.get_doc(self.db_name, comment_id)
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
            return self.manager.update_doc(self.db_name, comment_data["comment_id"], comment_data)
    
        def delete_comment(self, comment_id: str) -> bool:
            """
            Deletes a comment from the database.
            """
            return self.manager.delete_doc(self.db_name, comment_id)
    
        def get_comments_by_author(self, author: str) -> List[Comment]:
            """
            Retrieves comments by their author.
            """
            query = {"selector": {"author": author}}
            results = self.manager.query_documents(self.db_name, query)
            return [Comment.from_dict(doc) for doc in results]  
