import logging
import time
import json
import os

import boto3
import requests


def handler(event, context):
    '''
    General backend API handler for Ad Bounty
    '''
    try:
        path = event['path']
        endpoint = path.split('/')[1]
        httpMethod = event['httpMethod']

        rawBody = event['body']
        body = json.loads(event['body']) if rawBody else {}

        # API Routes:
        if endpoint == 'youtube-views':
            return __youtubeHandler(path)

        if endpoint == 'user':
            return __users(path, httpMethod, body)

        if endpoint == 'body':
            return __successResp(body)
        # Catch all default response, return 400
        return __errorResp('Unknown endpoint')
    except Exception as e:
        return __errorResp(str(e))


def __users(path, httpMethod, body):
    ethAddress = path.split('/')[2]
    table_name = 'adbounty-users'
    session = boto3.session.Session()
    dynamo_table = session.resource('dynamodb').Table(table_name)
    if httpMethod == 'GET':
        dynamo_item = dynamo_table.get_item(
            Key={
                'ethAddress': ethAddress
            }
        )['Item']
        return __successResp(dynamo_item)
    elif httpMethod == 'POST':
        contactEmail = body['contactEmail']
        dynamo_item = dict(ethAddress=ethAddress,
                           contactEmail=contactEmail)
        dynamo_table.put_item(
            Item=dynamo_item)
        return __successResp(dynamo_item)
    else:
        raise ValueError('Bad Argument')


def __youtubeHandler(path):

    videoId = path.split('/')[2]
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
        videoId=videoId,
        viewCount=viewCount
    )

    return __successResp(data)


def __getYoutubeUrl(id, apikey):
    '''
    Build URL for youtube data API
    '''
    ret = f'https://www.googleapis.com/youtube/v3/videos?part=contentDetails%2Cstatistics&'
    ret += f'id={id}&key={apikey}'
    return ret


def __successResp(respBodyDict):
    # CORS: allow all origins to pull

    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": __respHeaders(),
        "body": json.dumps(dict(success=True, **respBodyDict))
    }


def __errorResp(respStr):
    data = dict(
        success=False,
        error=respStr
    )
    return {
        "isBase64Encoded": False,
        "statusCode": 400,
        "headers": __respHeaders(),
        "body": json.dumps(data)
    }


def __respHeaders():
    return {
        'access-control-allow-headers': 'authorizationtoken,content-type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'access-control-allow-methods': 'GET,OPTIONS',
        'access-control-allow-origin': '*'
    }
