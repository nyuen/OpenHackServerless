import logging
import azure.cosmos.cosmos_client as cosmos_client
import azure.functions as func 
from datetime import datetime
import os 
import json
import requests
import uuid
import time
from jsonschema import validate

HOST            = os.environ['HOST']
MASTER_KEY      = os.environ['MASTER_KEY']
DATABASE_ID     = os.environ['DATABASE_ID']
CONTAINER_ID    = os.environ['CONTAINER_ID']


def main(req: func.HttpRequest) -> func.HttpResponse:

    client      = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY} )
    database    = client.get_database_client(DATABASE_ID)
    container   = database.get_container_client(CONTAINER_ID)
    newguid     = str(uuid.uuid4())
    timestamp   = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f") # datetime.fromtimestamp(time.time())

    
    schema = {
            "type" : "object",
            "properties" : {
            "userId" : {"type" : "string"},
            "productId" : {"type" :"string"},
            "locationName" : {"type" : "string"},
            "rating" : {"type" : "number", "minimum" : 0, "maximum" : 5},
            "usernotes" : {"type" :"string"}
            },
        }
    
    
    try:
        req_body = req.get_json()
        validate(instance = req_body,schema = schema)
        req_body["id"] = newguid
        req_body["timestamp"] = timestamp
        #print(req_body)


    except ValueError:
        return func.HttpResponse(f"Please insert valid format!", status_code= 400 )
    #except ValidationError as err : 
    #    return func.HttpResponse(f"Please insert request body!", status_code= 400 )

    userId = req_body["userId"]
    responseUser = requests.get('https://serverlessohapi.azurewebsites.net/api/GetUser?userId='+userId)
    if responseUser.status_code == 404:

        return func.HttpResponse(
            "Please pass a valid userid on the query string or in the request body",
            status_code=404
        )

    productId = req_body["productId"]
    responseProduct = requests.get(url="https://serverlessohapi.azurewebsites.net/api/GetProduct?productId="+productId)
    if responseProduct.status_code == 404:
        return func.HttpResponse(
            "Please pass a valid productId on the query string or in the request body",
            status_code=404
        )
        
    container.create_item(body=req_body)
    return func.HttpResponse(f"OK Inserted {req_body} ")
    

#def create_product_rating(container):
    #product_rating = get_product_rating("ProductRating1")
    
   # if product_rating:
   #     return func.HttpResponse(f"Success Insert", {0},{1},{2},{3},{4})
