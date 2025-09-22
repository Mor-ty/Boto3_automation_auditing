
# 📄 AWS Resource Inspection Script Documentation
This Python script uses the **Boto3 AWS SDK** to extract and display key information about AWS resources in your account. It is designed to help developers, DevOps engineers, and cloud administrators **inspect, audit, and validate** the configuration and security posture of their AWS environment.


## 🧰 Technologies Used

- **Python 3.x**
- **Boto3** (AWS SDK for Python)
- **Tabulate** (for optional tabular formatting)
- **AWS IAM credentials** (configured via environment or AWS CLI)

---

## 🔍 Script Capabilities

The script performs the following tasks:

### 1. **EC2 Volumes**
- Lists all EBS volumes in the account.
- Prints detailed metadata including volume ID, size, state, and encryption status.

### 2. **IAM Users and Access Keys**
- Lists all IAM users.
- Retrieves access keys for a specific user (`gp`).
- Calculates and prints the **age of each access key** in days.

### 3. **S3 Buckets**
- Lists all S3 buckets in the account.
- Retrieves and prints the **Access Control List (ACL)** for a specific bucket (`media-management-02112002-rahul-demo-proj`).
- Identifies if the bucket is publicly accessible.

### 4. **Lambda Functions**
- Lists all Lambda functions.
- Attempts to retrieve the **resource-based policy** for the first function.
- Handles the case where no policy is attached.

---

## 🧪 Sample Output

```bash
PRINTING VOLUME DATA
[{'VolumeId': 'vol-0abc123...', 'State': 'available', 'Encrypted': False, ...}]

PRINTING USERS
[{'UserName': 'gp', 'CreateDate': '...'}]

PRINTING KEYS
[{'AccessKeyId': 'AKIA...', 'CreateDate': '...'}]
Access key AKIA... is 120 days old

PRINTING BUCKETS
[{'Name': 'media-management-02112002-rahul-demo-proj'}]

PRINTING BUCKET DETAILS
{'Grants': [{'Grantee': {'URI': 'http://acs.amazonaws.com/groups/global/AllUsers'}, ...}]}

PRINTING LAMBDA FUNCTIONS
[{'FunctionName': 'trigger-function-demo-01'}]

No resource policy found for Lambda function: trigger-function-demo-01
```

---

## ⚠️ Error Handling

- **Lambda Policy**: If no resource policy is found, the script catches the `ResourceNotFoundException` and prints a friendly message.
- **S3 ACL**: If the bucket ACL cannot be retrieved, the script will raise an exception unless wrapped in a try-except block (recommended for production).

---

## 📂 File Structure

```
aws_resource_inspector.py
requirements.txt  # boto3, tabulate
aws_audit_report.json (optional output)
```

---

## 🚀 How to Run

1. Ensure AWS credentials are configured (`~/.aws/credentials` or via environment).
2. Install dependencies:
   ```bash
   pip install boto3 tabulate
   ```
3. Run the script:
   ```bash
   python aws_resource_inspector.py
   ```

---
