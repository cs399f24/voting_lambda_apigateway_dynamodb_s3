import json
import boto3


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('VoteCounts')


def lambda_handler(event, context):

    body = json.loads(event['body'])

    if 'vote' not in body:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Headers': "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                'Access-Control-Allow-Methods': "GET",
                'Access-Control-Allow-Origin': "*"
            },
            'body': json.dumps(event)
        }

    vote = body.get('vote')

    if not vote in ['yes', 'no']:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Headers': "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                'Access-Control-Allow-Methods': "GET",
                'Access-Control-Allow-Origin': "*"
            },
            'body': json.dumps('Invalid vote')
        }


    table.update_item(
        Key={'VoteType': vote},
        UpdateExpression="SET #C = if_not_exists(#C, :start) + :inc",
        ExpressionAttributeNames={'#C': 'Count'},
        ExpressionAttributeValues={':inc': 1, ':start': 0}
    )


    counts = {'yes': 0, 'no': 0}

    response_yes = table.get_item(Key={'VoteType': 'yes'})
    if 'Item' in response_yes:
        counts['yes'] = int(response_yes['Item']['Count'])

    response_no = table.get_item(Key={'VoteType': 'no'})
    if 'Item' in response_no:
        counts['no'] = int(response_no['Item']['Count'])

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            'Access-Control-Allow-Methods': "GET",
            'Access-Control-Allow-Origin': "*"
        },
        'body': json.dumps(counts)
    }