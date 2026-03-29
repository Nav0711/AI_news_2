#!/usr/bin/env python3
"""Direct Gemini API Test"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key loaded: {bool(api_key)}")
if api_key:
    print(f"API Key: {api_key[:20]}...")

import google.generativeai as genai

genai.configure(api_key=api_key)

# Test different models
models_to_test = [
    ("gemini-2.5-flash", "Basic model"),
    ("gemini-2.5-flash-vision", "Vision model"),
    ("gemini-1.5-pro", "1.5 Pro"),
    ("gemini-1.5-flash", "1.5 Flash"),
    ("gemini-2.0-flash", "2.0 Flash"),
]

print("\nTesting models:")
print("-" * 50)

for model_name, description in models_to_test:
    try:
        print(f"\nTesting: {model_name} ({description})")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Say 'ok' in one word")
        if response and response.text:
            print(f"  ✓ SUCCESS: {response.text.strip()}")
        else:
            print(f"  ✗ No response text")
    except Exception as e:
        error_str = str(e)
        print(f"  ✗ Error: {error_str[:120]}")

# List all available models
print("\n" + "=" * 50)
print("Available Models on Account:")
print("=" * 50)
try:
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✓ {model.name}")
except Exception as e:
    print(f"Error listing models: {e}")
