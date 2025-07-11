"""Custom Azure OpenAI service with working managed identity authentication."""

import logging
import os

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

logger = logging.getLogger(__name__)


def create_azure_chat_completion_with_managed_identity(service_id: str) -> AzureChatCompletion:
    """Create Azure OpenAI chat completion service with working managed identity.
    
    Args:
        service_id: The service identifier.
        
    Returns:
        AzureChatCompletion: Configured service with managed identity authentication.
    """
    # Get configuration from environment
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview")
    
    if not endpoint:
        raise ValueError("AZURE_OPENAI_ENDPOINT environment variable is required")
    if not deployment_name:
        raise ValueError("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME environment variable is required")
    
    logger.info(f"Creating Azure OpenAI service with managed identity: {endpoint}")
    
    # Create credential and token provider (same pattern that works in test)
    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(
        credential,
        "https://cognitiveservices.azure.com/.default"
    )
    
    # Create Azure OpenAI service with explicit token provider
    service = AzureChatCompletion(
        service_id=service_id,
        endpoint=endpoint,
        deployment_name=deployment_name,
        api_version=api_version,
        azure_ad_token_provider=token_provider
    )
    
    logger.info("Azure OpenAI service with managed identity created successfully")
    return service
