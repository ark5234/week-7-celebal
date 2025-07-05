#!/usr/bin/env python3
"""
Test script to verify all dependencies and model loading work correctly.
"""

def test_imports():
    """Test all required imports."""
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
        
        import pandas as pd
        print("✅ Pandas imported successfully")
        
        import numpy as np
        print("✅ NumPy imported successfully")
        
        import joblib
        print("✅ Joblib imported successfully")
        
        from sklearn.datasets import load_iris
        print("✅ Scikit-learn datasets imported successfully")
        
        import plotly.express as px
        print("✅ Plotly Express imported successfully")
        
        import plotly.graph_objects as go
        print("✅ Plotly Graph Objects imported successfully")
        
        from sklearn.metrics import confusion_matrix, roc_curve, auc
        print("✅ Scikit-learn metrics imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_model_loading():
    """Test model loading."""
    try:
        import joblib
        model = joblib.load('models/iris_rf.pkl')
        print("✅ Model loaded successfully")
        
        # Test prediction
        from sklearn.datasets import load_iris
        iris = load_iris()
        sample = iris.data[0:1]  # Take first sample
        prediction = model.predict(sample)
        print(f"✅ Model prediction test successful: {prediction[0]}")
        
        return True
    except Exception as e:
        print(f"❌ Model loading error: {e}")
        return False

def test_data_loading():
    """Test data loading."""
    try:
        from sklearn.datasets import load_iris
        iris = load_iris()
        print(f"✅ Iris dataset loaded: {iris.data.shape[0]} samples, {iris.data.shape[1]} features")
        print(f"✅ Target names: {iris.target_names}")
        return True
    except Exception as e:
        print(f"❌ Data loading error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Iris Species Predictor Application")
    print("=" * 50)
    
    tests = [
        ("Import Tests", test_imports),
        ("Data Loading Tests", test_data_loading),
        ("Model Loading Tests", test_model_loading),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed!")
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready for deployment.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    main() 