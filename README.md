Design Principles
1. Send only two stacks: 1 for your prod account, 1 for your security account.
2. Allow for remote updates of the stacks as the architecture evolves.
3. Few (3-5), simple, easily-understood roles instead of many roles.
4. One database, many tables.
5. Glue (PySpark) for ETL with simple transformations.


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

* Dead letter queue to receive failed messages from every zone, and every lambda consuming the queue.

* Lambda features:
  1. Python3.6
  2. Uses 2 layers - one for numpy, the other for pandas.
  3. An all-in-one serverless data science / data engineering lambda.
  4. The stub assumes a CSV was dropped into the zone bucket; it gets picked up, example transformation on it, and then re-saved as a new CSV in the next zone.

# datalake
Notes
* Works for one partition in each bucket. If your drop zone will spread to multiple data streams, such as images in one, and clickstream in another, add another SQS queue for notifications, and configure prefixes for each notifications (/images/ and /clickstream/). Then build a completely different lambda to work off the new queue. Modify the lambda to create a key that matches the partition.

TODO
* VPC
* Glue
* Other storage - RDS, Redshift, Elasticsearch
* Security account & VPC
* Auditing
* Monitoring
