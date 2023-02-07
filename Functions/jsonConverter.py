"""
This script implements a process to convert the metadata obtained from a
specified S3 bucket into a structured and hierarchical JSON representation.
"""


import json


def convert_to_json(filename):
    with open(filename) as f:
        lines = f.readlines()
    data = {}
    for line in lines:
        parts = line.strip().split("/")
        curr = data
        for part in parts:
            if part not in curr:
                curr[part] = {}
            curr = curr[part]
    return json.dumps(data, indent=4)


print(convert_to_json("text_file.txt"))
