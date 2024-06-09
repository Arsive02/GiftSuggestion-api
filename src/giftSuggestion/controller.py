import os
import uuid
import boto3
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

LOGGER = logging.getLogger(__name__)

app = FastAPI()

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          region_name='us-east-1'
                          )

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
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
        LOGGER.info("Number of items fetched: %s", len(items['Items']))
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
        LOGGER.info("Product added successfully")
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
