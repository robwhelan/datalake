import json
import boto3
import base64
import re
import string
import pickle
import os
import io
from io import StringIO
from datetime import datetime
import pandas as pd #from a layer
import numpy as np #from another layer

s3 = boto3.resource('s3')

DOWNSTREAM_BUCKET = os.environ['DOWNSTREAM_BUCKET']

COLUMNS = [
    'column_1',
    'column_2',
    'column_3'
]

def TransformData(old_df):
    new_df = pd.DataFrame(columns=COLUMNS)
    new_df.at[0, 'column_1'] = 'transformed_message' + old_df.at[0, 'column_1']
    new_df.at[0, 'column_2'] = 'transformed_message_3'
    new_df.at[0, 'column_3'] = 'final transformation'
    return new_df

def WriteDfToS3(df, bucket, key):
    csv_buffer = StringIO()
    df.to_csv(csv_buffer)
    response = s3.Object(bucket, key).put(Body=csv_buffer.getvalue())
    return response

def BuildCSVAndPostToS3(data, columns, bucket, key):
    df = pd.DataFrame(data, columns=columns)
    response = WriteDfToS3(df, bucket, key)
    return response

def TimestampPrefix():
    year = str(datetime.now().year)
    month = str(datetime.now().month)
    day = str(datetime.now().day)
    hour = str(datetime.now().hour)
    prefix = year + '/' + month + '/' + day + '/' + hour + '/'
    return prefix

def lambda_handler(event, context):
    try:
        #open the file and read it.
        #for each message, DropToRaw
        print('event:', event)
        #change this to be for each object in the sqs queue.
        for record in event['Records']:
            event_body = record['body']
            event_body = json.loads(event_body)
            print('event_body- records:', event_body)
            for s3_event in event_body['Records']:
                bucket = s3_event['s3']['bucket']['name']
                key = s3_event['s3']['object']['key']
                obj = s3.Object(bucket, key)
                local_obj = obj.get()
                df = pd.read_csv(io.BytesIO(local_obj['Body'].read()))

                new_data = TransformData(df)

        key = TimestampPrefix() + str(datetime.now()) + '.csv'
        #POST the csv to the next bucket.
        new_csv = WriteDfToS3(
            new_data,
            DOWNSTREAM_BUCKET,
            key
        )

        return {
            'new_csv': new_csv,
        }

    except Exception as e:
        print(e)
        raise e
