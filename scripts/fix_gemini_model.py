#!/usr/bin/env python3
"""
🔍 Google Gemini Model Discovery
Discovers available models and fixes compatibility issues

Author: Security Expert Agent + DevOps Engineer Agent
Date: September 27, 2025
Purpose: Resolve Gemini model access issues
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

def discover_available_models(api_key: str):
    """Discover available Gemini models for the API key."""
    try:
        genai.configure(api_key=api_key)
        
        print("🔍 Discovering available models...")
        models = genai.list_models()
        
        available_models = []
        for model in models:
            print(f"   📋 Model: {model.name}")
            print(f"      Supports: {', '.join(model.supported_generation_methods)}")
            available_models.append(model.name)
        
        return available_models
        
    except Exception as e:
        print(f"❌ Failed to discover models: {e}")
        return []

def test_model_compatibility(api_key: str, model_name: str) -> bool:
    """Test if a specific model works with generateContent."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Test message")
        print(f"✅ Model {model_name} works successfully!")
        return True
    except Exception as e:
        print(f"❌ Model {model_name} failed: {e}")
        return False

def find_working_model(api_key: str):
    """Find the best working Gemini model."""
    print("🎯 Finding compatible Gemini model...")
    
    # List of models to try (in order of preference)
    candidate_models = [
        "gemini-1.5-flash",
        "gemini-1.5-pro", 
        "gemini-pro",
        "gemini-1.0-pro",
        "models/gemini-1.5-flash",
        "models/gemini-1.5-pro",
        "models/gemini-pro"
    ]
    
    for model_name in candidate_models:
        print(f"\n🧪 Testing {model_name}...")
        if test_model_compatibility(api_key, model_name):
            return model_name
    
    print("❌ No compatible models found")
    return None

def main():
    """Main model discovery and compatibility testing."""
    print("🔍 Google Gemini Model Compatibility Check")
    print("=" * 55)
    
    # Load environment
    load_dotenv()
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("❌ No API key found in .env file")
        return False
    
    print(f"🔑 Using API key: {api_key[:10]}...{api_key[-4:]}")
    
    # First, try to discover available models
    available_models = discover_available_models(api_key)
    
    if not available_models:
        print("\n💡 Unable to discover models. This could mean:")
        print("   1. API key is completely invalid")
        print("   2. Billing is not set up")
        print("   3. Gemini API is not enabled")
        print("\n🔧 Steps to resolve:")
        print("   1. Visit: https://aistudio.google.com/")
        print("   2. Ensure billing is enabled")
        print("   3. Enable Gemini API in your project")
        print("   4. Generate a fresh API key")
        return False
    
    # Find a working model
    working_model = find_working_model(api_key)
    
    if working_model:
        print(f"\n🎉 Found working model: {working_model}")
        print("📝 Updating enhanced classifier to use this model...")
        return update_classifier_model(working_model)
    
    return False

def update_classifier_model(model_name: str):
    """Update the enhanced classifier to use the working model."""
    try:
        classifier_file = Path("enhanced_classifier.py")
        
        if not classifier_file.exists():
            print("❌ Enhanced classifier file not found")
            return False
        
        # Read current content
        with open(classifier_file) as f:
            content = f.read()
        
        # Replace model initialization
        old_line = "self.model = genai.GenerativeModel('gemini-1.5-flash')"
        new_line = f"self.model = genai.GenerativeModel('{model_name}')"
        
        if old_line in content:
            updated_content = content.replace(old_line, new_line)
            
            # Write updated file
            with open(classifier_file, 'w') as f:
                f.write(updated_content)
            
            print(f"✅ Updated classifier to use model: {model_name}")
            return True
        else:
            print("⚠️  Could not find model initialization line to update")
            print(f"💡 Manually update line: {old_line}")
            print(f"   To: {new_line}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to update classifier: {e}")
        return False

if __name__ == "__main__":
    if main():
        print("\n🚀 Ready to test enhanced classifier!")
        print("   Run: python -c \"from enhanced_classifier import GeminiEnhancedClassifier; c = GeminiEnhancedClassifier(); print('Success!')\"")
    else:
        print("\n⚠️  Manual intervention required")