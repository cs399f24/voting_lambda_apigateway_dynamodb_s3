ROLE=$(aws iam get-role --role-name labRole --query "Role.Arn" --output text)
zip  get_results_lambda.zip get_results_lambda.py
aws lambda create-function --function-name votingGetResults \
  --runtime python3.9 \
  --role $ROLE \
  --zip-file fileb://get_results_lambda.zip \
  --handler get_results_lambda.lambda_handler
aws lambda publish-version --function-name votingGetResults

