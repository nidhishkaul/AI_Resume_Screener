from resume_parser import get_resume_data
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

uri = os.getenv("MONGO_DB_URI")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))


def insert_into_db(data):
    collection = client["Resume_Database"]["Resume_Collection"]
    collection.insert_one(data)



