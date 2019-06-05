# datalake
Notes
* Works for one partition in each bucket. If your drop zone will spread to multiple data streams, such as images in one, and clickstream in another, add another SQS queue for notifications, and configure prefixes for each notifications (/images/ and /clickstream/). Then build a completely different lambda to work off the new queue. Modify the lambda to create a key that matches the partition.
