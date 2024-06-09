import uuid

import uvicorn

import boto3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.settings as keys


app = FastAPI()

dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=keys.ACCESS_KEY_ID,
                          aws_secret_access_key=keys.ACCESS_SECRET_KEY,
                          region_name='us-east-1'
                          )

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/greetings")
def read_root():
    return {
        "status": "success",
        "response": {
            "message": "Welcome to Gift Suggestion API"
        }
    }


@app.get("/api/v1/getProducts")
def getProducts():
    try:
        table = dynamodb.Table('GiftSuggestion')
        items = table.scan()
        print("ITEMS:\n", items)
        return {
            "status": "success",
            "response": {
                "message": "Products fetched successfully",
                "data": items['Items']
            }
        }
    except Exception as e:
        return {
            "status": "failure",
            "response": {
                "message": "Failed to fetch products",
                "error": str(e)
            }
        }


@app.post("/api/v1/addProduct")
async def addProduct(data: dict):
    try:
        table = dynamodb.Table('GiftSuggestion')
        item = {
            'productID': str(uuid.uuid4()),
            'title': data['title'],
            'description': data['description'],
            'occasion': data['occasion'],
            'relationship': data['relationship'],
            'gender': data['gender'],
            'age': data['age'],
            'budget': data['budget'],
            'productURL': data['productURL']
        }
        table.put_item(Item=item)
        print("DATA:\n", data)
        return {
            "status": "success",
            "response": {
                "message": "Product added successfully"
            }
        }
    except Exception as e:
        return {
            "status": "failure",
            "response": {
                "message": "Failed to add product",
                "error": str(e)
            }
        }
