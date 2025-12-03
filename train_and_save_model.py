import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle

# Load the dataset
df = pd.read_csv("diabetes.csv")

# Split features and target
X = df.drop("Outcome", axis=1)
y = df["Outcome"]

# Split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save the trained model to a file
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model has been trained and saved as model.pkl")
