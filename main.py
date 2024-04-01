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

# Define endpoints
@app.post("/predict")
async def predict(data: UserData):
    data_dict = data.dict()
    args = preprocess_data(data)
    preprocessed_input = preprocess_input(args)
    prediction = model.predict(preprocessed_input)
    if(prediction==1): 
        output = "The patient seems to be have heart disease"
    else:
        output = "The patient seems to be Normal"
    conn.test.test.insert_one(data_dict)
    return {"prediction": output}

