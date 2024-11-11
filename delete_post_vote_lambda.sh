if aws lambda delete-function --function-name votingPostVote >/dev/null 2>&1 ; then
    echo "DONE"
    rm post_vote_lambda.zip
else
    echo "Function does not exist"
fi
