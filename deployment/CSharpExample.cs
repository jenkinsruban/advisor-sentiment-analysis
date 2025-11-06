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
        
        // Create request body
        var requestBody = new
        {
            text = "I am very satisfied with the advisor's communication and investment recommendations"
        };
        
        // Serialize to JSON
        var jsonContent = JsonSerializer.Serialize(requestBody);
        var content = new StringContent(jsonContent, Encoding.UTF8, "application/json");
        
        request.Content = content;
        
        try
        {
            var response = await client.SendAsync(request);
            
            if (response.IsSuccessStatusCode)
            {
                var responseBody = await response.Content.ReadAsStringAsync();
                Console.WriteLine("Success Response:");
                Console.WriteLine(responseBody);
                
                // Parse JSON response
                var result = JsonSerializer.Deserialize<SentimentResponse>(responseBody, new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                });
                
                if (result != null && result.Success)
                {
                    Console.WriteLine($"\nSentiment: {result.Data.Sentiment}");
                    Console.WriteLine($"Confidence: {result.Data.Confidence:P2}");
                    Console.WriteLine($"Summary: {result.Data.Summary}");
                }
            }
            else
            {
                var errorContent = await response.Content.ReadAsStringAsync();
                Console.WriteLine($"Error ({response.StatusCode}): {errorContent}");
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Exception: {ex.Message}");
        }
    }
}

// Response models
public class SentimentResponse
{
    public bool Success { get; set; }
    public SentimentData Data { get; set; }
    public string Error { get; set; }
}

public class SentimentData
{
    public string Sentiment { get; set; }
    public double Confidence { get; set; }
    public string EmotionalTone { get; set; }
    public string[] KeyIndicators { get; set; }
    public string Summary { get; set; }
    public string Recommendations { get; set; }
    public string ModelUsed { get; set; }
    public int TextLength { get; set; }
}

