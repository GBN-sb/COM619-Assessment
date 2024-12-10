from db.dao.userDAO import UserDAO
from db.dao.recipeDAO import RecipeDAO
import uuid

class Comment:

    def __init__(self, user_id, post_id, content, created_at, id=0):
        self.id = id if id > 0 else uuid.uuid4().int
        self.user_id = user_id
        self.post_id = post_id
        self.content = content
        self.created_at = created_at

    def _check_user_id_is_valid(self, user_id):
        user = UserDAO().get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found.")
        
    def _check_recipe_id_is_valid(self, post_id):
        recipe = RecipeDAO().get_recipe_by_id(post_id)
        if not recipe:
            raise ValueError("Recipe not found.")

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'post_id': self.post_id,
            'content': self.content,
            'created_at': self.created_at
        }
    
    @staticmethod
    def from_dict(data: dict) -> "Comment":
        required_fields = {"id", "user_id", "post_id", "content", "created_at"}
        if not required_fields.issubset(data.keys()):
            raise ValueError(f"Missing required fields: {required_fields - data.keys()}")
        
        comment = Comment(
            id=data["id"],
            user_id=data["user_id"],
            post_id=data["post_id"],
            content=data["content"],
            created_at=data["created_at"]
        )
        return comment
