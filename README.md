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

## 4. Edit the drop zone crawler to match the partitions of the data sources you want.
```yaml
#/components/etl.yaml
rGlueCrawlerDropZone:
  Type: AWS::Glue::Crawler
  Properties:
    DatabaseName: !Ref rGlueDatabaseDrop
    ...
    Targets:
      S3Targets:
        - Path: !Sub 's3://${pDropZoneBucket}/order_items/'
        - Path: !Sub 's3://${pDropZoneBucket}/order_reviews/'
        - Path: !Sub 's3://${pDropZoneBucket}/orders/'
        - Path: !Sub 's3://${pDropZoneBucket}/sellers/'
```
Then upload the files to the S3 bucket, and update the stack.

```bash
aws s3 cp . s3://2ndwatch-datalake-template-for-486567699039 --recursive

bash update-datalake.sh make-datalake-0 https://2ndwatch-datalake-template-for-486567699039.s3.amazonaws.com/main.yaml
```

## 5. Run the drop zone first crawler to establish tables for your drop zone.

It will create metadata tables (one for each partition that you created the step before) for the drop zone.

```bash
aws glue start-crawler --name 2ndwatch-datalake-demo-datalake-crawler-dropzone
```
The crawler should generate four tables. Check the schema of the tables to ensure everything was captured correctly.

## 6. Create jobs to transform the dropped data into something you can analyze.
(TODO: make a dev endpoint, followed by a notebook, with userdata that immediately connects it to a codecommit repo)

At this point, your data in the drop zone needs to be modified into a format that is optimized for analytics - we use parquet. Run glue-job-drop-to-raw.yaml to create the glue job that will reformat data from the raw zone. *For each Table in the Database*, update the parameters `--stack-name`, `pTableName`, `pDataPartition`, `pScriptLocation`, then run the stack.
```bash
aws cloudformation create-stack --stack-name glue-job-drop-to-raw-sellers \
  --template-url https://2ndwatch-datalake-template-for-486567699039.s3.amazonaws.com/glue-job-drop-to-raw.yaml \
  --parameters \
    ParameterKey=pProjectName,ParameterValue=2ndwatch-datalake-demo \
    ParameterKey=pDatabaseName,ParameterValue=2ndwatch-datalake-demo-datalake-drop-zone-database \
    ParameterKey=pTableName,ParameterValue=2ndwatch-datalake-demo_drop_sellers \
    ParameterKey=pDataPartition,ParameterValue=sellers \
    ParameterKey=pDownstreamBucket,ParameterValue=2ndwatch-datalake-demo-raw-486567699039 \
    ParameterKey=pScriptLocation,ParameterValue=s3://2ndwatch-datalake-template-for-486567699039/demo/glue-scripts/drop-to-raw-sellers.py \
    ParameterKey=pGlueJobRoleArn,ParameterValue=arn:aws:iam::486567699039:role/BaseGlueServiceRole
```
TODO: automate this to create a new job for each partition -- each table that came out of the drop zone. Because each data set will have different treatment. OR, you'd have to manually modify the glue job to just do every partition while it is up... write a loop inside the partition.

### Run the jobs:
```bash
for job in \
  2ndwatch-datalake-demo-glue-job-drop-to-raw-2ndwatch-datalake-demo_drop_order_items \
  2ndwatch-datalake-demo-glue-job-drop-to-raw-2ndwatch-datalake-demo_drop_order_reviews \
  2ndwatch-datalake-demo-glue-job-drop-to-raw-2ndwatch-datalake-demo_drop_orders \
  2ndwatch-datalake-demo-glue-job-drop-to-raw-2ndwatch-datalake-demo_drop_sellers;
do
  aws glue start-job-run --job-name $job
done
```
Wait for the jobs to finish.

## 7. Run the Analytics zone crawler
Run the second crawler -- the one for the Analytics zone to create metadata tables.
```bash
$ aws glue start-crawler --name datalake-demo-datalake-crawler-rawzone
```

## 8. Explore your analytics-ready data in Athena.
Use as examples, the scripts in `/demo/athena-scripts/`. To review scores by seller:
```sql
SELECT order_reviews.order_id, closed_deals.seller_id, review_score, sdr_id, sr_id
    FROM "...-database"."..._order_reviews" order_reviews
    join "...-database"."..._order_items" order_items
    on (order_reviews.order_id = order_items.order_id)
    join "...-database"."..._closed_deals" closed_deals
    on (order_items.seller_id = closed_deals.seller_id)
limit 100;
```

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

* Dead letter queue to receive failed messages from every zone


TODO
* Roles from LakeFormation
* Other storage - RDS, Redshift, Elasticsearch
* VPC (especially needed to launch redshift cluster)
* Auditing
* Monitoring Cloudtrail is created as a multi region trail.
* Use Elasticsearch for a better, more searchable data catalog
* Rename resources and variables: "raw zone" --> "analytics zone".

make sure the crawler for the curated zone is looking at the correct path.
In the glue jobs, double check the databases are correctly named (different databases now, one for each zone)
TODO: cloudformation template for redshift cluster - 4 nodes, dc2.large, inside a VPC with the correct security group (create a security group with correct ports, to allow for quicksight to look at redshift)


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
