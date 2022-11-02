from uuid import UUID

import boto3
import json
import os
import uuid
from datetime import datetime
from botocore.exceptions import ClientError

DDB_TABLE = os.environ.get("DYNAMODB_TABLE")
if DDB_TABLE is None:
    raise ClientError("DYNAMODB_TABLE environment variable is undefined")
dynamodb = boto3.resource("dynamodb")

def lambda_handler(event, context):
    #Lambda handler for birth of a unicorn.
    
    # Initialise DDB client
    table = dynamodb.Table(DDB_TABLE)
    
    event_body = json.loads(event["body"])
    unicorn_tag = ''
    unicorn_birthday = ''
    
    if ("id" in event_body) == False:
        unicorn_tag: UUID = str(uuid.uuid4())
    
    if ("birthday" in event_body) == False:
        unicorn_birthday = datetime.now().strftime("%c")

    unicorn = {
        "id": unicorn_tag,
        "name": event_body["Name"],
        "weight": event_body["Weight"],
        "birthday": unicorn_birthday,
    }

    # create entry in ddb for newborn unicorn:
    response = register_unicorn(table,unicorn)

    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:

        # return generated unicorn tag and name back to user:
        return {
            "statusCode": 200
        }


def register_unicorn(table,unicorn):
    return table.put_item(Item=unicorn)
