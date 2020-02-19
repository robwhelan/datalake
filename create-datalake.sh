#!/bin/bash
#TODO: start in main root directory.
#clone the datalake repo.
#cd into the new repo folder.

#to turn back the clock:
#aws cloudformation delete-stack --stack-name make-datalake-template-stack

export BUCKET_STACK_NAME=make-datalake-template-stack
export DATALAKE_STACK_NAME=make-datalake-stack
export BUCKET_TO_HOLD_TEMPLATE=dlau-datalake-template

echo 'creating a bucket to hold the template'
aws cloudformation create-stack \
  --stack-name $BUCKET_STACK_NAME \
  --parameters ParameterKey=rS3BucketName,ParameterValue=$BUCKET_TO_HOLD_TEMPLATE \
  --template-body file://datalake-template-bucket.yaml

aws cloudformation wait stack-create-complete --stack-name $BUCKET_STACK_NAME

export S3_BUCKET_NAME=$(aws cloudformation describe-stacks \
  --stack-name $BUCKET_STACK_NAME \
  --output text \
  --query Stacks[0].Outputs[0].OutputValue )

echo 'bucket to hold template is created:'
echo $S3_BUCKET_NAME

export S3_LOCATION='s3://'$S3_BUCKET_NAME;
export S3_TEMPLATE_LOCATION='https://'$S3_BUCKET_NAME'.s3.amazonaws.com';
#upload everything to the new bucket.
echo 'uploading datalake files to '$S3_LOCATION;
aws s3 cp . $S3_LOCATION --recursive;

#now create the datalake
echo 'creating the datalake'
export DATALAKE_STACK_RESPONSE=$(aws cloudformation create-stack \
  --stack-name $DATALAKE_STACK_NAME \
  --template-url $S3_TEMPLATE_LOCATION'/main.yaml' \
  --parameters \
      ParameterKey='pProjectName',ParameterValue=$1 \
      ParameterKey='pS3TemplateLocation',ParameterValue=$S3_TEMPLATE_LOCATION \
      ParameterKey='pTemplateBucket',ParameterValue=$S3_BUCKET_NAME \
  --capabilities CAPABILITY_NAMED_IAM \
  )

echo 'datalake stack id:'
echo $DATALAKE_STACK_RESPONSE
