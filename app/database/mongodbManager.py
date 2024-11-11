
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import os
import urllib.parse

#url encode password
password = os.getenv('MONGO_PASSWORD')
print(password)
password = urllib.parse.quote_plus(password)

uri = f"mongodb+srv://{user}:{password}@cluster0.bffuo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"



# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)