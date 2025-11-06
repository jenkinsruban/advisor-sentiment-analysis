# Deployment Guide - Advisor Sentiment Analysis Lambda

This guide explains how to deploy the Advisor Sentiment Analysis tool as an AWS Lambda function with API Gateway for Angular application integration.

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **Terraform** installed (version >= 1.0)
   - Download from: https://www.terraform.io/downloads
   - Or install via package manager: `choco install terraform` (Windows)
3. **AWS CLI** configured with credentials
   - Run: `aws configure`
4. **Python 3.11** (for local testing, optional)
5. **Bedrock Model Access** enabled in your AWS account

## Project Structure

```
deployment/
├── lambda/                    # Lambda function code
│   ├── lambda_function.py    # Lambda handler
│   ├── bedrock_client.py     # Bedrock client
│   ├── sentiment_analyzer.py # Sentiment analyzer
│   ├── requirements.txt      # Python dependencies
│   └── __init__.py
├── terraform/                 # Terraform configuration
│   ├── main.tf               # Main infrastructure
│   ├── variables.tf          # Variable definitions
│   ├── outputs.tf           # Output values
│   └── terraform.tfvars.example
├── README.md                 # This file
└── .gitignore
```

## Deployment Steps

### Step 1: Install Python Dependencies (Optional)

If you want to test locally or package manually:

```bash
cd deployment/lambda
pip install -r requirements.txt -t .
```

**Note:** Terraform will handle packaging automatically, but you can test locally first.

### Step 2: Configure Terraform Variables

1. Copy the example variables file:
   ```bash
   cd deployment/terraform
   cp terraform.tfvars.example terraform.tfvars
   ```

2. Edit `terraform.tfvars` with your values:
   ```hcl
   aws_region       = "us-east-1"
   function_name    = "advisor-sentiment-analysis"
   bedrock_model_id = "amazon.titan-text-express-v1"
   cors_origins     = "*"  # Use specific URL in production
   environment      = "dev"
   ```

   **For Production:**
   - Set `cors_origins` to your Angular app URL: `"https://your-app.com"`
   - Update `environment` to `"prod"`

### Step 3: Initialize Terraform

```bash
cd deployment/terraform
terraform init
```

This downloads the required Terraform providers (AWS, archive).

### Step 4: Review Terraform Plan

```bash
terraform plan
```

Review the resources that will be created:
- Lambda function
- IAM role and policies
- API Gateway HTTP API
- CloudWatch log group

### Step 5: Deploy Infrastructure

```bash
terraform apply
```

Type `yes` when prompted. Terraform will:
1. Create a ZIP file from your Lambda code
2. Upload the ZIP to AWS Lambda
3. Create IAM roles and policies
4. Create API Gateway
5. Connect everything together

### Step 6: Get API Endpoint

After deployment, Terraform will output the API endpoint:

```bash
terraform output
```

You'll see output like:
```
api_endpoint = "abc123xyz.execute-api.us-east-1.amazonaws.com"
api_invoke_url = "https://abc123xyz.execute-api.us-east-1.amazonaws.com"
analyze_endpoint = "https://abc123xyz.execute-api.us-east-1.amazonaws.com/analyze"
analyze_batch_endpoint = "https://abc123xyz.execute-api.us-east-1.amazonaws.com/analyze-batch"
```

**Save the `analyze_endpoint` URL** - you'll need it for your Angular app!

## API Endpoints

### POST /analyze

Analyze a single text for sentiment.

**Request:**
```json
{
  "text": "I am very satisfied with the advisor's communication and investment recommendations",
  "model_id": "amazon.titan-text-express-v1"  // Optional, overrides default
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "sentiment": "positive",
    "confidence": 0.95,
    "emotional_tone": "Satisfied and optimistic",
    "key_indicators": ["very satisfied", "exceeded expectations"],
    "summary": "The communication expresses strong satisfaction...",
    "recommendations": "Continue current advisory approach...",
    "model_used": "amazon.titan-text-express-v1",
    "text_length": 83
  }
}
```

### POST /analyze-batch

Analyze multiple texts in batch.

**Request:**
```json
{
  "texts": [
    "I am very satisfied with the advisor",
    "I'm concerned about market volatility"
  ],
  "model_id": "amazon.titan-text-express-v1"  // Optional
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "sentiment": "positive",
        "confidence": 0.9,
        ...
        "index": 1
      },
      {
        "sentiment": "neutral",
        "confidence": 0.7,
        ...
        "index": 2
      }
    ],
    "count": 2
  }
}
```

## Angular Integration

### 1. Create Service

Create an Angular service to call the API:

