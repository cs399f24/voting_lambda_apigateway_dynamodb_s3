if aws lambda get-function --function-name votingGetResults >/dev/null 2>&1; then
    echo "Function already exists"
    exit 1
fi    

ROLE=$(aws iam get-role --role-name labRole --query "Role.Arn" --output text)
zip  get_results_lambda.zip get_results_lambda.py
aws lambda create-function --function-name votingGetResults \
  --runtime python3.9 \
  --role $ROLE \
  --zip-file fileb://get_results_lambda.zip \
  --handler get_results_lambda.lambda_handler
# Wait for the function to be created and active (starts as "Pending")
aws lambda wait function-active --function-name votingGetResults  
aws lambda publish-version --function-name votingGetResults

