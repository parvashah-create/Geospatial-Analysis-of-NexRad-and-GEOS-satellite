"""
This script encompasses the functionalities for extracting metadata,
synchronizing files from the NexRad S3 bucket to our own S3 storage, and executing
file retrieval procedures utilizing the inputs documented in the accompanying
technical documentation.
"""

import boto3
s3 = boto3.resource("s3")
my_bucket = s3.Bucket('noaa-goes18')

for my_bucket_object in my_bucket.objects.all():
    print(my_bucket_object.key)
