import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

order_items = glueContext.create_dynamic_frame.from_catalog(
    database="datalake-demo-datalake-main-database",
    table_name="datalake-demo_raw_order_items")

order_reviews = glueContext.create_dynamic_frame.from_catalog(
    database="datalake-demo-datalake-main-database",
    table_name="datalake-demo_raw_order_reviews")

closed_deals = glueContext.create_dynamic_frame.from_catalog(
    database="datalake-demo-datalake-main-database",
    table_name="datalake-demo_raw_closed_deals")

item_reviews = Join.apply(
    order_items, order_reviews, 'order_id', 'order_id')

seller_performance = Join.apply(
    item_reviews, closed_deals, 'seller_id', 'seller_id'
)

glueContext.write_dynamic_frame.from_options(
    frame=seller_performance,
    connection_type='s3',
    connection_options= { "path": "s3://datalake-demo-curated-773548596459/curated-data/"},
    format = 'parquet'
)

job.commit()
