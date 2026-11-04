"""Load the trained phrase classifier and predict one hand frame."""
import joblib
import numpy as np

MODEL_PATH = "models/communication_model.pkl"


def load_bundle():
    try:
        return joblib.load(MODEL_PATH)
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            "Trained model not found. Run collect_data.py and train_model.py first."
        ) from exc


def predict_gesture(features, bundle):
    model = bundle["model"]
    encoder = bundle["encoder"]
    row = np.asarray(features, dtype=np.float32).reshape(1, -1)
    probabilities = model.predict_proba(row)[0]
    index = int(np.argmax(probabilities))
    label = encoder.inverse_transform([model.classes_[index]])[0]
    return label, float(probabilities[index])
