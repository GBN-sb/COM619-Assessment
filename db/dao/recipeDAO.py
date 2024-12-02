from models.recipe import Recipe
from ..couch_client import CouchClient
from typing import Dict, List, Optional, Tuple

class RecipeDAO:

    def __init__(self):
        """
        Initializes the DAO with a CouchDBManager instance.
        """
        self.db_name = "recipes"
        self.manager = CouchClient()

    def create_recipe(self, recipe: Recipe) -> Tuple[str, bool, str]|None:
        """
        Creates a new recipe in the database.
        """
        recipe_data = recipe.to_dict()
        return self.manager.create_doc(self.db_name, recipe_data)

    def get_recipe_by_id(self, recipe_id: str) -> Optional[Recipe]:
        """
        Retrieves a recipe by its ID.
        """
        doc = self.manager.get_doc(self.db_name, recipe_id)
        return Recipe.from_dict(doc) if doc else None

    def get_recipes(self, query_params: Optional[Dict] = None) -> List[Recipe]:
        """
        Retrieves recipes based on optional query parameters.
        """
        query = {"selector": query_params or {}}
        results = self.manager.query_documents(self.db_name, query)
        return [Recipe.from_dict(doc) for doc in results]

    def update_recipe(self, recipe: Recipe) -> (Tuple[str, bool, str] | None):
        """
        Updates an existing recipe in the database.
        """
        recipe_data = recipe.to_dict()
        return self.manager.update_doc(self.db_name, recipe.id, recipe_data)

    def delete_recipe(self, recipe_id: str) -> bool:
        """
        Deletes a recipe from the database.
        """
        return self.manager.delete_doc(self.db_name, recipe_id)

    def get_recipe_by_name(self, name: str) -> Optional[Recipe]:    
        """
        Retrieves a recipe by its name.
        """
        query = {"selector": {"name": name}}
        results = self.manager.query_documents(self.db_name, query)
        if results:
            return Recipe.from_dict(results[0])
        return None

    def get_recipes_by_author(self, author: str) -> List[Recipe]:
        """
        Retrieves recipes by their author.
        """
        query = {"selector": {"author": author}}
        results = self.manager.query_documents(self.db_name, query)
        return [Recipe.from_dict(doc) for doc in results]
    