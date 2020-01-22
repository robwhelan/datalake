#!/bin/bash
aws cloudformation create-stack --stack-name $2 \
  --template-url $3 \
  --parameters pProjectName=$1 \
  --capabilities CAPABILITY_NAMED_IAM
