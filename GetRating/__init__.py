import json

import azure.functions as func
import azure.cosmos.cosmos_client as cosmos_client
import os

HOST            = os.environ["HOST"]
MASTER_KEY      = os.environ["MASTER_KEY"]
DATABASE_ID     = os.environ["DATABASE_ID"]
CONTAINER_ID    = os.environ["CONTAINER_ID"]

def main(req: func.HttpRequest) -> func.HttpResponse:
    client      = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY} )
    database    = client.get_database_client(DATABASE_ID)
    container   = database.get_container_client(CONTAINER_ID)

    ratingId = req.params.get('ratingId')

    if not ratingId:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('ratingId')

    rating = list(container.query_items(
        query="SELECT * FROM r WHERE r.id=@id",
        parameters=[
            { "name":"@id", "value": ratingId }
        ],
        enable_cross_partition_query=True
    ))

    if rating:
        return func.HttpResponse(json.dumps(rating[0], indent=True))
    else:
        return func.HttpResponse(
            "CANNOT FIND RATING, PLEASE MAKE SURE YOU INPUT THE CORRECT ID",
            status_code=404
        )
