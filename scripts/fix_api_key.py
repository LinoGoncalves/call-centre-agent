#!/usr/bin/env python3
"""
🔧 API Key Validator and Updater
Helps diagnose and fix Google Gemini API key issues

Author: DevOps Engineer Agent
Date: September 27, 2025
Purpose: HITL support for API key validation
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

def validate_api_key(api_key: str) -> bool:
    """Validate Google Gemini API key."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Test with minimal content
        response = model.generate_content("Test")
        return True
        
    except Exception as e:
        print(f"❌ API Key Validation Failed: {e}")
        return False

def update_env_file(new_api_key: str):
    """Update .env file with new API key."""
    env_file = Path(".env")
    
    if env_file.exists():
        # Read current content
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Replace API key line
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('GOOGLE_API_KEY='):
                lines[i] = f'GOOGLE_API_KEY={new_api_key}'
                break
        
        # Write updated content
        with open(env_file, 'w') as f:
            f.write('\n'.join(lines))
        
        print(f"✅ Updated .env file with new API key")
        return True
    else:
        print("❌ .env file not found")
        return False

def main():
    """Main API key diagnostic and update flow."""
    print("🔧 Google Gemini API Key Diagnostics")
    print("=" * 50)
    
    # Load current environment
    load_dotenv()
    current_key = os.getenv('GOOGLE_API_KEY')
    
    if current_key:
        print(f"📋 Current key: {current_key[:10]}...{current_key[-4:]}")
        
        print("\n🧪 Testing current API key...")
        if validate_api_key(current_key):
            print("✅ Current API key is valid!")
            print("💡 The issue might be temporary. Try refreshing the demo.")
            return True
        else:
            print("❌ Current API key is invalid")
    else:
        print("❌ No API key found in environment")
    
    print("\n🔑 API Key Update Required")
    print("1. Visit: https://aistudio.google.com/")
    print("2. Sign in and navigate to API Keys")
    print("3. Create a new API key")
    print("4. Copy the complete key")
    
    new_key = input("\n🔐 Enter your new Google Gemini API key: ").strip()
    
    if not new_key:
        print("❌ No key provided. Exiting.")
        return False
    
    if len(new_key) < 20:
        print("❌ Key seems too short. Please check and try again.")
        return False
    
    print("\n🧪 Testing new API key...")
    if validate_api_key(new_key):
        print("✅ New API key is valid!")
        
        if update_env_file(new_key):
            print("\n🎉 Setup Complete!")
            print("   1. Your .env file has been updated")
            print("   2. Restart the enhanced demo")
            print("   3. The classifier should initialize successfully")
            return True
    else:
        print("❌ New API key is also invalid")
        print("💡 Please check:")
        print("   - Key was copied completely")
        print("   - Billing is set up in Google Cloud")
        print("   - Gemini API is enabled")
    
    return False

if __name__ == "__main__":
    main()