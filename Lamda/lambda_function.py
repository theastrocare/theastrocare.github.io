import json
import os
import uuid
from datetime import datetime

import boto3
from botocore.exceptions import ClientError

CHARSET = 'UTF-8'
DYNAMODB_TABLE = os.environ['DYNAMODB_TABLE']
SENDER_EMAIL = os.environ['SENDER_EMAIL']  # Must be configured in SES
SES_REGION = 'us-east-1'


dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses', region_name=SES_REGION)


def lambda_handler(event, context):
    print(event)
    data = json.loads(event['body'])
    print(json.dumps(data))

    try:

        content = 'Message from ' + \
            data['name'] + '\n' + \
            data['City'] + '\n' + \
            data['DOB'] + '\n' + \
            data['TOB']
            
        save_to_dynamodb(data)
        response = send_mail_to_user(data, content)
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message Id:", response['MessageId'])

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": ""
    }


def save_to_dynamodb(data):
    timestamp = datetime.utcnow().replace(microsecond=0).isoformat()
    table = dynamodb.Table(DYNAMODB_TABLE)
    item = {
        'id': str(uuid.uuid1()),
        'name': data['name'],  # required
        'City': data['City'],  # required
        'DOB': data['DOB'],
        'TOB': data['TOB'] 
    }
    table.put_item(Item=item)
    return


def send_mail_to_user(data, content):
    return ses.send_email(
        Source=SENDER_EMAIL,
        Destination={
            'ToAddresses': [
                SENDER_EMAIL,
            ],
        },
        Message={
            'Subject': {
                'Charset': CHARSET,
                'Data': 'You have new entry in the form'
            },
            'Body': {
                'Html': {
                    'Charset': CHARSET,
                    'Data': content
                },
                'Text': {
                    'Charset': CHARSET,
                    'Data': content
                }
            }
        }
    )
