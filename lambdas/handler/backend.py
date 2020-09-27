import logging
import time
import json
import os

import uuid
import boto3
import requests
import traceback


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

        elif endpoint == 'user':
            return __user(path, httpMethod, body)

        elif endpoint == 'contract-template':
            return __contractTemplate(path, httpMethod, body)
        elif endpoint == 'contract-template-owned':
            return __contractTemplateOwned(path, httpMethod, body)

        elif endpoint == 'contract-template-available':
            return __contractTemplateAvailable(path, httpMethod, body)

        # for debugging, echo request
        elif endpoint == 'body':
            return __successResp(body)
        else:
            # Catch all default response, return 400
            return __errorResp('Unknown endpoint')
    except Exception:
        return __errorResp(str(traceback.format_exc()))


def __user(path, httpMethod, body):
    ethAddress = path.split('/')[2]
    dynamoTable = __tableResource('adbounty-users')
    if httpMethod == 'GET':
        dynamoResp = dynamoTable.get_item(
            Key={
                'ethAddress': ethAddress
            }
        )
        if 'Item' in dynamoResp:
            return __successResp(dynamoResp['Item'])
        else:
            return __successResp(dict(ethAddress=ethAddress, contactEmail=''))
    elif httpMethod == 'POST':
        contactEmail = body['contactEmail']
        dynamoItem = dict(ethAddress=ethAddress,
                          contactEmail=contactEmail)
        dynamoResp = dynamoTable.get_item(
            Key={
                'ethAddress': ethAddress
            }
        )
        dynamoTable.put_item(
            Item=dynamoItem)

        if 'Item' not in dynamoResp:
            # This has not been initialized yet, so initialize all tables
            initContractItem = dict(
                ethAddress=ethAddress,
                contracts=[]
            )
            dynamoTable = __tableResource('adbounty-connected-contract')
            dynamoTable.put_item(
                Item=initContractItem)

            initTemplateItem = dict(
                ethAddress=ethAddress,
                templates=[]
            )
            dynamoTable = __tableResource('adbounty-contract-template-owned')
            dynamoTable.put_item(
                Item=initTemplateItem)

            dynamoTable = __tableResource(
                'adbounty-contract-template')
            dynamoResp = dynamoTable.scan()
            availItems = dynamoResp['Items'] if 'Items' in dynamoResp else []
            initTemplateItem['templates'] = availItems
            dynamoTable = __tableResource(
                'adbounty-contract-template-available')
            dynamoTable.put_item(
                Item=initTemplateItem)

        return __successResp(dynamoItem)
    else:
        raise ValueError('Bad Argument')


def __contractTemplate(path, httpMethod, body):
    '''
    Create new contract template
    '''
    ethAddress = path.split('/')[2]
    if not __userExists(ethAddress):
        raise ValueError('User at given eth address does not exist')
    if httpMethod == 'POST':
        newId = str(uuid.uuid4())
        # Update contract template
        templateItem = dict(
            id=newId,
            name=body['name'],
            owner=ethAddress,
            validitySec=int(body['validitySec']),
            payment=int(body['payment']),
            threshold=int(body['threshold']),
            description=body['description']
        )
        dynamoTable = __tableResource('adbounty-contract-template')

        dynamoTable.put_item(
            Item=templateItem)

        # Update templates owned
        dynamoTable = __tableResource('adbounty-contract-template-owned')
        templatesOwnedItem = dynamoTable.get_item(
            Key={
                'ethAddress': ethAddress
            }
        )['Item']
        templatesOwnedItem['templates'].append(newId)
        dynamoTable.put_item(
            Item=templatesOwnedItem)

        # Update templates available
        dynamoTable = __tableResource('adbounty-contract-template-available')
        availableItems = dynamoTable.scan()['Items']

        for availableItem in availableItems:
            if availableItem['ethAddress'] != ethAddress:
                availableItem['templates'].append(newId)
                dynamoTable.put_item(
                    Item=availableItem)
        return __successResp(templateItem)

    else:
        raise ValueError('Bad Argument')


def __contractTemplateOwned(path, httpMethod, body):
    ethAddress = path.split('/')[2]
    dynamoTable = __tableResource('adbounty-contract-template-owned')
    if httpMethod == 'GET':
        dynamoItem = dynamoTable.get_item(
            Key={
                'ethAddress': ethAddress
            }
        )['Item']
        templateIds = dynamoItem['templates']
        dynamoItem['templates'] = __getTemplates(templateIds)
        return __successResp(dynamoItem)
    else:
        raise ValueError('Bad Argument')


def __contractTemplateAvailable(path, httpMethod, body):
    ethAddress = path.split('/')[2]
    dynamoTable = __tableResource('adbounty-contract-template-available')
    if httpMethod == 'GET':
        dynamoItem = dynamoTable.get_item(
            Key={
                'ethAddress': ethAddress
            }
        )['Item']
        templateIds = dynamoItem['templates']
        dynamoItem['templates'] = __getTemplates(templateIds)
        return __successResp(dynamoItem)
    else:
        raise ValueError('Bad Argument')


def __getTemplates(templateIds):
    dynamoTable = __tableResource('adbounty-contract-template')
    templates = []
    for templateId in templateIds:
        template = dynamoTable.get_item(
            Key={
                'id': templateId
            }
        )['Item']
        for key in ['validitySec', 'payment', 'threshold']:
            template[key] = int(template[key])
        templates.append(template)

    return templates


def __userExists(ethAddress):
    dynamoTable = __tableResource('adbounty-users')
    dynamoResp = dynamoTable.get_item(
        Key={
            'ethAddress': ethAddress
        }
    )
    return 'Item' in dynamoResp


def __tableResource(table_name):
    session = boto3.session.Session()
    return session.resource('dynamodb').Table(table_name)


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
        viewCount=int(viewCount)
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
