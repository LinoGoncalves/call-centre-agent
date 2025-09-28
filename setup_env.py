#!/usr/bin/env python3
"""
🔧 Interactive Environment Setup
Helps users create their .env file securely

Author: Data Scientist AI Assistant
Date: September 27, 2025
Purpose: Simplify .env setup for Product Owner and team
"""

import os
import sys
from pathlib import Path

def setup_env_file():
    """Interactive .env file creation."""
    print("🔧 Enhanced Classifier Environment Setup")
    print("=" * 50)
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    # Check if .env already exists
    if env_file.exists():
        print("⚠️  .env file already exists!")
        response = input("Do you want to update it? (y/n): ").lower()
        if response != 'y':
            print("👋 Setup cancelled")
            return False
    
    print("\n🔑 Google Gemini API Key Setup")
    print("   Get your key from: https://aistudio.google.com/")
    print("   1. Sign in to Google AI Studio")
    print("   2. Click 'Get API Key'")
    print("   3. Create a new API key")
    print("   4. Copy the key")
    
    # Get API key
    while True:
        api_key = input("\n🔐 Enter your Google Gemini API key: ").strip()
        if api_key:
            if len(api_key) > 20:  # Basic validation
                break
            else:
                print("❌ API key seems too short. Please check and try again.")
        else:
            print("❌ API key cannot be empty")
    
    print(f"\n✅ API key received: {api_key[:10]}...{api_key[-4:]}")
    
    # Optional configurations
    print("\n⚙️ Optional Configuration (press Enter for defaults)")
    
    threshold = input("OTHER category threshold (default: 0.6): ").strip()
    if not threshold:
        threshold = "0.6"
    
    ensemble_weight = input("Gemini ensemble weight (default: 0.7): ").strip()
    if not ensemble_weight:
        ensemble_weight = "0.7"
    
    demo_port = input("Demo port (default: 8502): ").strip()
    if not demo_port:
        demo_port = "8502"
    
    # Create .env content
    env_content = f"""# 🔐 Environment Variables for Telco Call Centre Agent
# Generated on {os.path.dirname(__file__) or 'local setup'}

# Google Gemini API Configuration (REQUIRED)
GOOGLE_API_KEY={api_key}

# Model Configuration
OTHER_CATEGORY_THRESHOLD={threshold}
ENSEMBLE_WEIGHT={ensemble_weight}

# Demo Configuration  
DEMO_PORT={demo_port}
DEMO_HOST=localhost

# Logging Configuration
LOG_LEVEL=INFO
"""
    
    # Write .env file
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print(f"\n✅ .env file created successfully!")
        print(f"   Location: {env_file.absolute()}")
        print(f"   🔐 Your API key is now securely stored")
        
        # Verify by loading
        from dotenv import load_dotenv
        load_dotenv()
        
        loaded_key = os.getenv('GOOGLE_API_KEY')
        if loaded_key == api_key:
            print("✅ Environment setup verified!")
        else:
            print("⚠️  Warning: Could not verify environment setup")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def test_setup():
    """Test the environment setup."""
    print("\n🧪 Testing Enhanced Classifier Setup")
    print("-" * 40)
    
    try:
        from enhanced_classifier import GeminiEnhancedClassifier
        print("✅ Enhanced classifier module available")
        
        # Try to initialize (will test API key)
        classifier = GeminiEnhancedClassifier()
        print("✅ Classifier initialized successfully!")
        print(f"   🎯 OTHER threshold: {classifier.other_threshold:.1%}")
        print(f"   ⚖️ Ensemble weight: {classifier.ensemble_weight:.1%} Gemini")
        
        return True
        
    except Exception as e:
        print(f"❌ Setup test failed: {e}")
        print("💡 Please check your API key and try again")
        return False

def main():
    """Main setup flow."""
    print("🚀 Enhanced Telco Ticket Classifier Setup")
    print("   Google Gemini LLM + Traditional ML Ensemble")
    print("   With AI reasoning and OTHER category support")
    print()
    
    # Setup environment
    if setup_env_file():
        print("\n" + "="*50)
        
        # Test setup
        if test_setup():
            print("\n🎉 Setup Complete! You can now:")
            print("   1. Run: python launch_enhanced_demo.py")
            print("   2. Open: http://localhost:8502")
            print("   3. Test with sample tickets")
            print("   4. View AI reasoning explanations")
            print("\n💡 Tip: Your API key is safely stored in .env file")
        else:
            print("\n⚠️  Setup incomplete - please resolve issues above")
    else:
        print("\n❌ Environment setup failed")

if __name__ == "__main__":
    main()