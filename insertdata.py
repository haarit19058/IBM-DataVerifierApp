from pymongo import MongoClient
import os
from dotenv import load_dotenv
import json

load_dotenv()
MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
client = MongoClient(MONGO_URL)
print(client.list_database_names())
db = client['IBM']
collection = db['demo_data']
# ----------- insert data ------------------------------------------

result = collection.delete_many({})
print(result.deleted_count)

documents = []
with open("combined_caseid.json", "r") as file:
    for line in file:
        documents.append(json.loads(line))

collection.insert_many(documents)
print("Data inserted successfully!")


# ------------------- fetch data ======================================



