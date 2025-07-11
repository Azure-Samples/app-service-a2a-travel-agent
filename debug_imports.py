#!/usr/bin/env python3
"""Debug script to test imports and identify issues."""

import os
import sys

print("Python version:", sys.version)
print("Current directory:", os.getcwd())
print("Environment variables:")
for var in ["AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", "AZURE_OPENAI_API_VERSION"]:
    print(f"  {var}: {os.getenv(var, 'NOT SET')}")

try:
    print("\n1. Testing basic imports...")
    import fastapi
    import semantic_kernel
    print("✅ Basic imports successful")
except Exception as e:
    print(f"❌ Basic imports failed: {e}")
    sys.exit(1)

try:
    print("\n2. Testing agent imports...")
    from src.agent.travel_agent import SemanticKernelTravelAgent
    print("✅ Agent import successful")
except Exception as e:
    print(f"❌ Agent import failed: {e}")
    sys.exit(1)

try:
    print("\n3. Testing agent initialization...")
    # Set some dummy environment variables for testing
    os.environ["AZURE_OPENAI_ENDPOINT"] = "https://test.openai.azure.com/"
    os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"] = "test-deployment"
    os.environ["AZURE_OPENAI_API_VERSION"] = "2024-02-01"
    
    agent = SemanticKernelTravelAgent()
    print("✅ Agent initialization successful")
except Exception as e:
    print(f"❌ Agent initialization failed: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ All tests completed successfully!")
