import boto3
import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

def get_dynamo_client():
    session = boto3.resource(
        "dynamodb",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION")
    )
    return session
