import boto3
import json
from tabulate import tabulate
from datetime import datetime, timezone

ec2 = boto3.client('ec2')
findings = []
volumes = ec2.describe_volumes()['Volumes']
print("PRINTING VOLUME DATA")
print("\n")
print(volumes)
print("########################################################")
print("########################################################")
print("\n")
print("\n")

iam = boto3.client('iam')
users = iam.list_users()['Users']
print("PRINTING USERS")
print("\n")
print(users)
keys = iam.list_access_keys(UserName='gp')['AccessKeyMetadata']
print("PRINTING KEYS")
print("\n")
print(keys)
for key in keys:
	create_date = key['CreateDate']
	age = (datetime.now(timezone.utc) - create_date).days
	print(f"Access key {key['AccessKeyId']} age: {age} days")
print("########################################################")
print("########################################################")
print("\n")
print("\n")

s3 = boto3.client('s3')
buckets = s3.list_buckets()['Buckets']
print("PRINTING BUCKETS")
print("\n")
print(buckets) # media-management-02112002-rahul-demo-proj
acl = s3.get_bucket_acl(Bucket='media-management-02112002-rahul-demo-proj')
print("PRINTING BUCKET DETAILS")
print("\n")
print(acl)
print("########################################################")
print("########################################################")
print("\n")
print("\n")

lambda_client = boto3.client('lambda')
functions = lambda_client.list_functions()['Functions']
print("PRINTING LAMBDA FUNCTIONS")
print("\n")
print(functions)          #trigger-function-demo-01
try:
	policy = lambda_client.get_policy(FunctionName=functions[0]['FunctionName'])
   
	print(policy)
except lambda_client.exceptions.ResourceNotFoundException:
	print(f"No resource policy found for Lambda function: {functions[0]['FunctionName']}")