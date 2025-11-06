# Troubleshooting Guide - IAM Permissions Error

## Error: "UnrecognizedClientException: The security token included in the request is invalid"

This error typically means the Lambda function's IAM role doesn't have proper Bedrock permissions or the role isn't attached correctly.

### Solution Steps

#### 1. Verify IAM Role Was Created

```powershell
aws iam get-role --role-name advisor-sentiment-analysis-role
```

#### 2. Check IAM Policy is Attached

```powershell
aws iam list-role-policies --role-name advisor-sentiment-analysis-role
```

You should see:
- `advisor-sentiment-analysis-bedrock-policy`
- `advisor-sentiment-analysis-logs-policy`

#### 3. Verify Bedrock Policy Permissions

```powershell
aws iam get-role-policy --role-name advisor-sentiment-analysis-role --policy-name advisor-sentiment-analysis-bedrock-policy
```

The policy should allow:
- `bedrock:InvokeModel`
- `bedrock:InvokeModelWithResponseStream`
- Resource: `arn:aws:bedrock:us-east-1::foundation-model/*`

#### 4. Check Lambda Function Configuration

```powershell
aws lambda get-function --function-name advisor-sentiment-analysis
```

Verify:
- The `Role` field shows the correct IAM role ARN
- The role ARN matches: `arn:aws:iam::<account-id>:role/advisor-sentiment-analysis-role`

#### 5. Verify Bedrock Model Access

Make sure Bedrock models are enabled in your AWS account:

```powershell
aws bedrock list-foundation-models --region us-east-1
```

#### 6. Test IAM Role Permissions

Create a test script to verify the role can access Bedrock:

```python
import boto3
import json

# This should use the Lambda execution role automatically
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

try:
    # Test with Titan model
    response = bedrock.invoke_model(
        modelId='amazon.titan-text-express-v1',
        body=json.dumps({
            "inputText": "test",
            "textGenerationConfig": {
                "maxTokenCount": 10,
                "temperature": 0.7
            }
        }).encode('utf-8'),
        contentType="application/json"
    )
    print("SUCCESS: Bedrock access works!")
except Exception as e:
    print(f"ERROR: {e}")
```

### Common Issues

#### Issue 1: IAM Policy Not Applied

**Solution:** Run `terraform apply` again to ensure the IAM policy is updated.

#### Issue 2: Wrong Region

**Solution:** Ensure the IAM policy resource ARN matches the region where:
- Lambda function is deployed
- Bedrock models are available

Check your `terraform.tfvars`:
```hcl
aws_region = "us-east-1"  # Must match where Bedrock is available
```

#### Issue 3: Bedrock Not Enabled in Region

**Solution:** Verify Bedrock is available in your region:
```powershell
aws bedrock list-foundation-models --region us-east-1
```

#### Issue 4: IAM Propagation Delay

**Solution:** Wait 1-2 minutes after `terraform apply` for IAM changes to propagate.

### Manual Fix: Update IAM Policy

If Terraform didn't apply the policy correctly, you can manually update it:

```powershell
# Get your account ID
$accountId = (Get-STSCallerIdentity).Account

# Create policy JSON
$policy = @{
    Version = "2012-10-17"
    Statement = @(
        @{
            Effect = "Allow"
            Action = @(
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            )
            Resource = "arn:aws:bedrock:us-east-1::foundation-model/*"
        }
    )
} | ConvertTo-Json

# Update the policy
aws iam put-role-policy `
    --role-name advisor-sentiment-analysis-role `
    --policy-name advisor-sentiment-analysis-bedrock-policy `
    --policy-document $policy
```

### Verify Lambda Function Region

Check that the Lambda function is in the same region as Bedrock:

```powershell
aws lambda get-function --function-name advisor-sentiment-analysis --query 'Configuration.[FunctionName,FunctionArn,Role]'
```

The function ARN should show the region (e.g., `us-east-1`).

### Check CloudWatch Logs

View detailed error logs:

```powershell
aws logs tail /aws/lambda/advisor-sentiment-analysis --follow
```

Look for:
- Region information
- IAM permission errors
- Bedrock client creation errors

### Next Steps

1. Run `terraform apply` to ensure IAM policy is updated
2. Wait 1-2 minutes for IAM propagation
3. Test the API endpoint again
4. Check CloudWatch logs for detailed error messages

