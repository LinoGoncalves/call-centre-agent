#!/usr/bin/env python3
"""
🚀 Demo Launcher for Telkom Call Centre Agent
Quick launcher for the professional Streamlit demo interface

Author: Data Scientist AI Assistant  
Date: September 28, 2025
Purpose: Easy launch of demo for Product Owner validation
"""

import os
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def launch_demo():
    """Launch the Streamlit demo."""
    print(" Launching Telkom Call Centre Agent Demo")
    print("   🌟 Features: Google Gemini LLM + AI Reasoning + 0-100% Ensemble Control")
    print("   📊 Advanced classification with explainable AI and Telkom branding")
    print("-" * 70)
    
    # Set up environment
    demo_file = Path(__file__).parent / "streamlit_demo.py"
    
    if not demo_file.exists():
        print("❌ Enhanced demo file not found!")
        print(f"   Expected: {demo_file}")
        sys.exit(1)
    
    # Check if models exist
    model_path = Path(__file__).parent / "models" / "telkom_ticket_classifier.pkl"
    if not model_path.exists():
        print("⚠️  Traditional model not found - will need to be trained first")
        print(f"   Expected: {model_path}")
    
    # Check environment setup
    api_key = os.getenv('GOOGLE_API_KEY')
    demo_port = os.getenv('DEMO_PORT', '8502')
    demo_host = os.getenv('DEMO_HOST', 'localhost')
    
    if api_key:
        print("✅ Google API key loaded from environment")
        print(f"   Key prefix: {api_key[:10]}...")
        print("🤖 Enhanced classifier will initialize automatically")
    else:
        print("⚠️  No API key in .env file")
        print("   Demo will show setup instructions")
    
    print(f"🌐 Demo will run on: http://{demo_host}:{demo_port}")
    print()
    
    try:
        # Launch Streamlit with environment configuration
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            str(demo_file),
            f"--server.port={demo_port}",
            "--server.headless=true",
            f"--server.address={demo_host}"
        ]
        
        print("🚀 Starting enhanced demo server...")
        print(f"   Command: {' '.join(cmd)}")
        print("   Demo will open in your browser automatically")
        print()
        print("💡 Tips:")
        if api_key:
            print("   - Classifier will initialize automatically from .env")
            print("   - Try the sample tickets for quick testing") 
            print("   - Compare Traditional ML vs LLM predictions")
            print("   - Check the AI reasoning explanations")
        else:
            print("   - Set GOOGLE_API_KEY in .env file for automatic setup")
            print("   - Visit: https://aistudio.google.com/ to get your API key")
            print("   - Demo will show detailed setup instructions")
        print()
        
        subprocess.run(cmd, check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to launch demo: {e}")
        print("💡 Try: pip install streamlit")
    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    launch_demo()