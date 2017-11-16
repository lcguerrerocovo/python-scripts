#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import boto3

DEFAULT_REGION = "us-east-1"

def get_human_readable(size,precision=2):
    suffixes=['B','KB','MB','GB','TB']
    suffixIndex = 0
    while size > 1024 and suffixIndex < 4:
        suffixIndex += 1
        size = size/1024.0
    return "%.*f %s"%(precision,size,suffixes[suffixIndex])

parser = argparse.ArgumentParser(description='List size of keys in bucket')
parser.add_argument('bucket', nargs='?', help='bucket')
parser.add_argument('key', nargs='?', help='key')
parser.add_argument('--human', action='store_true')

args = parser.parse_args()
bucket = args.bucket
key = args.key
human = args.human

s3_client = boto3.client('s3')
response = s3_client.list_objects_v2(
    Bucket=bucket,
    Prefix=key
)

paths = {}
for obj in response['Contents']:
    one_level = obj['Key'].split("/")[len(key.split("/"))]
    if not one_level in paths:
        paths[one_level] = obj['Size']
    else: paths[one_level] = paths[one_level] + obj['Size']

print("bucket:    %s" % bucket)
print("base path: %s" % key)
print("{0:50} {1}".format("key","size"))
for key, value in paths.iteritems():
    print("{0:50} {1:>10}".format(key,get_human_readable(value) if human else value))
