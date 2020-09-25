import logging
import time
import json
import os

import boto3
import requests


def handler(event, context):

    path = event['path']
    videoId = path.split('/')[1]
    data = dict(
        success=True,
        videoId=videoId
    )
    secretId = os.environ['SECRET_ID']

    client = boto3.client('secretsmanager')
    secretResp = client.get_secret_value(
        SecretId=secretId
    )
    apiKey = json.loads(secretResp['SecretString'])['api_key']

    youtubeUrl = __getYoutubeUrl(videoId, apiKey)
    viewCount = requests.get(youtubeUrl).json()[
        'items'][0]['statistics']['viewCount']
    data = dict(
        success=True,
        videoId=videoId,
        viewCount=viewCount
    )
    # headers = event['headers'] if 'headers' in event else {}
    # headers.update({
    #     'access-control-allow-headers': 'authorizationtoken,content-type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
    #     'access-control-allow-methods': 'GET,OPTIONS',
    #     'access-control-allow-origin': 'ad-bounty.com,localhost'

    # })

    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {},
        "body": json.dumps(data)
    }


def __getYoutubeUrl(id, apikey):
    '''
    Build URL for youtube data API
    '''
    ret = f'https://www.googleapis.com/youtube/v3/videos?part=contentDetails%2Cstatistics&'
    ret += f'id={id}&key={apikey}'
    return ret
