"""
Quick verification script to check if AWS CLI is configured correctly.
"""

import os
import sys
from pathlib import Path

def check_aws_cli_config():
    """Check if AWS CLI credentials are configured."""
    print("=" * 60)
    print("AWS CLI Configuration Check")
    print("=" * 60)
    print()
    
    # Check for credentials file
    aws_dir = Path.home() / ".aws"
    credentials_file = aws_dir / "credentials"
    config_file = aws_dir / "config"
    
    print("1. Checking AWS credentials file...")
    if credentials_file.exists():
        print(f"   [OK] Found: {credentials_file}")
        
        # Check if it has content
        try:
            with open(credentials_file, 'r') as f:
                content = f.read()
                if 'aws_access_key_id' in content.lower():
                    print("   [OK] Contains access key configuration")
                else:
                    print("   [WARN] File exists but may not have credentials")
        except Exception as e:
            print(f"   [WARN] Could not read file: {e}")
    else:
        print(f"   [FAIL] Not found: {credentials_file}")
        print("   → Run 'aws configure' to set up credentials")
    
    print()
    
    # Check for config file
    print("2. Checking AWS config file...")
    if config_file.exists():
        print(f"   [OK] Found: {config_file}")
        
        try:
            with open(config_file, 'r') as f:
                content = f.read()
                if 'region' in content.lower():
                    print("   [OK] Contains region configuration")
        except Exception as e:
            print(f"   [WARN] Could not read file: {e}")
    else:
        print(f"   [WARN] Not found: {config_file}")
        print("   → Region will default to us-east-1 or use AWS_REGION env var")
    
    print()
    
    # Check environment variables
    print("3. Checking environment variables...")
    env_vars = {
        'AWS_REGION': os.getenv('AWS_REGION'),
        'AWS_ACCESS_KEY_ID': os.getenv('AWS_ACCESS_KEY_ID'),
        'AWS_SECRET_ACCESS_KEY': os.getenv('AWS_SECRET_ACCESS_KEY'),
        'AWS_PROFILE': os.getenv('AWS_PROFILE'),
    }
    
    for var, value in env_vars.items():
        if value:
            masked = value[:4] + "..." if len(value) > 4 else "***"
            print(f"   [OK] {var} is set ({masked})")
        else:
            print(f"   [-] {var} not set (will use AWS CLI config if available)")
    
    print()
    
    # Test boto3 connection
    print("4. Testing boto3 credential resolution...")
    try:
        import boto3
        from botocore.exceptions import NoCredentialsError, ClientError
        
        # Try to create a session
        session = boto3.Session()
        credentials = session.get_credentials()
        
        if credentials:
            print("   [OK] boto3 can resolve credentials")
            print(f"   [OK] Access Key ID: {credentials.access_key[:4]}...")
            
            # Try to get caller identity
            try:
                sts = boto3.client('sts')
                identity = sts.get_caller_identity()
                print(f"   [OK] Successfully authenticated as: {identity.get('Arn', 'Unknown')}")
            except ClientError as e:
                print(f"   [WARN] Authentication test failed: {e}")
            except Exception as e:
                print(f"   [WARN] Error testing authentication: {e}")
        else:
            print("   [FAIL] boto3 cannot resolve credentials")
            print("   -> Run 'aws configure' to set up credentials")
            
    except NoCredentialsError:
        print("   [FAIL] No credentials found")
        print("   -> Run 'aws configure' to set up credentials")
    except ImportError:
        print("   [FAIL] boto3 not installed")
        print("   -> Run 'pip install -r requirements.txt'")
    except Exception as e:
        print(f"   [WARN] Error: {e}")
    
    print()
    
    # Test Bedrock access
    print("5. Testing Bedrock access...")
    try:
        import boto3
        from botocore.exceptions import ClientError
        
        region = os.getenv('AWS_REGION', 'us-east-1')
        bedrock = boto3.client('bedrock-runtime', region_name=region)
        
        # Try to list foundation models (requires bedrock:ListFoundationModels permission)
        try:
            bedrock_control = boto3.client('bedrock', region_name=region)
            models = bedrock_control.list_foundation_models()
            print(f"   [OK] Can access Bedrock API")
            print(f"   [OK] Found {len(models.get('modelSummaries', []))} available models")
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            if error_code == 'AccessDeniedException':
                print("   [WARN] Bedrock access denied - check IAM permissions")
            else:
                print(f"   [WARN] Bedrock API error: {error_code}")
        except Exception as e:
            print(f"   [WARN] Could not test Bedrock access: {e}")
            
    except Exception as e:
        print(f"   [WARN] Error testing Bedrock: {e}")
    
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print()
    print("If all checks show [OK], you're ready to use the tool!")
    print("Run: python cli.py 'Your advisor text here'")
    print()
    print("For detailed setup instructions, see: setup_aws_cli.md")
    print("=" * 60)

if __name__ == "__main__":
    check_aws_cli_config()

