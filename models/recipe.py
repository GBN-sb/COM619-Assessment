import datetime
from db.dao.userDAO import UserDAO

class Recipe:
    _id_counter = 1

    def __init__(self, title, description, ingredients, instructions, picture_location, creator_id, id=0):
        self.id = id if id > 0 else self._generate_id()
        self.title = title
        self.description = description
        self.ingredients = ingredients
        self.instructions = instructions
        self.picture_location = picture_location
        self.creator_id = creator_id
        self.created_at = datetime.datetime.now()

    def _check_valid_creator(self, user_id):
        user_dao = UserDAO()
        user = user_dao.get_user_by_id(user_id)
        if user is None:
            return False
        return user.role in ["user"] or user.id == self

    @classmethod
    def _generate_id(cls) -> int:
        """
        Generates a unique, sequential integer ID.
        """
        id_value = cls._id_counter
        cls._id_counter += 1
        return id_value

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "ingredients": self.ingredients,
            "instructions": self.instructions,
            "pictureLocation": self.picture_location,
            "creatorId": self.creator_id,
            "createdAt": self.created_at.isoformat()
        }
    
    @staticmethod
    def from_dict(data: dict) -> "Recipe":
        required_fields = {"id", "title", "description", "ingredients", "instructions", "pictureLocation", "creatorId", "createdAt"}
        if not required_fields.issubset(data.keys()):
            raise ValueError(f"Missing required fields: {required_fields - data.keys()}")
        
        recipe = Recipe(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            ingredients=data["ingredients"],
            instructions=data["instructions"],
            picture_location=data["pictureLocation"],
            creator_id=data["creatorId"]
        )
        recipe.created_at = datetime.datetime.fromisoformat(data["createdAt"])
        return recipe
    
    @staticmethod
    def verify_creator(user_id: str, recipe: dict) -> bool:
        return user_id == recipe["creatorId"]
