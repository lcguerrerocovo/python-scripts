#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import webbrowser
import boto3
import urllib
import pprint
from os.path import expanduser
import os

DEFAULT_REGION = "us-east-1"
BASE_URL = 'https://console.aws.amazon.com'
LB_URL = BASE_URL + '/ec2/v2/home?region=%s#LoadBalancers:search=%s'
AG_URL = BASE_URL + '/ec2/autoscaling/home?region=%s#AutoScalingGroups:id=%s;view=details'
EC2_URL = BASE_URL + '/ec2/v2/home?region=%s#Instances:search=%s;sort=desc:launchTime'
EB_URL = BASE_URL + '/elasticbeanstalk/home?region=%s#/environment/dashboard?environmentId=%s'

parser = argparse.ArgumentParser(description='List current beanstalk environments and open web consoles for configuration')
parser.add_argument('app_name', nargs='?', default = None, help='Elastic Beanstalk Application Name')
parser.add_argument('region', nargs='?', default = DEFAULT_REGION, help='AWS Region')

args = parser.parse_args()
app_name = args.app_name
region = args.region

eb_client = boto3.client('elasticbeanstalk', region_name=region)
ec2_client = boto3.client('ec2', region_name=region)

envs = eb_client.describe_environments() if app_name is None else client.describe_environments(ApplicationName=app_name)

print("Elastic Beanstalk environments")
for index, env in enumerate(envs['Environments'],start=1):
  print("%d -> %s" % (index,env['EnvironmentName']))

# user input
while True:
  try:
    choice = int(raw_input("Please choose environment to open web consoles: ")) - 1
    if choice < 0 or choice >= index:
      print("Not a valid choice")
      continue
  except ValueError:
    print("Not a valid choice")
    continue
  else:
    break

environment = envs['Environments'][choice]['EnvironmentName']
env_id = envs['Environments'][choice]['EnvironmentId']
resources = eb_client.describe_environment_resources(EnvironmentName=environment)

webbrowser.open(LB_URL % (region,resources['EnvironmentResources']['LoadBalancers'][0]['Name']))
webbrowser.open(AG_URL % (region,resources['EnvironmentResources']['AutoScalingGroups'][0]['Name']))
webbrowser.open(EC2_URL % (region,environment))
webbrowser.open(EB_URL % (region,env_id))

instance_ids = [instance['Id'] for instance in resources['EnvironmentResources']['Instances']]

with open("%s/%s.beanstalk" % (expanduser("~"),environment),'w') as file:
  response = ec2_client.describe_instances(InstanceIds=instance_ids)
  instances = response['Reservations'][0]['Instances']
  file.write(instances[0]['KeyName'] + os.linesep)
  for data in instances:
    file.write(data['PrivateIpAddress'] + os.linesep)
