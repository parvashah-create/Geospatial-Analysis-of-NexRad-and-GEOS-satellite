"""
This script encompasses the functionalities for extracting metadata,
synchronizing files from the GEOS S3 bucket to our own S3 storage, and executing
file retrieval procedures utilizing the inputs documented in the accompanying
technical documentation.
"""

import boto3
s3 = boto3.resource("s3")
my_bucket = s3.Bucket('noaa-goes18')

f = open('GEOS.txt', 'w')
for my_bucket_object in my_bucket.objects.all().filter(Prefix="ABI-L1b-RadC/"):
    f.write(my_bucket_object.key + '\n')
    print(my_bucket_object.key)

f.close()
