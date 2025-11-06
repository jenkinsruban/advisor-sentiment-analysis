# API Usage Examples - Advisor Sentiment Analysis

## Quick Start

### 1. Get Your API Endpoint

```powershell
cd deployment/terraform
terraform output analyze_endpoint
```

## Calling Methods

### Method 1: cURL (Command Line)

#### Single Text Analysis
```bash
curl -X POST https://YOUR_API_URL/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I am very satisfied with the advisor'\''s communication"
  }'
```

#### Batch Analysis
```bash
curl -X POST https://YOUR_API_URL/analyze-batch \
  -H "Content-Type: application/json" \
  -d '{
    "texts": [
      "I am very satisfied with the advisor",
      "I'\''m concerned about market volatility"
    ]
  }'
```

### Method 2: Angular Service

```typescript
// sentiment-analysis.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SentimentAnalysisService {
  private apiUrl = 'https://YOUR_API_URL.execute-api.us-east-1.amazonaws.com';
  
  private httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json'
    })
  };

  constructor(private http: HttpClient) {}

  // Analyze single text
  analyzeText(text: string, modelId?: string): Observable<any> {
    const body: any = { text };
    if (modelId) {
      body.model_id = modelId;
    }
    
    return this.http.post(`${this.apiUrl}/analyze`, body, this.httpOptions);
  }

  // Analyze multiple texts
  analyzeBatch(texts: string[], modelId?: string): Observable<any> {
    const body: any = { texts };
    if (modelId) {
      body.model_id = modelId;
    }
    
    return this.http.post(`${this.apiUrl}/analyze-batch`, body, this.httpOptions);
  }
}
```

### Method 3: Angular Component Usage

