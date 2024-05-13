from pymongo import MongoClient

MONGO_DB_URL = "mongodb://localhost:27017"
mongo_client = MongoClient(MONGO_DB_URL)
mongo_db = mongo_client['dental_clinic']

