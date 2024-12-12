from models.recipe import Recipe
from ..couch_client import CouchClient
from typing import Dict, List, Optional, Tuple

class RecipeDAO:

    def __init__(self, db_name="recipes") -> None:
        """
        Initialises the DAO with a CouchDBclient instance.
        """
        self.db_name = db_name
        self.client = CouchClient()

    def create_recipe(self, recipe: Recipe) -> Tuple[str, bool, str]|None:
        """
        Creates a new recipe in the database.
        """
        recipe_data = recipe.to_dict()
        return self.client.create_doc(self.db_name, recipe_data)

    def get_recipe_by_id(self, recipe_id: str) -> Optional[Recipe]:
        """
        Retrieves a recipe by its ID.
        """
        doc = self.client.get_doc(self.db_name, recipe_id)
        return Recipe.from_dict(doc) if doc else None

    def get_recipes(self, query_params: Optional[Dict] = None) -> List[Recipe]:
        """
        Retrieves recipes based on optional query parameters.
        """
        query = query_params or {}
        results = self.client.query_documents(self.db_name, query)
        return [Recipe.from_dict(doc) for doc in results]

    def update_recipe(self, recipe: Recipe) -> (Tuple[str, bool, str] | None):
        """
        Updates an existing recipe in the database.
        """
        recipe_data = recipe.to_dict()
        # Get recipe doc ID
        recipe_doc = self.client.query_documents(self.db_name, {"title": recipe.title})[0]
        updated_doc = self._add_changes_to_doc(recipe_doc, recipe_data)
        if not recipe_doc:
            return None
        print(updated_doc)
        return self.client.update_doc(self.db_name, recipe_doc["_id"], updated_doc)
    
    def _add_changes_to_doc(self, doc: Dict, recipe_dict: Dict) -> Dict:
        """
        Detect changes and add them to the document.
        """
        for key, value in recipe_dict.items():
            if key in doc and doc[key] != value:
                doc[key] = value
        return doc
    

    def delete_recipe(self, recipe_id: int) -> bool:
        """
        Deletes a recipe from the database.
        """
        # Get recipe doc ID
        recipe_doc = self.client.query_documents(self.db_name, {"id": recipe_id})[0]
        print(recipe_doc)
        if not recipe_doc:
            return False
    
        return self.client.delete_doc(self.db_name, recipe_doc["_id"])

    def get_recipe_by_name(self, title: str) -> Optional[Recipe]:    
        """
        Retrieves a recipe by its name.
        """
        query = {"title": title}
        results = self.client.query_documents(self.db_name, query)
        if results:
            return Recipe.from_dict(results[0])
        return None

    def get_recipes_by_author(self, author: str) -> List[Recipe]:
        """
        Retrieves recipes by their author.
        """
        query = {"creatorId": author}
        results = self.client.query_documents(self.db_name, query)
        return [Recipe.from_dict(doc) for doc in results]
    