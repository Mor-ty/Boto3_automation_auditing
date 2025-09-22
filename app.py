import boto3
import json
from tabulate import tabulate
from datetime import datetime, timezone
 
def check_security_groups():
    ec2 = boto3.client('ec2')
    findings = []
    response = ec2.describe_security_groups()
    for sg in response['SecurityGroups']:
        for perm in sg.get('IpPermissions', []):
            for ip_range in perm.get('IpRanges', []):
                cidr = ip_range.get('CidrIp')
                if cidr == '0.0.0.0/0':
                    port = perm.get('FromPort')
                    if port in [22, 3389, 80, 443]:
                        findings.append({
                            "ResourceType": "Security Group",
                            "Identifier": sg['GroupId'],
                            "Issue": f"Allows {cidr} on port {port}"
                        })
    return findings
 
def check_iam_mfa():
    iam = boto3.client('iam')
    findings = []
    users = iam.list_users()['Users']
    for user in users:
        mfa = iam.list_mfa_devices(UserName=user['UserName'])['MFADevices']
        if not mfa:
            findings.append({
                "ResourceType": "IAM User",
                "Identifier": user['UserName'],
                "Issue": "MFA not enabled"
            })
    return findings
 
def check_old_access_keys():
    iam = boto3.client('iam')
    findings = []
    users = iam.list_users()['Users']
    for user in users:
        keys = iam.list_access_keys(UserName=user['UserName'])['AccessKeyMetadata']
        for key in keys:
            age = (datetime.now(timezone.utc) - key['CreateDate']).days
            if age > 90:
                findings.append({
                    "ResourceType": "IAM User",
                    "Identifier": user['UserName'],
                    "Issue": f"Access key {key['AccessKeyId']} is {age} days old"
                })
    return findings
 
def check_public_s3_buckets():
    s3 = boto3.client('s3')
    findings = []
    buckets = s3.list_buckets()['Buckets']
    for bucket in buckets:
        name = bucket['Name']
        try:
            acl = s3.get_bucket_acl(Bucket=name)
            for grant in acl['Grants']:
                grantee = grant.get('Grantee', {})
                if grantee.get('URI') == 'http://acs.amazonaws.com/groups/global/AllUsers':
                    findings.append({
                        "ResourceType": "S3 Bucket",
                        "Identifier": name,
                        "Issue": "Public access via ACL"
                    })
        except Exception:
            continue
    return findings
 
def check_unencrypted_volumes():
    ec2 = boto3.client('ec2')
    findings = []
    volumes = ec2.describe_volumes()['Volumes']
    for vol in volumes:
        if not vol['Encrypted']:
            findings.append({
                "ResourceType": "EBS Volume",
                "Identifier": vol['VolumeId'],
                "Issue": "Not encrypted"
            })
    return findings
 
def check_lambda_permissions():
    lambda_client = boto3.client('lambda')
    findings = []
    functions = lambda_client.list_functions()['Functions']
    for fn in functions:
        try:
            policy = lambda_client.get_policy(FunctionName=fn['FunctionName'])
            if '"Principal":"*"' in policy['Policy']:
                findings.append({
                    "ResourceType": "Lambda Function",
                    "Identifier": fn['FunctionName'],
                    "Issue": "Unrestricted permissions"
                })
        except Exception:
            continue
    return findings
 
def run_audit():
    findings = []
    findings.extend(check_security_groups())
    findings.extend(check_iam_mfa())
    findings.extend(check_old_access_keys())
    findings.extend(check_public_s3_buckets())
    findings.extend(check_unencrypted_volumes())
    findings.extend(check_lambda_permissions())

    with open('aws_audit_report.json', 'w') as f:
        json.dump(findings, f, indent=4)
    print("Audit complete. Report saved to aws_audit_report.json")

if __name__ == "__main__":
    run_audit()
