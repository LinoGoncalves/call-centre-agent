#!/usr/bin/env python3
"""
Test script to validate the Docker development environment
Run this inside the Docker container to verify everything works
"""

def test_imports():
    """Test critical package imports"""
    try:
        import torch
        import transformers
        import sentence_transformers
        import spacy
        import nltk
        import mlflow
        import prefect
        import pandas
        import numpy
        import scikit_learn
        print("✅ All critical packages imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_models():
    """Test pre-cached model loading"""
    try:
        # Test sentence transformers (offline)
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = model.encode(['test sentence'])
        print("✅ Sentence transformer model loaded successfully")
        
        # Test spaCy (offline)
        import spacy
        nlp = spacy.load('en_core_web_sm')
        doc = nlp("Test sentence for spaCy")
        print("✅ spaCy model loaded successfully")
        
        # Test NLTK (offline)
        import nltk
        from nltk.tokenize import word_tokenize
        tokens = word_tokenize("Test sentence for NLTK")
        print("✅ NLTK data loaded successfully")
        
        return True
    except Exception as e:
        print(f"❌ Model loading error: {e}")
        return False

def test_services():
    """Test service connectivity"""
    try:
        import requests
        
        # Test MLflow
        try:
            response = requests.get('http://localhost:5000', timeout=5)
            print("✅ MLflow service accessible")
        except:
            print("⚠️ MLflow service not accessible (may still be starting)")
        
        # Test if we're in the container
        import socket
        hostname = socket.gethostname()
        if 'call-centre' in hostname:
            print("✅ Running inside Docker container")
        else:
            print("ℹ️ Running outside container (testing locally)")
            
        return True
    except Exception as e:
        print(f"⚠️ Service connectivity issue: {e}")
        return False

def test_file_access():
    """Test file system access"""
    try:
        import os
        
        # Check if we can access the app directory
        if os.path.exists('/app'):
            print("✅ App directory accessible")
        
        # Check model cache directories
        model_dirs = [
            '/opt/models/huggingface',
            '/opt/models/spacy', 
            '/opt/models/nltk'
        ]
        
        for model_dir in model_dirs:
            if os.path.exists(model_dir):
                print(f"✅ Model directory exists: {model_dir}")
            else:
                print(f"⚠️ Model directory missing: {model_dir}")
        
        return True
    except Exception as e:
        print(f"❌ File access error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Call Centre Agent Docker Environment")
    print("=" * 60)
    
    all_tests_passed = True
    
    print("\n📦 Testing Package Imports...")
    all_tests_passed &= test_imports()
    
    print("\n🤖 Testing AI Model Loading...")
    all_tests_passed &= test_models()
    
    print("\n🌐 Testing Service Connectivity...")
    all_tests_passed &= test_services()
    
    print("\n📁 Testing File System Access...")
    all_tests_passed &= test_file_access()
    
    print("\n" + "=" * 60)
    if all_tests_passed:
        print("🎉 Environment validation completed successfully!")
        print("🚀 You're ready to start developing AI solutions!")
    else:
        print("⚠️ Some tests failed. Check the logs above.")
        print("💡 Try rebuilding the Docker environment if issues persist.")
    
    print("\n🔗 Next Steps:")
    print("1. Open JupyterLab: http://localhost:8888")
    print("2. Create a new notebook in /app/notebooks/")
    print("3. Start building your AI models!")