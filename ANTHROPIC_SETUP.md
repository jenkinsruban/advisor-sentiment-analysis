# Setting Up Anthropic Claude Models on AWS Bedrock

## Important Update

**The Model access page has been retired!** AWS Bedrock now automatically enables access to all serverless foundation models. However, **first-time users of Anthropic models still need to submit use case details** before accessing Claude models.

## Steps to Enable Claude Models

### Option 1: Submit Use Case Details via Model Catalog/Playground

1. **Go to AWS Bedrock Console**
   - Navigate to: https://console.aws.amazon.com/bedrock/
   - Make sure you're in the correct AWS region (e.g., us-east-1)

2. **Access the Model Catalog**
   - Click on "Model catalog" in the left sidebar
   - Or go directly to: https://console.aws.amazon.com/bedrock/home?region=us-east-1#/modelCatalog

3. **Select a Claude Model**
   - Find and click on a Claude model (e.g., "Claude 3 Sonnet")
   - Open it in the playground

4. **Submit Use Case Details**
   - When you try to use the model for the first time, you'll be prompted to submit use case details
   - See the "Personal Usage Form Guide" section below for detailed instructions on filling out the form

5. **Wait for Approval**
   - Most requests are approved within 15 minutes
   - Some may take up to 24 hours
   - You'll receive an email confirmation when approved

6. **Verify Access**
   - Once approved, you can use Claude models
   - Test with: `python cli.py "test" --model anthropic.claude-3-sonnet-20240229-v1:0`

### Option 2: Submit Use Case When First Invoking the Model

Alternatively, you can try invoking the model directly - if use case details are required, AWS will prompt you to complete them at that time.

## Alternative: Use Amazon Titan (No Form Required)

If you need to use the tool immediately without waiting, you can use Amazon Titan models which don't require the use case form:

```bash
python cli.py "Your text here" --model amazon.titan-text-express-v1
```

Amazon Titan models are available immediately and don't require additional forms. The tool is currently configured to use Titan as the default model.

## Personal Usage Form Guide

If you're using this for **personal projects, learning, or individual development**, here's how to fill out the form:

### Form Fields:

1. **Company name:**
   - Options: "Personal Project", "Self-Employed", "Independent Developer", "N/A", or your name
   - Example: `Independent Developer`

2. **Company website URL:**
   - Leave blank if you don't have one
   - Or provide: GitHub profile, LinkedIn, portfolio site, or personal website
   - Example: `https://github.com/yourusername` (optional)

3. **What industry do you operate in?**
   - Select from dropdown: "Software Development", "Education", "Research", or "Other"
   - Best choice: `Software Development` or `Education`

4. **Who are the intended users you are building for?**
   - ✅ Check: **"Internal users (employees, staff, team members)"**
   - ❌ Uncheck: "External users" (unless you're building a public app)
   - For personal use, "Internal users" means yourself

5. **Describe your use cases (Maximum 500 characters):**
   
   **⚠️ IMPORTANT:** Do NOT mention the word "Claude" in your description - it will be automatically denied!
   
   **Recommended description for Advisor Sentiment Analysis:**
   ```
   I am developing a sentiment analysis tool for analyzing financial advisor 
   communications using Anthropic models on Amazon Bedrock. This is a personal 
   learning project to explore AI capabilities for text analysis. The tool will 
   process advisor-client communications to identify sentiment, emotional tone, 
   and provide recommendations. All data will be non-sensitive and used for 
   educational purposes only. No PII or proprietary information will be processed.
   ```
   
   **Alternative shorter version (if character limit is tight):**
   ```
   Personal development project: Building a sentiment analysis tool for financial 
   advisor communications using Anthropic models. Educational use case for 
   exploring AI text analysis capabilities. No sensitive data or PII will be 
   processed. Internal use only.
   ```

### Tips:
- ✅ Use "Anthropic models" or "generative AI models" - never mention "Claude"
- ✅ Focus on educational/learning purposes
- ✅ Emphasize no PII or sensitive data
- ✅ Keep it under 500 characters
- ✅ Be honest but professional

### After Submitting:
- Click "Submit use case details"
- Wait 15 minutes to 24 hours for approval
- You'll receive email confirmation when approved
- Then you can use Claude models: `python cli.py "text" --model anthropic.claude-3-sonnet-20240229-v1:0`

## Key Points

- **Model access is automatic** - No need to manually enable models
- **Anthropic models require use case details** - First-time users must submit a use case form
- **Never mention "Claude"** - Use "Anthropic models" instead
- **IAM policies can restrict access** - Use IAM policies and Service Control Policies to control access
- **All models are in the Model Catalog** - Browse available models there

