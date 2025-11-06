# Quick Start Guide - Advisor Sentiment Analysis

## ✅ Current Status

**The tool is now working with Amazon Titan model!** You can use it immediately.

## Using the Tool Now (Titan Model)

The default model has been set to Amazon Titan, which works without any additional forms:

```bash
# Basic usage
python cli.py "I am very satisfied with the call"

# Analyze from file
python cli.py --file advisor_texts.txt

# Batch processing
python cli.py --file texts.txt --batch

# JSON output
python cli.py "Your text" --format json
```

## Upgrading to Claude Models (Better Quality)

If you want better analysis quality, you can use Claude models after completing the Anthropic use case form:

### Step 1: Submit Use Case Details for Claude
**Note:** Model access is now automatic! You just need to submit use case details for Anthropic models.

1. Go to: https://console.aws.amazon.com/bedrock/
2. Click "Model catalog" in the sidebar
3. Select a Claude model (e.g., "Claude 3 Sonnet")
4. Open it in the playground - you'll be prompted to fill out the use case form
5. Fill out the form (takes ~2 minutes) with your use case details
6. Wait 15 minutes to 24 hours for approval

### Step 2: Use Claude Models
Once approved, use Claude models with the `--model` flag:

```bash
# Claude 3 Sonnet (recommended - balanced)
python cli.py "Your text" --model anthropic.claude-3-sonnet-20240229-v1:0

# Claude 3 Haiku (faster/cheaper)
python cli.py "Your text" --model anthropic.claude-3-haiku-20240307-v1:0

# Claude 3 Opus (most capable)
python cli.py "Your text" --model anthropic.claude-3-opus-20240229-v1:0
```

### Step 3: Make Claude Default (Optional)
To make Claude the default, set an environment variable:

```powershell
$env:BEDROCK_MODEL_ID="anthropic.claude-3-sonnet-20240229-v1:0"
```

Or create a `.env` file:
```
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
```

## Model Comparison

| Model | Quality | Speed | Cost | Form Required |
|-------|---------|-------|------|---------------|
| **Amazon Titan** | Good | Fast | Low | ❌ No |
| **Claude 3 Haiku** | Very Good | Very Fast | Low | ✅ Yes |
| **Claude 3 Sonnet** | Excellent | Fast | Medium | ✅ Yes |
| **Claude 3 Opus** | Excellent | Slower | Higher | ✅ Yes |

## Troubleshooting

**Error: "Model use case details have not been submitted"**
- This means you're trying to use Claude without completing the form
- Solution: Use Titan model (default) or complete the Anthropic form
- Titan works immediately: `python cli.py "text" --model amazon.titan-text-express-v1`

**Need help?**
- See `ANTHROPIC_SETUP.md` for detailed Claude setup instructions
- See `setup_aws_cli.md` for AWS configuration help
- Run `python verify_aws_setup.py` to check your setup

