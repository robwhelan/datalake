#!/bin/bash
aws cloudformation create-stack --stack-name $1 \
  --template-url $2 \
  --parameters file://main-template-parameters.json \
  --capabilities CAPABILITY_NAMED_IAM
