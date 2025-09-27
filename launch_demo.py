#!/usr/bin/env python3
"""
🚀 Launch script for Telkom Ticket Classifier Demo
Quick start script for Product Owner demonstration
"""

import subprocess
import sys
import webbrowser
import time
from pathlib import Path

def main():
    """Launch the Streamlit demo application."""
    print("🎯 Telkom Call Centre Ticket Classifier - Demo Launcher")
    print("=" * 60)
    
    # Check if model exists
    model_path = Path("models/telkom_ticket_classifier.pkl")
    if not model_path.exists():
        print("❌ Trained model not found!")
        print("💡 Please run: python train_model.py")
        return False
    
    print("✅ Model found - Ready for demo")
    print("🚀 Starting Streamlit demo server...")
    print("📱 Demo will open in your web browser")
    print("\n🔗 Manual URL: http://localhost:8502")
    print("🛑 Press Ctrl+C in terminal to stop the demo")
    print("=" * 60)
    
    try:
        # Launch Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "streamlit_demo.py",
            "--server.port=8502",
            "--server.address=localhost",
            "--browser.gatherUsageStats=false"
        ], check=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Demo stopped by user")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting demo: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)