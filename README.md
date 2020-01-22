![architecture](https://github.com/robwhelan/datalake/blob/master/2ndWatch%20DataOps%20Platform.png)

## 1. Set your AWS profile.
```bash
export AWS_PROFILE=...
```

## 2. Run the main datalake creation script.
This will download the template files, make a bucket to place them in AWS, and then generate a 3 zone datalake, a glue database for each zone, and crawlers.

From the root directory:
```bash
$ bash create-datalake.sh <name-of-your-project>
```

Example:
```bash
$ bash create-datalake.sh toyota-demo-1
```
to update:
```bash
$ bash update-datalake.sh toyota-demo-1 https://datalake-rww.s3.amazonaws.com/main.yaml
```

## 3. Upload some data to the drop zone.
For a demo, this upload is ~50MB and the source data can be found on Kaggle: https://www.kaggle.com/olistbr/brazilian-ecommerce

## 4. Run the first crawler (drop zone crawler) in order to establish a table for your drop zone.
It will create metadata tables (one for each partition -- for each file you have) for the drop zone.

```bash
$ aws glue start-crawler --name 2ndwatch-datalake-demo-datalake-crawler-dropzone
```

## 5. Write a job to transform the dropped data into something you can analyze.
TODO: make a dev endpoint, followed by a notebook, with userdata that immediately connects it to a codecommit repo.

Run glue-job-drop-to-raw.yaml CloudFormation to create the glue job that will reformat data from the raw zone. For each Table in this Database, update the parameters 'table name' and 'partition', then run the stack -- be sure to name the stack something different each time.
```bash
$ aws cloudformation create-stack --stack-name glue-job-drop-to-raw-closed-deals-2 \
  --template-url https://datalake-rww.s3.amazonaws.com/glue-job-drop-to-raw.yaml \
  --parameters file://glue-job-drop-to-raw-parameters.json
```
TODO: automate this to create a new job for each partition -- each table that came out of the drop zone. Because each data set will have different treatment. OR, you'd have to manually modify the glue job to just do every partition while it is up... write a loop inside the partition.

5. Run the glue job for each partition (table name). This will move data into the raw zone, and set up for an hourly schedule.
```bash
$ bash run-raw-glue-jobs.sh
```

TODO:::::
6. Wait until the first transform jobs are done. Run the second crawler -- the one for the raw zone. This will create metadata tables for the raw zone. This is defined in etl.yaml.
```bash
$ aws glue start-crawler --name datalake-demo-datalake-crawler-rawzone
```

7. Explore your analytics-ready data in Athena.

8. Run glue-job-raw-to-curated.yaml. This will create a glue job responsible for reformatting / joining the data. And, it will create a trigger for the job, to make it run anytime the first job succeeds.
```bash
$ aws cloudformation create-stack --stack-name glue-job-raw-to-curated \
  --template-url https://datalake-rww.s3.amazonaws.com/glue-job-raw-to-curated.yaml \
  --parameters file://glue-job-raw-to-curated-parameters.json
```

9. Run the glue job. This will move the new dataset into the curated zone.

10. Turn on a redshift cluster
Make sure the security group is there.

11. Query editor:
a. create table that matches the schema from S3 curated zone.
b. copy data from s3 into redshift table.
c. Do some queries -- aggregate # of deals and sum of deal value per seller; average review per seller / per SDR.

Design Principles
1.
2. Allow for remote updates of the stacks as the architecture evolves.
3. Few (3-5), simple, easily-understood roles instead of many roles.
4. One database per zone
5. many tables, all populated by Glue crawlers
5. Glue (PySpark) for ETL with simple transformations.
6. ETL to be built out after data initially loaded.

Features
* As many zones as you want. 3 zones by default.

* Dead letter queue to receive failed messages from every zone, and every lambda consuming the queue.

TODO: * Lambda features:
  1. Python3.6
  2. Uses 2 layers - one for numpy, the other for pandas.
  3. An all-in-one serverless data science / data engineering lambda.
  4. The stub assumes a CSV was dropped into the zone bucket; it gets picked up, example transformation on it, and then re-saved as a new CSV in the next zone.

* Monitoring:
Cloudtrail is created as a multi region trail.


# datalake
Notes
* Works for one partition in each bucket. If your drop zone will spread to multiple data streams, such as images in one, and clickstream in another, add another SQS queue for notifications, and configure prefixes for each notifications (/images/ and /clickstream/). Then build a completely different lambda to work off the new queue. Modify the lambda to create a key that matches the partition.

TODO
* Roles
* Other storage - RDS, Redshift, Elasticsearch
* VPC (especially needed to launch redshift cluster)
* Auditing
* Monitoring

  make sure the crawler for the curated zone is looking at the correct path.
  In the glue jobs, double check the databases are correctly named (different databases now, one for each zone)
  TODO: cloudformation template for redshift cluster - 4 nodes, dc2.large, inside a VPC with the correct security group (create a security group with correct ports, to allow for quicksight to look at redshift)

  2ndwatch-datalake-demo-datalake-crawler-dropzone2ndwatch-datalake-demo-datalake-crawler-dropzone


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
