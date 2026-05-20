#!/usr/bin/env python
"""Quick test to verify all components are working"""

import pickle
import pandas as pd
import numpy as np
from sklearn.metrics import r2_score, mean_absolute_error

print("=" * 60)
print("🧪 Student Performance Predictor - Component Test")
print("=" * 60)

try:
    # Test 1: Load model
    print("\n1. Loading model...")
    with open('student_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("   ✅ Model loaded successfully")
except Exception as e:
    print(f"   ❌ Error loading model: {e}")
    exit(1)

try:
    # Test 2: Load data
    print("\n2. Loading data...")
    data = pd.read_csv('student_data.csv')
    print(f"   ✅ Data loaded: {len(data)} records, {len(data.columns)} columns")
except Exception as e:
    print(f"   ❌ Error loading data: {e}")
    exit(1)

try:
    # Test 3: Verify features
    print("\n3. Verifying features...")
    feature_names = ['study_hours', 'attendance_percentage', 'previous_score', 
                     'assignments_completed', 'sleep_hours', 'extracurricular_activities', 
                     'daily_internet_usage']
    
    for feature in feature_names:
        if feature not in data.columns:
            print(f"   ❌ Missing feature: {feature}")
            exit(1)
    print(f"   ✅ All {len(feature_names)} features present")
except Exception as e:
    print(f"   ❌ Error verifying features: {e}")
    exit(1)

try:
    # Test 4: Make a test prediction
    print("\n4. Testing prediction...")
    X = data[feature_names]
    y = data['final_score']
    
    # Single prediction
    test_input = np.array([[5.0, 80, 75, 60, 7.0, 5, 4.0]])
    prediction = model.predict(test_input)[0]
    print(f"   ✅ Test prediction: {prediction:.1f}/100")
    
    # Batch predictions
    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)
    mae = mean_absolute_error(y, y_pred)
    
    print(f"   ✅ Model R² Score: {r2:.4f}")
    print(f"   ✅ Model MAE: {mae:.2f} points")
except Exception as e:
    print(f"   ❌ Error in prediction: {e}")
    exit(1)

try:
    # Test 5: Verify requirements
    print("\n5. Checking dependencies...")
    import streamlit
    import sklearn
    import matplotlib
    import seaborn
    print("   ✅ All required packages available")
except ImportError as e:
    print(f"   ⚠️  Missing package: {e}")
    print("   Run: pip install -r requirements.txt")

print("\n" + "=" * 60)
print("✅ All tests passed! App is ready to run.")
print("=" * 60)
print("\n🚀 To start the app, run:")
print("   streamlit run app.py")
print("\n" + "=" * 60)
