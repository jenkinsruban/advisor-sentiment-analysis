# C# and Angular Examples for Advisor Sentiment Analysis API

## C# Examples

### Method 1: Using HttpClient (Your Code - Fixed)

```csharp
using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Text.Json;

class Program
{
    static async Task Main(string[] args)
    {
        var client = new HttpClient();
        var apiUrl = "https://rvz0a310j2.execute-api.us-east-1.amazonaws.com/analyze";
        
        var request = new HttpRequestMessage(HttpMethod.Post, apiUrl);
        
        var requestBody = new
        {
            text = "I am very satisfied with the advisor's communication and investment recommendations"
        };
        
        var jsonContent = JsonSerializer.Serialize(requestBody);
        var content = new StringContent(jsonContent, Encoding.UTF8, "application/json");
        
        request.Content = content;
        
        try
        {
            var response = await client.SendAsync(request);
            response.EnsureSuccessStatusCode();
            
            var responseBody = await response.Content.ReadAsStringAsync();
            Console.WriteLine(responseBody);
            
            // Parse JSON response
            var result = JsonSerializer.Deserialize<SentimentResponse>(responseBody);
            Console.WriteLine($"Sentiment: {result.data.sentiment}");
            Console.WriteLine($"Confidence: {result.data.confidence}");
        }
        catch (HttpRequestException ex)
        {
            Console.WriteLine($"Error: {ex.Message}");
        }
    }
}

public class SentimentResponse
{
    public bool success { get; set; }
    public SentimentData data { get; set; }
}

public class SentimentData
{
    public string sentiment { get; set; }
    public double confidence { get; set; }
    public string emotional_tone { get; set; }
    public string[] key_indicators { get; set; }
    public string summary { get; set; }
    public string recommendations { get; set; }
}
```

### Method 2: Using HttpClient with Error Handling

```csharp
using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Text.Json;

public class SentimentAnalysisClient
{
    private readonly HttpClient _httpClient;
    private readonly string _apiBaseUrl;
    
    public SentimentAnalysisClient(string apiBaseUrl)
    {
        _httpClient = new HttpClient();
        _apiBaseUrl = apiBaseUrl.TrimEnd('/');
    }
    
    public async Task<SentimentResponse> AnalyzeAsync(string text, string modelId = null)
    {
        var requestBody = new
        {
            text = text,
            model_id = modelId
        };
        
        var jsonContent = JsonSerializer.Serialize(requestBody);
        var content = new StringContent(jsonContent, Encoding.UTF8, "application/json");
        
        try
        {
            var response = await _httpClient.PostAsync($"{_apiBaseUrl}/analyze", content);
            
            if (!response.IsSuccessStatusCode)
            {
                var errorContent = await response.Content.ReadAsStringAsync();
                throw new HttpRequestException($"API Error: {response.StatusCode} - {errorContent}");
            }
            
            var responseBody = await response.Content.ReadAsStringAsync();
            return JsonSerializer.Deserialize<SentimentResponse>(responseBody);
        }
        catch (Exception ex)
        {
            throw new Exception($"Failed to analyze sentiment: {ex.Message}", ex);
        }
    }
    
    public async Task<BatchSentimentResponse> AnalyzeBatchAsync(string[] texts, string modelId = null)
    {
        var requestBody = new
        {
            texts = texts,
            model_id = modelId
        };
        
        var jsonContent = JsonSerializer.Serialize(requestBody);
        var content = new StringContent(jsonContent, Encoding.UTF8, "application/json");
        
        try
        {
            var response = await _httpClient.PostAsync($"{_apiBaseUrl}/analyze-batch", content);
            response.EnsureSuccessStatusCode();
            
            var responseBody = await response.Content.ReadAsStringAsync();
            return JsonSerializer.Deserialize<BatchSentimentResponse>(responseBody);
        }
        catch (Exception ex)
        {
            throw new Exception($"Failed to analyze batch: {ex.Message}", ex);
        }
    }
}

// Usage
var client = new SentimentAnalysisClient("https://rvz0a310j2.execute-api.us-east-1.amazonaws.com");
var result = await client.AnalyzeAsync("I am very satisfied with the advisor");
Console.WriteLine($"Sentiment: {result.data.sentiment}");
```

