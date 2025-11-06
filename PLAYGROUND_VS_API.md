# Playground vs API Access - Understanding the Difference

## Current Situation

You can use Claude models in the **AWS Bedrock Playground** (UI), but you're getting an error when trying to use them via the **API** (our CLI tool).

## Why This Happens

1. **Playground access** may be enabled separately or have different approval status
2. **API access** requires the use case form to be fully approved
3. There can be a delay between playground access and API access activation

## What You're Seeing

✅ **Playground:** Working (Claude Sonnet 4.5 responds correctly)  
❌ **API:** Still requires use case approval ("Model use case details have not been submitted")

## Solutions

### Option 1: Wait for Approval (Recommended)

If you've already submitted the use case form:
- Wait 15 minutes to 24 hours
- Check your email for approval confirmation
- Try the API again after approval

### Option 2: Submit Use Case Form via API Invocation

1. Try invoking the model via our tool:
   ```bash
   python cli.py "test" --model anthropic.claude-3-sonnet-20240229-v1:0
   ```

2. If you get the "use case details" error, AWS may provide a link to submit the form directly

### Option 3: Check Form Submission Status

1. Go to AWS Bedrock Console
2. Check if there's a status indicator for your use case submission
3. Look for any pending approvals or notifications

### Option 4: Use Newer Model IDs

The playground shows "Claude Sonnet 4.5" - try using the newer model ID:

```bash
# Claude Sonnet 4.5 (matches playground)
python cli.py "Your text" --model anthropic.claude-sonnet-4-5-20250929-v1:0

# Claude 3.7 Sonnet (newer)
python cli.py "Your text" --model anthropic.claude-3-7-sonnet-20250219-v1:0

# Claude 3.5 Sonnet v2 (stable)
python cli.py "Your text" --model anthropic.claude-3-5-sonnet-20241022-v2:0
```

## Available Claude Models

Based on your account, these models are available:

**Claude 4 Series (Latest):**
- `anthropic.claude-sonnet-4-5-20250929-v1:0` - Claude Sonnet 4.5
- `anthropic.claude-opus-4-1-20250805-v1:0` - Claude Opus 4.1
- `anthropic.claude-sonnet-4-20250514-v1:0` - Claude Sonnet 4

**Claude 3.7/3.5 Series:**
- `anthropic.claude-3-7-sonnet-20250219-v1:0` - Claude 3.7 Sonnet
- `anthropic.claude-3-5-sonnet-20241022-v2:0` - Claude 3.5 Sonnet v2
- `anthropic.claude-3-5-sonnet-20240620-v1:0` - Claude 3.5 Sonnet

**Claude 3 Series (Original):**
- `anthropic.claude-3-sonnet-20240229-v1:0` - Claude 3 Sonnet
- `anthropic.claude-3-haiku-20240307-v1:0` - Claude 3 Haiku
- `anthropic.claude-3-opus-20240229-v1:0` - Claude 3 Opus

## Next Steps

1. **If you haven't submitted the form yet:**
   - Go to Model Catalog → Select Claude model → Open in playground
   - Fill out the use case form when prompted
   - Wait for approval

2. **If you've already submitted:**
   - Wait 15 minutes to 24 hours
   - Check your email for confirmation
   - Try the API again

3. **In the meantime:**
   - Continue using Amazon Titan (current default)
   - Or use the playground for testing

## Troubleshooting

**Q: Why can I use it in playground but not API?**
A: Playground and API may have separate access controls. API access requires full approval.

**Q: How long does approval take?**
A: Usually 15 minutes to 24 hours after form submission.

**Q: Can I speed up the process?**
A: No, it's an automated process. Just wait for approval.

**Q: Should I resubmit the form?**
A: No, if you've already submitted, wait for approval. Resubmitting won't help.

