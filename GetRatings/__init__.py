import logging

import azure.cosmos.cosmos_client as cosmos_client
import azure.functions as func
import json
import os

#HOST            = "https://oh10team.documents.azure.com:443/"
#MASTER_KEY      = "ujMdDf0YfMLIctvI4S8ly8QsJ8mfDzj9AhAWt5qjTPHUFY6SOn1niKJQZI5I94zRLhjjMzo839OowlANDiYxTg=="
#DATABASE_ID     = "BFYOC"
#CONTAINER_ID    = "IceCreamRating"

HOST            = os.environ['HOST']
MASTER_KEY      = os.environ['MASTER_KEY']
DATABASE_ID     = os.environ['DATABASE_ID']
CONTAINER_ID    = os.environ['CONTAINER_ID']

def main(req: func.HttpRequest) -> func.HttpResponse:
    client      = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY} )
    database    = client.get_database_client(DATABASE_ID)
    container   = database.get_container_client(CONTAINER_ID)

    userId = req.params.get('userId')

    ratings = list(container.query_items(
        query="SELECT * FROM r WHERE r.userId=@id",
        parameters=[
            { "name":"@id", "value": userId }
        ],
        enable_cross_partition_query=True
    ))

    if ratings:
        return func.HttpResponse(json.dumps(ratings, indent=True))
    else:
        return func.HttpResponse(
            "CANNOT FIND RATINGS, PLEASE MAKE SURE YOU INPUT THE CORRECT USERID",
            status_code=404
        )

def query_items(container, userId):
    # enable_cross_partition_query should be set to True as the container is partitioned
    items = list(container.query_items(
        query="SELECT * FROM r WHERE r.userId=@id",
        parameters=[
            { "name":"@id", "value": userId }
        ],
        enable_cross_partition_query=True
    ))
