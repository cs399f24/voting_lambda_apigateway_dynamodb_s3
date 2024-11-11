ROLE=$(aws iam get-role --role-name labRole --query "Role.Arn" --output text)
zip  post_vote_lambda.zip post_vote_lambda.py
aws lambda create-function --function-name votingPostVote \
  --runtime python3.9 \
  --role $ROLE \
  --zip-file fileb://post_vote_lambda.zip \
  --handler post_vote_lambda.lambda_handler
aws lambda publish-version --function-name votingPostVote

