from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()
try:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    conn = MongoClient(database_url)
    print("Connected to Database")
except Exception as e:
    print(f"Error connecting to the database: {e}")
  