### Method 3: Using RestSharp (Alternative)

```csharp
using RestSharp;

var client = new RestClient("https://rvz0a310j2.execute-api.us-east-1.amazonaws.com");
var request = new RestRequest("/analyze", Method.Post);

request.AddJsonBody(new
{
    text = "I am very satisfied with the advisor's communication"
});

var response = await client.ExecuteAsync<SentimentResponse>(request);

if (response.IsSuccessful)
{
    Console.WriteLine($"Sentiment: {response.Data.data.sentiment}");
}
else
{
    Console.WriteLine($"Error: {response.ErrorMessage}");
}
```

## Angular Examples

### Service Implementation

```typescript
// sentiment-analysis.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

export interface SentimentData {
  sentiment: string;
  confidence: number;
  emotional_tone: string;
  key_indicators: string[];
  summary: string;
  recommendations: string;
  model_used?: string;
  text_length?: number;
}

export interface SentimentResponse {
  success: boolean;
  data: SentimentData;
}

export interface BatchSentimentResponse {
  success: boolean;
  data: {
    results: (SentimentData & { index: number })[];
    count: number;
  };
}

@Injectable({
  providedIn: 'root'
})
export class SentimentAnalysisService {
  private apiUrl = 'https://rvz0a310j2.execute-api.us-east-1.amazonaws.com';

  constructor(private http: HttpClient) {}

  analyzeText(text: string, modelId?: string): Observable<SentimentResponse> {
    const body: any = { text };
    if (modelId) {
      body.model_id = modelId;
    }

    return this.http.post<SentimentResponse>(`${this.apiUrl}/analyze`, body)
      .pipe(
        catchError(this.handleError)
      );
  }

  analyzeBatch(texts: string[], modelId?: string): Observable<BatchSentimentResponse> {
    const body: any = { texts };
    if (modelId) {
      body.model_id = modelId;
    }

    return this.http.post<BatchSentimentResponse>(`${this.apiUrl}/analyze-batch`, body)
      .pipe(
        catchError(this.handleError)
      );
  }

  private handleError(error: HttpErrorResponse): Observable<never> {
    let errorMessage = 'An unknown error occurred';
    
    if (error.error instanceof ErrorEvent) {
      // Client-side error
      errorMessage = `Error: ${error.error.message}`;
    } else {
      // Server-side error
      errorMessage = `Error Code: ${error.status}\nMessage: ${error.error?.error || error.message}`;
    }
    
    console.error(errorMessage);
    return throwError(() => new Error(errorMessage));
  }
}
```

### Component Implementation

```typescript
// sentiment.component.ts
import { Component } from '@angular/core';
import { SentimentAnalysisService, SentimentResponse } from './sentiment-analysis.service';

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
          <div class="sentiment-badge" [ngClass]="result.data.sentiment">
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
  result: SentimentResponse | null = null;
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
        this.error = err.error?.error || err.message || 'An error occurred';
        console.error('Error:', err);
      }
    });
  }
}
```

### Module Setup (app.module.ts)

```typescript
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { SentimentComponent } from './sentiment/sentiment.component';
import { SentimentAnalysisService } from './sentiment-analysis.service';

@NgModule({
  declarations: [
    AppComponent,
    SentimentComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [SentimentAnalysisService],
  bootstrap: [AppComponent]
})
export class AppModule { }
```

## API Endpoints

### Single Text Analysis
```
POST https://rvz0a310j2.execute-api.us-east-1.amazonaws.com/analyze
Content-Type: application/json

{
  "text": "Your advisor text here",
  "model_id": "amazon.titan-text-express-v1"  // Optional
}
```

### Batch Analysis
```
POST https://rvz0a310j2.execute-api.us-east-1.amazonaws.com/analyze-batch
Content-Type: application/json

{
  "texts": ["Text 1", "Text 2"],
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
  "error": "Error message here"
}
```

## Testing Your C# Code

Your code looks correct! Make sure:
1. The API endpoint is correct: `https://rvz0a310j2.execute-api.us-east-1.amazonaws.com/analyze`
2. Content-Type header is set: `application/json`
3. JSON body is properly formatted
4. CORS is configured (if calling from browser)

Try running your C# code and check if it works now after the IAM policy update!

