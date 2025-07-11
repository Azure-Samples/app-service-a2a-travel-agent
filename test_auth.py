#!/usr/bin/env python3
"""Test Azure OpenAI authentication with managed identity."""

import os
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI

def test_azure_openai_auth():
    """Test Azure OpenAI authentication."""
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4.1-mini")
    
    print(f"Testing Azure OpenAI authentication...")
    print(f"Endpoint: {endpoint}")
    print(f"Deployment: {deployment_name}")
    
    try:
        # Create token provider
        credential = DefaultAzureCredential()
        token_provider = get_bearer_token_provider(
            credential,
            "https://cognitiveservices.azure.com/.default"
        )
        
        # Create client
        client = AzureOpenAI(
            api_version="2024-09-01-preview",
            azure_endpoint=endpoint,
            azure_ad_token_provider=token_provider
        )
        
        # Test with a simple completion
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "user", "content": "Say hello!"}
            ],
            max_tokens=10
        )
        
        print("✅ Authentication successful!")
        print(f"Response: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_azure_openai_auth()