```typescript
// sentiment.component.ts
import { Component } from '@angular/core';
import { SentimentAnalysisService } from './sentiment-analysis.service';

@Component({
  selector: 'app-sentiment',
  template: `
    <div class="container">
      <h2>Advisor Sentiment Analysis</h2>
      
      <div class="input-section">
        <textarea 
          [(ngModel)]="inputText" 
          placeholder="Enter advisor communication text..."
          rows="5"
          class="form-control">
        </textarea>
        <button 
          (click)="analyze()" 
          [disabled]="loading || !inputText.trim()"
          class="btn btn-primary">
          {{ loading ? 'Analyzing...' : 'Analyze Sentiment' }}
        </button>
      </div>
      
      <div *ngIf="result" class="result-section">
        <h3>Analysis Results</h3>
        <div class="result-card">
          <div class="sentiment-badge" [class]="result.data.sentiment">
            {{ result.data.sentiment.toUpperCase() }}
          </div>
          <p><strong>Confidence:</strong> {{ (result.data.confidence * 100).toFixed(1) }}%</p>
          <p><strong>Emotional Tone:</strong> {{ result.data.emotional_tone }}</p>
          <p><strong>Summary:</strong> {{ result.data.summary }}</p>
          
          <div *ngIf="result.data.key_indicators?.length > 0">
            <strong>Key Indicators:</strong>
            <ul>
              <li *ngFor="let indicator of result.data.key_indicators">
                {{ indicator }}
              </li>
            </ul>
          </div>
          
          <div *ngIf="result.data.recommendations">
            <strong>Recommendations:</strong>
            <p>{{ result.data.recommendations }}</p>
          </div>
        </div>
      </div>
      
      <div *ngIf="error" class="error-section">
        <p class="error-message">{{ error }}</p>
      </div>
    </div>
  `,
  styles: [`
    .container { max-width: 800px; margin: 0 auto; padding: 20px; }
    .input-section { margin-bottom: 20px; }
    .form-control { width: 100%; padding: 10px; margin-bottom: 10px; }
    .btn { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
    .btn:disabled { opacity: 0.6; cursor: not-allowed; }
    .result-section { margin-top: 20px; }
    .result-card { background: #f8f9fa; padding: 20px; border-radius: 8px; }
    .sentiment-badge { 
      display: inline-block; 
      padding: 5px 15px; 
      border-radius: 20px; 
      font-weight: bold;
      margin-bottom: 10px;
    }
    .sentiment-badge.positive { background: #28a745; color: white; }
    .sentiment-badge.negative { background: #dc3545; color: white; }
    .sentiment-badge.neutral { background: #6c757d; color: white; }
    .sentiment-badge.mixed { background: #ffc107; color: black; }
    .error-message { color: #dc3545; padding: 10px; background: #f8d7da; border-radius: 4px; }
  `]
})
export class SentimentComponent {
  inputText = '';
  result: any = null;
  error: string = '';
  loading = false;

  constructor(private sentimentService: SentimentAnalysisService) {}

  analyze() {
    if (!this.inputText.trim()) {
      this.error = 'Please enter some text to analyze';
      return;
    }

    this.loading = true;
    this.error = '';
    this.result = null;

    this.sentimentService.analyzeText(this.inputText).subscribe({
      next: (response) => {
        this.loading = false;
        if (response.success) {
          this.result = response;
        } else {
          this.error = 'Analysis failed';
        }
      },
      error: (err) => {
        this.loading = false;
        this.error = err.error?.error || err.error?.message || 'An error occurred';
        console.error('Error:', err);
      }
    });
  }
}
```

### Method 4: JavaScript Fetch API

```javascript
// Single text analysis
async function analyzeSentiment(text) {
  try {
    const response = await fetch('https://YOUR_API_URL/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: text
      })
    });
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}

// Usage
analyzeSentiment("I am very satisfied with the advisor")
  .then(result => {
    console.log('Sentiment:', result.data.sentiment);
    console.log('Confidence:', result.data.confidence);
  })
  .catch(error => {
    console.error('Failed:', error);
  });
```

### Method 5: Python (requests library)

```python
import requests
import json

# Single text analysis
def analyze_sentiment(text, api_url):
    response = requests.post(
        f"{api_url}/analyze",
        headers={"Content-Type": "application/json"},
        json={"text": text}
    )
    return response.json()

# Batch analysis
def analyze_batch(texts, api_url):
    response = requests.post(
        f"{api_url}/analyze-batch",
        headers={"Content-Type": "application/json"},
        json={"texts": texts}
    )
    return response.json()

# Usage
api_url = "https://YOUR_API_URL.execute-api.us-east-1.amazonaws.com"
result = analyze_sentiment(
    "I am very satisfied with the advisor's communication",
    api_url
)
print(f"Sentiment: {result['data']['sentiment']}")
print(f"Confidence: {result['data']['confidence']}")
```

### Method 6: Postman

1. **Create a new POST request**
2. **URL**: `https://YOUR_API_URL/analyze`
3. **Headers**: 
   - `Content-Type: application/json`
4. **Body** (raw JSON):
   ```json
   {
     "text": "I am very satisfied with the advisor's communication"
   }
   ```
5. **Click Send**

## Request Format

### Single Analysis (`POST /analyze`)

```json
{
  "text": "Your advisor text here",
  "model_id": "amazon.titan-text-express-v1"  // Optional
}
```

### Batch Analysis (`POST /analyze-batch`)

```json
{
  "texts": [
    "First advisor text",
    "Second advisor text"
  ],
  "model_id": "amazon.titan-text-express-v1"  // Optional
}
```

## Response Format

### Success Response

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

### Error Response

```json
{
  "error": "Missing 'text' field in request body"
}
```

## Error Handling

### Common Errors

1. **400 Bad Request**: Missing or invalid input
   ```json
   {
     "error": "Text cannot be empty"
   }
   ```

2. **404 Not Found**: Wrong endpoint
   ```json
   {
     "error": "Endpoint not found. Use /analyze or /analyze-batch"
   }
   ```

3. **500 Internal Server Error**: Server-side error
   ```json
   {
     "error": "Internal server error",
     "message": "Error details here"
   }
   ```

## Testing Your API

### Quick Test Script (PowerShell)

```powershell
$apiUrl = "https://YOUR_API_URL/analyze"
$body = @{
    text = "I am very satisfied with the advisor's communication"
} | ConvertTo-Json

Invoke-RestMethod -Uri $apiUrl -Method Post -Body $body -ContentType "application/json"
```

### Quick Test Script (Bash)

```bash
#!/bin/bash
API_URL="https://YOUR_API_URL/analyze"

curl -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d '{"text": "I am very satisfied with the advisor"}'
```

## CORS Configuration

The API is configured with CORS enabled. If you're calling from a browser:
- Make sure your Angular app URL matches the `cors_origins` in Terraform variables
- For development: `cors_origins = "*"` (allows all origins)
- For production: Set to your specific domain: `cors_origins = "https://your-app.com"`

## Next Steps

1. Get your API endpoint: `terraform output analyze_endpoint`
2. Test with cURL or Postman
3. Integrate into your Angular app using the service examples above
4. Handle errors gracefully in your UI

