import boto3, json
import sys


client = boto3.client('apigateway', region_name='us-east-1')

response = client.get_rest_apis()
apis = response.get('items', [])
        
for api in apis:
    if api.get('name') == 'VotesAPI':
        print('API already exits')
        sys.exit(0)


response = client.create_rest_api(
    name='VotesAPI',
    description='API to tally votes.',
    endpointConfiguration={
        'types': [
            'REGIONAL',
        ]
    }
)
api_id = response["id"]

resources = client.get_resources(restApiId=api_id)
root_id = [resource for resource in resources["items"] if resource["path"] == "/"][0]["id"]

results = client.create_resource(
    restApiId=api_id,
    parentId=root_id,
    pathPart='results'
)
results_resource_id = results["id"]


results_method = client.put_method(
    restApiId=api_id,
    resourceId=results_resource_id,
    httpMethod='GET',
    authorizationType='NONE'
)

results_response = client.put_method_response(
    restApiId=api_id,
    resourceId=results_resource_id,
    httpMethod='GET',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': True,
        'method.response.header.Access-Control-Allow-Origin': True,
        'method.response.header.Access-Control-Allow-Methods': True
    },
    responseModels={
        'application/json': 'Empty'
    }
)


# Get the ARN for the votingGetResults lambda function
lambda_client = boto3.client('lambda', region_name='us-east-1')
lambda_arn=lambda_client.get_function(FunctionName='votingGetResults')['Configuration']['FunctionArn']
# API Gateway requires a special URI that contains the lambda ARN as a substring
uri=f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'

# Get the ARN for the IAM LabRole
iam_client = boto3.client('iam')
lab_role = iam_client.get_role(RoleName='LabRole')['Role']['Arn']

results_integration = client.put_integration(
    restApiId=api_id,
    resourceId=results_resource_id,
    httpMethod='GET',
    credentials=lab_role,
    # API Gateway calls the Lambda function via an HTTP POST
    integrationHttpMethod='POST',
    # Set up the integration as a proxy integration.
    type='AWS_PROXY',
    uri=uri
)

# Because we use an AWS_PROXY for the integration, there is not integration response
# to configure.  





vote_resource = client.create_resource(
    restApiId=api_id,
    parentId=root_id,
    pathPart='vote'
)
vote_resource_id = vote_resource["id"]



vote_method = client.put_method(
    restApiId=api_id,
    resourceId=vote_resource_id,
    httpMethod='POST',
    authorizationType='NONE'
)

vote_response = client.put_method_response(
    restApiId=api_id,
    resourceId=vote_resource_id,
    httpMethod='POST',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': False,
        'method.response.header.Access-Control-Allow-Origin': False,
        'method.response.header.Access-Control-Allow-Methods': False
    },
    responseModels={
        'application/json': 'Empty'
    }
)


# Get the ARN for the votingGetResults lambda function
#lambda_client = boto3.client('lambda', region_name='us-east-1')
lambda_arn=lambda_client.get_function(FunctionName='votingPostVote')['Configuration']['FunctionArn']
# API Gateway requires a special URI that contains the lambda ARN as a substring
uri=f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'

# Get the ARN for the IAM LabRole
#iam_client = boto3.client('iam')
#lab_role = iam_client.get_role(RoleName='LabRole')['Role']['Arn']

results_integration = client.put_integration(
    restApiId=api_id,
    resourceId=vote_resource_id,
    httpMethod='POST',
    credentials=lab_role,
    # API Gateway calls the Lambda function via an HTTP POST
    integrationHttpMethod='POST',
    # Set up the integration as a proxy integration.
    type='AWS_PROXY',
    uri=uri
)

#vote_integration = client.put_integration(
#    restApiId=api_id,
#    resourceId=vote_resource_id,
#    httpMethod='POST',
#    type='MOCK',
#    requestTemplates={
#        'application/json': '{"statusCode": 200}'
#    }
#)


#vote_integration_response = client.put_integration_response(
#    restApiId=api_id,
#    resourceId=vote_resource_id,
##    httpMethod='POST',
#    statusCode='200',
#    responseParameters={
#        'method.response.header.Access-Control-Allow-Headers': '\'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token\'',
#        'method.response.header.Access-Control-Allow-Methods': '\'POST\'.\'OPTIONS\'',
#        'method.response.header.Access-Control-Allow-Origin': '\'*\''
#    },
#    responseTemplates={
#        "application/json": json.dumps({
#            "yes": 20,
#            "no": 10               
#        })
#    }
#)


vote_method = client.put_method(
    restApiId=api_id,
    resourceId=vote_resource_id,
    httpMethod='OPTIONS',
    authorizationType='NONE'
)

vote_response = client.put_method_response(
    restApiId=api_id,
    resourceId=vote_resource_id,
    httpMethod='OPTIONS',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': False,
        'method.response.header.Access-Control-Allow-Origin': False,
        'method.response.header.Access-Control-Allow-Methods': False
    },
    responseModels={
        'application/json': 'Empty'
    }
)


vote_integration = client.put_integration(
    restApiId=api_id,
    resourceId=vote_resource_id,
    httpMethod='OPTIONS',
    type='MOCK',
    requestTemplates={
        'application/json': '{"statusCode": 200}'
    }
)


vote_integration_response = client.put_integration_response(
    restApiId=api_id,
    resourceId=vote_resource_id,
    httpMethod='OPTIONS',
    statusCode='200',
    responseParameters={
        'method.response.header.Access-Control-Allow-Headers': '\'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token\'',
        'method.response.header.Access-Control-Allow-Methods': '\'POST\',\'OPTIONS\'',
        'method.response.header.Access-Control-Allow-Origin': '\'*\''
    }
)



print ("DONE")
