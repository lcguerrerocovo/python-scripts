#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import webbrowser
import boto3
import urllib
import pprint
from os.path import expanduser
import os

parser = argparse.ArgumentParser(description='Generate iterm layouts to start ssh sessions for ec2 instances')
parser.add_argument('filename', nargs='?', default = None, help='file with ec2 instance info')
parser.add_argument('command', nargs='?', default = "ls", help='command to run on ssh')

args = parser.parse_args()
filename = args.filename
command = args.command

with open(filename, 'r') as fr:
   key = fr.readline()
   with open("%s/iTermocil.yml" % expanduser("~"),'w') as fw:
      fw.write("windows:" + os.linesep)
      fw.write("  - name: eb environment ssh" + os.linesep)
      fw.write("    root: ~/" + os.linesep)
      fw.write("    layout: tiled" + os.linesep)
      fw.write("    panes:" + os.linesep)
      for line in fr:
        fw.write("      - it2prof ssh; ssh -o \"StrictHostKeyChecking no\" -i ~/Development/keys/" \
            + key.rstrip() + ".pem ec2-user@" + line.rstrip() \
            + (" -t \'%s; /bin/bash -i\'" % command)+ os.linesep)
