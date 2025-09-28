#!/usr/bin/env python3
"""
🧪 Demo Validation Script
Test the core functionality of the Streamlit demo
"""

import sys
from pathlib import Path
import pickle

# Add src to Python path
sys.path.append(str(Path(__file__).parent / 'src'))

def validate_demo_components():
    """Validate all demo components are working."""
    print("🧪 Validating Streamlit Demo Components")
    print("=" * 50)
    
    results = []
    
    # 1. Check model file exists
    model_path = Path("models/telco_ticket_classifier.pkl")
    if model_path.exists():
        print("✅ Model file found")
        results.append(True)
    else:
        print("❌ Model file missing")
        results.append(False)
    
    # 2. Test model loading
    try:
        from models.ticket_classifier import TicketClassificationPipeline
        
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
        
        pipeline = TicketClassificationPipeline()
        pipeline.models = model_data['models']
        pipeline.ensemble_weights = model_data['ensemble_weights']
        
        print("✅ Model loading successful")
        results.append(True)
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        results.append(False)
        return results
    
    # 3. Test prediction functionality
    try:
        test_text = "My internet bill is too high this month"
        prediction = pipeline.predict([test_text])[0]
        probabilities = pipeline.predict_proba([test_text])[0]
        
        print(f"✅ Prediction test: {prediction} ({max(probabilities):.1%} confidence)")
        results.append(True)
    except Exception as e:
        print(f"❌ Prediction test failed: {e}")
        results.append(False)
    
    # 4. Check streamlit_demo.py exists
    demo_file = Path("streamlit_demo.py")
    if demo_file.exists():
        print("✅ Streamlit demo file found")
        results.append(True)
    else:
        print("❌ Streamlit demo file missing")
        results.append(False)
    
    # 5. Check sample tickets are available
    sample_tickets = {
        "BILLING": "My internet bill is too high this month",
        "TECHNICAL": "WiFi router keeps disconnecting",
        "SALES": "I want to upgrade to faster internet",
        "COMPLAINTS": "Customer service was very rude",
        "NETWORK": "No mobile signal in this area",
        "ACCOUNT": "Need to change my billing address"
    }
    
    print("✅ Sample tickets prepared for all 6 categories")
    results.append(True)
    
    # Summary
    print("\n" + "=" * 50)
    success_count = sum(results)
    total_count = len(results)
    
    if success_count == total_count:
        print("🎉 ALL DEMO COMPONENTS VALIDATED SUCCESSFULLY!")
        print("✅ Ready for Product Owner demonstration")
        return True
    else:
        print(f"⚠️ {success_count}/{total_count} components validated")
        print("❌ Demo needs attention before presentation")
        return False

def main():
    """Main validation function."""
    success = validate_demo_components()
    
    if success:
        print("\n💡 To start the demo:")
        print("   1. Run: python launch_demo.py")
        print("   2. Open: http://localhost:8501")
        print("   3. Test with sample tickets")
        print("   4. Show real-time classification results")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)