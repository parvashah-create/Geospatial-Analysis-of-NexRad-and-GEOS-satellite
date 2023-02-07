"""
This script encompasses the functionalities for extracting metadata,
synchronizing files from the GEOS S3 bucket to our own S3 storage, and executing
file retrieval procedures utilizing the inputs documented in the accompanying
technical documentation.
"""

import boto3
import json

s3 = boto3.resource("s3")
bucket = s3.Bucket("noaa-goes18")


def list_files(bucket, prefix=""):
    result = {"name": prefix, "children": []}

    for obj in bucket.objects.filter(Prefix=prefix):
        parts = obj.key.split("/")

        if len(parts) > 1:
            folder = parts[0]
            file_name = parts[-1]

            subfolder = next((item for item in result["children"] if item["name"] == folder), None)
            if subfolder is None:
                subfolder = {"name": folder, "children": []}
                result["children"].append(subfolder)

            subfolder["children"].append({"name": file_name})

    return result


result = list_files(bucket)
with open("s3_files.json", "w") as f:
    f.write(json.dumps(result, indent=4))
