import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"

model = joblib.load(
    MODELS_DIR / "probability" / "rf_calibrated.pkl"
)

print("Expected input feature names:")
print(model.feature_names_in_)
print("Number of features:", len(model.feature_names_in_))
