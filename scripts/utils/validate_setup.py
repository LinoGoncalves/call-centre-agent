#!/usr/bin/env python3
"""
Call Centre Agent - Client Validation Script
============================================

Run this script to verify your environment is ready for the demo.

Usage: python validate_setup.py
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Check Python version compatibility."""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python version is compatible")
        return True
    else:
        print("❌ Python 3.8+ required")
        return False

def check_dependencies():
    """Check all required dependencies."""
    print("\n📦 Checking dependencies...")
    
    required_packages = {
        'streamlit': '1.28.0',
        'plotly': '5.17.0', 
        'pandas': '2.0.0',
        'numpy': '1.24.0',
        'google.generativeai': None,
        'dotenv': None,
        'sklearn': '1.3.0',
        'yaml': None,
        'bs4': None,
        'markupsafe': '2.1.0',
        'requests': '2.31.0'
    }
    
    missing = []
    for package, min_version in required_packages.items():
        try:
            if package == 'dotenv':
                import dotenv
                print(f"✅ python-dotenv: imported")
            elif package == 'bs4':
                from bs4 import BeautifulSoup
                print(f"✅ beautifulsoup4: imported")
            elif package == 'yaml':
                import yaml
                print(f"✅ PyYAML: imported")
            elif package == 'google.generativeai':
                import google.generativeai
                print(f"✅ google-generativeai: imported")
            else:
                module = __import__(package)
                version = getattr(module, '__version__', 'unknown')
                print(f"✅ {package}: {version}")
        except ImportError:
            missing.append(package)
            print(f"❌ {package}: NOT FOUND")
    
    return len(missing) == 0, missing

def check_environment():
    """Check environment configuration."""
    print("\n🔑 Checking environment configuration...")
    
    env_file = Path('.env')
    if env_file.exists():
        print("✅ .env file found")
        
        # Check for Google API key
        from dotenv import load_dotenv
        load_dotenv()
        
        google_key = os.getenv('GOOGLE_API_KEY')
        if google_key:
            print(f"✅ GOOGLE_API_KEY configured (prefix: {google_key[:10]}...)")
        else:
            print("⚠️  GOOGLE_API_KEY not found - Gemini features will not work")
            
        pinecone_key = os.getenv('PINECONE_API_KEY')
        if pinecone_key:
            print(f"✅ PINECONE_API_KEY configured (optional)")
        else:
            print("ℹ️  PINECONE_API_KEY not set (optional for vector features)")
            
        return google_key is not None
    else:
        print("❌ .env file not found")
        print("   Create .env file with: GOOGLE_API_KEY=your_key_here")
        return False

def check_project_structure():
    """Check essential project files."""
    print("\n📁 Checking project structure...")
    
    essential_files = [
        'src/models/enhanced_classifier.py',
        'src/models/rules_engine.py', 
        'src/ui/streamlit_demo.py',
        'launch_demo.py',
        'data/telecoms_tickets_train.csv'
    ]
    
    missing_files = []
    for file_path in essential_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"❌ {file_path}: NOT FOUND")
    
    return len(missing_files) == 0, missing_files

def main():
    """Main validation function."""
    print("🔍 Call Centre Agent - Environment Validation")
    print("=" * 50)
    
    all_good = True
    
    # Check Python version
    if not check_python_version():
        all_good = False
    
    # Check dependencies
    deps_ok, missing_deps = check_dependencies()
    if not deps_ok:
        all_good = False
        print(f"\n❌ Missing packages: {', '.join(missing_deps)}")
        print("   Run: pip install -r requirements.txt")
    
    # Check environment
    if not check_environment():
        all_good = False
    
    # Check project structure
    structure_ok, missing_files = check_project_structure()
    if not structure_ok:
        all_good = False
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
    
    # Final result
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 VALIDATION PASSED - Ready to launch!")
        print("\n🚀 Start the demo with: python launch_demo.py")
        print("   Demo URL: http://localhost:8502")
    else:
        print("❌ VALIDATION FAILED - Please fix issues above")
        print("\n📋 Setup checklist:")
        print("   1. Install Python 3.8+")
        print("   2. Run: pip install -r requirements.txt")  
        print("   3. Create .env with GOOGLE_API_KEY=your_key")
        print("   4. Ensure all project files are present")
    
    return all_good

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)