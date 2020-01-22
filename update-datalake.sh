#!/bin/bash
aws cloudformation update-stack --stack-name $1 \
  --template-url $2 \
  --parameters \
    ParameterKey=pS3TemplateLocation,UsePreviousValue=true \
    ParameterKey=pProjectName,UsePreviousValue=true \
  --capabilities CAPABILITY_NAMED_IAM
