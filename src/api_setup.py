"""API configuration and client initialization."""

import os
import google.generativeai as genai
from together import Together
from dotenv import load_dotenv

def load_api_keys():
    """Load API keys from environment variables."""
    load_dotenv()
    
    keys = {
        'newsapi': os.getenv('NEWSAPI_KEY'),
        'gemini': os.getenv('GEMINI_API_KEY'),
        'together': os.getenv('TOGETHER_API_KEY')
    }
    
    # Validate that keys are available
    for name, key in keys.items():
        if not key:
            print(f"Warning: {name.upper()}_KEY not found in environment variables")
    
    return keys

def initialize_clients(api_keys):
    """Initialize API clients."""
    # Configure Gemini API
    genai.configure(api_key=api_keys['gemini'])
    
    # Initialize Together API client
    together_client = Together(api_key=api_keys['together'])
    
    return together_client

# Export the functions and initialized variables
api_keys = load_api_keys()
together_client = initialize_clients(api_keys)