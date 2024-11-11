if aws dynamodb delete-table --table-name VoteCounts > /dev/null 2>&1; then
    echo "DONE"
else
    echo "NO TABLE FOUND"
    exit 1
fi
