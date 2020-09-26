

import boto3

'''
Sandbox for testing code snippets
'''
def main():
    session = boto3.session.Session()
    tableName = 'adbounty-users'
    dynamoTable = session.resource('dynamodb').Table(tableName)

    ethAddress = 'abc'

    dynamoItem = dict(ethAddress=ethAddress,
                      contactEmail='emailll')

    dynamoResp = dynamoTable.get_item(Key={
        'ethAddress': ethAddress
    })
    print(dynamoResp)
    dynamoTable.put_item(
        Item=dynamoItem)


def __insert_item(dynamoTable):
    dynamoItem = dict(
        id='test2',
        name='test name'
    )
    dynamoTable.put_item(
        Item=dynamoItem)


def __scan(dynamoTable):
    return dynamoTable.scan()['Items']


if __name__ == '__main__':
    main()
