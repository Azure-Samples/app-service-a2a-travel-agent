"""Test configuration and shared fixtures."""

import os
from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Set up test environment variables."""
    test_env = {
        "DEBUG": "true",
        "AZURE_OPENAI_ENDPOINT": "https://test.openai.azure.com/",
        "AZURE_OPENAI_DEPLOYMENT_NAME": "test-gpt-4",
        "AZURE_OPENAI_API_VERSION": "2025-01-01-preview",
    }

    with patch.dict(os.environ, test_env, clear=False):
        yield
