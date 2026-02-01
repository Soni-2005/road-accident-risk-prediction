import numpy as np
import pandas as pd

from sklearn.feature_selection import VarianceThreshold, mutual_info_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer


def select_probability_features(
    X: pd.DataFrame,
    y: pd.Series,
    mi_threshold: float = 0.001
):
    """
    Robust feature selection for accident probability.
    Handles:
    - object columns
    - NaNs
    - empty numeric sets
    - MI edge cases
    """

    # -----------------------------
    # 0. Sanity checks
    # -----------------------------
    if X.empty:
        raise ValueError("X is empty — cannot perform feature selection")

    if len(y.unique()) < 2:
        raise ValueError("Target has only one class — invalid for selection")

    # -----------------------------
    # 1. Split numeric / non-numeric
    # -----------------------------
    numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
    non_numeric_cols = X.select_dtypes(exclude=[np.number]).columns.tolist()

    # If no numeric features exist, return categorical safely
    if len(numeric_cols) == 0:
        print("⚠️ No numeric features found — returning categorical only")
        return non_numeric_cols

    X_num = X[numeric_cols]

    # -----------------------------
    # 2. Variance Threshold
    # -----------------------------
    try:
        var_selector = VarianceThreshold(threshold=0.0)
        X_var_array = var_selector.fit_transform(X_num)

        kept_numeric = [
            col for col, keep in zip(numeric_cols, var_selector.get_support())
            if keep
        ]
    except Exception as e:
        print("⚠️ VarianceThreshold failed, keeping all numeric features")
        kept_numeric = numeric_cols
        X_var_array = X_num.values

    if len(kept_numeric) == 0:
        print("⚠️ All numeric features removed by variance filter")
        return non_numeric_cols

    X_var = pd.DataFrame(X_var_array, columns=kept_numeric)

    # -----------------------------
    # 3. Temporary imputation (median)
    # -----------------------------
    imputer = SimpleImputer(strategy="median")
    X_var[:] = imputer.fit_transform(X_var)

    # -----------------------------
    # 4. Mutual Information
    # -----------------------------
    try:
        mi_scores = mutual_info_classif(
            X_var,
            y,
            random_state=42
        )
        mi_series = pd.Series(mi_scores, index=X_var.columns)
        mi_selected = mi_series[mi_series > mi_threshold].index.tolist()
    except Exception as e:
        print("⚠️ Mutual Information failed, skipping MI step")
        mi_selected = X_var.columns.tolist()

    if len(mi_selected) == 0:
        print("⚠️ MI removed all features — falling back to variance set")
        mi_selected = X_var.columns.tolist()

    X_mi = X_var[mi_selected]

    # -----------------------------
    # 5. Tree-based importance (optional)
    # -----------------------------
    if X_mi.shape[1] < 2:
        print("⚠️ Too few features for RF — skipping RF importance")
        selected_numeric = X_mi.columns.tolist()
    else:
        rf = RandomForestClassifier(
            n_estimators=200,
            random_state=42,
            n_jobs=-1,
            class_weight="balanced"
        )
        rf.fit(X_mi, y)

        importance = pd.Series(
            rf.feature_importances_,
            index=X_mi.columns
        ).sort_values(ascending=False)

        cumulative = importance.cumsum()
        selected_numeric = cumulative[cumulative <= 0.95].index.tolist()

        if len(selected_numeric) == 0:
            selected_numeric = importance.index.tolist()

    # -----------------------------
    # 6. Final feature list
    # -----------------------------
    final_features = selected_numeric + non_numeric_cols

    return final_features
