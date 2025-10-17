#!/usr/bin/env python3
"""
🚀 Enhanced Demo Launcher with Multi-Provider Support
Intelligent launcher that detects available components and launches appropriate demo

Author: Quantum Thinking Framework Agent
Date: October 9, 2025  
Purpose: Universal demo launcher with graceful degradation
"""

import os
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_multi_provider_availability():
    """Check if multi-provider components are available."""
    try:
        # Test imports without actually loading heavy modules
        import importlib.util
        
        # Check for multi-provider components
        modules_to_check = [
            'src.models.multi_provider_manager',
            'src.models.opensource_llm', 
            'src.models.config_manager',
            'src.ui.pipeline_visualization'
        ]
        
        for module_name in modules_to_check:
            spec = importlib.util.find_spec(module_name)
            if spec is None:
                return False
                
        return True
    except Exception:
        return False

def launch_enhanced_demo():
    """Launch the enhanced multi-provider demo."""
    print("🚀 Launching Enhanced Multi-Provider Demo")
    print("   🌟 Features: Multi-LLM + Multi-Vector DB + Cost Optimization")
    print("   📊 Providers: Gemini+Ollama LLMs | Pinecone+ChromaDB Vector DBs")
    print("-" * 70)
    
    demo_file = "src/ui/enhanced_multi_provider_demo.py"
    
    if not Path(demo_file).exists():
        print(f"❌ Enhanced demo file not found: {demo_file}")
        return False
        
    return launch_streamlit_demo(demo_file, "Enhanced Multi-Provider Demo", 8501)

def launch_simple_demo():
    """Launch the simple Gemini-only demo."""
    print("🚀 Launching Simple Gemini Demo")
    print("   🌟 Features: Google Gemini LLM + AI Reasoning + Ensemble Control")
    print("   📊 Advanced classification with explainable AI and Telco branding")
    print("-" * 70)
    
    demo_file = "src/ui/streamlit_demo.py"
    
    if not Path(demo_file).exists():
        print(f"❌ Demo file not found: {demo_file}")
        return False
        
    return launch_streamlit_demo(demo_file, "Simple Gemini Demo", 8502)

def launch_streamlit_demo(demo_file, demo_name, port):
    """Launch a Streamlit demo with proper configuration."""
    
    # Check environment setup
    api_key = os.getenv('GOOGLE_API_KEY')
    demo_host = os.getenv('DEMO_HOST', 'localhost')
    
    if api_key:
        print("✅ Google API key loaded from environment")
        print(f"   Key prefix: {api_key[:10]}...")
        print("🤖 Enhanced classifier will initialize automatically")
    else:
        print("⚠️  No API key in .env file")
        print("   Demo will show setup instructions")
    
    print(f"🌐 Demo will run on: http://{demo_host}:{port}")
    print()
    
    try:
        # Launch Streamlit with environment configuration
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            str(demo_file),
            f"--server.port={port}",
            "--server.headless=true",
            f"--server.address={demo_host}"
        ]
        
        print(f"🚀 Starting {demo_name}...")
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
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to launch demo: {e}")
        print("💡 Try: pip install streamlit")
        return False
    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user")
        return True
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main launcher with intelligent demo selection."""
    print("🎯 Telco Call Centre Agent - Demo Launcher")
    print("=" * 50)
    
    # Check what's available
    multi_provider_available = check_multi_provider_availability()
    
    if multi_provider_available:
        print("✅ Multi-provider components detected")
        print("📋 Available demos:")
        print("   1. Enhanced Multi-Provider Demo (recommended)")
        print("   2. Simple Gemini Demo")
        print()
        
        # Let user choose or auto-select
        choice = input("Select demo [1/2] or press Enter for enhanced demo: ").strip()
        
        if choice == "2":
            return launch_simple_demo()
        else:
            # Try enhanced demo first, fall back to simple
            if not launch_enhanced_demo():
                print("⚠️ Enhanced demo failed, falling back to simple demo...")
                return launch_simple_demo()
            return True
    else:
        print("⚠️ Multi-provider components not available")
        print("📋 Launching simple Gemini demo...")
        print()
        return launch_simple_demo()

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Demo session completed successfully!")
    else:
        print("\n❌ Demo launch failed!")
        sys.exit(1)