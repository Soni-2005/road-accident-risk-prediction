import numpy as np
import pandas as pd

from sklearn.feature_selection import VarianceThreshold, mutual_info_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer


def select_severity_features(
    X: pd.DataFrame,
    y: pd.Series,
    mi_threshold: float = 0.001
):
    """
    Robust feature selection for accident severity.
    Handles:
    - object columns
    - NaNs
    - empty numeric sets
    - MI edge cases
    - RF / L1 failures
    """

    # -----------------------------
    # 0. Sanity checks
    # -----------------------------
    if X.empty:
        raise ValueError("X is empty — cannot perform feature selection")

    if y.nunique() < 2:
        raise ValueError("Severity target has <2 classes — invalid")

    # -----------------------------
    # 1. Split numeric / non-numeric
    # -----------------------------
    numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
    non_numeric_cols = X.select_dtypes(exclude=[np.number]).columns.tolist()

    # If no numeric features exist
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
    except Exception:
        print("⚠️ VarianceThreshold failed — keeping all numeric features")
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
            random_state=42,
            discrete_target=True
        )
        mi_series = pd.Series(mi_scores, index=X_var.columns)
        mi_selected = mi_series[mi_series > mi_threshold].index.tolist()
    except Exception:
        print("⚠️ Mutual Information failed — skipping MI")
        mi_selected = X_var.columns.tolist()

    if len(mi_selected) == 0:
        print("⚠️ MI removed all features — fallback to variance set")
        mi_selected = X_var.columns.tolist()

    X_mi = X_var[mi_selected]

    # -----------------------------
    # 5. Model-based importance
    # -----------------------------
    selected_numeric = []

    # ---- 5a. Random Forest ----
    try:
        if X_mi.shape[1] >= 2:
           rf = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1,
                class_weight="balanced"
            )
           print("   → Training RandomForest for severity FS...")

           rf.fit(X_mi, y)

           rf_imp = pd.Series(
                rf.feature_importances_,
                index=X_mi.columns
           )
        else:
            rf_imp = pd.Series(0.0, index=X_mi.columns)
    except Exception:
        print("⚠️ RF importance failed")
        rf_imp = pd.Series(0.0, index=X_mi.columns)

    # ---- 5b. L1 Regularization ----
    try:
        l1 = LogisticRegression(
            penalty="l1",
            solver="saga",
            max_iter=1000,
            tol=1e-3,
            class_weight="balanced"
        )
        print("   → Training L1 LogisticRegression for severity FS...")

        l1.fit(X_mi, y)

        l1_imp = pd.Series(
            np.abs(l1.coef_).sum(axis=0),
            index=X_mi.columns
        )
    except Exception:
        print("⚠️ L1 regularization failed")
        l1_imp = pd.Series(0.0, index=X_mi.columns)

    # -----------------------------
    # 6. Combine importance signals
    # -----------------------------
    combined_importance = rf_imp + l1_imp

    if combined_importance.sum() == 0:
        print("⚠️ All model importances are zero — keeping MI features")
        selected_numeric = X_mi.columns.tolist()
    else:
        combined_sorted = combined_importance.sort_values(ascending=False)
        cumulative = combined_sorted.cumsum()

        selected_numeric = cumulative[cumulative <= 0.95].index.tolist()

        if len(selected_numeric) == 0:
            selected_numeric = combined_sorted.index.tolist()

    # -----------------------------
    # 7. Final feature list
    # -----------------------------
    final_features = selected_numeric + non_numeric_cols

    return final_features
