import joblib
from pathlib import Path

model = joblib.load(
    Path("models/probability/rf_calibrated.pkl")
)

base_pipeline = model.estimator

# Correct step name
ct = base_pipeline.named_steps["preprocess"]

encoder = ct.named_transformers_["cat"]

print("=== Allowed categorical values used during training ===\n")
for col, cats in zip(encoder.feature_names_in_, encoder.categories_):
    print(f"{col} -> {cats}")
