#!/usr/bin/env python3
"""
🚀 Enhanced Demo Launcher
Unified launcher for Call Centre Agent demonstrations

Options:
1. Original Gemini + Pinecone demo (existing functionality)
2. Multi-provider demo with Ollama + ChromaDB options
3. Comparison mode (side-by-side)
4. Development mode (hot reload)

Author: GitHub Copilot Assistant
Date: October 9, 2025
Purpose: Unified demo launcher with multi-provider support
"""

import os
import sys
import subprocess
import argparse
import json
from pathlib import Path
from typing import Optional

def check_dependencies():
    """Check if all required dependencies are available"""
    required_packages = [
        'streamlit',
        'google-generativeai',
        'pandas',
        'plotly',
        'markupsafe',
        'chromadb',  # New requirement
        'ollama'     # New requirement
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install " + " ".join(missing_packages))
        return False
    
    return True

def check_environment():
    """Check environment configuration"""
    print("🔍 Checking environment...")
    
    # Check for .env file
    env_file = Path('.env')
    if env_file.exists():
        print("✅ .env file found")
        
        # Check for Google API key
        from dotenv import load_dotenv
        load_dotenv()
        
        if os.getenv('GOOGLE_API_KEY'):
            print("✅ GOOGLE_API_KEY configured")
        else:
            print("⚠️  GOOGLE_API_KEY not found in .env")
    else:
        print("⚠️  .env file not found")
        print("Create .env file with: GOOGLE_API_KEY=your_api_key_here")
    
    # Check Ollama availability
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ Ollama available")
            models = [line.split()[0] for line in result.stdout.strip().split('\n')[1:] if line.strip()]
            if models:
                print(f"   Models: {', '.join(models[:3])}{'...' if len(models) > 3 else ''}")
            else:
                print("   No models installed. Install with: ollama pull llama2")
        else:
            print("⚠️  Ollama not responding")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Ollama not installed or not running")
        print("   Install from: https://ollama.ai/")
    
    return True

def launch_original_demo(port: int = 8501, host: str = "localhost"):
    """Launch original Gemini + Pinecone demo"""
    print("🚀 Launching Original Demo (Gemini + Pinecone)...")
    
    demo_path = Path("src/ui/streamlit_demo.py")
    if not demo_path.exists():
        print(f"❌ Demo file not found: {demo_path}")
        return False
    
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        str(demo_path),
        "--server.port", str(port),
        "--server.address", host,
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to launch demo: {e}")
        return False

def launch_multi_provider_demo(port: int = 8502, host: str = "localhost"):
    """Launch enhanced multi-provider demo"""
    print("🚀 Launching Multi-Provider Demo (Ollama + ChromaDB + Existing)...")
    
    demo_path = Path("src/ui/enhanced_multi_provider_demo.py")
    if not demo_path.exists():
        print(f"❌ Demo file not found: {demo_path}")
        return False
    
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        str(demo_path),
        "--server.port", str(port),
        "--server.address", host,
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to launch demo: {e}")
        return False

def launch_comparison_mode():
    """Launch both demos for side-by-side comparison"""
    print("🔄 Launching Comparison Mode (Both Demos)...")
    
    import threading
    import time
    
    # Launch original demo on port 8501
    original_thread = threading.Thread(
        target=launch_original_demo,
        args=(8501, "localhost")
    )
    
    # Launch multi-provider demo on port 8502
    multi_thread = threading.Thread(
        target=launch_multi_provider_demo,
        args=(8502, "localhost")
    )
    
    print("Starting Original Demo on http://localhost:8501")
    original_thread.start()
    
    time.sleep(2)  # Stagger startup
    
    print("Starting Multi-Provider Demo on http://localhost:8502")
    multi_thread.start()
    
    print("\n🌐 Access URLs:")
    print("   Original Demo: http://localhost:8501")
    print("   Multi-Provider Demo: http://localhost:8502")
    print("\n📊 Compare features side-by-side!")
    
    try:
        original_thread.join()
        multi_thread.join()
    except KeyboardInterrupt:
        print("\n👋 Shutting down demos...")
        return True

def show_interactive_menu():
    """Show interactive demo selection menu"""
    print("\n" + "="*60)
    print("📞 CALL CENTRE AGENT - DEMO LAUNCHER")
    print("="*60)
    
    print("\nAvailable Demos:")
    print("1. 🏢 Original Demo (Gemini Pro + Pinecone)")
    print("   - Production-ready cloud providers")
    print("   - Full feature set with existing data")
    print("   - Recommended for production evaluation")
    
    print("\n2. 🏠 Multi-Provider Demo (+ Ollama + ChromaDB)")
    print("   - Configurable provider selection")
    print("   - Local and cloud provider options")
    print("   - Cost optimization and comparison")
    print("   - Recommended for development/testing")
    
    print("\n3. 🔄 Comparison Mode (Both Simultaneously)")
    print("   - Side-by-side feature comparison")
    print("   - Performance benchmarking")
    print("   - Runs on ports 8501 and 8502")
    
    print("\n4. 🔧 Environment Check")
    print("   - Verify dependencies and configuration")
    print("   - Check Ollama and model availability")
    
    print("\n5. ❌ Exit")
    
    while True:
        try:
            choice = input("\n🎯 Select option (1-5): ").strip()
            
            if choice == '1':
                check_environment()
                return launch_original_demo()
            
            elif choice == '2':
                check_environment()
                return launch_multi_provider_demo()
            
            elif choice == '3':
                check_environment()
                return launch_comparison_mode()
            
            elif choice == '4':
                print("\n🔍 Environment Check:")
                print("-" * 40)
                check_dependencies()
                check_environment()
                input("\nPress Enter to return to menu...")
                show_interactive_menu()
                return
            
            elif choice == '5':
                print("👋 Goodbye!")
                return True
            
            else:
                print("❌ Invalid choice. Please select 1-5.")
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return True

def main():
    """Main launcher function"""
    parser = argparse.ArgumentParser(description="Call Centre Agent Demo Launcher")
    parser.add_argument(
        '--mode', 
        choices=['original', 'multi', 'compare', 'check', 'menu'],
        default='menu',
        help='Demo mode to launch'
    )
    parser.add_argument('--port', type=int, default=8501, help='Port for Streamlit server')
    parser.add_argument('--host', default='localhost', help='Host for Streamlit server')
    parser.add_argument('--no-browser', action='store_true', help='Do not open browser')
    
    args = parser.parse_args()
    
    # Set Streamlit configuration
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    
    if args.mode == 'original':
        print("🏢 Original Demo Mode")
        check_environment()
        return launch_original_demo(args.port, args.host)
    
    elif args.mode == 'multi':
        print("🏠 Multi-Provider Demo Mode")
        check_environment()
        return launch_multi_provider_demo(args.port, args.host)
    
    elif args.mode == 'compare':
        print("🔄 Comparison Mode")
        check_environment()
        return launch_comparison_mode()
    
    elif args.mode == 'check':
        print("🔧 Environment Check Mode")
        print("-" * 40)
        deps_ok = check_dependencies()
        env_ok = check_environment()
        
        if deps_ok and env_ok:
            print("\n✅ Environment ready for demos!")
        else:
            print("\n⚠️  Please fix issues above before running demos")
        
        return True
    
    elif args.mode == 'menu':
        return show_interactive_menu()

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Demo launcher interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)