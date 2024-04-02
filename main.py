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
    try:
        data_dict = data.dict()
        data_dict['processed'] = False
        conn.test.test.insert_one(data_dict)
        return {"message": "User data stored successfully"}
    except Exception as e:
        print(f"Error storing user data: {e}")
        return {"message": "Error: Failed to store user data"}

# When fetching user data for prediction
@app.get("/predict_from_mongodb")
async def predict_from_mongodb():
    user_data = conn.test.test.find_one({"processed": False})  # Fetch the first unprocessed user data
    if user_data:
        user_id = user_data.pop('_id', None)  # Remove _id from the user_data for ML model
        user_data.pop('processed', None)  # Remove the processed field
        
        args = preprocess_data(user_data)
        preprocessed_input = preprocess_input(args)
        
        if preprocessed_input.shape[1] > 0:  # Ensure there are features for prediction
            prediction = model.predict(preprocessed_input)
        
            if prediction == 1:
                output = "The patient seems to have heart disease"
            else:
                output = "The patient seems to be normal"
                
                # Insert the prediction result back to MongoDB with _id
            if user_id:
                conn.test.test.update_one({"_id": user_id}, {"$set": {"prediction": output}})
                
                # Mark the record as processed
            conn.test.test.update_one({"_id": user_id}, {"$set": {"processed": True}})
                
            return {"prediction": output}
        else:
            return {"message": "No features found for prediction"}
    else:
        return {"message": "No unprocessed user data found in MongoDB"}
