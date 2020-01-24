import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, [
    'JOB_NAME',
    'database_name', #array of arguemnts you want to grab.
    'table_name',
    'downstream_bucket',
    'data_partition']
    )

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

print("arguments: ", args)

downstreamBucket = 's3://' + args['downstream_bucket'] + '/' + args['data_partition'] + '/'
## @type: DataSource
## @args: [database = "robs-kewl-datalake-test-datalake-main-database", table_name = "robs-kewl-datalake-test_drop_order_items", transformation_ctx = "datasource0"]
## @return: datasource0
## @inputs: []
datasource0 = glueContext.create_dynamic_frame.from_catalog(database = args['database_name'], table_name = args['table_name'], transformation_ctx = "datasource0")
## @type: ApplyMapping
## @args: [mapping = [("order_id", "string", "order_id", "string"), ("order_item_id", "long", "order_item_id", "long"), ("product_id", "string", "product_id", "string"), ("seller_id", "string", "seller_id", "string"), ("shipping_limit_date", "string", "shipping_limit_date", "string"), ("price", "double", "price", "double"), ("freight_value", "double", "freight_value", "double")], transformation_ctx = "applymapping1"]
## @return: applymapping1
## @inputs: [frame = datasource0]
applymapping1 = ApplyMapping.apply(frame = datasource0, mappings = [("order_id", "string", "order_id", "string"), ("order_item_id", "string", "order_item_id", "long"), ("product_id", "string", "product_id", "string"), ("seller_id", "string", "seller_id", "string"), ("shipping_limit_date", "string", "shipping_limit_date", "string"), ("price", "string", "price", "double"), ("freight_value", "string", "freight_value", "double")], transformation_ctx = "applymapping1")
## @type: ResolveChoice
## @args: [choice = "make_struct", transformation_ctx = "resolvechoice2"]
## @return: resolvechoice2
## @inputs: [frame = applymapping1]
resolvechoice2 = ResolveChoice.apply(frame = applymapping1, choice = "make_struct", transformation_ctx = "resolvechoice2")
## @type: DropNullFields
## @args: [transformation_ctx = "dropnullfields3"]
## @return: dropnullfields3
## @inputs: [frame = resolvechoice2]
dropnullfields3 = DropNullFields.apply(frame = resolvechoice2, transformation_ctx = "dropnullfields3")
## @type: DataSink
## @return: datasink4
## @inputs: [frame = dropnullfields3]
datasink4 = glueContext.write_dynamic_frame.from_options(frame = dropnullfields3, connection_type = "s3", connection_options = {"path": downstreamBucket}, format = "parquet", transformation_ctx = "datasink4")
job.commit()
