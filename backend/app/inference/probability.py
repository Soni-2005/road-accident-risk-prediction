import joblib
import numpy as np
from backend.app.config import PROB_MODEL_PATH

print("Loading calibrated probability model...")
MODEL = joblib.load(PROB_MODEL_PATH)
print("Probability model loaded.")

def predict_probability(X):
    """
    Returns probability of accident
    """
    return float(MODEL.predict_proba(X)[0, 1])
