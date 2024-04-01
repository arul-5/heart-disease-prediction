from pymongo import MongoClient

try:
    database_url = "mongodb://localhost:27017"
    conn = MongoClient(database_url)
    print("Connected to Database")
except Exception as e:
    print(f"Error connecting to the database: {e}")
  