if aws lambda delete-function --function-name votingGetResults >/dev/null 2>&1 ; then
    echo "DONE"
    rm get_results_lambda.zip
else
    echo "Function does not exist"
fi
