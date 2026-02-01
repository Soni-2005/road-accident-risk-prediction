import pandas as pd
from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

# ----------------------------------
# Feature list (LOCKED)
# ----------------------------------
NUMERIC_FEATURES = [
    "latitude", "longitude",
    "Speed_limit"
]

CATEGORICAL_FEATURES = [
    "Road_Type", "Junction_Detail", "Junction_Control",
    "Light_Conditions", "Weather_Conditions",
    "Road_Surface_Conditions",
    "Urban_or_Rural_Area",
    "Day_of_Week"
]

# ----------------------------------
# Preprocessing pipeline
# ----------------------------------
numeric_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

probability_preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_pipeline, NUMERIC_FEATURES),
        ("cat", categorical_pipeline, CATEGORICAL_FEATURES)
    ]
)
