# Random Python scripts for odd jobs

## elastic-beanstalk-envs

This script list any configured elastic beanstalk environments running in your AWS account (it assumes credentials are configured property in the environment) and handily opens a web console for the related autoscaling group, load balancer, ec2 intances and the EB environment console itself. It also writes a file with the pem key and internal ip information to the user directory with the environment name and a *.beanstalk extension

## github-repos

List all github repos and generates a CSV file with relevant information

## generate-iterm-layout.py

WARNING: this script is heavily customized for generating iTerm 2 layouts based on the output of `elastic-beanstalk-envs` script so that it is easy to automatically login via ssh to all machines tied to a beanstalk environment
