from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["My_Database"]
collection = db["my_database"]
