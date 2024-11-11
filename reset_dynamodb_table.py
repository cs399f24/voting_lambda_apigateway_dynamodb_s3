import boto3

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('VoteCounts')

# Define the keys for each item to update
vote_types = ['yes', 'no']

# Loop through each VoteType and set the Count to 0
for vote_type in vote_types:
    response = table.update_item(
        Key={'VoteType': vote_type},
        UpdateExpression='SET #count = :value',
        ExpressionAttributeNames={'#count': 'Count'},
        ExpressionAttributeValues={':value': 0}
    )

print('DONE')
