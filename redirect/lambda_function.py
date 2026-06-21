import os
import boto3

table = boto3.resource('dynamodb').Table(os.environ['TABLE_NAME'])


def lambda_handler(event, context):
    code = event['pathParameters']['shortcode']
    item = table.get_item(Key={'shortcode': code}).get('Item')

    if not item:
        return {'statusCode': 404, 'body': 'Not found'}

    return {'statusCode': 301, 'headers': {'Location': item['url']}}
