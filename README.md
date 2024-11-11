
## Overview

This version of the voting system hosts the `index.html` file in an S3 bucket and the API for voting with an API Gateway.  Each endpoint of the API is implemented as a Lambda function that interacts with DynamoDB.

![Architecture](https://i.ibb.co/cLkdGdY/architecture.png)

## Deploy

* Create the lambda function that will process `GET /results`

  ```
  ./create_get_results_lambda.sh
  ```
  
* Create the lambda function that will process `POST /vote`

  ```
  ./create_post_vote_lambda.sh
  ```
  
* Create the API Gateway with the both endpoints

  ```
  source .venv/bin/activiate
  python create_voting_api.py
  ```
  
* Deploy the API

  ```
  ./deploy.sh
  ```
  
* Test that the endpoints are working (NOTE: this will add one "yes" vote)

  ```
  ./test.sh
  ```

  This test requires manual verification:  The script calls the `GET /results` endpoint, which returns the current number of votes.  Then it calls the `POST /vote` endpoint, which also returns the number of votes (with +1 "yes" vote).  Finally, it shows the headers for the `OPTIONS /vote`, which should be a 200 status code with the `access-control` headers set for CORS.
  
* Update the `index.html` in the S3 bucket

  ```
  ./update_index.sh
  ```
  
## Tear Down

* Delete the API

  ```
  ./delete_api.sh
  ```
  
* Delete the lambda function for `GET /results` 

  ```
  ./delete_get_results_lambda.sh
  ```
  
* Delete the lambda function for `POST /vote`

  ```
  ./delete_post_vote_lambda.sh
  ```
  
    

## TODO

* Create a script to reset the database
* Refactor the Lambda functions
  * duplicate code to get current counts
  * Application vs. delivery mechanism (API Gateway)
    
    
  