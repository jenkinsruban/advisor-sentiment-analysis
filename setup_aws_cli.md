# Setting Up AWS CLI for Advisor Sentiment Analysis

This guide will help you configure AWS CLI credentials for the Advisor Sentiment Analysis tool.

## Step 1: Install AWS CLI

If you haven't installed AWS CLI yet, download and install it from:
https://aws.amazon.com/cli/

Or using pip:
```bash
pip install awscli
```

## Step 2: Configure AWS Credentials

Run the following command:
```bash
aws configure
```

You'll be prompted to enter:

1. **AWS Access Key ID**: Your AWS access key
   - Get this from AWS IAM Console → Users → Your User → Security Credentials
   - Or create a new access key if you don't have one

2. **AWS Secret Access Key**: Your AWS secret key
   - Provided when you create an access key
   - Keep this secure and never share it

3. **Default region name**: The AWS region where Bedrock is available
   - Recommended: `us-east-1` (most models available)
   - Other options: `us-west-2`, `ap-southeast-1`, etc.
   - Check Bedrock availability in your region

4. **Default output format**: Press Enter for default (json)
   - This doesn't affect the sentiment analysis tool

## Step 3: Verify Configuration

Test your AWS CLI configuration:
```bash
aws sts get-caller-identity
```

This should return your AWS account information.

## Step 4: Verify Bedrock Access

Check if you can access Bedrock:
```bash
aws bedrock list-foundation-models --region us-east-1
```

If you see a list of models, you're all set!

## Step 5: Enable Bedrock Models

1. Go to AWS Bedrock Console: https://console.aws.amazon.com/bedrock/
2. Navigate to "Model access" in the left sidebar
3. Request access to the models you want to use:
   - **Claude 3 Sonnet** (recommended): `anthropic.claude-3-sonnet-20240229-v1:0`
   - **Claude 3 Haiku** (faster/cheaper): `anthropic.claude-3-haiku-20240307-v1:0`
   - **Claude 3 Opus** (most capable): `anthropic.claude-3-opus-20240229-v1:0`
4. Wait for approval (usually instant for most models)

## Using Multiple AWS Profiles

If you have multiple AWS accounts, you can use profiles:

1. Create/update `~/.aws/credentials`:
   ```
   [default]
   aws_access_key_id = YOUR_DEFAULT_KEY
   aws_secret_access_key = YOUR_DEFAULT_SECRET

   [bedrock]
   aws_access_key_id = YOUR_BEDROCK_KEY
   aws_secret_access_key = YOUR_BEDROCK_SECRET
   ```

2. Use the profile with the tool:
   ```bash
   export AWS_PROFILE=bedrock
   python cli.py "Your text here"
   ```

## Troubleshooting

### "Unable to locate credentials"
- Make sure you ran `aws configure`
- Verify `~/.aws/credentials` exists and contains your keys
- Check that the credentials file has correct permissions (600 on Linux/Mac)

### "Access Denied" or "UnauthorizedOperation"
- Verify your AWS user has Bedrock permissions
- Check IAM policy allows `bedrock:InvokeModel` action
- Ensure model access is enabled in Bedrock Console

### "Model not found" or "Model access denied"
- Enable the model in AWS Bedrock Console → Model access
- Wait for approval if pending
- Check the model ID is correct

### Region issues
- Verify Bedrock is available in your region
- Some models may only be available in specific regions
- Use `--region` flag to specify a different region

## Security Best Practices

- Never commit AWS credentials to version control
- Use IAM roles when possible (on EC2/ECS/Lambda)
- Rotate access keys regularly
- Use least-privilege IAM policies
- Consider using AWS SSO for enterprise setups

