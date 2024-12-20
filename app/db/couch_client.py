import couchdb3
import os
import dotenv
import time

class CouchClient:
    def __init__(self):
        dotenv.load_dotenv()
        if not self._get_env_vars():
            raise Exception('Missing environment variables')
        
        self.client = couchdb3.Server(
            url=self.url,
            port=int(self.port),
            user=self.user,
            password=self.password
        )


    def _get_env_vars(self):
        self.url = os.getenv('COUCH_URL')
        self.port = os.getenv('COUCH_PORT')
        self.user = os.getenv('COUCH_USER')
        self.password = os.getenv('COUCH_PASSWORD')
        
        return all([self.url, self.port, self.user, self.password])

    def get_all_dbs(self):
        return self.client.all_dbs()
    
    def create_db(self, db_name):
        if db_name in self.get_all_dbs():
            print(f"Database '{db_name}' already exists.")
            return self.client[db_name]
        try:
            return self.client.create(db_name)
        except couchdb3.exceptions.PreconditionFailedError as e:
            print(f"Error creating database '{db_name}': {e}")
            return None

    def delete_db(self, db_name):
        return self.client.delete(db_name)
    
    def get_all_docs(self, db_name):
        all_docs = self.client[db_name].all_docs()
        doc_ids = [doc['id'] for doc in all_docs['rows']]
        return [self.get_doc(db_name, doc_id) for doc_id in doc_ids]
    
    def get_doc(self, db_name, doc_id):
        return self.client[db_name][doc_id]
    
    def delete_doc(self, db_name, doc_id):
        try:
            db = self.client[db_name]
            doc = db[doc_id]
            return db.delete(doc['_id'], rev=doc['_rev'])
        except couchdb3.exceptions.ConflictError as e:
            print(f"Document not found: {e}")
            return False
    
    def create_doc(self, db_name, doc):
        db = self.client[db_name]
        try:
            if '_id' not in doc:
                doc['_id'] = f"{doc.get('name', 'doc')}_{int(time.time())}"
            return db.save(doc)
        except couchdb3.exceptions.ConflictError as e:
            print(f"Document conflict: {e}")
            return None
        
    def update_doc(self, db_name, doc_id, doc):
        db = self.client[db_name]
        try:
            doc['_id'] = doc_id
            return db.save(doc)
        except couchdb3.exceptions.ConflictError as e:
            print(f"Document conflict: {e}")
            return None

    def query_documents(self, db_name, query):
        return self.client[db_name].find(query)["docs"]
