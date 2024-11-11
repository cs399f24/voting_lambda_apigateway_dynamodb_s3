if aws dynamodb describe-table --table-name VoteCounts >/dev/null 2>&1; then
    echo "Table Already Exists"
    exit 0
fi
aws dynamodb create-table \
    --table-name VoteCounts \
    --key-schema AttributeName=VoteType,KeyType=HASH \
    --attribute-definitions AttributeName=VoteType,AttributeType=S \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 > /dev/null || exit 1
echo "DONE"

