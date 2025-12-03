import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os


def train_model():
    """Train the diabetes prediction model"""
    # Create synthetic diabetes dataset for demo
    np.random.seed(42)
    n_samples = 1000

    # Generate synthetic diabetes dataset
    data = {
        'Pregnancies': np.random.randint(0, 17, n_samples),
        'Glucose': np.random.normal(120, 30, n_samples),
        'BloodPressure': np.random.normal(70, 20, n_samples),
        'SkinThickness': np.random.normal(20, 15, n_samples),
        'Insulin': np.random.normal(80, 100, n_samples),
        'BMI': np.random.normal(25, 7, n_samples),
        'DiabetesPedigreeFunction': np.random.normal(0.5, 0.3, n_samples),
        'Age': np.random.randint(21, 81, n_samples)
    }

    # Create synthetic outcomes based on risk factors
    risk_score = (
            (data['Glucose'] > 140) * 0.3 +
            (data['BMI'] > 30) * 0.2 +
            (data['Age'] > 50) * 0.2 +
            (data['BloodPressure'] > 90) * 0.1 +
            (data['Pregnancies'] > 5) * 0.1 +
            np.random.random(n_samples) * 0.1
    )
    data['Outcome'] = (risk_score > 0.5).astype(int)

    df = pd.DataFrame(data)

    # Prepare features and target
    X = df.drop('Outcome', axis=1)
    y = df['Outcome']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)

    # Evaluate model
    accuracy = accuracy_score(y_test, model.predict(X_test_scaled))
    print(f"Model accuracy: {accuracy:.2f}")

    # Save model and scaler
    os.makedirs('model', exist_ok=True)
    joblib.dump(model, 'model/diabetes_model.pkl')
    joblib.dump(scaler, 'model/scaler.pkl')

    return model, scaler


def load_model():
    """Load the trained model and scaler"""
    try:
        model = joblib.load('model/diabetes_model.pkl')
        scaler = joblib.load('model/scaler.pkl')
        return model, scaler
    except FileNotFoundError:
        print("Model not found. Training new model...")
        return train_model()


def predict_diabetes(input_data):
    """Make diabetes prediction"""
    model, scaler = load_model()
    scaled_data = scaler.transform(np.array(input_data).reshape(1, -1))
    prediction = model.predict(scaled_data)[0]
    probability = model.predict_proba(scaled_data)[0][1]  # % chance of diabetes
    return prediction, round(probability * 100, 2)