"""Train and evaluate the phrase gesture classifier."""
import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

DATASET = "dataset/hand_landmarks.csv"
MODEL_PATH = "models/communication_model.pkl"

if not os.path.exists(DATASET):
    raise FileNotFoundError("Dataset not found. Run python collect_data.py first.")

data = pd.read_csv(DATASET).dropna()
if data.empty:
    raise ValueError("Dataset is empty. Collect gesture samples first.")

counts = data["label"].value_counts()
print("Samples per phrase:\n", counts)
if len(counts) < 2:
    raise ValueError("Collect samples for at least two different phrases.")
if (counts < 2).any():
    raise ValueError("Each phrase needs at least two samples for stratified splitting.")

X = data.drop(columns=["label"]).astype("float32")
y = data["label"].astype(str)
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

model = RandomForestClassifier(
    n_estimators=250,
    max_depth=22,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1,
)
print("\nTraining...")
model.fit(X_train, y_train)
pred = model.predict(X_test)

print(f"Holdout accuracy: {accuracy_score(y_test, pred) * 100:.2f}%")
print(classification_report(
    y_test, pred,
    labels=list(range(len(encoder.classes_))),
    target_names=encoder.classes_,
    zero_division=0,
))

os.makedirs("models", exist_ok=True)
joblib.dump({"model": model, "encoder": encoder}, MODEL_PATH)
print(f"Saved model to {MODEL_PATH}")
