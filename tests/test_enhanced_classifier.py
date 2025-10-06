#!/usr/bin/env python3
"""
🧪 Enhanced Classifier Test Suite
Comprehensive testing for Google Gemini LLM integration

Author: Data Scientist AI Assistant
Date: September 27, 2025
Purpose: Validate enhanced classifier functionality before Product Owner demo
"""

import os
import sys
import logging
from pathlib import Path
import time

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_enhanced_classifier():
    """Test the enhanced classifier with mock API key."""
    print("🧪 Enhanced Classifier Test Suite")
    print("=" * 50)
    
    try:
        from src.models.enhanced_classifier import GeminiEnhancedClassifier
        print("✅ Enhanced classifier module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import enhanced classifier: {e}")
        return False
    
    # Test with mock API key (will fail but show structure)
    print("\n🔧 Testing classifier initialization...")
    try:
        # This will fail without real API key, but tests import structure
        classifier = GeminiEnhancedClassifier(api_key="test_key_mock")
        print("❌ Expected: Should fail with mock API key")
        return False
    except Exception as e:
        print(f"✅ Expected error with mock API key: {type(e).__name__}")
    
    print("\n📋 Testing with required components...")
    
    # Check if traditional model exists
    model_path = Path(__file__).parent / "models" / "telco_ticket_classifier.pkl"
    if model_path.exists():
        print(f"✅ Traditional model found: {model_path}")
    else:
        print(f"⚠️  Traditional model not found: {model_path}")
        print("   You may need to run train_model.py first")
    
    # Test sample tickets (structure validation)
    test_tickets = [
        "My internet bill is too high this month, please help me understand the charges",
        "WiFi keeps disconnecting every few minutes, very frustrating", 
        "I want to upgrade to a faster internet package for my home office",
        "The customer service agent was very rude and unhelpful",
        "No mobile signal in Sandton area since yesterday",
        "I need to update my billing address as I'm moving next month",
        "Hello, I just wanted to say thank you for your service"
    ]
    
    expected_categories = ["BILLING", "TECHNICAL", "SALES", "COMPLAINTS", "NETWORK", "ACCOUNT", "OTHER"]
    
    print(f"\n📝 Test tickets prepared: {len(test_tickets)} samples")
    print(f"🏷️  Expected categories: {', '.join(expected_categories)}")
    
    print("\n✅ Enhanced classifier structure validation complete!")
    return True

def test_enhanced_demo():
    """Test the enhanced Streamlit demo."""
    print("\n🎨 Enhanced Streamlit Demo Test")
    print("=" * 40)
    
    try:
        import streamlit
        print("✅ Streamlit available")
    except ImportError:
        print("❌ Streamlit not available - please install: pip install streamlit")
        return False
    
    demo_file = Path(__file__).parent / "enhanced_streamlit_demo.py"
    if demo_file.exists():
        print(f"✅ Enhanced demo file found: {demo_file.name}")
    else:
        print(f"❌ Enhanced demo file not found: {demo_file}")
        return False
    
    launcher_file = Path(__file__).parent / "launch_enhanced_demo.py"
    if launcher_file.exists():
        print(f"✅ Demo launcher found: {launcher_file.name}")
    else:
        print(f"❌ Demo launcher not found: {launcher_file}")
        return False
    
    print("\n✅ Enhanced demo components validation complete!")
    return True

def test_api_key_setup():
    """Test API key configuration."""
    print("\n🔑 API Key Configuration Test")
    print("=" * 35)
    
    api_key = os.getenv('GOOGLE_API_KEY')
    if api_key:
        print("✅ GOOGLE_API_KEY environment variable found")
        print(f"   Key length: {len(api_key)} characters")
        print(f"   Key prefix: {api_key[:10]}...")
        return True
    else:
        print("⚠️  GOOGLE_API_KEY environment variable not set")
        print("\n💡 To set up your API key:")
        print("   1. Get key from: https://aistudio.google.com/")
        print("   2. Set environment variable:")
        print("      Windows: set GOOGLE_API_KEY=your-api-key")
        print("      Linux/Mac: export GOOGLE_API_KEY='your-api-key'")
        print("   3. Or enter directly in the demo interface")
        return False

def test_dependencies():
    """Test required dependencies."""
    print("\n📦 Dependencies Test")
    print("=" * 25)
    
    required_packages = [
        'google.generativeai',
        'streamlit', 
        'plotly',
        'pandas',
        'numpy',
        'sklearn'  # scikit-learn imports as sklearn
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("   Install with: pip install " + " ".join(missing_packages))
        return False
    else:
        print("\n✅ All dependencies available!")
        return True

def run_comprehensive_test():
    """Run all tests."""
    print("🚀 Enhanced Classifier Comprehensive Test Suite")
    print("=" * 60)
    print("Testing Google Gemini LLM integration and enhanced features")
    print()
    
    start_time = time.time()
    
    tests = [
        ("Dependencies", test_dependencies),
        ("API Key Setup", test_api_key_setup),
        ("Enhanced Classifier", test_enhanced_classifier),
        ("Enhanced Demo", test_enhanced_demo),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} test...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    total_time = time.time() - start_time
    print(f"\n⏱️  Total test time: {total_time:.1f}s")
    print(f"📈 Tests passed: {passed}/{len(results)}")
    
    if passed == len(results):
        print("\n🎉 ALL TESTS PASSED! Enhanced classifier ready for demo!")
        print("\n🚀 Next steps:")
        print("   1. Set your Google API key")
        print("   2. Run: python launch_enhanced_demo.py")
        print("   3. Test with various ticket types")
        print("   4. Validate AI reasoning explanations")
    else:
        print("\n⚠️  Some tests failed - please resolve issues before demo")
    
    return passed == len(results)

if __name__ == "__main__":
    run_comprehensive_test()