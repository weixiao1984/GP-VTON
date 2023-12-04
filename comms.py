import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
import json
import logging
import websocket

logger = logging.getLogger(__name__)

def send2client(msg):
    ws = websocket.WebSocket()
    ws.connect('wss://snxlf627sc.execute-api.us-east-2.amazonaws.com/production/')
    ws.send(json.dumps({"action": "sendmessage", "msg": msg}))
    # Wait for client to send over ack message
    ws.recv()
    ws.close()

def generate_presigned_url(bucket, key):
    try:
        s3_client = boto3.client('s3', config=Config(region_name='us-east-2', signature_version='s3v4'))
        client_method = "get_object"
        method_parameters = {"Bucket": bucket, "Key": key}
        expires_in = 3600
        url = s3_client.generate_presigned_url(
            ClientMethod=client_method, Params=method_parameters, ExpiresIn=expires_in
        )
        logger.info("Got presigned URL: %s", url)
    except ClientError:
        logger.exception(
            "Couldn't get a presigned URL for client method '%s'.", client_method
        )
        raise
    return url