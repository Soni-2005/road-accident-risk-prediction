import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


def scale_probability_data(train, val, test):
    """
    Scale numeric probability features using StandardScaler.
    Binary and non-numeric features are NOT scaled.
    """

    # Identify numeric columns
    numeric_cols = train.select_dtypes(include=[np.number]).columns.tolist()

    # Identify binary columns (0/1)
    binary_cols = [
        col for col in numeric_cols
        if train[col].dropna().nunique() <= 2
    ]

    # Columns to scale = numeric - binary
    scale_cols = [c for c in numeric_cols if c not in binary_cols]

    scaler = StandardScaler()

    # Fit on TRAIN only
    train_scaled = train.copy()
    val_scaled = val.copy()
    test_scaled = test.copy()

    train_scaled[scale_cols] = scaler.fit_transform(train[scale_cols])
    val_scaled[scale_cols] = scaler.transform(val[scale_cols])
    test_scaled[scale_cols] = scaler.transform(test[scale_cols])

    return train_scaled, val_scaled, test_scaled, scaler, scale_cols
