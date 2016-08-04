# -*- coding:utf-8 -*-

import json
import boto3
from boto3.session import Session

import time
from datetime import datetime as dt

ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')

response = ec2_client.describe_instances()

for ec2_group in response["Reservations"]:
	for instance_info in ec2_group['Instances']:
		if instance_info['State']['Name'] == 'running':
			print instance_info['Tags']
		