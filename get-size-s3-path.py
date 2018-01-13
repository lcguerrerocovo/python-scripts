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

s3 = boto3.resource('s3')
client = boto3.client('s3')
paginator = client.get_paginator('list_objects')
result = paginator.paginate(Bucket=bucket, Delimiter='/', Prefix=key)

prefixes = {}

for prefix in result.search('CommonPrefixes'):
    prefix = prefix.get('Prefix')
    prefixes[prefix] = sum(_.size for _ in s3.Bucket(bucket).objects.filter(Prefix=prefix))

print("bucket:    %s" % bucket)
print("base path: %s" % key)
print("{0:60} {1:>15}".format("key","size"))
for key, value in prefixes.iteritems():
    print("{0:60} {1:>15}".format(key.split('/')[-2],get_human_readable(value) if human else value))
