from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from db import conn
import pickle
from preprocess import preprocess_input, preprocess_data
import numpy as np

# Load the pre-trained machine learning model
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

app = FastAPI()


# Define the input data model
class UserData(BaseModel):
    age: int
    sex: int
    cp: int
    trestbps: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int

@app.post("/store_user_data")
async def store_user_data(data: UserData):
    data_dict = data.dict()
    data_dict['processed'] = False  # Add a processed field and set it to False
    conn.test.test.insert_one(data_dict)
    return {"message": "User data stored successfully"}


