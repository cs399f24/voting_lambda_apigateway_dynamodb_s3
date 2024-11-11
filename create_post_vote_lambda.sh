if aws lambda get-function --function-name votingPostVote >/dev/null 2>&1; then
    echo "Function already exists"
    exit 1
fi    

ROLE=$(aws iam get-role --role-name labRole --query "Role.Arn" --output text)
zip  post_vote_lambda.zip post_vote_lambda.py
aws lambda create-function --function-name votingPostVote \
  --runtime python3.9 \
  --role $ROLE \
  --zip-file fileb://post_vote_lambda.zip \
  --handler post_vote_lambda.lambda_handler
# Wait for the function to be created and active (starts as "Pending")
aws lambda wait function-active --function-name votingPostVote
aws lambda publish-version --function-name votingPostVote

