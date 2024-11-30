import jsonschema
from jsonschema.exceptions import ValidationError
import couch_client
import json
import os
import logging


class CouchDAO:
    def __init__(self):
        self.server = couch_client.CouchClient()
        self.schemas = {}

    def _import_schemas(self):
        schema_dir = 'db/schemas'
        for filename in os.listdir(schema_dir):
            if filename.endswith('.json'):
                db_name = filename.split('.')[0]
                with open(os.path.join(schema_dir, filename), 'r') as f:
                    self.schemas[db_name] = json.load(f)

    def _validate(self, db_name, doc):
        if db_name in self.schemas:
            jsonschema.validate(doc, self.schemas[db_name])
        else:
            raise ValueError(f"No schema found for database: {db_name}")

    def add_document(self, db_name, doc):
        if not self.schemas:  # Load schemas only once
            self._import_schemas()
        self._validate(db_name, doc)
        self.server.create_doc(db_name, doc)
    
    def get_document_ids(self, db_name):
        db_contents = self.server.get_all_docs(db_name)
        return [doc['id'] for doc in db_contents['rows']]
    
    def get_document(self, db_name, doc_id):
        return self.server.get_doc(db_name, doc_id)
    
    def delete_document(self, db_name, doc_id):
        self.server.delete_doc(db_name, doc_id)

    def update_document(self, db_name, doc_id, doc):
        if not self.schemas:  # Load schemas only once
            self._import_schemas()
        self._validate(db_name, doc)
        self.server.update_doc(db_name, doc_id, doc)


if __name__ == "__main__":
    dao = CouchDAO()
    
    # Example for 'comments'
    dao.server.create_db('comments')
    dao.add_document('comments', {
        "id": 1,
        "recipe_id": 1,
        "user_id": 1,
        "comment": "This is a comment",
    })
    ids = dao.get_document_ids('comments')
    print(dao.get_document('comments', ids[0]))
    dao.delete_document('comments', ids[0])
    dao.server.delete_db('comments')
    
    # Example for 'recipes'
    dao.server.create_db('recipes')
    try:
        dao.add_document('recipes', {
            "id": 1,
            "name": "Sample Item",
            "description": "This is a sample item for demonstration purposes.",
            "notes": "Additional details about the sample item.",
            "picture": "http://example.com/images/sample.jpg",
            "created_at": "2024-11-30T12:00:00Z"
        })
    except ValidationError as e:
        logging.error(f"Validation error: {e}")
    ids = dao.get_document_ids('recipes')
    print(dao.get_document('recipes', ids[0]))
    dao.delete_document('recipes', ids[0])
    dao.server.delete_db('recipes')
