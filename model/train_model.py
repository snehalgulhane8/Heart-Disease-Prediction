import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "dataset", "heart.csv")
MODEL_DIR = os.path.join(BASE_DIR, "model")

MODEL_PATH = os.path.join(MODEL_DIR, "heart_model.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")


# Load dataset
df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

# Remove unnecessary spaces from column names
df.columns = df.columns.str.strip()


# Detect target column
possible_targets = [
    "target",
    "Target",
    "output",
    "Output",
    "HeartDisease",
    "heartdisease",
    "condition",
    "Condition"
]

target_column = None

for column in possible_targets:
    if column in df.columns:
        target_column = column
        break

if target_column is None:
    raise ValueError(
        "Target column not found. Please set target_column manually."
    )

print("\nTarget column:", target_column)


# Separate features and target
X = df.drop(columns=[target_column])
y = df[target_column]


# Convert categorical columns to numerical values
X = pd.get_dummies(X, drop_first=True)


# Make sure target is numeric
if y.dtype == "object":
    y = pd.factorize(y)[0]


# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Scaling
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# Model
model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

model.fit(X_train_scaled, y_train)


# Prediction
y_pred = model.predict(X_test_scaled)


# Evaluation
accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", accuracy)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# Save model and scaler
joblib.dump(model, MODEL_PATH)
joblib.dump(scaler, SCALER_PATH)

# Save feature names
FEATURE_PATH = os.path.join(MODEL_DIR, "features.pkl")
joblib.dump(X.columns.tolist(), FEATURE_PATH)


print("\nModel saved:", MODEL_PATH)
print("Scaler saved:", SCALER_PATH)
print("Features saved:", FEATURE_PATH)