```typescript
// sentiment-analysis.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SentimentAnalysisService {
  private apiUrl = 'https://YOUR_API_GATEWAY_URL.execute-api.us-east-1.amazonaws.com';

  constructor(private http: HttpClient) {}

  analyzeText(text: string, modelId?: string): Observable<any> {
    const body: any = { text };
    if (modelId) {
      body.model_id = modelId;
    }
    
    return this.http.post(`${this.apiUrl}/analyze`, body);
  }

  analyzeBatch(texts: string[], modelId?: string): Observable<any> {
    const body: any = { texts };
    if (modelId) {
      body.model_id = modelId;
    }
    
    return this.http.post(`${this.apiUrl}/analyze-batch`, body);
  }
}
```

### 2. Use in Component

```typescript
// your-component.ts
import { Component } from '@angular/core';
import { SentimentAnalysisService } from './sentiment-analysis.service';

@Component({
  selector: 'app-sentiment',
  template: `
    <div>
      <textarea [(ngModel)]="inputText" placeholder="Enter advisor text"></textarea>
      <button (click)="analyze()">Analyze Sentiment</button>
      
      <div *ngIf="result">
        <h3>Sentiment: {{ result.data.sentiment }}</h3>
        <p>Confidence: {{ result.data.confidence * 100 }}%</p>
        <p>{{ result.data.summary }}</p>
      </div>
    </div>
  `
})
export class SentimentComponent {
  inputText = '';
  result: any = null;

  constructor(private sentimentService: SentimentAnalysisService) {}

  analyze() {
    this.sentimentService.analyzeText(this.inputText).subscribe(
      response => {
        this.result = response;
      },
      error => {
        console.error('Error:', error);
      }
    );
  }
}
```

### 3. Update CORS Origins (Production)

Before deploying to production, update `terraform.tfvars`:

```hcl
cors_origins = "https://your-angular-app.com"
```

Then run:
```bash
terraform apply
```

## Updating the Lambda Function

After making changes to Lambda code:

1. **Update code** in `deployment/lambda/`
2. **Run Terraform apply**:
   ```bash
   cd deployment/terraform
   terraform apply
   ```
   
Terraform will automatically:
- Detect code changes
- Create a new ZIP file
- Upload and deploy to Lambda

## Troubleshooting

### Error: "Model use case details have not been submitted"

**Solution:** You need to enable Bedrock model access. See the main project README for details.

### Error: "Access Denied" when calling API

**Solution:** Check CORS configuration. Make sure your Angular app URL matches `cors_origins` in Terraform variables.

### Error: Lambda timeout

**Solution:** Increase `lambda_timeout` in `terraform.tfvars`:
```hcl
lambda_timeout = 60  # Increase to 60 seconds
```

### Viewing Lambda Logs

```bash
aws logs tail /aws/lambda/advisor-sentiment-analysis --follow
```

Or view in AWS Console: CloudWatch → Log Groups → `/aws/lambda/advisor-sentiment-analysis`

## Testing the API

### Using cURL

```bash
# Single text analysis
curl -X POST https://YOUR_API_URL/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "I am very satisfied with the advisor"}'

# Batch analysis
curl -X POST https://YOUR_API_URL/analyze-batch \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Text 1", "Text 2"]}'
```

### Using Postman

1. Create a new POST request
2. URL: `https://YOUR_API_URL/analyze`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
   ```json
   {
     "text": "Your advisor text here"
   }
   ```

## Cleanup

To remove all resources:

```bash
cd deployment/terraform
terraform destroy
```

Type `yes` to confirm. This will delete:
- Lambda function
- API Gateway
- IAM roles and policies
- CloudWatch log group

## Cost Estimation

- **Lambda**: Pay per request + compute time (very low cost)
- **API Gateway**: $1.00 per million requests (first million free)
- **Bedrock**: Pay per token (varies by model)
- **CloudWatch Logs**: First 5GB free, then $0.50/GB

For typical usage, expect <$10/month for moderate traffic.

## Security Best Practices

1. **Production:** Set `cors_origins` to your specific Angular app URL
2. **API Keys:** Consider adding API Gateway API keys for production
3. **Rate Limiting:** Add throttling in API Gateway for production
4. **IAM:** Use least privilege - the Lambda role only has Bedrock invoke permissions
5. **Environment Variables:** Don't store secrets in Terraform variables - use AWS Secrets Manager

## Next Steps

- Add API Gateway API keys for authentication
- Implement rate limiting
- Add monitoring and alerting
- Set up CI/CD pipeline for automated deployments
- Configure custom domain for API Gateway

## Support

For issues or questions:
- Check CloudWatch logs for Lambda errors
- Review Terraform plan output
- Verify Bedrock model access in AWS Console
- Ensure IAM permissions are correct

