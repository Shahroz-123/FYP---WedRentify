#!/usr/bin/env python3
"""
Train ML Model for Pakistani Wedding Dress Rental Price Prediction
Using 8 key features specified by the user
"""

import pandas as pd
import numpy as np
import pickle
import json
from datetime import datetime
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

print("\n" + "="*70)
print("PAKISTANI WEDDING DRESS RENTAL PRICE PREDICTION")
print("Model Training Script")
print("="*70)

# Load dataset
print("\n📥 Loading dataset...")
df = pd.read_csv('dataset.csv')
print(f"✅ Loaded {len(df)} records")
print(f"✅ Total columns: {len(df.columns)}")

# Define the 8 features to use
feature_names = [
    'original_price_pkr',      # Most important (76%)
    'condition',                # 9% importance
    'dress_age_months',         # 5%
    'fabric',                   # 3%
    'is_fully_embroidered',     # 2%
    'work_intensity',           # 2%
    'trail_length_ft',          # 2%
    'is_handwork'               # 2%
]

target = 'rental_price_pkr'

print(f"\n🎯 Using 8 key features:")
for i, feat in enumerate(feature_names, 1):
    print(f"   {i}. {feat}")

# Check if all columns exist
print(f"\n🔍 Verifying columns...")
missing_cols = []
for col in feature_names + [target]:
    if col not in df.columns:
        missing_cols.append(col)
        
if missing_cols:
    print(f"❌ Missing columns: {missing_cols}")
    exit(1)
else:
    print(f"✅ All required columns present")

# Select only required columns
df = df[feature_names + [target]].copy()

# Check for missing values
print(f"\n🔍 Checking missing values...")
missing = df.isnull().sum()
if missing.sum() > 0:
    print(f"⚠️  Found missing values:")
    for col, count in missing[missing > 0].items():
        print(f"   {col}: {count} ({count/len(df)*100:.2f}%)")
    print(f"\n🧹 Dropping rows with missing values...")
    df = df.dropna()
    print(f"✅ Remaining records: {len(df)}")
else:
    print(f"✅ No missing values")

# Display basic statistics
print(f"\n📊 Target Variable Statistics:")
print(f"   Min:    PKR {df[target].min():,.2f}")
print(f"   Max:    PKR {df[target].max():,.2f}")
print(f"   Mean:   PKR {df[target].mean():,.2f}")
print(f"   Median: PKR {df[target].median():,.2f}")

# Preprocessing
print(f"\n🔧 Preprocessing features...")

# Initialize label encoders
label_encoders = {}

# Encode categorical features
categorical_features = ['condition', 'fabric', 'work_intensity']

for feature in categorical_features:
    print(f"   Encoding '{feature}'...")
    le = LabelEncoder()
    df[feature] = le.fit_transform(df[feature].astype(str))
    label_encoders[feature] = le
    print(f"      Classes: {len(le.classes_)} -> {le.classes_[:5]}...")

# Ensure boolean features are 0/1
boolean_features = ['is_fully_embroidered', 'is_handwork']
for feature in boolean_features:
    df[feature] = df[feature].astype(int)

print(f"✅ Preprocessing complete")

# Prepare features and target
X = df[feature_names]
y = df[target]

print(f"\n📊 Final Dataset Shape:")
print(f"   Features: {X.shape}")
print(f"   Target:   {y.shape}")

