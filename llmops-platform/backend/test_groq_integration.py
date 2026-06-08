"""
Test script to verify Groq integration and model comparison functionality
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_auth():
    """Test authentication"""
    print("\n=== Testing Authentication ===")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": "test@example.com", "password": "password123"}
    )
    if response.status_code == 200:
        print("✅ Authentication successful")
        return response.json()["access_token"]
    else:
        print(f"❌ Authentication failed: {response.text}")
        return None

def test_models(token):
    """Test fetching available models"""
    print("\n=== Testing Models Endpoint ===")
    response = requests.get(
        f"{BASE_URL}/models",
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code == 200:
        models = response.json()
        print(f"✅ Found {len(models)} models:")
        for model in models:
            print(f"   • {model['name']} ({model['id']})")
            print(f"     Max tokens: {model['max_tokens']}, Speed: {model['speed']}")
        return models
    else:
        print(f"❌ Failed to fetch models: {response.text}")
        return []

def test_chat(token, model_id, message):
    """Test chat with specific model"""
    print(f"\n=== Testing Chat with {model_id} ===")
    print(f"Message: {message}")
    
    response = requests.post(
        f"{BASE_URL}/chat",
        headers={"Authorization": f"Bearer {token}"},
        json={"message": message, "model": model_id}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Response received:")
        print(f"   Model: {data['model']}")
        print(f"   Tokens: {data['tokens_used']}")
        print(f"   Latency: {data['latency_ms']}ms")
        print(f"   Cost: ${data['tokens_used'] * 0.0000002:.6f}")
        print(f"   Response: {data['response'][:200]}...")
        return data
    else:
        print(f"❌ Chat failed: {response.text}")
        return None

def test_metrics(token):
    """Test metrics endpoints"""
    print("\n=== Testing Metrics ===")
    
    # Summary
    response = requests.get(
        f"{BASE_URL}/metrics/summary",
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code == 200:
        summary = response.json()
        print(f"✅ Summary:")
        print(f"   Total requests: {summary['total_requests']}")
        print(f"   Total tokens: {summary['total_tokens']}")
        print(f"   Total cost: ${summary['total_cost']:.6f}")
        print(f"   Avg latency: {summary['average_latency']:.0f}ms")
    
    # Model metrics
    response = requests.get(
        f"{BASE_URL}/metrics/models",
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code == 200:
        models = response.json()
        print(f"✅ Model Performance:")
        for model in models:
            print(f"   • {model['model']}:")
            print(f"     Requests: {model['requests']}, Tokens: {model['tokens']}")
            print(f"     Avg latency: {model['avg_latency']:.0f}ms, Error rate: {model['error_rate']:.1f}%")

def main():
    print("="*60)
    print("🚀 Testing Groq Integration & Model Comparison")
    print("="*60)
    
    # Authenticate
    token = test_auth()
    if not token:
        return
    
    # Get available models
    models = test_models(token)
    if not models:
        return
    
    # Test with first 3 models
    test_models_list = models[:3]
    test_message = "Explain what is machine learning in 2-3 sentences."
    
    for model in test_models_list:
        test_chat(token, model['id'], test_message)
    
    # Check metrics
    test_metrics(token)
    
    print("\n" + "="*60)
    print("✅ All tests completed!")
    print("="*60)

if __name__ == "__main__":
    main()
