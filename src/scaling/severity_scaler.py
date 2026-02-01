import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


def scale_severity_data(train, val, test, target_col="Accident_Severity"):
    """
    Scale numeric severity features using StandardScaler.
    Target column is excluded.
    Binary and categorical-encoded features are NOT scaled.
    """

    X_train = train.drop(columns=[target_col])
    X_val = val.drop(columns=[target_col])
    X_test = test.drop(columns=[target_col])

    y_train = train[target_col]
    y_val = val[target_col]
    y_test = test[target_col]

    numeric_cols = X_train.select_dtypes(include=[np.number]).columns.tolist()

    # Binary columns
    binary_cols = [
        col for col in numeric_cols
        if X_train[col].dropna().nunique() <= 2
    ]

    scale_cols = [c for c in numeric_cols if c not in binary_cols]

    scaler = StandardScaler()

    X_train_scaled = X_train.copy()
    X_val_scaled = X_val.copy()
    X_test_scaled = X_test.copy()

    X_train_scaled[scale_cols] = scaler.fit_transform(X_train[scale_cols])
    X_val_scaled[scale_cols] = scaler.transform(X_val[scale_cols])
    X_test_scaled[scale_cols] = scaler.transform(X_test[scale_cols])

    # Reattach target
    train_scaled = X_train_scaled.copy()
    train_scaled[target_col] = y_train

    val_scaled = X_val_scaled.copy()
    val_scaled[target_col] = y_val

    test_scaled = X_test_scaled.copy()
    test_scaled[target_col] = y_test

    return train_scaled, val_scaled, test_scaled, scaler, scale_cols
