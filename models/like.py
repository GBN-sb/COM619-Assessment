from db.dao.userDAO import UserDAO
from db.dao.recipeDAO import RecipeDAO

class Like:
    _id_counter = 1
    def __init__(self, user_id, recipe_id, id=0):
        self.id = id if id > 0 else self._generate_id()
        self.user_id = user_id
        self.recipe_id = recipe_id


    @classmethod
    def _generate_id(cls) -> int:
        """
        Generates a unique, sequential integer ID.
        """
        id_value = cls._id_counter
        cls._id_counter += 1
        return id_value
    
    def _check_user_id_is_valid(self, user_id):
        user = UserDAO().get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found.")
        
    def _check_recipe_id_is_valid(self, recipe_id):
        recipe = RecipeDAO().get_recipe_by_id(recipe_id)
        if not recipe:
            raise ValueError("Recipe not found.")

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'recipe_id': self.recipe_id
        }
    
    @staticmethod
    def from_dict(data: dict) -> "Like":
        required_fields = {"id", "user_id", "recipe_id"}
        if not required_fields.issubset(data.keys()):
            raise ValueError(f"Missing required fields: {required_fields - data.keys()}")
        
        like = Like(
            id=data["id"],
            user_id=data["user_id"],
            recipe_id=data["recipe_id"]
        )
        return like