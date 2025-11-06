# Quick Test Guide

## Your C# Code (Corrected)

Your code is almost perfect! Here's a slightly improved version:

```csharp
using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Text.Json;

var client = new HttpClient();
var apiUrl = "https://rvz0a310j2.execute-api.us-east-1.amazonaws.com/analyze";

var requestBody = new
{
    text = "I am very satisfied with the advisor's communication and investment recommendations"
};

var jsonContent = JsonSerializer.Serialize(requestBody);
var content = new StringContent(jsonContent, Encoding.UTF8, "application/json");

var response = await client.PostAsync(apiUrl, content);
response.EnsureSuccessStatusCode();

var responseBody = await response.Content.ReadAsStringAsync();
Console.WriteLine(responseBody);
```

## Current Status

The API is deployed, but there's still an IAM permissions issue. The error indicates:
- The Lambda function is being called correctly ✅
- The routing is working ✅  
- But Bedrock access is failing ❌

## Next Steps

1. **Wait 2-3 minutes** for IAM changes to fully propagate
2. **Test again** with your C# code
3. **Check CloudWatch logs** for detailed error information:
   ```powershell
   aws logs tail /aws/lambda/advisor-sentiment-analysis --follow
   ```

## If Error Persists

The "UnrecognizedClientException" might require:
1. Verifying Bedrock model access is enabled in AWS Console
2. Checking if there are service control policies blocking access
3. Ensuring the IAM role has propagated (can take a few minutes)

Your C# code is correct - the issue is on the AWS side with IAM permissions propagation.

