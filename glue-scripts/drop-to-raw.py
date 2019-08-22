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
## @type: DataSource
## @args: [database = "cloud-custodian-test", table_name = "metadata_json_gz", transformation_ctx = "datasource0"]
## @return: datasource0
## @inputs: []
datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "cloud-custodian-test", table_name = "metadata_json_gz", transformation_ctx = "datasource0")
## @type: ApplyMapping
## @args: [mapping = [("policy.name", "string", "`policy.name`", "string"), ("policy.mode.type", "string", "`policy.mode.type`", "string"), ("policy.mode.schedule", "string", "`policy.mode.schedule`", "string"), ("policy.mode.role", "string", "`policy.mode.role`", "string"), ("policy.resource", "string", "`policy.resource`", "string"), ("policy.description", "string", "`policy.description`", "string"), ("policy.filters", "array", "`policy.filters`", "string"), ("policy.actions", "array", "`policy.actions`", "string"), ("version", "string", "version", "string"), ("execution.id", "string", "`execution.id`", "string"), ("execution.start", "double", "`execution.start`", "double"), ("execution.end_time", "double", "`execution.end_time`", "double"), ("execution.duration", "double", "`execution.duration`", "double"), ("config.region", "string", "`config.region`", "string"), ("config.regions", "array", "`config.regions`", "string"), ("config.cache", "string", "`config.cache`", "string"), ("config.profile", "string", "`config.profile`", "string"), ("config.account_id", "string", "`config.account_id`", "string"), ("config.assume_role", "string", "`config.assume_role`", "string"), ("config.external_id", "string", "`config.external_id`", "string"), ("config.log_group", "string", "`config.log_group`", "string"), ("config.tracer", "string", "`config.tracer`", "string"), ("config.metrics_enabled", "string", "`config.metrics_enabled`", "string"), ("config.output_dir", "string", "`config.output_dir`", "string"), ("config.cache_period", "int", "`config.cache_period`", "int"), ("config.dryrun", "boolean", "`config.dryrun`", "boolean"), ("config.authorization_file", "string", "`config.authorization_file`", "string"), ("config.subparser", "string", "`config.subparser`", "string"), ("config.config", "string", "`config.config`", "string"), ("config.configs", "array", "`config.configs`", "string"), ("config.policy_filter", "string", "`config.policy_filter`", "string"), ("config.resource_type", "string", "`config.resource_type`", "string"), ("config.verbose", "string", "`config.verbose`", "string"), ("config.quiet", "string", "`config.quiet`", "string"), ("config.debug", "boolean", "`config.debug`", "boolean"), ("config.skip_validation", "boolean", "`config.skip_validation`", "boolean"), ("config.command", "string", "`config.command`", "string"), ("config.vars", "string", "`config.vars`", "string"), ("sys-stats", "string", "sys-stats", "string"), ("api-stats.`ec2.DescribeInstances`", "int", "`api-stats.``ec2.DescribeInstances```", "int"), ("metrics", "array", "metrics", "string")], transformation_ctx = "applymapping1"]
## @return: applymapping1
## @inputs: [frame = datasource0]
applymapping1 = ApplyMapping.apply(frame = datasource0, mappings = [("policy.name", "string", "`policy.name`", "string"), ("policy.mode.type", "string", "`policy.mode.type`", "string"), ("policy.mode.schedule", "string", "`policy.mode.schedule`", "string"), ("policy.mode.role", "string", "`policy.mode.role`", "string"), ("policy.resource", "string", "`policy.resource`", "string"), ("policy.description", "string", "`policy.description`", "string"), ("policy.filters", "array", "`policy.filters`", "string"), ("policy.actions", "array", "`policy.actions`", "string"), ("version", "string", "version", "string"), ("execution.id", "string", "`execution.id`", "string"), ("execution.start", "double", "`execution.start`", "double"), ("execution.end_time", "double", "`execution.end_time`", "double"), ("execution.duration", "double", "`execution.duration`", "double"), ("config.region", "string", "`config.region`", "string"), ("config.regions", "array", "`config.regions`", "string"), ("config.cache", "string", "`config.cache`", "string"), ("config.profile", "string", "`config.profile`", "string"), ("config.account_id", "string", "`config.account_id`", "string"), ("config.assume_role", "string", "`config.assume_role`", "string"), ("config.external_id", "string", "`config.external_id`", "string"), ("config.log_group", "string", "`config.log_group`", "string"), ("config.tracer", "string", "`config.tracer`", "string"), ("config.metrics_enabled", "string", "`config.metrics_enabled`", "string"), ("config.output_dir", "string", "`config.output_dir`", "string"), ("config.cache_period", "int", "`config.cache_period`", "int"), ("config.dryrun", "boolean", "`config.dryrun`", "boolean"), ("config.authorization_file", "string", "`config.authorization_file`", "string"), ("config.subparser", "string", "`config.subparser`", "string"), ("config.config", "string", "`config.config`", "string"), ("config.configs", "array", "`config.configs`", "string"), ("config.policy_filter", "string", "`config.policy_filter`", "string"), ("config.resource_type", "string", "`config.resource_type`", "string"), ("config.verbose", "string", "`config.verbose`", "string"), ("config.quiet", "string", "`config.quiet`", "string"), ("config.debug", "boolean", "`config.debug`", "boolean"), ("config.skip_validation", "boolean", "`config.skip_validation`", "boolean"), ("config.command", "string", "`config.command`", "string"), ("config.vars", "string", "`config.vars`", "string"), ("sys-stats", "string", "sys-stats", "string"), ("api-stats.`ec2.DescribeInstances`", "int", "`api-stats.``ec2.DescribeInstances```", "int"), ("metrics", "array", "metrics", "string")], transformation_ctx = "applymapping1")
## @type: DataSink
## @args: [connection_type = "s3", connection_options = {"path": "s3://cloudjanitorz/raw"}, format = "csv", transformation_ctx = "datasink2"]
## @return: datasink2
## @inputs: [frame = applymapping1]
datasink2 = glueContext.write_dynamic_frame.from_options(frame = applymapping1, connection_type = "s3", connection_options = {"path": "s3://cloudjanitorz/raw"}, format = "parquet", transformation_ctx = "datasink2")
job.commit()
