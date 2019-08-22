How:
1. First, run the main.yaml script. This will generate, among other things, a glue database, all your s3 buckets, and crawlers.

from the root directory:
```bash
$ bash create-datalake.sh <name-of-your-stack> <https path to main.yaml>
```

Example:
```bash
$ bash create-datalake.sh robs-kewl-stack-5 https://datalake-rww.s3.amazonaws.com/main.yaml
```

2. Upload some data to the drop zone.
The source data can be found on Kaggle: https://www.kaggle.com/olistbr/brazilian-ecommerce
```bash
$ bash upload-data.sh <path-to-source-data> <your-drop-zone-bucket...output from the main.yaml stack>
```

Example:
```bash
$ bash upload-data.sh ../Downloads/brazilian-ecommerce/ s3://robs-kewl-datalake-test-drop-773548596459/
```

3. Run the first crawler (drop zone crawler). It will create a metadata table for the drop zone.
4. Run glue-job-drop-to-raw.yaml CloudFormation to create the glue job that will reformat data from the raw zone.
5. Run the glue job. This will move data into the raw zone, and set up for an hourly schedule.
6. Run the second crawler -- the one for the raw zone. This will create a metadata table for the raw zone.
7. Run glue-job-raw-to-curated.yaml. This will create a glue job responsible for reformatting / joining the data. And, it will create a trigger for the job, to make it run anytime the first job succeeds.
8. Run the glue job. This will move the new dataset into the curated zone.

Design Principles
1. Send only two stacks: 1 for your prod account, 1 for your security account.
2. Allow for remote updates of the stacks as the architecture evolves.
3. Few (3-5), simple, easily-understood roles instead of many roles.
4. One database, many tables, all populated by Glue crawlers
5. Glue (PySpark) for ETL with simple transformations.
6. ETL to be built out after data initially loaded.
7. Private S3 and DDB endpoints from the private subnets (not from the public or data subnets). Any lambda should run inside the private subnets.

Features
* As many zones as you want. 4 zones by default.
* Each zone:
  1. Bucket
  2. Dedicated customer-managed CMK to encrypt the bucket, event notifications to SQS
  3. Lambda stub to consume the queue
* ETL:
  Create one Glue database.
  Then, create a Crawler and specify the location for the initial data. This will create a table prefixed with the prefix you specify ()
  (Run the crawler via SQS / lambda after the resource is created? )
  After the table is created, update the stack with a transformation?
* Network: launched in us-east-1. Update the VPC stack otherwise (DHCP option sets)

* Dead letter queue to receive failed messages from every zone, and every lambda consuming the queue.

* Lambda features:
  1. Python3.6
  2. Uses 2 layers - one for numpy, the other for pandas.
  3. An all-in-one serverless data science / data engineering lambda.
  4. The stub assumes a CSV was dropped into the zone bucket; it gets picked up, example transformation on it, and then re-saved as a new CSV in the next zone.

* Monitoring:
Cloudtrail is created as a multi region trail.


* architecture
Zone:
1. bucket
2. CMK
3. SQS queue for new object puts
4. Lambda to consume the queue.

ETL:
1. Glue database - built at the beginning.
2. Glue crawler - also built at the beginning.
3. Later, TODO run the crawler after first data stored.
4. Build a Job from cloudformation, that runs on new data.

# datalake
Notes
* Works for one partition in each bucket. If your drop zone will spread to multiple data streams, such as images in one, and clickstream in another, add another SQS queue for notifications, and configure prefixes for each notifications (/images/ and /clickstream/). Then build a completely different lambda to work off the new queue. Modify the lambda to create a key that matches the partition.

TODO
* Roles
* Other storage - RDS, Redshift, Elasticsearch
* Security account & VPC
* Auditing
* Monitoring
  * set up Macie outside of cloudformation. Might be a lambda or something that runs every week.

ROLES


--Group
  --Users
  --Permissions (policies and/or roles (which are a collection of policies))


Intersection of two areas:
Groups set by job function (data steward, engineer, scientist, bi user) -- put this in the path
Groups set by ability to see data of varying security (proprietary, restricted, secret) -- put in the path

Data Steward -- administrator.
Data Engineer -- can read/write to all buckets.
Data Scientist -- can write only to the curated zone. Can create new glue jobs to stage data. Can do everything with sagemaker.
Business Intelligence Analyst -- run queries (read only), upload new data to a sandbox, use quicksight etc.
