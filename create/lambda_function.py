import json, os, string, random
import boto3

table = boto3.resource('dynamodb').Table(os.environ['TABLE_NAME'])


def generate_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))


def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body') or '{}')
        long_url = body.get('url')
        if not long_url:
            return {'statusCode': 400, 'body': json.dumps({'error': 'url is required'})}

        code = generate_code()
        table.put_item(Item={'shortcode': code, 'url': long_url})

        domain = event['requestContext']['domainName']
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'short_url': f"https://{domain}/{code}", 'code': code})
        }
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}