# Split data
print(f"\n✂️  Splitting data (80/20)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"   Training:   {X_train.shape[0]} samples")
print(f"   Test:       {X_test.shape[0]} samples")

# Train model
print(f"\n🤖 Training Gradient Boosting Model...")
print(f"   This may take a few minutes with 100K records...")

model = GradientBoostingRegressor(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=5,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    verbose=0
)

model.fit(X_train, y_train)
print(f"✅ Training complete!")

# Evaluate model
print(f"\n📈 Model Evaluation:")

# Training set
y_train_pred = model.predict(X_train)
train_mae = mean_absolute_error(y_train, y_train_pred)
train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
train_r2 = r2_score(y_train, y_train_pred)

print(f"\n   Training Set:")
print(f"      MAE:  PKR {train_mae:,.2f}")
print(f"      RMSE: PKR {train_rmse:,.2f}")
print(f"      R²:   {train_r2:.4f} ({train_r2*100:.2f}%)")

# Test set
y_test_pred = model.predict(X_test)
test_mae = mean_absolute_error(y_test, y_test_pred)
test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
test_r2 = r2_score(y_test, y_test_pred)

print(f"\n   Test Set:")
print(f"      MAE:  PKR {test_mae:,.2f}")
print(f"      RMSE: PKR {test_rmse:,.2f}")
print(f"      R²:   {test_r2:.4f} ({test_r2*100:.2f}%)")

# Feature importance
print(f"\n🔍 Feature Importance:")
feature_importance = sorted(
    zip(feature_names, model.feature_importances_),
    key=lambda x: x[1],
    reverse=True
)

for feature, importance in feature_importance:
    bar = "█" * int(importance * 50)
    print(f"   {feature:30s} {importance*100:6.2f}%  {bar}")

# Sample predictions
print(f"\n🎯 Sample Predictions (first 10 test records):")
print(f"   {'Actual':>12} {'Predicted':>12} {'Error':>12} {'Error %':>10}")
print(f"   {'-'*12} {'-'*12} {'-'*12} {'-'*10}")

for i in range(min(10, len(y_test))):
    actual = y_test.iloc[i]
    predicted = y_test_pred[i]
    error = predicted - actual
    error_pct = (error / actual) * 100
    print(f"   {actual:>12,.2f} {predicted:>12,.2f} {error:>12,.2f} {error_pct:>9.1f}%")

# Save model
print(f"\n💾 Saving model...")
output_dir = Path('models')
output_dir.mkdir(exist_ok=True)

model_data = {
    'model': model,
    'label_encoders': label_encoders,
    'feature_names': feature_names,
    'target': target,
    'metadata': {
        'training_date': datetime.now().isoformat(),
        'model_type': 'GradientBoostingRegressor',
        'n_training_samples': len(X_train),
        'n_test_samples': len(X_test),
        'test_r2_score': float(test_r2),
        'test_mae': float(test_mae),
        'test_rmse': float(test_rmse),
        'feature_importances': {
            feature: float(importance) 
            for feature, importance in zip(feature_names, model.feature_importances_)
        }
    }
}

model_path = output_dir / 'dress_rental_model.pkl'
with open(model_path, 'wb') as f:
    pickle.dump(model_data, f)

print(f"✅ Model saved to: {model_path}")

# Save encoder information
encoders_info = {
    feature: encoder.classes_.tolist()
    for feature, encoder in label_encoders.items()
}

encoders_path = output_dir / 'encoders.json'
with open(encoders_path, 'w') as f:
    json.dump(encoders_info, f, indent=2)

print(f"✅ Encoders saved to: {encoders_path}")

# Save model info
info = {
    'model_type': 'GradientBoostingRegressor',
    'features': feature_names,
    'target': target,
    'training_date': datetime.now().isoformat(),
    'training_samples': len(X_train),
    'test_samples': len(X_test),
    'performance': {
        'test_r2': float(test_r2),
        'test_mae': float(test_mae),
        'test_rmse': float(test_rmse)
    },
    'feature_importance': {
        feature: float(importance)
        for feature, importance in zip(feature_names, model.feature_importances_)
    },
    'categorical_features': {
        feature: encoders_info[feature]
        for feature in categorical_features
    }
}

info_path = output_dir / 'model_info.json'
with open(info_path, 'w') as f:
    json.dump(info, f, indent=2)

print(f"✅ Model info saved to: {info_path}")

# Final summary
print(f"\n" + "="*70)
print(f"✅ TRAINING COMPLETED SUCCESSFULLY!")
print(f"="*70)
print(f"\n📊 Final Results:")
print(f"   ✅ Model Type:        Gradient Boosting Regressor")
print(f"   ✅ Training Samples:  {len(X_train):,}")
print(f"   ✅ Test Samples:      {len(X_test):,}")
print(f"   ✅ Test R² Score:     {test_r2:.4f} ({test_r2*100:.2f}%)")
print(f"   ✅ Test MAE:          PKR {test_mae:,.2f}")
print(f"   ✅ Model Saved:       {model_path}")
print(f"\n🎉 Your model is ready for deployment!")
print(f"="*70 + "\n")
