# train_model.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os


def create_synthetic_data():
    """Create synthetic diabetes dataset for demo purposes"""
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

    return pd.DataFrame(data)


def train_and_save_model():
    """Train the diabetes prediction model and save it"""
    print("Creating synthetic dataset...")
    df = create_synthetic_data()

    # Save the dataset for reference
    df.to_csv('diabetes.csv', index=False)
    print("Dataset saved as diabetes.csv")

    # Prepare features and target
    X = df.drop('Outcome', axis=1)
    y = df['Outcome']

    print(f"Dataset shape: {X.shape}")
    print(f"Positive cases: {y.sum()}/{len(y)} ({y.mean() * 100:.1f}%)")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train model
    print("Training Random Forest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)

    # Evaluate model
    train_accuracy = accuracy_score(y_train, model.predict(X_train_scaled))
    test_accuracy = accuracy_score(y_test, model.predict(X_test_scaled))

    print(f"Training accuracy: {train_accuracy:.3f}")
    print(f"Test accuracy: {test_accuracy:.3f}")

    # Save model and scaler
    os.makedirs('model', exist_ok=True)
    joblib.dump(model, 'model/diabetes_model.pkl')
    joblib.dump(scaler, 'model/scaler.pkl')

    print("\nModel and scaler saved successfully!")
    return model, scaler


if __name__ == "__main__":
    train_and_save_model()