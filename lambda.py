import boto3

lambda_client = boto3.client('lambda')

response = lambda_client.add_permission(
    FunctionName='trigger-function-demo-01',
    StatementId='AllowPublicInvoke',
    Action='lambda:InvokeFunction',
    Principal='*'
)

print("Permission added:", response)
