"""Simple endpoint to test Azure OpenAI authentication."""

import logging
import os
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI
from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/test-auth")
async def test_openai_auth():
    """Test Azure OpenAI authentication with managed identity."""
    try:
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4.1-mini")
        
        logger.info(f"Testing authentication to {endpoint} with deployment {deployment_name}")
        
        # Create credential
        credential = DefaultAzureCredential()
        
        # Get token to test credential
        token = credential.get_token("https://cognitiveservices.azure.com/.default")
        logger.info(f"Token acquired successfully, expires at: {token.expires_on}")
        
        # Create token provider
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
                {"role": "user", "content": "Say hello in one word!"}
            ],
            max_tokens=10
        )
        
        result = response.choices[0].message.content
        logger.info(f"✅ Authentication successful! Response: {result}")
        
        return {
            "success": True,
            "message": "Authentication successful",
            "response": result,
            "endpoint": endpoint,
            "deployment": deployment_name
        }
        
    except Exception as e:
        logger.error(f"❌ Authentication failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__,
                "endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
                "deployment": os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
            }
        )
